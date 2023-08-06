# Copyright (C) 2020 Arm Limited or its affiliates. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Description:
# Early optimisation of the network graph, using the rewrite_graph module to do the traversal of the graph. These are
# split into two parts optimise_graph_a and optimise_graph_b.
import math

import numpy as np

from . import fp_math
from . import lut
from . import rewrite_graph
from . import scaling
from .data_type import DataType
from .debug_database import DebugDatabase
from .errors import UnsupportedFeatureError
from .ethos_u55_regs.ethos_u55_regs import resampling_mode
from .numeric_util import clamp_sigmoid
from .numeric_util import full_shape
from .numeric_util import round_away_zero
from .operation import create_activation_function
from .operation import create_avgpool_nop
from .operation import NpuBlockType
from .operation import Op
from .operation import Operation
from .softmax import SoftMax
from .tensor import check_quantized_tens_scaling_equal
from .tensor import create_const_tensor
from .tensor import create_reshape_tensor
from .tensor import QuantizationParameters
from .tensor import Tensor

passthrough_nodes = set((Op.Identity,))

memory_only_ops = set((Op.Reshape,))


def remove_passthrough_tensor(tens, arch, nng):
    if len(tens.ops) == 1 and tens.ops[0].type in passthrough_nodes:
        assert len(tens.ops[0].inputs) == 1
        tens = tens.ops[0].inputs[0]
    return tens


def rewrite_concat(tens, arch, nng):
    if len(tens.ops) == 1 and tens.ops[0].type.is_concat_op():
        concat_op = tens.ops[0]
        if tens != concat_op.outputs[0]:
            return tens  # don't attempt to rewrite the min/max outputs of QuantizedConcat

        # Not supported so leave it and run on CPU
        if not concat_op.run_on_npu:
            return tens

        inputs, axis = concat_op.get_concat_inputs_axis()

        tens.ops = []
        offset = 0
        for idx, inp in enumerate(inputs):
            new_op = Operation(Op.ConcatSliceWrite, concat_op.name + str(idx))
            new_op.inputs = [inp]
            new_op.outputs = [tens]
            new_op.attrs["concat_axis"] = axis
            new_op.attrs["concat_start"] = offset
            offset += inp.shape[axis]
            new_op.attrs["concat_end"] = offset
            new_op.run_on_npu = True
            tens.ops.append(new_op)
            DebugDatabase.add_optimised(concat_op, new_op)
        assert tens.shape[axis] == offset

        # If axis corresponds to C-dimension, NHCWB16 can only be used in the output if all the concat_start's are a
        # multiple of 16. This as, it is only then the address offset for the ofm, for all operations, will be 16 byte
        # aligned. For other values of axis the address offsets will be 16 byte aligned, as they are all based on c = 0
        # and those addresses are always 16 byte aligned due to the NHCWB16 format.
        if axis == -1 or axis == (len(tens.shape) - 1):
            for op in tens.ops:
                if op.attrs["concat_start"] % 16 != 0:
                    tens.avoid_NHCWB16 = True
                    break

    return tens


def rewrite_split(tens, arch, nng):

    if len(tens.ops) == 1 and tens.ops[0].type.is_split_op():
        split_op = tens.ops[0]

        # Not supported so leave it and run on CPU
        if not split_op.run_on_npu:
            return tens

        inp, outputs, axis, offset_start, offset_end = split_op.get_split_inputs_axis()

        tens.ops = []
        new_op = Operation(Op.SplitSliceRead, split_op.name)
        new_op.inputs = [inp]

        # For Split the offset cannot be extracted from the tensor so it has to
        # be calculated from the index of the output tensor
        if axis is not None:
            # Get the start and end of the split
            offset_start = [0] * len(tens.shape)
            offset_end = [0] * len(tens.shape)
            for out in outputs:
                if out == tens:
                    break
                offset_start[axis] += out.shape[axis]

                # If start offset is not a multiple of 16 in the C-dimension, NHCWB16 need to be avoided in the input
                if (offset_start[-1] % 16) != 0:
                    inp.avoid_NHCWB16 = True

            offset_end[axis] = offset_start[axis] + tens.shape[axis]

        new_op.attrs["split_start"] = offset_start
        new_op.attrs["split_end"] = offset_end
        new_op.run_on_npu = True
        new_op.set_output_tensor(tens)
        DebugDatabase.add_optimised(split_op, new_op)

    return tens


def needed_total_padding(input_size, stride, filter_size):
    out_size = (input_size + stride - 1) // stride
    needed_input = (out_size - 1) * stride + filter_size
    total_padding = max(0, needed_input - input_size)
    return total_padding


def calc_padding_and_skirt(padding_type, kernel_size, stride, input_dims):
    ypad = needed_total_padding(int(input_dims[1]), int(stride[1]), int(kernel_size[0]))
    xpad = needed_total_padding(int(input_dims[2]), int(stride[2]), int(kernel_size[1]))
    if padding_type == b"SAME":
        left_pad = (xpad + 0) // 2
        right_pad = (xpad + 1) // 2
        top_pad = (ypad + 0) // 2
        bottom_pad = (ypad + 1) // 2
    elif padding_type == b"VALID":
        left_pad = 0
        right_pad = 0
        top_pad = 0
        bottom_pad = 0
    else:
        raise UnsupportedFeatureError("Unknown padding {}".format(str(padding_type)))
    padding = (top_pad, left_pad, bottom_pad, right_pad)
    skirt = (top_pad, left_pad, ypad - top_pad, xpad - left_pad)
    return padding, skirt


def calc_upscaled_padding_and_skirt(padding_type, kernel_size, stride, input_dims, upscaling_factor):
    kernel_height, kernel_width = kernel_size[0], kernel_size[1]
    if padding_type == b"SAME":
        ypad = needed_total_padding(int(input_dims[1]) * upscaling_factor, int(stride[1]), int(kernel_height))
        xpad = needed_total_padding(int(input_dims[2]) * upscaling_factor, int(stride[2]), int(kernel_width))

        right_pad = max(((xpad + 1) // upscaling_factor) - 1, 0)
        bottom_pad = max(((ypad + 1) // upscaling_factor) - 1, 0)
        left_pad = max(kernel_width - 1 - right_pad, 0)
        top_pad = max(kernel_height - 1 - bottom_pad, 0)

    elif padding_type == b"VALID":
        right_pad = max(kernel_width - 2, 0)
        bottom_pad = max(kernel_height - 2, 0)
        left_pad = kernel_width - 1
        top_pad = kernel_height - 1
    else:
        assert 0, "Unknown padding"

    padding = (top_pad, left_pad, bottom_pad, right_pad)
    skirt = padding
    return padding, skirt


def fixup_conv2d_backprop(op, arch, nng):
    if op.type == Op.Conv2DBackpropInput:
        # flip the inputs
        op.inputs[0], op.inputs[2] = op.inputs[2], op.inputs[0]
        op.type = Op.Conv2DBackpropInputSwitchedBias

        # Update strides
        op.attrs.update({"stride_w": 1, "stride_h": 1, "strides": (1, 1, 1, 1)})

    return op


# Convert the op to an elementwise add
def convert_resizebilinear_1x1_to_add(op):
    op.type = Op.Add
    op.name = op.name + "_add"
    op.attrs["resizebilinear"] = True
    # Create an input tensor filled with zeros
    shape = op.outputs[0].shape
    tens = Tensor(shape, op.inputs[0].dtype, op.inputs[1].name + "_add")
    tens.values = np.zeros(shape)
    tens.quant_values = np.zeros(shape, np.uint8)
    tens.quantization = QuantizationParameters(0.0, 255.0)
    tens.quantization.scale_f32 = 1.0
    tens.quantization.zero_point = 0
    tens.consumer_list = [op]
    tens_op = op.inputs[1].ops[0]
    tens_op.set_output_tensor(tens)
    # Set the add inputs
    op.inputs[1] = op.inputs[0]
    op.inputs[0] = tens

    return op


# Convert ResizeBilinear to a number of 2x2 pool ops
def convert_resizebilinear_to_2x2_pool(op):
    count = 0
    pre_op = op
    outputs = op.outputs

    op.attrs.update({"strides": (1, 1, 1, 1), "ksize": (1, 2, 2, 1)})
    if op.attrs["align_corners"]:
        shape_modifier = 1
        op.attrs["padding"] = b"VALID"
    else:
        shape_modifier = 0
        op.attrs["padding"] = b"SAME"
    op.inputs[0].resampling_mode = resampling_mode.NEAREST

    upscaled_shape = np.array(op.inputs[0].shape[1:3])
    out_shape = np.array(op.outputs[0].shape[1:3])
    if (upscaled_shape == upscaled_shape * 2 - shape_modifier).all():
        return op

    while (upscaled_shape < out_shape).all():
        if count == 0:
            scaled_op = pre_op
        else:
            scaled_op = op.clone("_{}".format(count))
            scaled_op.inputs[0] = pre_op.outputs[0]

        upscaled_shape = upscaled_shape * 2 - shape_modifier

        if (upscaled_shape == out_shape).all():
            scaled_op.outputs = outputs
            scaled_op.outputs[0].ops = [scaled_op]
        else:
            shape = outputs[0].shape.copy()
            shape[1:3] = upscaled_shape[0:2]
            out_tens = Tensor(shape, DataType.int16, "{}_{}".format(op.outputs[0].name, count))
            out_tens.quantization = op.outputs[0].quantization.clone()
            out_tens.quantization.quant_min = np.iinfo(np.int16).min
            out_tens.quantization.quant_max = np.iinfo(np.int16).max
            scaled_op.set_output_tensor(out_tens)
            pre_op = scaled_op
            count += 1

        # Setup the scale value
        if scaled_op.inputs[0].dtype.bits == 8 and scaled_op.outputs[0].dtype.bits == 16:
            scaled_op.attrs["rescale"] = 128
        elif scaled_op.inputs[0].dtype.bits == 16 and scaled_op.outputs[0].dtype.bits == 8:
            scaled_op.attrs["rescale"] = 1 / 128
        elif "rescale" in scaled_op.attrs:
            del scaled_op.attrs["rescale"]

    return op


def fixup_resizebilinear(op, arch, nng):
    if op.type == Op.ResizeBilinear and op.run_on_npu:
        if op.inputs[0].shape == op.outputs[0].shape:
            # Bypass nop resizebilinear
            op.inputs = op.inputs[:1]
            op.type = Op.Identity
        elif op.inputs[0].shape[1] == 1 and op.inputs[0].shape[2] == 1:
            convert_resizebilinear_1x1_to_add(op)
        else:
            convert_resizebilinear_to_2x2_pool(op)

    return op


def convert_nop_split_to_identity(op, arch, nng):
    if op.type == Op.Split and op.attrs.get("num_splits") == 1:
        # the list comprehension should return a list with a single tensor
        # if it shouldn't, remove_passthrough_tensor will fail appropriately
        op.inputs = [i for i in op.inputs if i.shape == op.outputs[0].shape]
        op.type = Op.Identity
    return op


def fixup_fully_connected_input(op, arch, nng):
    if op.type == Op.FullyConnected:
        inp = op.inputs[0]
        weights = op.inputs[1]

        n_in_elems = weights.shape[-2]
        elms = inp.elements()
        batch_size = elms // n_in_elems
        assert batch_size * n_in_elems == elms

        desired_shape = [batch_size, n_in_elems]
        if inp.shape != desired_shape:
            # mismatch, insert a reshape to fix this.
            op.set_input_tensor(create_reshape_tensor(inp, desired_shape), 0)

    return op


def convert_batched_fc_to_conv(op, arch, nng):
    if op.type == Op.FullyConnected:
        ifm = op.inputs[0]
        ofm = op.outputs[0]
        # Check if the FC is 2D and first dimension indicates batching
        if len(ifm.shape) == len(ofm.shape) == 2 and ifm.shape[0] > 1:
            n = ifm.shape[0]
            batching_split = {4: (2, 2), 8: (2, 4), 16: (4, 4)}
            h, w = batching_split.get(n, (1, n))

            # Convert to convolution
            op.name += "_conv"
            op.type = Op.Conv2DBias
            op.attrs = {
                "dilation": (1, 1, 1, 1),
                "dilation_h_factor": 1,
                "dilation_w_factor": 1,
                "padding": b"SAME",
                "stride_h": 1,
                "stride_w": 1,
                "strides": (1, 1, 1, 1),
                "is_converted_fc": True,
            }

            prev_op = ifm.ops[0]
            desired_shape = [1, h, w, ifm.shape[-1]]
            if len(ifm.consumer_list) == 1 and prev_op is not None and prev_op.type == Op.Reshape:
                # There is a preceding Reshape
                # Compare input of prev_op and input of op, to see if prev_op can be removed
                ifm_prev_op = prev_op.inputs[0]
                if ifm_prev_op.shape == ifm.shape and check_quantized_tens_scaling_equal(ifm_prev_op, ifm):
                    # prev_op can be removed
                    op.set_input_tensor(ifm_prev_op, 0)
                else:
                    op.inputs[0].set_all_shapes(desired_shape)
                    prev_op.set_input_tensor(
                        create_const_tensor(prev_op.inputs[1].name, [1], DataType.int32, desired_shape), 1
                    )
                    prev_op.attrs["new_shape"] = desired_shape
            else:
                # Add reshape op to the input if there is no preceding reshape
                ifm.consumer_list.remove(op)
                op.set_input_tensor(create_reshape_tensor(ifm, desired_shape), 0)

            # Reshape Weights to be 4D. IO becomes HWIO
            weight_tensor = op.inputs[1]
            weight_tensor.quant_values = np.expand_dims(np.expand_dims(weight_tensor.quant_values, axis=0), axis=0)
            weight_tensor.set_all_shapes(list(weight_tensor.quant_values.shape))

            desired_shape = [1, h, w, ofm.shape[-1]]
            if (
                len(ofm.consumer_list) == 1
                and ofm.consumer_list[0] is not None
                and ofm.consumer_list[0].type == Op.Reshape
            ):
                # There is a subsequent Reshape
                # Compare desired shape and output of consumer op, to see if consumer op can be removed
                ofm_cons_op = ofm.consumer_list[0].outputs[0]
                if desired_shape == ofm_cons_op.shape and check_quantized_tens_scaling_equal(ofm, ofm_cons_op):
                    op.outputs[0] = ofm_cons_op
                    op.outputs[0].ops = [op]
                else:
                    op.outputs[0].set_all_shapes(desired_shape)
            else:
                # Add rehape op to the output
                op.set_output_tensor(create_reshape_tensor(ofm, desired_shape, False))
    return op


def fixup_pack_input(op, arch, nng):
    if op.type == Op.Pack:
        # Pack is also referred to as Stack
        # Requires the rewrite_concat function to be called on the op afterwards
        axis = int(op.attrs["axis"])
        desired_shape = op.inputs[0].shape[:axis] + [1] + op.inputs[0].shape[axis:]

        # Construct 1 shape tensor to be used by all inserted reshape ops
        new_shape_tens = create_const_tensor(op.name + "_reshape_shape", [1], DataType.int32, desired_shape)

        for idx, inp in enumerate(op.inputs):
            reshape_out = inp.clone("_reshaped")
            reshape_out.set_all_shapes(desired_shape)

            reshape_op = Operation(Op.Reshape, "{}{}_reshape".format(op.name, idx))
            reshape_op.attrs["new_shape"] = desired_shape
            reshape_op.inputs = [inp, new_shape_tens]
            reshape_op.set_output_tensor(reshape_out)
            DebugDatabase.add_optimised(op, reshape_op)

            op.inputs[idx] = reshape_out

        op.type = Op.PackReshaped

    return op


def unfuse_activation_function(op, arch, nng):
    if op.type == Op.ConcatTFLite and op.run_on_npu and op.activation is not None:
        act_op = Operation(op.activation.op_type, op.name + op.activation.op_type.name)
        op.activation = None
        out_tens = op.outputs[0]
        intermediate_tens = out_tens.clone("_act_intermediate")
        act_op.set_output_tensor(out_tens)
        act_op.add_input_tensor(intermediate_tens)
        op.set_output_tensor(intermediate_tens)

    return op


def fixup_stridedslice_output(tens, arch, nng):
    op = tens.ops[0]
    if op.run_on_npu and op.type == Op.StridedSlice:
        reshape_input_shape = tens.shape
        new_axis_mask = op.attrs["new_axis_mask"]
        shrink_axis_mask = op.attrs["shrink_axis_mask"]

        if shrink_axis_mask != 0:
            n = 0
            axis = 0
            while shrink_axis_mask:
                prev_mask = shrink_axis_mask
                n += 1
                shrink_axis_mask &= shrink_axis_mask - 1
                axis = int(math.log2(prev_mask - shrink_axis_mask))
                reshape_input_shape = reshape_input_shape[:axis] + [1] + reshape_input_shape[axis:]

            assert len(tens.shape) == (len(op.inputs[0].shape) - n)
            op.attrs["shrink_axis_mask"] = 0
        elif new_axis_mask != 0:
            n = 0
            axis = 0
            while new_axis_mask:
                prev_mask = new_axis_mask
                n += 1
                new_axis_mask &= new_axis_mask - 1
                axis = int(math.log2(prev_mask - new_axis_mask))
                reshape_input_shape = reshape_input_shape[:axis] + reshape_input_shape[(axis + 1) :]
                new_axis_mask >>= 1

            assert len(tens.shape) == (len(op.inputs[0].shape) + n)
            op.attrs["new_axis_mask"] = 0
        else:
            # Equal Rank StridedSlice, no need to insert reshape
            return tens

        # Construct 1 shape tensor to be used by all inserted reshape ops
        new_shape_tens = create_const_tensor(op.name + "_reshape_shape", [1], DataType.int32, tens.shape)

        for idx, out_tens in enumerate(op.outputs):
            reshape_in = out_tens.clone("_reshaped")
            reshape_in.set_all_shapes(reshape_input_shape)
            reshape_in.ops = [op]

            reshape_op = Operation(Op.Reshape, "{}{}_reshape".format(op.name, idx))
            reshape_op.attrs["new_shape"] = reshape_input_shape
            reshape_op.inputs = [reshape_in, new_shape_tens]
            reshape_op.set_output_tensor(out_tens)

            op.outputs[idx] = reshape_in

    return tens


def fixup_unpack_output(tens, arch, nng):
    op = tens.ops[0]
    if op.run_on_npu and op.type == Op.Unpack:
        # Unpack is also referred to as Unstack
        # Requires the rewrite_split function to be called on the op afterwards
        axis = int(op.attrs["axis"])
        op.type = Op.UnpackReshaped
        reshape_input_shape = tens.shape[:axis] + [1] + tens.shape[axis:]

        # Construct 1 shape tensor to be used by all inserted reshape ops
        new_shape_tens = create_const_tensor(op.name + "_reshape_shape", [1], DataType.int32, tens.shape)

        for idx, out_tens in enumerate(op.outputs):
            reshape_in = out_tens.clone("_reshaped")
            reshape_in.set_all_shapes(reshape_input_shape)
            reshape_in.ops = [op]

            reshape_op = Operation(Op.Reshape, "{}{}_reshape".format(op.name, idx))
            reshape_op.attrs["new_shape"] = reshape_input_shape
            reshape_op.inputs = [reshape_in, new_shape_tens]
            reshape_op.set_output_tensor(out_tens)
            DebugDatabase.add_optimised(op, reshape_op)

            op.outputs[idx] = reshape_in

    return tens


def add_padding_fields(op, arch, nng):
    if op.run_on_npu:
        if "padding" in op.attrs:
            if op.type.is_conv2d_op() or op.type.is_depthwise_conv2d_op():
                kernel_size = op.inputs[1].shape[:2]
                input_shape = op.inputs[0].shape
            elif op.type.is_pool_op() or op.type.npu_block_type == NpuBlockType.ReduceSum:
                kernel_size = op.attrs["ksize"][1:3]
                input_shape = op.inputs[0].shape
            else:
                raise UnsupportedFeatureError("Unknown operation that uses padding: {}".format(op.type))

            if op.type == Op.Conv2DBackpropInputSwitchedBias:
                upscaling_factor = op.outputs[0].shape[1] // input_shape[1]
                padding, skirt = calc_upscaled_padding_and_skirt(
                    op.attrs["padding"], kernel_size, op.attrs["strides"], input_shape, upscaling_factor
                )
            else:
                dilation_h, dilation_w = op.get_dilation_h_w()
                dilated_kernel_size = [dilation_h * (kernel_size[0] - 1) + 1, dilation_w * (kernel_size[1] - 1) + 1]
                padding, skirt = calc_padding_and_skirt(
                    op.attrs["padding"], dilated_kernel_size, op.attrs["strides"], input_shape
                )

            op.attrs["explicit_padding"] = padding
            op.attrs["skirt"] = skirt

    return op


# Check if the op can be reordered
def get_prepend_op(op):
    inp = op.inputs[0]
    # The op should be reordered between prev_op and prep_op
    prev_op = inp.ops[-1]
    prep_op = None
    while prev_op.type in memory_only_ops and len(prev_op.outputs) == 1 and len(prev_op.outputs[0].consumers()) == 1:
        prep_op = prev_op
        inp = prev_op.inputs[0]
        prev_op = inp.ops[-1]
    if prev_op is not None and len(prev_op.outputs) == 1 and len(prev_op.outputs[0].consumers()) == 1:
        return prep_op

    return None


def convert_depthwise_to_conv(op, arch, nng):
    # Depthwise is equivalent to a single conv2d if the ifm depth is 1 and
    # the ofm depth equals the depth multipler.
    # If those conditions are true, then we can perform a simple
    # switch of the operator type (and weight order)

    if op.type == Op.DepthwiseConv2DBias and (op.attrs["depth_multiplier"] != 1):
        ifm_tensor = op.inputs[0]
        weight_tensor = op.inputs[1]
        ofm_tensor = op.outputs[0]
        if (ifm_tensor.shape[3] == 1) and (ofm_tensor.shape[3] == op.attrs["depth_multiplier"]):
            # Change op type to Conv2d
            op.type = Op.Conv2DBias
            del op.attrs["channel_multiplier"]
            del op.attrs["depth_multiplier"]

            weight_tensor.quant_values = np.transpose(weight_tensor.quant_values, (0, 1, 3, 2))
            weight_tensor.set_all_shapes(list(weight_tensor.quant_values.shape))
        else:
            raise UnsupportedFeatureError(
                "Unsupported DepthwiseConv2d with depth_multiplier = {}, ifm channels = {}, ofm channels = {}".format(
                    op.attrs["depth_multiplier"], ifm_tensor.shape[3], ofm_tensor.shape[3]
                )
            )
        DebugDatabase.add_optimised(op, op)
    return op


def reorder_depthwise_weights(op, arch, nng):
    if op.type.is_depthwise_conv2d_op():
        weight_tensor = op.inputs[1]
        weight_tensor.quant_values = np.transpose(weight_tensor.quant_values, (0, 1, 3, 2))
        weight_tensor.set_all_shapes(list(weight_tensor.quant_values.shape))
        weight_tensor.weight_transpose_depthwise = True

    return op


def convert_conv_to_fc(op, arch, nng):
    # Conv 1x1 can be equivalent to Fully Connected.
    # By representing certain convs as fully connected layers, Vela can better determine wether or not to use
    # caching/double buffering for the weights.
    # (Weights dont need to be reloaded for convs when IFM H and W are 1)
    if op.type == Op.Conv2DBias:
        _, h, w, _ = op.inputs[0].shape
        kh, kw, _, _ = op.inputs[1].shape
        if h == 1 and w == 1 and kh == 1 and kw == 1:
            # Overwrite this op as a Fully Connected Op
            op.name += "_fc"
            op.type = Op.FullyConnected
            op.attrs = {
                "weights_format": 0,
            }
            # Reshape Weights to be 2D. HWIO becomes just IO (as H and W are 1, they can just be dropped)
            weight_tensor = op.inputs[1]
            weight_tensor.quant_values = weight_tensor.quant_values.squeeze(axis=(0, 1))
            weight_tensor.set_all_shapes(list(weight_tensor.quant_values.shape))
            # The output from a fully connected is expected to be 2D so we need to add a reshape layer to convert it
            # back to 4D afterwards as the next layer is expecting that shape
            orig_ofm_tensor = op.outputs[0]
            # Reshape this ops output to be 2D: {(N*H*W), C} (We know N H and W are all 1 so this becomes {1, C})
            fc_ofm_tensor = orig_ofm_tensor.clone("_fc")
            fc_ofm_tensor.set_all_shapes([1, fc_ofm_tensor.shape[-1]])
            fc_ofm_tensor.ops = [op]
            # Add a reshape after the new OFM to convert it back to the original 4D shape
            reshape_name = op.name + "_reshape"
            new_shape_tens = create_const_tensor(reshape_name + "_shape", [1], DataType.int32, orig_ofm_tensor.shape)
            reshape_op = Operation(Op.Reshape, reshape_name)
            reshape_op.attrs["new_shape"] = orig_ofm_tensor.shape
            reshape_op.inputs = [fc_ofm_tensor, new_shape_tens]
            reshape_op.set_output_tensor(orig_ofm_tensor)
            # Replace this ops OFM to point to the 2D tensor
            op.outputs[0] = fc_ofm_tensor
            # Record optimisation in debug database
            DebugDatabase.add_optimised(op, reshape_op)
            DebugDatabase.add_optimised(op, op)
    return op


def fixup_relus_with_differing_ifm_ofm_scaling(op, arch, nng):
    if op.run_on_npu and op.type.is_relu_op():
        ifm = op.inputs[0]
        ofm = op.outputs[0]
        # Relu with differing IFM and OFM scaling cannot be fused with another primary op
        # and requires its own to be inserted
        if not check_quantized_tens_scaling_equal(ifm, ofm):
            # Override this op with its own primary op (avgpool)
            relu_fused_op = create_avgpool_nop(op.name + "_avgpool")
            # And fuse the original activation function to it
            relu_fused_op.activation = create_activation_function(op.type)
            # Tidy up and assign the ifm and ofm to the new op
            ifm.consumer_list.remove(op)

            # if not 4d, reshape ifm/ofm
            if len(ifm.shape) < 4:
                ifm_shaped = create_reshape_tensor(ifm, full_shape(4, ifm.shape, 1))
                ifm = ifm_shaped
            if len(ofm.shape) < 4:
                ofm_shaped = create_reshape_tensor(ofm, full_shape(4, ofm.shape, 1), False)
                ofm = ofm_shaped

            relu_fused_op.add_input_tensor(ifm)
            relu_fused_op.set_output_tensor(ofm)
            op = relu_fused_op
    return op


# Reorder activation op if it's after the memory only operations
def fixup_act_reorder(op, arch, nng):
    if op.type.is_relu_op() or op.type in set((Op.Sigmoid, Op.Tanh)):
        prep_op = get_prepend_op(op)
        if prep_op is not None:
            act_op = op.clone("_reordered")

            # There is only one input tensor, overwrite it
            act_op.set_input_tensor(prep_op.inputs[0], 0)

            act_op_out = act_op.inputs[0].clone("_acted")
            act_op_out.quantization = op.outputs[0].quantization.clone()
            act_op.set_output_tensor(act_op_out)

            # Update the consumer list
            act_op_out.consumer_list = op.outputs[0].consumer_list.copy()
            act_op_out.consumer_list.append(prep_op)

            prep_op.inputs[0] = act_op_out
            prep_op.outputs[0].quantization = act_op_out.quantization.clone()

            # Mark the op so that it will be removed as passthrough later on
            op.type = Op.Identity

            # Record optimisation in debug database
            DebugDatabase.add_optimised(op, act_op)
            DebugDatabase.add_optimised(op, op)
    return op


def fixup_elementwise_with_scalars(op, arch, nng):
    if op.type.is_binary_elementwise_op():
        ifm_tensor, ifm2_tensor, _, _ = op.get_ifm_ifm2_weights_ofm()
        if ifm2_tensor.shape != [] and ifm_tensor.shape != []:
            diff = len(ifm_tensor.shape) - len(ifm2_tensor.shape)
            if diff > 0:
                ifm2_tensor.shape = full_shape(len(ifm_tensor.shape), ifm2_tensor.shape, 1)
            elif diff < 0:
                ifm_tensor.shape = full_shape(len(ifm2_tensor.shape), ifm_tensor.shape, 1)
        elif ifm_tensor.shape == [] and ifm_tensor.quant_values is None:
            # IFM is marked as a scalar, but is a result of an operation; change it to a shape of size 1
            ifm_tensor.shape = len(ifm2_tensor.shape) * [1]
            ifm_tensor.storage_shape = ifm_tensor.shape
        elif ifm2_tensor.shape == [] and ifm2_tensor.quant_values is None:
            # IFM2 is marked as a scalar, but is a result of an operation; change it to a shape of size 1
            ifm2_tensor.shape = len(ifm_tensor.shape) * [1]
            ifm2_tensor.storage_shape = ifm2_tensor.shape
    return op


# Set input/output tensor equivalence to the same id for memory operations
def set_tensor_equivalence(op, arch, nng):
    if op.type in memory_only_ops:
        eid = op.outputs[0].equivalence_id
        for inp in op.inputs:
            inp.equivalence_id = eid
    return op


def convert_softmax(op, arch, nng):
    if op.type == Op.Softmax and op.run_on_npu:
        softmax = SoftMax(op)
        op = softmax.get_graph()
    return op


def convert_mul_max_to_abs_or_lrelu(op, arch, nng):
    r"""Whenever there is a subgraph with this topology:

       Input    X   For X = -1 or X > 0
       |   \   /    This subgraph can be replaced with either
       |    Mul     an Abs (if X = -1) or a LeakyReLU (if X > 0)
       |   /
       Max
    """

    if op.type == Op.Maximum:
        # finds the Mul input(s) to the Max
        muls = [i for i in op.inputs if i.ops[0].type == Op.Mul]
        if len(muls) == 1:
            mul = muls[0].ops[0]
        elif len(muls) == 2:
            # In the case both inputs are Muls, find the one with the same input as the Max
            mul = [m for m in muls if len(set(op.inputs + m.ops[0].inputs)) == 1][0].ops[0]
        else:
            # No Mul inputs
            return op

        # make sure the Mul doesn't have any other consumers
        mul_ofm = mul.outputs[0]
        if len(mul_ofm.consumers()) != 1:
            return op
        # make sure the Mul doesn't have a fused activation function
        if mul.activation:
            return op
        ifm, ofm = op.get_ifm_ofm()
        if ifm is None or ofm is None:
            return op

        if ifm.dtype not in (DataType.uint8, DataType.int8) or ifm.dtype != ofm.dtype:
            return op
        if not check_quantized_tens_scaling_equal(ifm, ofm) or not check_quantized_tens_scaling_equal(ifm, mul_ofm):
            # rewrite to LeakyRelu currently only makes sense if the quantization is identical
            return op

        # finds the branched input that goes to both the Max and the Mul
        shared = set(op.inputs) & set(mul.inputs)
        if len(shared) == 1:
            shared_in = shared.pop()
            # find the constant scalar input to the Mul
            const_tens = (set(mul.inputs) - {shared_in}).pop()
            # check that it is a scalar
            if const_tens.shape != []:
                return op
            const = const_tens.ops[0]
            # check that it is a constant
            if const.type != Op.Const:
                return op
            # Remove the Mul from the shared input's consumers
            shared_in.consumer_list.remove(mul)
        else:
            return op

        val = const.outputs[0].values
        if val >= 0:
            new_op = Op.LeakyRelu
            op.attrs["alpha"] = val
            # to produce bit exact results, the alpha is not enough;
            # save additional scaling info in attr "alpha_scale", to be used as input
            # to the LUT construction
            alpha_scalar = const_tens.quant_values - const_tens.quantization.zero_point
            mul_ifm_scale = np.double(ifm.quantization.scale_f32)
            mul_ifm2_scale = np.double(const_tens.quantization.scale_f32)
            mul_ofm_scale = np.double(mul_ofm.quantization.scale_f32)
            alpha_scale, alpha_shift = scaling.elementwise_mul_scale(mul_ifm_scale, mul_ifm2_scale, mul_ofm_scale)
            op.attrs["alpha_scaling"] = (alpha_scalar, alpha_scale, alpha_shift)
        elif val == -1:
            new_op = Op.Abs
        else:
            return op

        op.type = new_op
        op.name = op.name.replace("Maximum", new_op.name)
        op.outputs[0].name = op.outputs[0].name.replace("Maximum", new_op.name)
        op.inputs = [shared_in]

        # Record optimisation in debug database
        DebugDatabase.add_optimised(op, op)

    return op


def convert_lrelu_to_mul_max(op, arch):
    # Converts LeakyRelu to Max(alpha * IFM, identity * IFM)
    # (the opposite of convert_mul_max_to_abs_or_lrelu)
    ifm, ofm = op.get_ifm_ofm()
    if ifm is None or ofm is None:
        return op

    # Add multiplication with alpha
    mul_alpha = Operation(Op.Mul, op.name + "_mul_alpha")
    mul_alpha.add_input_tensor(ifm)
    # Create const tensor containing alpha as scalar
    alpha = op.attrs["alpha"]
    quantization = ifm.quantization.clone()
    quantization.min = 0
    quantization.max = alpha * (quantization.quant_max - quantization.quant_min)
    quantization.scale_f32 = alpha
    quantization.zero_point = 0
    alpha_tens = create_const_tensor(op.name + "_alpha_scalar", [], ifm.dtype, [1], np.int8, quantization=quantization)
    mul_alpha.add_input_tensor(alpha_tens)
    fm_alpha = ofm.clone(op.name + "_alpha")
    mul_alpha.set_output_tensor(fm_alpha)
    DebugDatabase.add_optimised(op, mul_alpha)

    if check_quantized_tens_scaling_equal(ifm, ofm):
        # No identity multiplication is needed
        fm_id = ifm
    else:
        # Add multiplication with identity
        mul_identity = Operation(Op.Mul, op.name + "_mul_identity")
        mul_identity.add_input_tensor(ifm)
        # Create const tensor containing identity as scalar
        quantization = ifm.quantization.clone()
        quantization.min = 0
        quantization.max = quantization.quant_max - quantization.quant_min
        quantization.scale_f32 = 1
        quantization.zero_point = 0
        identity_tens = create_const_tensor(
            op.name + "_id_scalar", [], ifm.dtype, [1], np.uint8, quantization=quantization
        )
        mul_identity.add_input_tensor(identity_tens)
        fm_id = ofm.clone(op.name + "_id")
        mul_identity.set_output_tensor(fm_id)
        DebugDatabase.add_optimised(op, mul_alpha)

    # Convert LeakyRelu to Max, add the results of the multiplication(s) as inputs
    op.type = Op.Maximum
    op.name = op.name.replace("LeakyRelu", "Maximum")
    op.inputs = []
    ifm.consumer_list.remove(op)
    op.add_input_tensor(fm_alpha)
    op.add_input_tensor(fm_id)

    DebugDatabase.add_optimised(op, op)
    return op


def convert_to_lut(op, lut_values, lut_name):
    # Rewrite the operation by Add with scalar 0 + LUT activation
    ifm = op.inputs[0]
    if ifm is None:
        return op
    assert ifm.dtype.size_in_bytes() == 1
    op.type = Op.Add
    op.name = op.name + "_lut_" + lut_name
    # Mark as no-op to enable potential fusing optimizations
    op.attrs["is_nop"] = True
    # Create an input tensor containing scalar zero
    quantization = QuantizationParameters(0.0, 255.0)
    quantization.scale_f32 = ifm.quantization.scale_f32
    quantization.zero_point = 0
    tens = create_const_tensor(op.inputs[0].name + "_scalar0", [], ifm.dtype, [0], np.uint8, quantization=quantization)
    op.add_input_tensor(tens)
    # The LUT must be applied without any preceding rescaling (the LUT itself performs the rescale),
    # so even if the OFM has a different scale than the IFM, the generated OFM scale instructions
    # should be the same as the IFM
    op.forced_output_quantization = ifm.quantization
    lut_tensor = lut.create_lut_tensor(op.name + "_values", lut_values, DataType.int8)
    op.set_activation_lut(lut_tensor)
    return op


def convert_to_lut8(op, fn, fn_name):
    # Converts op to a no-op + int8/uint8 LUT which is generated with the given function.
    # fn is a function(real) -> real
    ifm, ofm = op.get_ifm_ofm()
    if ifm.dtype not in (DataType.uint8, DataType.int8) or ifm.dtype != ofm.dtype:
        return op
    # Generate the LUT
    ifm_scale = np.double(ifm.quantization.scale_f32)
    ofm_scale = np.double(ofm.quantization.scale_f32)
    zp_in = ifm.quantization.zero_point
    zp_out = ofm.quantization.zero_point
    values = []
    ix = range(256) if ifm.dtype == DataType.uint8 else range(-128, 128)
    quantized_min = min(ix)
    quantized_max = max(ix)
    for x in ix:
        x_real = ifm_scale * (x - zp_in)
        y_real = fn(x_real)
        lut_result = round_away_zero(zp_out + y_real / ofm_scale)
        lut_result = min(quantized_max, max(quantized_min, lut_result))
        values.append(lut_result)
    return convert_to_lut(op, values, fn_name)


def convert_lrelu_to_lut(op, arch):
    ifm, ofm = op.get_ifm_ofm()
    # Generate the LUT
    alpha = op.attrs["alpha"]
    ifm_scale = np.double(ifm.quantization.scale_f32)
    ofm_scale = np.double(ofm.quantization.scale_f32)
    zp_in = ifm.quantization.zero_point
    zp_out = ofm.quantization.zero_point
    identity_scale, identity_shift = scaling.elementwise_mul_scale(ifm_scale, 1, ofm_scale)
    alpha_scalar = 1
    alpha_scale, alpha_shift = scaling.elementwise_mul_scale(ifm_scale, alpha, ofm_scale)
    if "alpha_scaling" in op.attrs:
        # The LeakyRelu was the result from convert_mul_max_to_abs_or_lrelu
        alpha_scalar, alpha_scale, alpha_shift = op.attrs["alpha_scaling"]
    values = []
    ix = range(256) if ifm.dtype == DataType.uint8 else range(-128, 128)
    quantized_min = min(ix)
    quantized_max = max(ix)
    for x in ix:
        if x < zp_in:
            lut_result = zp_out + fp_math.multiply_by_quantized_multiplier(
                alpha_scalar * (x - zp_in), alpha_scale, alpha_shift
            )
        else:
            lut_result = zp_out + fp_math.multiply_by_quantized_multiplier(x - zp_in, identity_scale, identity_shift)
        lut_result = min(quantized_max, max(quantized_min, lut_result))
        values.append(lut_result)
    return convert_to_lut(op, values, "lrelu")


def convert_lrelu(op, arch, nng):
    # Converts LeakyRelu to a LUT based solution if possible, otherwise a mul + max
    if op.type != Op.LeakyRelu:
        return op
    ifm, ofm = op.get_ifm_ofm()
    if ifm is None or ofm is None:
        return op
    if ifm.dtype in (DataType.uint8, DataType.int8) and ifm.dtype == ofm.dtype:
        # use LUT for int8/uint8
        return convert_lrelu_to_lut(op, arch)
    if check_quantized_tens_scaling_equal(ifm, ofm) and ifm.dtype == ofm.dtype == DataType.int16:
        # use LeakyRelu unmodified for int16 with equal input/output scaling
        return op
    return convert_lrelu_to_mul_max(op, arch)


def convert_tanh_sigmoid_to_lut(op, arch, nng):
    # Converts int8/uint8 Sigmoid and Tanh to a LUT based solution
    if op.type == Op.Sigmoid:
        return convert_to_lut8(op, clamp_sigmoid, "sigmoid")
    elif op.type == Op.Tanh:
        return convert_to_lut8(op, math.tanh, "tanh")
    return op


def remove_unwanted_reshapes(op, arch, nng):
    # Try to remove reshapes enclosing ElementWise operator with only one non-constant input
    if not op.run_on_npu or not op.type.is_elementwise_op():
        return op

    # Check if the ElementWise operator only have one non-constant input
    non_const_tens = [x for x in op.inputs if x.ops[0].type != Op.Const]
    if len(non_const_tens) != 1:
        return op
    ifm = non_const_tens[0]

    # Check if operation is enclosed by Reshapes that can be removed
    ofm = op.outputs[0]
    prev_op = ifm.ops[0]
    if (
        len(ifm.consumer_list) == 1
        and prev_op.type == Op.Reshape
        and len(ofm.consumer_list) == 1
        and ofm.consumer_list[0].type == Op.Reshape
    ):
        # Operation is enclosed by reshapes, check if they can be removed
        prev_op_ifm, prev_op_ofm = prev_op.get_ifm_ofm()
        cons_op = ofm.consumer_list[0]
        cons_op_ifm = ofm
        cons_op_ofm = cons_op.outputs[0]
        if len(prev_op_ifm.shape) == len(cons_op_ofm.shape):
            # Check if quantization is the same in the input and output for the reshape ops
            if check_quantized_tens_scaling_equal(prev_op_ifm, prev_op_ofm) and check_quantized_tens_scaling_equal(
                cons_op_ifm, cons_op_ofm
            ):
                op.set_input_tensor(prev_op_ifm, 0)
                op.set_output_tensor(cons_op_ofm)
    return op


def fuse_activation_function_with_prev(op, arch, nng):
    # if op is a no-op: attempts to move the activation function to the preceding op
    if not op.attrs.get("is_nop", False) or op.activation is None:
        return op
    ifm, ofm = op.get_ifm_ofm()
    if ifm is None or ofm is None:
        return op
    # finds the input(s) to the operation
    prev_op = ifm.ops[0]
    # Note: the below checks on prev_op require that a first optimize pass on the full graph has been performed
    fuse = (
        prev_op.run_on_npu
        and prev_op.type.npu_block_type != NpuBlockType.Default
        and len(ifm.ops) == 1
        and len(prev_op.outputs[0].consumers()) == 1
        and prev_op.activation is None
    )
    if op.activation_lut is not None and arch.shram_reserved_unused_banks == 0:
        # TODO: if SHRAM LUT space is shared with SHRAM ACC (32, 64 MAC),
        # LUT currently only works correctly for elementwise ops
        fuse = False
    if not fuse:
        return op
    # Move the fused activation function + corresponding info to prev_op
    prev_op.activation = op.activation
    prev_op.forced_output_quantization = op.forced_output_quantization
    if op.activation_lut is not None:
        prev_op.set_activation_lut(op.activation_lut)
    # Bypass op
    prev_op.set_output_tensor(ofm)
    DebugDatabase.add_optimised(op, prev_op)
    return op


def add_attrs_to_resizebilinear(op, arch, nng):
    if op.type == Op.ResizeBilinear and op.run_on_npu:
        input_tensor = op.inputs[0]
        upscaled_shape = [input_tensor.shape[1] * 2, input_tensor.shape[2] * 2]
        out_shape = op.outputs[0].shape[1:3]
        if not op.attrs["align_corners"] and out_shape == upscaled_shape:
            # this means the output is supposed to be a x2 upscale,
            # so we need to do SAME padding
            op.attrs["padding"] = b"SAME"
        elif op.attrs["align_corners"] and out_shape == [upscaled_shape[0] - 1, upscaled_shape[1] - 1]:
            # here we can just run the avg pool without padding and
            # produce a (M * 2 - 1, N * 2 - 1) sized output
            op.attrs["padding"] = b"VALID"
        else:
            return op
        input_tensor.resampling_mode = resampling_mode.NEAREST
        op.attrs.update({"strides": (1, 1, 1, 1), "ksize": (1, 2, 2, 1)})
    return op


def fixup_bias_tensors(op, arch, nng):
    if op.type.needs_bias() and op.bias is None:
        # Op has no bias, add bias tensor filled with zeros
        nr_biases = op.inputs[1].shape[-1]
        bias_values = [0] * nr_biases
        bias_tensor = create_const_tensor(op.name + "_bias", [nr_biases], DataType.int32, bias_values)
        bias_tensor.quant_values = bias_tensor.values
        op.set_input_tensor(bias_tensor, -1)

    return op


def supported_operator_check(op, arch, nng):
    op.run_on_npu = arch.supported_operators.is_operator_supported(op)
    return op


def _record_optimised(op, arch):
    if op.type != Op.Const:
        DebugDatabase.add_optimised(op, op)


def optimise_graph_a(nng, arch, verbose_graph=False):
    if verbose_graph:
        nng.print_graph()

    op_rewrite_list = [
        set_tensor_equivalence,
        supported_operator_check,
        # then do any rewrites of supported operators
        convert_depthwise_to_conv,
        convert_conv_to_fc,
        convert_softmax,
        fixup_fully_connected_input,
        convert_batched_fc_to_conv,
        fixup_pack_input,
        unfuse_activation_function,
        fixup_conv2d_backprop,
        fixup_relus_with_differing_ifm_ofm_scaling,
        fixup_act_reorder,
        fixup_elementwise_with_scalars,
        reorder_depthwise_weights,
        fixup_resizebilinear,
        fixup_bias_tensors,
        convert_nop_split_to_identity,
        convert_mul_max_to_abs_or_lrelu,
        remove_unwanted_reshapes,
        convert_lrelu,
        convert_tanh_sigmoid_to_lut,
    ]

    for idx, sg in enumerate(nng.subgraphs):
        # rewrite graph pass
        nng.subgraphs[idx] = rewrite_graph.rewrite_graph_pre_order(
            nng, sg, arch, [], op_rewrite_list, rewrite_unsupported=False,
        )

    for idx, sg in enumerate(nng.subgraphs):
        # remove passthrough tensors and attempt further optimizations
        nng.subgraphs[idx] = rewrite_graph.rewrite_graph_pre_order(
            nng, sg, arch, [remove_passthrough_tensor], [fuse_activation_function_with_prev, add_padding_fields]
        )

    # Post-optimisation operator debug tracing
    for sg in nng.subgraphs:
        rewrite_graph.visit_graph_post_order(sg.output_tensors, arch, [], [_record_optimised])

    if verbose_graph:
        nng.print_graph()
    return nng


def optimise_graph_b(nng, arch, verbose_graph=False):
    if verbose_graph:
        nng.print_graph()

    for idx, sg in enumerate(nng.subgraphs):
        # combined rewrite graph pass
        nng.subgraphs[idx] = rewrite_graph.rewrite_graph_pre_order(
            nng, sg, arch, [fixup_unpack_output, fixup_stridedslice_output, rewrite_concat, rewrite_split], []
        )

    if verbose_graph:
        nng.print_graph()
    return nng

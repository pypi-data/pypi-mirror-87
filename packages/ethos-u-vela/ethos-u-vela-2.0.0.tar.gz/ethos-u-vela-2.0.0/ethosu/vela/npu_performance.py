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
# NPU performance estimation functions to estimate performance of a Pass and CascadedPass. Uses a model that takes the
# maximum of the 'cycles required for bandwidth' and 'cycles required for computing'.
#
# Called during scheduling to evaluate different proposals, as well as post-scheduling to provide a final performance
# estimate.
from enum import auto
from enum import IntEnum

import numpy as np

from . import numeric_util
from .architecture_features import Accelerator
from .architecture_features import Block
from .data_type import DataType
from .nn_graph import PassPlacement
from .nn_graph import SchedulerRewrite
from .operation import NpuBlockType
from .operation import Op
from .shared_buffer_allocation import is_acc_40bits_used
from .tensor import MemArea
from .tensor import shape_num_elements
from .tensor import Tensor
from .tensor import TensorBlockTraversal
from .tensor import TensorFormat
from .tensor import TensorPurpose


def rolling_buffer_dims_from_passes(arch, ps1, block_config_ps1, ps2, block_config_ps2):
    ofm_block = Block(block_config_ps2[-3], block_config_ps2[-4], block_config_ps2[-1])
    kernel = ps2.primary_op.kernel

    if ps2.npu_block_type in set((NpuBlockType.ConvolutionMxN, NpuBlockType.VectorProduct)):
        op = ps2.primary_op
        ifm_block_depth = arch.calc_ifm_block_depth(op.ifm.shape[-1], op.ifm.dtype.size_in_bits())
    else:
        ifm_block_depth = block_config_ps2[-1]

    ifm_block = arch.get_ifm_block_size(ifm_block_depth, ofm_block, kernel, arch.ofm_block_max)

    # The performed height calculation is for worst case
    height = numeric_util.round_up(ifm_block.height + block_config_ps1[0], block_config_ps1[0])
    width = ifm_block.width
    return [height, width]


class PassCycles(IntEnum):
    Npu = 0
    SramAccess = auto()
    DramAccess = auto()
    OnChipFlashAccess = auto()
    OffChipFlashAccess = auto()
    Total = auto()
    Size = auto()

    def display_name(self):
        return ("NPU", "SRAM Access", "DRAM Access", "On-chip Flash Access", "Off-chip Flash Access", "Total", "Size",)[
            self.value
        ]

    def identifier_name(self):
        return ("npu", "sram_access", "dram_access", "on_chip_flash_access", "off_chip_flash_access", "total", "size",)[
            self.value
        ]

    @staticmethod
    def all():
        return (
            PassCycles.Npu,
            PassCycles.SramAccess,
            PassCycles.DramAccess,
            PassCycles.OnChipFlashAccess,
            PassCycles.OffChipFlashAccess,
            PassCycles.Total,
        )


class MacCount(IntEnum):
    NeuralNetworkMacs = 0
    HardwareMacs = auto()
    Size = auto()

    def display_name(self):
        return ("Neural Network Macs", "Hardware Macs", "Size")[self.value]

    def identifier_name(self):
        return ("nn_macs", "hardware_macs", "size")[self.value]

    @staticmethod
    def all():
        return (MacCount.NeuralNetworkMacs, MacCount.HardwareMacs)


class BandwidthDirection(IntEnum):
    Read = 0
    Write = auto()
    Size = auto()

    def display_name(self):
        return self.name

    def identifier_name(self):
        return self.name.lower()

    @staticmethod
    def all():
        return (BandwidthDirection.Read, BandwidthDirection.Write)


def make_bandwidth_array():
    return np.zeros((MemArea.Size, TensorPurpose.Size, BandwidthDirection.Size))


def make_macs_array():
    return np.zeros(MacCount.Size, np.int)


def make_cycles_array():
    return np.zeros(PassCycles.Size)


def make_metrics_arrays():
    return (make_bandwidth_array(), make_macs_array(), make_cycles_array())


def get_n_blocks_and_area(
    ifm_brick_size, ifm_height_width, orig_skirt, clamped_skirt, block_config, min_block_size, strides
):

    ifm_block_config = (block_config[0] * strides[1], block_config[1] * strides[2])

    n_normal_blocks = []
    remainder_size = []
    for i in range(2):
        non_skirt_dim = ifm_height_width[i] - orig_skirt[i] - orig_skirt[2 + i]
        n_blocks = non_skirt_dim // ifm_block_config[i]
        n_normal_blocks.append(n_blocks)
        remainder_dim = numeric_util.round_up(
            ((non_skirt_dim - n_blocks * ifm_block_config[i] - 1) // strides[i + 1]) + 1, min_block_size[i]
        )
        remainder_size.append(remainder_dim)

    # this will actually calculate reads into the edge padding.

    # there are four cases in total, handling the edges that will not fill a complete block.

    # 0000000001
    # 0000000001
    # 0000000001
    # 0000000001
    # 0000000001
    # 0000000001
    # 2222222223
    total_blocks = 0
    total_area = 0

    block_setup = (
        (n_normal_blocks[0] * n_normal_blocks[1], block_config),
        (1 * n_normal_blocks[1], (remainder_size[0], block_config[1])),
        (n_normal_blocks[0] * 1, (block_config[0], remainder_size[1])),
        (1 * 1, remainder_size),
    )

    for n_blocks, block_size in block_setup:
        if block_size[0] == 0 or block_size[1] == 0:
            continue
        read_dims = [0, 0]
        for i in range(2):
            read_dims[i] = (
                numeric_util.round_up(clamped_skirt[i], ifm_brick_size[i + 1])
                + block_size[i] * strides[i + 1]
                + numeric_util.round_up(clamped_skirt[2 + i], ifm_brick_size[i + 1])
            )
        assert n_blocks >= 0
        total_blocks += n_blocks
        total_area += n_blocks * read_dims[0] * read_dims[1]
    assert total_blocks >= 1
    return total_blocks, total_area, block_setup


def get_ifm_block_depth(npu_block_type, ifm_depth, ifm_elemwidth, block_traversal, ofm_blk_depth):
    ifm_blk_depth = ofm_blk_depth

    if npu_block_type == NpuBlockType.ConvolutionMxN or npu_block_type == NpuBlockType.ReduceSum:
        if ifm_elemwidth == 16 or block_traversal == TensorBlockTraversal.PartKernelFirst:
            ifm_blk_depth = 16
        elif ifm_elemwidth == 8:
            ifm_blk_depth = 32
        else:
            ifm_blk_depth = 8

    return min(ifm_depth, ifm_blk_depth)


def get_minimal_cmd_cycles(arch, ifm_tensor, ofm_tensor, ifm_blk: Block, ofm_blk: Block, output_cycles, dpu_cycles=0):
    latencies_rd = {MemArea.Sram: 32, MemArea.Dram: 500, MemArea.OnChipFlash: 64, MemArea.OffChipFlash: 64}
    latencies_wr = {MemArea.Sram: 32, MemArea.Dram: 250, MemArea.OnChipFlash: 64, MemArea.OffChipFlash: 64}
    ifm_tens_blk = Tensor((1, ifm_blk.height, ifm_blk.width, ifm_blk.depth), ifm_tensor.dtype, "ifm_blk")
    ofm_tens_blk = Tensor((1, ofm_blk.height, ofm_blk.width, ofm_blk.depth), ofm_tensor.dtype, "ofm_blk")
    cycles_ifm_blk = (
        estimate_memory_bandwidth(arch, ifm_tensor.mem_area, BandwidthDirection.Read, ifm_tens_blk, ifm_blk)
        / arch.memory_bandwidths_per_cycle[ifm_tensor.mem_area]
    )
    cycles_ofm_blk = (
        estimate_memory_bandwidth(arch, ofm_tensor.mem_area, BandwidthDirection.Write, ofm_tens_blk, ofm_blk)
        / arch.memory_bandwidths_per_cycle[ofm_tensor.mem_area]
    )
    return (
        latencies_rd[ifm_tensor.mem_area]
        + cycles_ifm_blk
        + dpu_cycles
        + output_cycles
        + latencies_wr[ofm_tensor.mem_area]
        + cycles_ofm_blk
    ) / 4


def estimate_output_cycles(
    arch,
    npu_block_type,
    primary_op,
    num_elems,
    ifm_tensor,
    ofm_tensor,
    use_acc_40bits=False,
    ifm2_tensor=None,
    block_config: Block = None,
):
    faf = None if primary_op.activation is None else primary_op.activation.op_type
    if npu_block_type == NpuBlockType.ElementWise and ifm_tensor.dtype == DataType.int32:
        if ifm2_tensor is None:
            # Unary op
            output_perf_index = 0
        else:
            # Binary op
            output_perf_index = 1
    elif primary_op.type == Op.Mul and ofm_tensor.dtype == DataType.int32:
        output_perf_index = 2
    elif primary_op.type == Op.Mul or (
        npu_block_type
        in (
            NpuBlockType.ConvolutionMxN,
            NpuBlockType.ConvolutionDepthWise,
            NpuBlockType.Pooling,
            NpuBlockType.ReduceSum,
            NpuBlockType.VectorProduct,
        )
        and use_acc_40bits
    ):
        output_perf_index = 3
    elif primary_op.type in (Op.Add, Op.Sub):
        input_scale = ifm_tensor.quantization.scale_f32
        input2_scale = ifm2_tensor.quantization.scale_f32
        output_scale = ofm_tensor.quantization.scale_f32

        if "resizebilinear" in primary_op.attrs:
            output_scale = input2_scale

        if None in (input_scale, input2_scale, output_scale) or input_scale == input2_scale:
            # Simple Add/Sub
            output_perf_index = 4
        else:
            # Advanced Add/Sub
            output_perf_index = 5
    elif primary_op.type.is_maxpool_op():
        output_perf_index = 6
    else:
        output_perf_index = 7

    if faf in (Op.Sigmoid, Op.Tanh, Op.LUT):
        activation_perf_index = 0
    elif faf in (Op.Relu, Op.Relu6, Op.ReluN1To1):
        activation_perf_index = 1
    else:
        activation_perf_index = 2

    cycle_per_elem = max(
        arch.output_cycles_per_elem[output_perf_index], arch.activation_cycles_per_elem[activation_perf_index]
    )

    if primary_op.type.is_elementwise_op() and block_config is not None:
        num_elems_blk = block_config.width * block_config.height * block_config.depth
        cycle_cmd = get_minimal_cmd_cycles(
            arch, ifm_tensor, ofm_tensor, block_config, block_config, num_elems_blk * cycle_per_elem
        )
        cycle_per_elem = max(cycle_per_elem, cycle_cmd / num_elems_blk)

    return num_elems * cycle_per_elem


def estimate_conv_pooling_cycles(
    arch,
    npu_block_type,
    primary_op,
    ifm_block: Block,
    ofm_block: Block,
    block_traversal,
    kernel_dims,
    ifm_tensor,
    ofm_tensor,
    scale_tensor=None,
):
    ofm_ublock = Block(arch.config.ofm_ublock.width, arch.config.ofm_ublock.height, arch.config.ofm_ublock.depth)
    ifm_tens_shape = numeric_util.full_shape(4, ifm_tensor.shape, 1)
    ofm_tens_shape = numeric_util.full_shape(4, ofm_tensor.shape, 1)

    if (
        arch.config.ofm_ublock.height == 2
        and npu_block_type
        in (NpuBlockType.ConvolutionMxN, NpuBlockType.ConvolutionDepthWise, NpuBlockType.VectorProduct)
        and ofm_tens_shape[1] == 1
        # Optimisation only applies for even width tensors
        and ofm_tens_shape[2] % 2 == 0
        and kernel_dims[0] == 1
    ):
        ofm_ublock.width = 4
        ofm_ublock.height = 1
        ofm_block.height = 1

    num_ublk_x = numeric_util.round_up_divide(ofm_block.width, ofm_ublock.width)
    num_ublk_y = ofm_block.height // ofm_ublock.height
    num_ublk_xy = num_ublk_x * num_ublk_y
    num_ublk_z = ofm_block.depth // ofm_ublock.depth
    num_ofm_blk = 0
    total_cycles = 0
    num_elems_blk = ofm_block.width * ofm_block.height * ofm_block.depth
    use_acc_40bits = is_acc_40bits_used(npu_block_type, ifm_tensor, ofm_tensor)

    sub_kernel_limits = arch.sub_kernel_limits[npu_block_type]
    n_sub_kernels_y = numeric_util.round_up_divide(kernel_dims[0], sub_kernel_limits[0])
    n_sub_kernels_x = numeric_util.round_up_divide(kernel_dims[1], sub_kernel_limits[1])
    sub_kernel_x = [
        min((kernel_dims[1] - i * sub_kernel_limits[1]), sub_kernel_limits[1]) for i in range(n_sub_kernels_x)
    ]
    sub_kernel_y = [
        min((kernel_dims[0] - i * sub_kernel_limits[0]), sub_kernel_limits[0]) for i in range(n_sub_kernels_y)
    ]
    sub_kernel_size = (x * y for y in sub_kernel_y for x in sub_kernel_x)

    cycles_dpu_blk = 0
    cycles_wb = 32 * ofm_ublock.depth // 8

    for num_kernel_elems in sub_kernel_size:
        if npu_block_type == NpuBlockType.Pooling:
            num_kernel_steps = 1
            cycles = max(4, num_kernel_elems) * num_ublk_xy * num_ublk_z
            if ifm_tensor.dtype.size_in_bits() == 16 and arch.accelerator_config != Accelerator.Ethos_U55_32:
                cycles *= 2
        elif npu_block_type == NpuBlockType.ConvolutionDepthWise:
            cycles = 4 * num_ublk_xy
            if ifm_tensor.dtype.size_in_bits() == 16:
                cycles *= 2
            num_kernel_steps = numeric_util.round_up_divide(num_kernel_elems, 4)
            cycles = max(cycles_wb, cycles) * num_kernel_steps * num_ublk_z
        elif (
            (npu_block_type == NpuBlockType.ConvolutionMxN and block_traversal != TensorBlockTraversal.PartKernelFirst)
            or npu_block_type == NpuBlockType.VectorProduct
            or npu_block_type == NpuBlockType.ReduceSum
        ):
            num_kernel_steps = num_kernel_elems
            cycles = max(cycles_wb, 4 * num_ublk_xy) * num_kernel_steps * num_ublk_z
        else:
            assert block_traversal == TensorBlockTraversal.PartKernelFirst
            divider = 2 if ifm_tensor.dtype.size_in_bits() == 16 else 4
            num_kernel_steps = numeric_util.round_up_divide(num_kernel_elems, divider)
            cycles = max(cycles_wb, 4 * num_ublk_xy) * (
                num_kernel_steps * numeric_util.round_up_divide(ifm_block.depth, 8) * num_ublk_z
            )

        delay_cycles = 0
        if arch.accelerator_config is Accelerator.Ethos_U55_32:
            delay = 7 if use_acc_40bits else 3
            if num_ublk_x == 1 and num_ublk_y == 1:
                if num_ublk_z == 1:
                    delay_cycles = delay * num_kernel_steps
                elif num_kernel_steps > 1:
                    delay_cycles = delay * (num_kernel_steps - 1) * num_ublk_z
            if (num_ublk_x == 1 or num_ublk_y == 1) and num_ublk_z > 1 and use_acc_40bits:
                delay_cycles += delay * num_ublk_z
        else:
            delay = (
                3
                if use_acc_40bits and arch.accelerator_config in (Accelerator.Ethos_U55_64, Accelerator.Ethos_U55_128)
                else 2
            )
            if num_ublk_x == 1 and num_ublk_y == 1:
                if num_ublk_z == 1:
                    delay_cycles = delay * num_kernel_steps
                elif num_kernel_steps > 1:
                    delay_cycles = delay * (num_kernel_steps - 1) * num_ublk_z

        if npu_block_type == NpuBlockType.ConvolutionMxN and block_traversal == TensorBlockTraversal.PartKernelFirst:
            delay_cycles *= numeric_util.round_up_divide(ifm_block.depth, 8)

        cycles_dpu_blk += cycles
        cycles_dpu_blk += delay_cycles

    if npu_block_type in (NpuBlockType.ConvolutionMxN, NpuBlockType.VectorProduct, NpuBlockType.ReduceSum):
        cycles_dpu_blk *= numeric_util.round_up_divide(ifm_tens_shape[3], ifm_block.depth)

    cycles_dpu_blk /= arch.ncores

    num_ofm_blk = (
        numeric_util.round_up_divide(ofm_tens_shape[1], ofm_block.height)
        * numeric_util.round_up_divide(ofm_tens_shape[2], ofm_block.width)
        * numeric_util.round_up_divide(ofm_tens_shape[3], ofm_block.depth)
    )

    cycles_output_blk = estimate_output_cycles(
        arch, npu_block_type, primary_op, num_elems_blk, ifm_tensor, ofm_tensor, use_acc_40bits
    )

    if scale_tensor:
        if scale_tensor.mem_area is MemArea.Sram:
            latency = 32
        elif scale_tensor.mem_area is MemArea.Dram:
            latency = 500
        else:
            latency = 64
        cycles_bias_blk = 10 * min(ofm_block.depth, ofm_tens_shape[3]) * latency / 256
        cycles_output_blk = max(cycles_output_blk, cycles_bias_blk)

    cycles_cmd = get_minimal_cmd_cycles(
        arch, ifm_tensor, ofm_tensor, ifm_block, ofm_block, cycles_dpu_blk, cycles_output_blk
    )
    cycles_dpu_blk = max(cycles_dpu_blk, cycles_cmd)
    cycles_output_blk = max(cycles_output_blk, cycles_cmd)

    if cycles_dpu_blk > cycles_output_blk:
        total_cycles = cycles_dpu_blk * num_ofm_blk + cycles_output_blk
    else:
        total_cycles = cycles_output_blk * num_ofm_blk + cycles_dpu_blk

    return total_cycles


def estimate_memory_bandwidth(arch, mem_area, direction, tensor, block_size: Block, replace_bw=None):
    if tensor.format not in (TensorFormat.NHWC, TensorFormat.NHCWB16):
        return tensor.bandwidth() if replace_bw is None else replace_bw

    # Estimate memory transfer efficiency by calculating the burst length
    # this is related to data format, block shape, and tensor shape, etc.
    max_burst_len = 32 if mem_area == MemArea.Sram else 128
    burst_len = 0
    elem_size = tensor.dtype.size_in_bytes()
    is_ifm = direction == BandwidthDirection.Read
    tens = tensor.clone()
    if not tens.avoid_NHCWB16:
        tens.set_format(TensorFormat.NHCWB16, arch)

    if tens.format == TensorFormat.NHCWB16:
        if tens.get_strides()[1] == block_size.depth:
            burst_len = elem_size * block_size.depth * block_size.width
        elif is_ifm:
            burst_len = 16 * elem_size * block_size.width
        else:
            burst_len = 16 * elem_size * block_size.width * arch.ncores
    else:
        assert tens.format == TensorFormat.NHWC
        if is_ifm:
            if tens.get_strides()[3] == block_size.depth:
                burst_len = elem_size * block_size.depth * block_size.width
            else:
                burst_len = elem_size * block_size.depth
        else:
            if block_size.depth <= 16 and tens.get_strides()[3] == block_size.depth:
                burst_len = elem_size * block_size.depth * block_size.width
            else:
                burst_len = min(64, 16 * elem_size * arch.ncores, block_size.depth * elem_size)

    burst_len = min(max_burst_len, burst_len)
    bw = tens.bandwidth() if replace_bw is None else replace_bw

    return bw * (max_burst_len / burst_len)


def performance_metrics_for_pass(arch, ps, block_config=None, rewrite_list=[], force_outputs_to_fast_storage=False):
    if block_config is None:
        block_config = ps.block_config
    bws = make_bandwidth_array()
    macs = make_macs_array()
    cycles = make_cycles_array()
    blocks = 0
    ifm_read_multiple = 1
    weight_read_multiple = 0

    if ps.placement in set((PassPlacement.MemoryOnly, PassPlacement.StartupInit)):
        return bws, macs, cycles, blocks, ifm_read_multiple, weight_read_multiple  # nothing real happening in this pass

    min_block_size = arch.min_block_sizes[ps.npu_block_type]

    skirt = (0, 0, 0, 0)
    explicit_padding = (0, 0, 0, 0)
    primary_op = ps.primary_op
    replacement_read_bws = {}
    ofm_block = Block(block_config[1], block_config[0], block_config[3])
    ifm_block = Block(block_config[1], block_config[0], block_config[3])

    if ps.placement == PassPlacement.Npu and primary_op:
        skirt = primary_op.attrs.get("skirt", skirt)
        explicit_padding = primary_op.attrs.get("explicit_padding", explicit_padding)
        assert primary_op.type.npu_block_type == ps.npu_block_type
        npu_block_type = primary_op.type.npu_block_type

        ifm_tensor, _, weight_tensor, ofm_tensor = ps.get_primary_op_ifm_ifm2_weights_ofm()
        ifm_tensor_shape = numeric_util.full_shape(4, ifm_tensor.shape, 1)

        if npu_block_type == NpuBlockType.ReduceSum:
            block_traversal = TensorBlockTraversal.DepthFirst
        elif npu_block_type in (
            NpuBlockType.ConvolutionMxN,
            NpuBlockType.ConvolutionDepthWise,
            NpuBlockType.VectorProduct,
        ):
            block_traversal = weight_tensor.block_traversal
        else:
            block_traversal = TensorBlockTraversal.Default
        ifm_block_depth = get_ifm_block_depth(
            npu_block_type, ifm_tensor_shape[3], ifm_tensor.dtype.size_in_bits(), block_traversal, ofm_block.depth
        )
        ifm_block = arch.get_ifm_block_size(
            ifm_block_depth, ofm_block, primary_op.kernel, ifm_resampling_mode=ifm_tensor.resampling_mode
        )

        if npu_block_type in set(
            (
                NpuBlockType.ConvolutionMxN,
                NpuBlockType.ConvolutionDepthWise,
                NpuBlockType.Pooling,
                NpuBlockType.ReduceSum,
            )
        ):
            # extent the ifm to full dimension
            ifm_tensor_brick_size = tuple(numeric_util.full_shape(4, list(ifm_tensor.brick_size), 1))
            ifm_tensor_bandwidth_shape = numeric_util.full_shape(4, ifm_tensor.bandwidth_shape, 1)

            batch_size = ifm_tensor_shape[0]
            ifm_depth = ifm_tensor_bandwidth_shape[3]

            # add in padding
            ifm_tensor_shape[1] += explicit_padding[0] + explicit_padding[2]  # height += top and bottom
            ifm_tensor_shape[2] += explicit_padding[1] + explicit_padding[3]  # width  += left and right

            strides = primary_op.attrs["strides"]
            if npu_block_type != NpuBlockType.Pooling:
                if npu_block_type == NpuBlockType.ReduceSum:
                    weight_tensor_shape = [1, 1, ifm_tensor.shape[3], ofm_tensor.shape[3]]
                    weight_tensor_bandwidth_shape = [0] * 4
                    weight_tensor_element_size = 0
                    weight_tensor_bandwidth_compression_scale = 0.0
                else:
                    weight_tensor_shape = weight_tensor.shape
                    weight_tensor_bandwidth_shape = weight_tensor.bandwidth_shape
                    weight_tensor_element_size = weight_tensor.element_size()
                    weight_tensor_bandwidth_compression_scale = weight_tensor.bandwidth_compression_scale
                nn_ops = (
                    int(ofm_tensor.shape[0])
                    * int(ofm_tensor.shape[1])
                    * int(ofm_tensor.shape[2])
                    * int(weight_tensor_shape[0])
                    * int(weight_tensor_shape[1])
                    * int(weight_tensor_shape[2])
                    * int(weight_tensor_shape[3])
                )
            else:
                weight_tensor_shape = [
                    primary_op.attrs["ksize"][1],
                    primary_op.attrs["ksize"][2],
                    1,
                    ifm_tensor_shape[3],
                ]
                weight_tensor_bandwidth_shape = weight_tensor_shape
                weight_tensor_element_size = 0
                weight_tensor_bandwidth_compression_scale = 0.0
                nn_ops = 0  # pooling doesn't count as NN ops

            kernel_dims = weight_tensor_shape[:2]

            sub_kernel_limits = arch.sub_kernel_limits[npu_block_type]
            # count the sub kernels; the IFM block needs to be refetched for each of them
            n_sub_kernels_y = numeric_util.round_up_divide(kernel_dims[0], sub_kernel_limits[0])
            n_sub_kernels_x = numeric_util.round_up_divide(kernel_dims[1], sub_kernel_limits[1])
            n_sub_kernels = n_sub_kernels_y * n_sub_kernels_x

            clamped_skirt = list(skirt)
            clamped_skirt[2] = min(clamped_skirt[2], sub_kernel_limits[0] - 1 - clamped_skirt[0])
            clamped_skirt[3] = min(clamped_skirt[3], sub_kernel_limits[1] - 1 - clamped_skirt[1])
            n_blocks, area, block_setup = get_n_blocks_and_area(
                ifm_tensor_brick_size,
                ifm_tensor_shape[1:3],
                skirt,
                clamped_skirt,
                block_config,
                min_block_size,
                strides,
            )

            blocks = n_blocks * numeric_util.round_up_divide(weight_tensor_shape[3], ofm_block.depth)

            n_weight_stages = numeric_util.round_up_divide(weight_tensor_bandwidth_shape[3], ofm_block.depth)
            if npu_block_type == NpuBlockType.ConvolutionDepthWise or npu_block_type == NpuBlockType.Pooling:
                n_weight_stages = 1  # force to no reread

            ifm_tensor_bw = (
                n_sub_kernels
                * batch_size
                * area
                * ifm_depth
                * n_weight_stages
                * ifm_tensor.element_size()
                * ifm_tensor.bandwidth_compression_scale
            )
            replacement_read_bws[ifm_tensor] = ifm_tensor_bw
            ifm_read_multiple = n_weight_stages

            replacement_read_bws[weight_tensor] = (
                batch_size
                * shape_num_elements(weight_tensor_bandwidth_shape)
                * weight_tensor_element_size
                * weight_tensor_bandwidth_compression_scale
                * n_blocks
            )  # read once per block and batch
            weight_read_multiple = n_blocks

            n_kernel_xy = kernel_dims[0] * kernel_dims[1]
            n_input_channels_at_a_time = block_config[2]

            if npu_block_type == NpuBlockType.Pooling or block_traversal in set(
                (TensorBlockTraversal.PartKernelFirst, TensorBlockTraversal.DepthWise)
            ):
                n_input_channels_at_a_time = numeric_util.round_up_divide(n_input_channels_at_a_time, 4)
                n_kernel_xy = max(
                    n_kernel_xy, 4
                )  # need at least 4, as this is the minimum duty cycle for secondary accumulator writes
                if weight_tensor is not None:
                    n_kernel_xy = numeric_util.round_up(n_kernel_xy, 4)  # weights need to be read in blocks of 4

            num_mac_ops = 0
            for n_blocks_for_size, block_size in block_setup:
                num_mac_ops += (
                    batch_size
                    * n_blocks_for_size
                    * block_size[0]
                    * block_size[1]
                    * numeric_util.round_up(weight_tensor_shape[2], n_input_channels_at_a_time)
                    * numeric_util.round_up(weight_tensor_shape[3], ofm_block.depth)
                    * n_kernel_xy
                )
            macs[MacCount.NeuralNetworkMacs] += nn_ops
            macs[MacCount.HardwareMacs] += num_mac_ops
            cycles[PassCycles.Npu] = estimate_conv_pooling_cycles(
                arch,
                npu_block_type,
                primary_op,
                ifm_block,
                ofm_block,
                block_traversal,
                kernel_dims,
                ifm_tensor,
                ofm_tensor,
                ps.scale_tensor,
            )
        elif npu_block_type == NpuBlockType.VectorProduct:
            nn_macs = (
                ifm_tensor.shape[0]
                * numeric_util.round_up(weight_tensor.shape[-2], block_config[2])
                * numeric_util.round_up(weight_tensor.shape[-1], block_config[3])
            )
            num_mac_ops = nn_macs

            cycles[PassCycles.Npu] = estimate_conv_pooling_cycles(
                arch, npu_block_type, primary_op, ifm_block, ofm_block, block_traversal, [1, 1], ifm_tensor, ofm_tensor,
            )
            macs[MacCount.NeuralNetworkMacs] += nn_macs
            macs[MacCount.HardwareMacs] += num_mac_ops

            blocks = 1 * numeric_util.round_up_divide(weight_tensor.shape[-1], ofm_block.depth)

            non_zero_fraction = 1.0
            if ifm_tensor.values is not None:
                nz_vector = np.amax(ifm_tensor.values != 0, axis=0)  # max across batch axis
                non_zero_fraction = np.average(nz_vector)

            replacement_read_bws[ifm_tensor] = ifm_tensor.bandwidth()
            replacement_read_bws[weight_tensor] = weight_tensor.bandwidth() * non_zero_fraction
            ifm_read_multiple = 1
            weight_read_multiple = non_zero_fraction
        elif npu_block_type == NpuBlockType.ElementWise:
            # Work out how many elements we have and calculate performance.
            cycles[PassCycles.Npu] = estimate_output_cycles(
                arch,
                npu_block_type,
                primary_op,
                ofm_tensor.elements(),
                ps.ifm_tensor,
                ps.ofm_tensor,
                None,
                ps.ifm2_tensor,
                ofm_block,
            )

        prev_npu_pass = next((npu_ps for npu_ps in ps.dag_predecessors if npu_ps.placement is PassPlacement.Npu), None)
        if prev_npu_pass is None:
            # cycles for DMA ops in first pass
            dma_ops = (op for op in ps.ops if op.type == Op.DMA)
            for dma_op in dma_ops:
                mem_area = dma_op.attrs["source"]
                for tens in dma_op.inputs:
                    cycles[PassCycles.Npu] += tens.storage_size() / arch.memory_bandwidths_per_cycle[mem_area]

    # apply the desired rewrites
    for rewrite_op, tens, _, _, _, ps_to_rewrite in rewrite_list:
        if ps != ps_to_rewrite:
            continue
        if rewrite_op == SchedulerRewrite.Nop:
            pass  # these are fine, no bandwidth changes
        elif rewrite_op in (SchedulerRewrite.ChangeTensorSubPurpose,):
            if tens.purpose == TensorPurpose.FeatureMap:
                bw = estimate_memory_bandwidth(
                    arch,
                    arch.fast_storage_mem_area,
                    BandwidthDirection.Read,
                    tens,
                    ifm_block,
                    replacement_read_bws[tens],
                )
            else:
                bw = replacement_read_bws[tens]
            bws[arch.fast_storage_mem_area][tens.purpose][BandwidthDirection.Read] += bw
            replacement_read_bws[tens] = 0

    for tens in ps.outputs:
        if force_outputs_to_fast_storage:
            bws[arch.fast_storage_mem_area][tens.purpose][BandwidthDirection.Write] += estimate_memory_bandwidth(
                arch, arch.fast_storage_mem_area, BandwidthDirection.Write, tens, ofm_block
            )
        else:
            bws[tens.mem_area][tens.purpose][BandwidthDirection.Write] += estimate_memory_bandwidth(
                arch, tens.mem_area, BandwidthDirection.Write, tens, ofm_block
            )

    for tens in ps.intermediates:
        bws[tens.mem_area][tens.purpose][BandwidthDirection.Write] += tens.bandwidth()

        if tens in replacement_read_bws:
            bw = replacement_read_bws[tens]
        else:
            bw = tens.bandwidth()

        bws[tens.mem_area][tens.purpose][BandwidthDirection.Read] += bw

    for tens in ps.inputs:
        bws[tens.mem_area][tens.purpose][BandwidthDirection.Read] += estimate_memory_bandwidth(
            arch, tens.mem_area, BandwidthDirection.Read, tens, ifm_block, replacement_read_bws.get(tens)
        )

    # quick build access counts for only current pass, even though these aren't the final numbers
    update_summary_cycles(arch, bws, cycles)

    return bws, macs, cycles, blocks, ifm_read_multiple, weight_read_multiple


def update_summary_cycles(arch, bws, cycles):
    cycles[PassCycles.SramAccess] = np.sum(bws[MemArea.Sram]) / arch.memory_bandwidths_per_cycle[MemArea.Sram]
    cycles[PassCycles.DramAccess] = np.sum(bws[MemArea.Dram]) / arch.memory_bandwidths_per_cycle[MemArea.Dram]
    cycles[PassCycles.OnChipFlashAccess] = (
        np.sum(bws[MemArea.OnChipFlash]) / arch.memory_bandwidths_per_cycle[MemArea.OnChipFlash]
    )
    cycles[PassCycles.OffChipFlashAccess] = (
        np.sum(bws[MemArea.OffChipFlash]) / arch.memory_bandwidths_per_cycle[MemArea.OffChipFlash]
    )

    cycles[PassCycles.Total] = np.max(cycles[: PassCycles.Total])
    return cycles


def collate_stats_for_cascaded_pass(arch, bws, macs, cycles):
    return bws, macs, cycles


def performance_for_cascaded_pass(arch, cps):
    total_bws = make_bandwidth_array()
    total_macs = make_macs_array()
    total_cycles = make_cycles_array()

    for ps in cps.passes:
        bws, macs, cycles, blocks, _, _ = performance_metrics_for_pass(arch, ps)
        ps.bandwidths = bws
        ps.macs = macs
        ps.cycles = cycles
        ps.n_blocks = blocks
        total_bws += bws
        total_macs += macs
        total_cycles += cycles

    bws, macs, cycles = collate_stats_for_cascaded_pass(arch, total_bws, total_macs, total_cycles)
    cps.bandwidths = bws
    cps.macs = macs
    cps.cycles = cycles
    return bws, macs, cycles


def calc_performance_for_network(nng, arch):
    total_bws = make_bandwidth_array()
    total_macs = np.zeros(MacCount.Size)
    total_cycles = np.zeros(PassCycles.Size)

    for sg in nng.subgraphs:
        for cps in sg.cascaded_passes:
            bws, macs, cycles = performance_for_cascaded_pass(arch, cps)
            total_bws += bws
            total_macs += macs
            total_cycles += cycles

    nng.bandwidths = total_bws
    nng.macs = total_macs
    nng.cycles = total_cycles

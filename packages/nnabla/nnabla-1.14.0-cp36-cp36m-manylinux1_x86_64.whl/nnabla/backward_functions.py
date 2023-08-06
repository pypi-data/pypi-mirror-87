# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Backward function
from .backward_function.affine import AffineBackward
from .backward_function.rnn import RNNBackward
from .backward_function.lstm import LSTMBackward
from .backward_function.gru import GRUBackward
from .backward_function.convolution import ConvolutionBackward
from .backward_function.fused_convolution import FusedConvolutionBackward
from .backward_function.depthwise_convolution import DepthwiseConvolutionBackward
from .backward_function.deconvolution import DeconvolutionBackward
from .backward_function.depthwise_deconvolution import DepthwiseDeconvolutionBackward
from .backward_function.adaptive_separable_convolution import AdaptiveSeparableConvolutionBackward
from .backward_function.max_pooling import MaxPoolingBackward
from .backward_function.average_pooling import AveragePoolingBackward
from .backward_function.global_average_pooling import GlobalAveragePoolingBackward
from .backward_function.sum_pooling import SumPoolingBackward
from .backward_function.unpooling import UnpoolingBackward
from .backward_function.embed import EmbedBackward
from .backward_function.sigmoid import SigmoidBackward
from .backward_function.swish import SwishBackward
from .backward_function.tanh import TanhBackward
from .backward_function.relu import ReLUBackward
from .backward_function.leaky_relu import LeakyReLUBackward
from .backward_function.softmax import SoftmaxBackward
from .backward_function.log_softmax import LogSoftmaxBackward
from .backward_function.elu import ELUBackward
from .backward_function.selu import SELUBackward
from .backward_function.crelu import CReLUBackward
from .backward_function.celu import CELUBackward
from .backward_function.prelu import PReLUBackward
from .backward_function.gelu import GELUBackward
from .backward_function.mish import MishBackward
from .backward_function.relu6 import ReLU6Backward
from .backward_function.hard_sigmoid import HardSigmoidBackward
from .backward_function.hard_tanh import HardTanhBackward
from .backward_function.log_sigmoid import LogSigmoidBackward
from .backward_function.softplus import SoftPlusBackward
from .backward_function.softsign import SoftSignBackward
from .backward_function.tanh_shrink import TanhShrinkBackward
from .backward_function.sinc import SincBackward
from .backward_function.fused_batch_normalization import FusedBatchNormalizationBackward
from .backward_function.batch_normalization import BatchNormalizationBackward
from .backward_function.norm_normalization import NormNormalizationBackward
from .backward_function.sync_batch_normalization import SyncBatchNormalizationBackward
from .backward_function.weight_normalization import WeightNormalizationBackward
from .backward_function.mean_subtraction import MeanSubtractionBackward
from .backward_function.clip_grad_by_value import ClipGradByValueBackward
from .backward_function.clip_grad_by_norm import ClipGradByNormBackward
from .backward_function.sum import SumBackward
from .backward_function.mean import MeanBackward
from .backward_function.max import MaxBackward
from .backward_function.min import MinBackward
from .backward_function.norm import NormBackward
from .backward_function.prod import ProdBackward
from .backward_function.reduce_sum import ReduceSumBackward
from .backward_function.reduce_mean import ReduceMeanBackward
from .backward_function.add2 import Add2Backward
from .backward_function.add_n import AddNBackward
from .backward_function.bc_add2 import BcAdd2Backward
from .backward_function.sub2 import Sub2Backward
from .backward_function.mul2 import Mul2Backward
from .backward_function.mul_n import MulNBackward
from .backward_function.div2 import Div2Backward
from .backward_function.pow2 import Pow2Backward
from .backward_function.add_scalar import AddScalarBackward
from .backward_function.mul_scalar import MulScalarBackward
from .backward_function.pow_scalar import PowScalarBackward
from .backward_function.r_sub_scalar import RSubScalarBackward
from .backward_function.r_div_scalar import RDivScalarBackward
from .backward_function.r_pow_scalar import RPowScalarBackward
from .backward_function.sign import SignBackward
from .backward_function.minimum2 import Minimum2Backward
from .backward_function.maximum2 import Maximum2Backward
from .backward_function.minimum_scalar import MinimumScalarBackward
from .backward_function.maximum_scalar import MaximumScalarBackward
from .backward_function.logical_and import LogicalAndBackward
from .backward_function.logical_or import LogicalOrBackward
from .backward_function.logical_xor import LogicalXorBackward
from .backward_function.equal import EqualBackward
from .backward_function.not_equal import NotEqualBackward
from .backward_function.greater_equal import GreaterEqualBackward
from .backward_function.greater import GreaterBackward
from .backward_function.less_equal import LessEqualBackward
from .backward_function.less import LessBackward
from .backward_function.logical_and_scalar import LogicalAndScalarBackward
from .backward_function.logical_or_scalar import LogicalOrScalarBackward
from .backward_function.logical_xor_scalar import LogicalXorScalarBackward
from .backward_function.equal_scalar import EqualScalarBackward
from .backward_function.not_equal_scalar import NotEqualScalarBackward
from .backward_function.greater_equal_scalar import GreaterEqualScalarBackward
from .backward_function.greater_scalar import GreaterScalarBackward
from .backward_function.less_equal_scalar import LessEqualScalarBackward
from .backward_function.less_scalar import LessScalarBackward
from .backward_function.logical_not import LogicalNotBackward
from .backward_function.isnan import IsNaNBackward
from .backward_function.isinf import IsInfBackward
from .backward_function.reset_nan import ResetNaNBackward
from .backward_function.reset_inf import ResetInfBackward
from .backward_function.where import WhereBackward
from .backward_function.constant import ConstantBackward
from .backward_function.arange import ArangeBackward
from .backward_function.abs import AbsBackward
from .backward_function.exp import ExpBackward
from .backward_function.log import LogBackward
from .backward_function.identity import IdentityBackward
from .backward_function.batch_matmul import BatchMatmulBackward
from .backward_function.round import RoundBackward
from .backward_function.ceil import CeilBackward
from .backward_function.floor import FloorBackward
from .backward_function.sin import SinBackward
from .backward_function.cos import CosBackward
from .backward_function.tan import TanBackward
from .backward_function.sinh import SinhBackward
from .backward_function.cosh import CoshBackward
from .backward_function.asin import ASinBackward
from .backward_function.acos import ACosBackward
from .backward_function.atan import ATanBackward
from .backward_function.atan2 import ATan2Backward
from .backward_function.asinh import ASinhBackward
from .backward_function.acosh import ACoshBackward
from .backward_function.atanh import ATanhBackward
from .backward_function.concatenate import ConcatenateBackward
from .backward_function.split import SplitBackward
from .backward_function.stack import StackBackward
from .backward_function.slice import SliceBackward
from .backward_function.pad import PadBackward
from .backward_function.transpose import TransposeBackward
from .backward_function.broadcast import BroadcastBackward
from .backward_function.broadcast_to import BroadcastToBackward
from .backward_function.tile import TileBackward
from .backward_function.one_hot import OneHotBackward
from .backward_function.flip import FlipBackward
from .backward_function.shift import ShiftBackward
from .backward_function.sort import SortBackward
from .backward_function.reshape import ReshapeBackward
from .backward_function.matrix_diag import MatrixDiagBackward
from .backward_function.matrix_diag_part import MatrixDiagPartBackward
from .backward_function.batch_inv import BatchInvBackward
from .backward_function.batch_det import BatchDetBackward
from .backward_function.assign import AssignBackward
from .backward_function.gather import GatherBackward
from .backward_function.gather_nd import GatherNdBackward
from .backward_function.scatter_nd import ScatterNdBackward
from .backward_function.scatter_add import ScatterAddBackward
from .backward_function.pack_padded_sequence import PackPaddedSequenceBackward
from .backward_function.pad_packed_sequence import PadPackedSequenceBackward
from .backward_function.interpolate import InterpolateBackward
from .backward_function.fft import FFTBackward
from .backward_function.ifft import IFFTBackward
from .backward_function.dropout import DropoutBackward
from .backward_function.top_k_data import TopKDataBackward
from .backward_function.top_k_grad import TopKGradBackward
from .backward_function.rand import RandBackward
from .backward_function.randint import RandintBackward
from .backward_function.randn import RandnBackward
from .backward_function.rand_binomial import RandBinomialBackward
from .backward_function.rand_beta import RandBetaBackward
from .backward_function.rand_gamma import RandGammaBackward
from .backward_function.random_choice import RandomChoiceBackward
from .backward_function.random_crop import RandomCropBackward
from .backward_function.random_flip import RandomFlipBackward
from .backward_function.random_shift import RandomShiftBackward
from .backward_function.random_erase import RandomEraseBackward
from .backward_function.image_augmentation import ImageAugmentationBackward
from .backward_function.sigmoid_cross_entropy import SigmoidCrossEntropyBackward
from .backward_function.binary_cross_entropy import BinaryCrossEntropyBackward
from .backward_function.softmax_cross_entropy import SoftmaxCrossEntropyBackward
from .backward_function.categorical_cross_entropy import CategoricalCrossEntropyBackward
from .backward_function.squared_error import SquaredErrorBackward
from .backward_function.absolute_error import AbsoluteErrorBackward
from .backward_function.huber_loss import HuberLossBackward
from .backward_function.epsilon_insensitive_loss import EpsilonInsensitiveLossBackward
from .backward_function.kl_multinomial import KLMultinomialBackward
from .backward_function.affine_grid import AffineGridBackward
from .backward_function.warp_by_grid import WarpByGridBackward
from .backward_function.warp_by_flow import WarpByFlowBackward
from .backward_function.binary_sigmoid import BinarySigmoidBackward
from .backward_function.binary_tanh import BinaryTanhBackward
from .backward_function.binary_connect_affine import BinaryConnectAffineBackward
from .backward_function.binary_connect_convolution import BinaryConnectConvolutionBackward
from .backward_function.binary_weight_affine import BinaryWeightAffineBackward
from .backward_function.binary_weight_convolution import BinaryWeightConvolutionBackward
from .backward_function.inq_affine import INQAffineBackward
from .backward_function.inq_convolution import INQConvolutionBackward
from .backward_function.fixed_point_quantize import FixedPointQuantizeBackward
from .backward_function.min_max_quantize import MinMaxQuantizeBackward
from .backward_function.pow2_quantize import Pow2QuantizeBackward
from .backward_function.prune import PruneBackward
from .backward_function.quantize_linear import QuantizeLinearBackward
from .backward_function.dequantize_linear import DequantizeLinearBackward
from .backward_function.top_n_error import TopNErrorBackward
from .backward_function.binary_error import BinaryErrorBackward
from .backward_function.confusion_matrix import ConfusionMatrixBackward
from .backward_function.vat_noise import VATNoiseBackward
from .backward_function.unlink import UnlinkBackward
from .backward_function.sink import SinkBackward
from .backward_function.nms_detection2d import NmsDetection2dBackward
from .backward_function.max_pooling_backward import MaxPoolingBackwardBackward
from .backward_function.patch_correlation import PatchCorrelationBackward

# Mapping
mappings = {
    "Affine": AffineBackward,
    "RNN": RNNBackward,
    "LSTM": LSTMBackward,
    "GRU": GRUBackward,
    "Convolution": ConvolutionBackward,
    "FusedConvolution": FusedConvolutionBackward,
    "DepthwiseConvolution": DepthwiseConvolutionBackward,
    "Deconvolution": DeconvolutionBackward,
    "DepthwiseDeconvolution": DepthwiseDeconvolutionBackward,
    "AdaptiveSeparableConvolution": AdaptiveSeparableConvolutionBackward,
    "MaxPooling": MaxPoolingBackward,
    "AveragePooling": AveragePoolingBackward,
    "GlobalAveragePooling": GlobalAveragePoolingBackward,
    "SumPooling": SumPoolingBackward,
    "Unpooling": UnpoolingBackward,
    "Embed": EmbedBackward,
    "Sigmoid": SigmoidBackward,
    "Swish": SwishBackward,
    "Tanh": TanhBackward,
    "ReLU": ReLUBackward,
    "LeakyReLU": LeakyReLUBackward,
    "Softmax": SoftmaxBackward,
    "LogSoftmax": LogSoftmaxBackward,
    "ELU": ELUBackward,
    "SELU": SELUBackward,
    "CReLU": CReLUBackward,
    "CELU": CELUBackward,
    "PReLU": PReLUBackward,
    "GELU": GELUBackward,
    "Mish": MishBackward,
    "ReLU6": ReLU6Backward,
    "HardSigmoid": HardSigmoidBackward,
    "HardTanh": HardTanhBackward,
    "LogSigmoid": LogSigmoidBackward,
    "SoftPlus": SoftPlusBackward,
    "SoftSign": SoftSignBackward,
    "TanhShrink": TanhShrinkBackward,
    "Sinc": SincBackward,
    "FusedBatchNormalization": FusedBatchNormalizationBackward,
    "BatchNormalization": BatchNormalizationBackward,
    "NormNormalization": NormNormalizationBackward,
    "SyncBatchNormalization": SyncBatchNormalizationBackward,
    "WeightNormalization": WeightNormalizationBackward,
    "MeanSubtraction": MeanSubtractionBackward,
    "ClipGradByValue": ClipGradByValueBackward,
    "ClipGradByNorm": ClipGradByNormBackward,
    "Sum": SumBackward,
    "Mean": MeanBackward,
    "Max": MaxBackward,
    "Min": MinBackward,
    "Norm": NormBackward,
    "Prod": ProdBackward,
    "ReduceSum": ReduceSumBackward,
    "ReduceMean": ReduceMeanBackward,
    "Add2": Add2Backward,
    "AddN": AddNBackward,
    "BcAdd2": BcAdd2Backward,
    "Sub2": Sub2Backward,
    "Mul2": Mul2Backward,
    "MulN": MulNBackward,
    "Div2": Div2Backward,
    "Pow2": Pow2Backward,
    "AddScalar": AddScalarBackward,
    "MulScalar": MulScalarBackward,
    "PowScalar": PowScalarBackward,
    "RSubScalar": RSubScalarBackward,
    "RDivScalar": RDivScalarBackward,
    "RPowScalar": RPowScalarBackward,
    "Sign": SignBackward,
    "Minimum2": Minimum2Backward,
    "Maximum2": Maximum2Backward,
    "MinimumScalar": MinimumScalarBackward,
    "MaximumScalar": MaximumScalarBackward,
    "LogicalAnd": LogicalAndBackward,
    "LogicalOr": LogicalOrBackward,
    "LogicalXor": LogicalXorBackward,
    "Equal": EqualBackward,
    "NotEqual": NotEqualBackward,
    "GreaterEqual": GreaterEqualBackward,
    "Greater": GreaterBackward,
    "LessEqual": LessEqualBackward,
    "Less": LessBackward,
    "LogicalAndScalar": LogicalAndScalarBackward,
    "LogicalOrScalar": LogicalOrScalarBackward,
    "LogicalXorScalar": LogicalXorScalarBackward,
    "EqualScalar": EqualScalarBackward,
    "NotEqualScalar": NotEqualScalarBackward,
    "GreaterEqualScalar": GreaterEqualScalarBackward,
    "GreaterScalar": GreaterScalarBackward,
    "LessEqualScalar": LessEqualScalarBackward,
    "LessScalar": LessScalarBackward,
    "LogicalNot": LogicalNotBackward,
    "IsNaN": IsNaNBackward,
    "IsInf": IsInfBackward,
    "ResetNaN": ResetNaNBackward,
    "ResetInf": ResetInfBackward,
    "Where": WhereBackward,
    "Constant": ConstantBackward,
    "Arange": ArangeBackward,
    "Abs": AbsBackward,
    "Exp": ExpBackward,
    "Log": LogBackward,
    "Identity": IdentityBackward,
    "BatchMatmul": BatchMatmulBackward,
    "Round": RoundBackward,
    "Ceil": CeilBackward,
    "Floor": FloorBackward,
    "Sin": SinBackward,
    "Cos": CosBackward,
    "Tan": TanBackward,
    "Sinh": SinhBackward,
    "Cosh": CoshBackward,
    "ASin": ASinBackward,
    "ACos": ACosBackward,
    "ATan": ATanBackward,
    "ATan2": ATan2Backward,
    "ASinh": ASinhBackward,
    "ACosh": ACoshBackward,
    "ATanh": ATanhBackward,
    "Concatenate": ConcatenateBackward,
    "Split": SplitBackward,
    "Stack": StackBackward,
    "Slice": SliceBackward,
    "Pad": PadBackward,
    "Transpose": TransposeBackward,
    "Broadcast": BroadcastBackward,
    "BroadcastTo": BroadcastToBackward,
    "Tile": TileBackward,
    "OneHot": OneHotBackward,
    "Flip": FlipBackward,
    "Shift": ShiftBackward,
    "Sort": SortBackward,
    "Reshape": ReshapeBackward,
    "MatrixDiag": MatrixDiagBackward,
    "MatrixDiagPart": MatrixDiagPartBackward,
    "BatchInv": BatchInvBackward,
    "BatchDet": BatchDetBackward,
    "Assign": AssignBackward,
    "Gather": GatherBackward,
    "GatherNd": GatherNdBackward,
    "ScatterNd": ScatterNdBackward,
    "ScatterAdd": ScatterAddBackward,
    "PackPaddedSequence": PackPaddedSequenceBackward,
    "PadPackedSequence": PadPackedSequenceBackward,
    "Interpolate": InterpolateBackward,
    "FFT": FFTBackward,
    "IFFT": IFFTBackward,
    "Dropout": DropoutBackward,
    "TopKData": TopKDataBackward,
    "TopKGrad": TopKGradBackward,
    "Rand": RandBackward,
    "Randint": RandintBackward,
    "Randn": RandnBackward,
    "RandBinomial": RandBinomialBackward,
    "RandBeta": RandBetaBackward,
    "RandGamma": RandGammaBackward,
    "RandomChoice": RandomChoiceBackward,
    "RandomCrop": RandomCropBackward,
    "RandomFlip": RandomFlipBackward,
    "RandomShift": RandomShiftBackward,
    "RandomErase": RandomEraseBackward,
    "ImageAugmentation": ImageAugmentationBackward,
    "SigmoidCrossEntropy": SigmoidCrossEntropyBackward,
    "BinaryCrossEntropy": BinaryCrossEntropyBackward,
    "SoftmaxCrossEntropy": SoftmaxCrossEntropyBackward,
    "CategoricalCrossEntropy": CategoricalCrossEntropyBackward,
    "SquaredError": SquaredErrorBackward,
    "AbsoluteError": AbsoluteErrorBackward,
    "HuberLoss": HuberLossBackward,
    "EpsilonInsensitiveLoss": EpsilonInsensitiveLossBackward,
    "KLMultinomial": KLMultinomialBackward,
    "AffineGrid": AffineGridBackward,
    "WarpByGrid": WarpByGridBackward,
    "WarpByFlow": WarpByFlowBackward,
    "BinarySigmoid": BinarySigmoidBackward,
    "BinaryTanh": BinaryTanhBackward,
    "BinaryConnectAffine": BinaryConnectAffineBackward,
    "BinaryConnectConvolution": BinaryConnectConvolutionBackward,
    "BinaryWeightAffine": BinaryWeightAffineBackward,
    "BinaryWeightConvolution": BinaryWeightConvolutionBackward,
    "INQAffine": INQAffineBackward,
    "INQConvolution": INQConvolutionBackward,
    "FixedPointQuantize": FixedPointQuantizeBackward,
    "MinMaxQuantize": MinMaxQuantizeBackward,
    "Pow2Quantize": Pow2QuantizeBackward,
    "Prune": PruneBackward,
    "QuantizeLinear": QuantizeLinearBackward,
    "DequantizeLinear": DequantizeLinearBackward,
    "TopNError": TopNErrorBackward,
    "BinaryError": BinaryErrorBackward,
    "ConfusionMatrix": ConfusionMatrixBackward,
    "VATNoise": VATNoiseBackward,
    "Unlink": UnlinkBackward,
    "Sink": SinkBackward,
    "NmsDetection2d": NmsDetection2dBackward,
    "MaxPoolingBackward": MaxPoolingBackwardBackward,
    "PatchCorrelation": PatchCorrelationBackward,
}


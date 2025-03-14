# Copyright The Lightning AI team.
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
"""General utilities."""

import numpy

from lightning_fabric.utilities import (
    LightningEnum,
    disable_possible_user_warnings,
    is_shared_filesystem,
    measure_flops,
    move_data_to_device,
    suggested_max_num_workers,
)
from pytorch_lightning.utilities.combined_loader import CombinedLoader
from pytorch_lightning.utilities.enums import GradClipAlgorithmType
from pytorch_lightning.utilities.grads import grad_norm
from pytorch_lightning.utilities.parameter_tying import find_shared_parameters, set_shared_parameters
from pytorch_lightning.utilities.parsing import AttributeDict, is_picklable
from pytorch_lightning.utilities.rank_zero import (
    rank_zero_deprecation,
    rank_zero_info,
    rank_zero_only,
    rank_zero_warn,
)

__all__ = [
    "AttributeDict",
    "CombinedLoader",
    "disable_possible_user_warnings",
    "find_shared_parameters",
    "grad_norm",
    "GradClipAlgorithmType",
    "is_picklable",
    "is_shared_filesystem",
    "LightningEnum",
    "measure_flops",
    "move_data_to_device",
    "rank_zero_deprecation",
    "rank_zero_info",
    "rank_zero_only",
    "rank_zero_warn",
    "set_shared_parameters",
    "suggested_max_num_workers",
]

FLOAT16_EPSILON = numpy.finfo(numpy.float16).eps
FLOAT32_EPSILON = numpy.finfo(numpy.float32).eps
FLOAT64_EPSILON = numpy.finfo(numpy.float64).eps

# Copyright 2017 The Abseil Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Internal helper for running tests on Windows Bazel."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import flags

try:
  from absl.testing import _bazel_selected_py3
except ImportError:
  _bazel_selected_py3 = None

FLAGS = flags.FLAGS


def get_executable_path(py_binary_name, add_version_suffix=True):
  """Returns the executable path of a py_binary.

  This returns the executable path of a py_binary that is in another Bazel
  target's data dependencies.

  On Linux/macOS, the path and __file__ has the same root directory.
  On Windows, bazel builds an .exe file and we need to use the MANIFEST file
  the location the actual binary.

  Args:
    py_binary_name: string, the name of a py_binary that is in another Bazel
        target's data dependencies.
    add_version_suffix: bool, whether to add a Python version specific suffix
        to `py_binary_name` when locating the file.

  Raises:
    RuntimeError: Raised when it cannot locate the executable path.
  """
  if add_version_suffix:
    root, ext = os.path.splitext(py_binary_name)
    suffix = 'py3' if _bazel_selected_py3 else 'py2'
    py_binary_name = '{}_{}{}'.format(root, suffix, ext)

  if os.name == 'nt':
    py_binary_name += '.exe'
    manifest_file = os.path.join(FLAGS.test_srcdir, 'MANIFEST')
    workspace_name = os.environ['TEST_WORKSPACE']
    manifest_entry = '{}/{}'.format(workspace_name, py_binary_name)
    with open(manifest_file, 'r') as manifest_fd:
      for line in manifest_fd:
        tokens = line.strip().split(' ')
        if len(tokens) != 2:
          continue
        if manifest_entry == tokens[0]:
          return tokens[1]
    raise RuntimeError(
        'Cannot locate executable path for {}, MANIFEST file: {}.'.format(
            py_binary_name, manifest_file))
  else:
    # NOTE: __file__ may be .py or .pyc, depending on how the module was
    # loaded and executed.
    path = __file__

    # Use the package name to find the root directory: every dot is
    # a directory, plus one for ourselves.
    for _ in range(__name__.count('.') + 1):
      path = os.path.dirname(path)

    root_directory = path
    return os.path.join(root_directory, py_binary_name)

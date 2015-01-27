# Copyright 2014 0xc0170
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

"""
Settings needed:
UV4
IARBUILD
PROJECT_ROOT
GCC_BIN_PATH
"""

import os.environ as ENV
from os.path import join, pardir

UV4 = ENV['UV4'] or join('C:', 'Keil', 'UV4', 'UV4.exe')
IARBUILD = ENV['IARBUILD'] or join(
    'C:', 'Program Files (x86)', 
    'IAR Systems', 'Embedded Workbench 7.0', 
    'common', 'bin', 'IarBuild.exe')
GCC_BIN_PATH = ENV['ARM_GCC_PATH'] or ''

PROJECT_ROOT = ENV['PROJECT_GENERATOR_ROOT'] or join(pardir, pardir)
DEFAULT_TOOL = ENV['PROJECT_GENERATOR_DEFAULT_TOOL'] or 'uvision'

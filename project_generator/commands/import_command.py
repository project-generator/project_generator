# Copyright 2015 0xc0170
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

import os
import logging

help = 'Import mcu to pgen. Provide a valid project file, pgen will parse to create mcu definition'

from ..tools_supported import ToolsSupported
from ..targets import mcu_create

def run(args):
    root = os.getcwd()

    tool = ToolsSupported().get_tool(args.tool)
    if tool is None:
        return -1
    return mcu_create(tool, args.mcu, args.file, args.tool)

def setup(subparser):
    subparser.add_argument(
        '-mcu', action='store', required = True, help='MCU name')
    # we need tool as some tools have same extensions and we might have problems
    subparser.add_argument(
        '-t', '--tool', action='store', required = True, help='Tool to be set')
    subparser.add_argument(
        '-f', '--file', action='store', required = True, help='Project file to be parsed (a valid tool project)')

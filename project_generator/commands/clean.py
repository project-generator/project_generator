# Copyright 2014-2015 0xc0170
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

from ..tools_supported import ToolsSupported
from ..generate import Generator
from . import argparse_filestring_type, argparse_string_type

help = 'Clean generated projects'


def run(args):
    generator = Generator(args.file)
    for project in generator.generate(args.project):
        project.clean(args.tool)
    return 0

def setup(subparser):
    subparser.add_argument("-f", "--file", help="YAML projects file", default='projects.yaml', type=argparse_filestring_type)
    subparser.add_argument("-p", "--project", required = True, help="Specify which project to be removed")
    subparser.add_argument(
        "-t", "--tool", help="Clean project files for this tool",
        type=argparse_string_type(str.lower, False), choices=list(ToolsSupported.TOOLS_DICT.keys()) + list(ToolsSupported.TOOLS_ALIAS.keys()))

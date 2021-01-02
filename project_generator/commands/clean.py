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
    combined_projects = args.projects + args.project or ['']
    generator = Generator(args.file)
    for project_name in (combined_projects):
        for project in generator.generate(project_name):
            project.clean(args.tool)
    return 0

def setup(subparser):
    subparser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help='Increase the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument('-q', dest='quietness', action='count', default=0,
                        help='Decrease the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument("-f", "--file", help="YAML projects file", default='projects.yaml', type=argparse_filestring_type)
    subparser.add_argument("-p", "--project", dest="projects", action='append', default=[],
                        help="Specify which project to be removed")
    subparser.add_argument(
        "-t", "--tool", help="Clean project files for this tool", required=True,
        type=argparse_string_type(str.lower, False), choices=list(ToolsSupported.TOOLS_DICT.keys()) + list(ToolsSupported.TOOLS_ALIAS.keys()))
    subparser.add_argument("project", nargs='*',
                        help="Specify projects to be removed")

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
from project_generator_definitions.definitions import ProGenTargets

from ..tools_supported import ToolsSupported
from ..generate import Generator
from ..settings import ProjectSettings
from . import argparse_filestring_type

help = 'List general progen data as projects, tools or targets'


def run(args):
    if not args.all:
        generator = Generator(args.file)
        for project in generator.generate():
            if args.section == 'targets':
                try:
                    print("%s supports: %s" % (project.name, project.project['target']))
                except KeyError:
                    print("%s supports: (no targets specified)" % project.name)
            elif args.section == 'projects':
                print (project.name)
            elif args.section == 'tools':
                tools = [tool for tool, value in project.project['tool_specific'].items() if value.get('linker_file')]
                print("%s supports: %s" % (project.name, ", ".join(tools)))
    else:
        if args.section == 'targets':
            print("Progen supports the following targets:\n")
            print("\n".join(sorted(ProGenTargets().get_targets())))
        elif args.section == 'tools':
            print("Progen supports the following tools:\n")
            print("\n".join(sorted(ToolsSupported().get_supported())))
        elif args.section == 'projects':
            print("--all does not apply to projects.")
    return 0


def setup(subparser):
    subparser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help='Increase the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument('-q', dest='quietness', action='count', default=0,
                        help='Decrease the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument("section", choices = ['targets','tools','projects'], nargs="?",
                           help="What section you would like listed", default='projects')
    subparser.add_argument("-f", "--file", help="YAML projects file", default='projects.yaml', type=argparse_filestring_type)
    subparser.add_argument("-a", "--all", help="List all available options.", action="store_true")

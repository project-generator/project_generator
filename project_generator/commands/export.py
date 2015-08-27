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

from ..generate import Generator

help = 'Export a project record'


def run(args):
    if os.path.exists(args.file):
        generator = Generator(args.file)
        build_result = 0
        if args.defdirectory:
            generator.settings.update_definitions_dir(os.path.join(os.getcwd(), args.defdirectory))
        for project in generator.generate(args.project):
            export_result = project.export(args.tool, args.copy)
            if args.build:
                build_result = project.build(args.tool)
        if build_result == 0 and export_result == 0:
            return 0
        else:
            return -1
    else:
        # not project known by pgen
        logging.warning("%s not found." % args.file)
        return -1

def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml')
    subparser.add_argument(
        "-p", "--project", help="Project to be generated", default = '')
    subparser.add_argument(
        "-t", "--tool", help="Create project files for provided tool")
    subparser.add_argument(
        "-b", "--build", action="store_true", help="Build defined projects")
    subparser.add_argument(
        "-defdir", "--defdirectory",
        help="Path to the definitions, otherwise default (~/.pg/definitions) is used")
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")

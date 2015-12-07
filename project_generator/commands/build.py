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

from ..tools_supported import ToolsSupported
from ..generate import Generator
from ..settings import ProjectSettings

help = 'Build a project'


def run(args):
    # Export if we know how, otherwise return
    if os.path.exists(args.file):
        generator = Generator(args.file)
        build_failed = False
        export_failed = False
        for project in generator.generate(args.project):
            if project.generate(args.tool, args.copy) == -1:
                export_failed = True
            if project.build(args.tool) == -1:
                build_failed = True

        if build_failed or export_failed:
            return -1
        else:
            return 0
    else:
        # not project known by progen
        logging.warning("%s not found." % args.file)
        return -1

def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml')
    subparser.add_argument(
        "-p", "--project", help="Name of the project to build", default = '')
    subparser.add_argument(
        "-t", "--tool", help="Build a project files for provided tool")
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")

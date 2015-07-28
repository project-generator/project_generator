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

from ..tools import ToolsSupported
from ..workspace import PgenWorkspace
from ..settings import ProjectSettings

help = 'Build a project'


def run(args):
    # Export if we know how, otherwise return
    if os.path.exists(args.file):
        # known project from records
        workspace = PgenWorkspace(args.file, os.getcwd())
        if args.project:
            export_result = workspace.export(args.project, args.tool, args.copy)
            build_result = workspace.build(args.project, args.tool)
        else:
            export_result = workspace.export_all(args.tool, args.copy)
            build_result = workspace.build_all(args.tool)

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
    subparser.add_argument("-p", "--project", help="Name of the project to build")
    subparser.add_argument(
        "-t", "--tool", help="Build a project files for provided tool")
    subparser.add_argument(
        "-dir", "--directory", help="The projects directory")
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")

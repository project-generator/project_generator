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
import build

from .tool import ToolsSupported
from .workspace import Workspace
from .settings import ProjectSettings

help = 'Flash a project'

def run(args):
    #first build a project then flash it
    build.run(args)
    # time to flash
    if args.file:
        # known project from records
        workspace = Workspace(args.file, os.getcwd())
        if args.project:
            workspace.flash_project(args.project, args.tool)
        else:
            workspace.flash_projects(args.tool)
    else:
        # not project known by pgen
        project_settings = ProjectSettings()
        project_files = [os.path.join(args.directory, args.project)]
        flasher = ToolsSupported().get_value(args.tool, 'flasher')
        build(flasher, args.project, project_files, args.tool, project_settings)

def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file")
    subparser.add_argument("-p", "--project", help="Name of the project to flash")
    subparser.add_argument(
        "-t", "--tool", help="Flash a project files for provided tool")
    subparser.add_argument(
        "-dir", "--directory", help="The projects directory")
    subparser.add_argument(
        "-defdir", "--defdirectory",
        help="Path to the definitions, otherwise default (~/.pg/definitions) is used")

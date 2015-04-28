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
from .tool import build
from .workspace import Workspace

help = 'Build a project'

def run(args):
    # either known project from a project file or any uknown project
    if args.file:
        workspace = Workspace(args.file, os.getcwd())
        if args.project:
            workspace.build_project(args.project, args.tool)
        else:
            workspace.build_projects(args.tool)
    else:
        # not project known to pgen
        project_settings = ProjectSettings()
        builder = tool.ToolsSupported().get_value(tool, 'builder')
        build(builder, args.project, args.dir, args.tool, project_settings)

def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml')
    subparser.add_argument("-p", "--project", help="Project to be built")
    subparser.add_argument(
        "-t", "--tool", help="Create project files for provided tool (uvision by default)")
    subparser.add_argument(
        "-dir", "--directory", help="The projects directory", default='projects.yaml')

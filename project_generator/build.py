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
import export
import logging

from .tool import build, ToolsSupported
from .workspace import Workspace
from .settings import ProjectSettings

help = 'Build a project'


def run(args):
    # Export if we know how, otherwise return
    if args.file:
        args.copy = False
        args.build = False
        export.run(args)
    else:
        if not os.path.exists(os.path.join(args.directory, args.project)):
            logging.debug("The project: %s does not exist." % os.path.join(args.directory, args.project))
            return

    if args.file:
        # known project from records
        workspace = Workspace(args.file, os.getcwd())
        if args.project:
            workspace.build_project(args.project, args.tool)
        else:
            workspace.build_projects(args.tool)
    else:
        # not project known by pgen
        project_settings = ProjectSettings()
        project_files = [os.path.join(args.directory, args.project)]
        builder = ToolsSupported().get_value(args.tool, 'builder')
        build(builder, args.project, project_files, args.tool, project_settings)


def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file")
    subparser.add_argument("-p", "--project", help="Name of the project to build")
    subparser.add_argument(
        "-t", "--tool", help="Build a project files for provided tool")
    subparser.add_argument(
        "-dir", "--directory", help="The projects directory")

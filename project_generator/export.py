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

import argparse
import os
import logging
import pkg_resources

from . import settings

from .builder import ProjectBuilder
from .generator import ProjectGenerator
from .settings import ProjectSettings

def main():
    logging.basicConfig(level=logging.INFO)
    # Should be launched from root/tools but all scripts are referenced to root
    root = os.path.normpath(os.getcwd())
    os.chdir(root)
    logging.debug('This should be the project root: %s', os.getcwd())

    # Parse Options
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="YAML projects file.")
    parser.add_argument("-p", "--project", help="Project to be generated.")
    parser.add_argument(
        "-t", "--tool", help="Create project files for provided tool (uvision by default).")
    parser.add_argument("-l", "--list", action="store_true",
                      help="List projects defined in the project file.")
    parser.add_argument(
        "-b", "--build", action="store_true", help="Build defined projects.")
    parser.add_argument("--version", action='version',
        version=pkg_resources.require("project_generator")[0].version, help="Display version.")

    args = parser.parse_args()

    if not args.file:
        args.file = 'projects.yaml'

    settings = ProjectSettings()
    if not args.tool:
        args.tool = settings.DEFAULT_TOOL

    # Generate projects
    generator = ProjectGenerator(settings)
    generator.set_toolchain(args)
    projects, project_paths = generator.run(args)

    # Build all exported projects
    if args.build:
        ProjectBuilder(settings).run(args, projects, project_paths, root)

if __name__ == '__main__':
    main()

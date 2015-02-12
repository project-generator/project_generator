# Copyright 2014 0xc0170
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

from optparse import OptionParser

import os
import logging

from . import settings

from .builder import ProjectBuilder
from .generator import ProjectGenerator
from .settings import ProjectSettings

def main():
    logging.basicConfig(level=logging.DEBUG)
    # Should be launched from root/tools but all scripts are referenced to root
    root = os.path.normpath(os.getcwd())
    os.chdir(root)
    logging.debug('This should be the project root: %s', os.getcwd())

    # Parse Options
    parser = OptionParser()
    parser.add_option("-f", "--file", help="YAML projects file")
    parser.add_option("-p", "--project", help="Project to be generated")
    parser.add_option(
        "-t", "--tool", help="Create project files for provided tool (uvision by default)")
    parser.add_option("-l", "--list", action="store_true",
                      help="List projects defined in the project file.")
    parser.add_option(
        "-b", "--build", action="store_true", help="Build defined projects.")

    (options, args) = parser.parse_args()

    if not options.tool:
        options.tool = settings.DEFAULT_TOOL

    settings = ProjectSettings()

    # Generate projects
    generator = ProjectGenerator()
    generator.set_toolchain(options)
    projects, project_paths = generator.run(options, settings)

    # Build all exported projects
    if options.build:
        ProjectBuilder().run(options, projects, project_paths, settings, root)

if __name__ == '__main__':
    main()

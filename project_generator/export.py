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
import sys
import logging
import pkg_resources

from . import settings

from .builder import ProjectBuilder
from .generator import ProjectGenerator
from .settings import ProjectSettings

def init(generator, settings, args):
    logging.debug("Generating the records.")
    generator.scrape_dir(args.board, args.directory, args.all)
    sys.exit()

def export(generator, settings, args):
    if not args.tool:
        args.tool = settings.DEFAULT_TOOL
    if not args.file:
        args.file = 'projects.yaml'
    generator.set_toolchain(args)
    projects, project_paths = generator.run(args)
    if args.execute:
        ProjectBuilder(settings).run(args, projects, project_paths, root)

def clean(generator, settings, args):
    generator.clean(args)

def main():
    logging.basicConfig(level=logging.DEBUG)
    # Should be launched from project's root
    root = os.path.normpath(os.getcwd())
    os.chdir(root)
    logging.debug('This should be the project root: %s', os.getcwd())

    # Parse Options
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # Init commands
    init_parser = subparsers.add_parser('init', help='Create a project record')
    init_parser.add_argument('-b','--board', action='store', help='Board selection')
    init_parser.add_argument('-dir','--directory', action='store', help='Directory selection')
    init_parser.add_argument('-all','--all', action='store_true', help='List all files, otherwise only folders for sources.')
    init_parser.set_defaults(func=init)

    # Export commands
    export_parser = subparsers.add_parser('export', help='Export a project record')
    export_parser.add_argument("-f", "--file", help="YAML projects file.")
    export_parser.add_argument("-p", "--project", help="Project to be generated.")
    export_parser.add_argument(
        "-t", "--tool", help="Create project files for provided tool (uvision by default).")
    export_parser.add_argument("-l", "--list", action="store_true",
        help="List projects defined in the project file.")
    export_parser.add_argument(
        "-e", "--execute", action="store_true", help="Build defined projects.")
    export_parser.set_defaults(func=export)

    # Clean commands
    clean_parser = subparsers.add_parser('clean', help='Clean generated projects')
    clean_parser.add_argument("--all", help="All generated projects.")
    clean_parser.add_argument("-f", "--file", help="YAML projects file.")
    clean_parser.add_argument("-p", "--project", help="Specify which project to be removed")
    clean_parser.add_argument(
        "-t", "--tool", help="Create project files for provided tool (uvision by default).")
    clean_parser.set_defaults(func=clean)

    parser.add_argument("--version", action='version',
        version=pkg_resources.require("project_generator")[0].version, help="Display version.")

    args = parser.parse_args()

    settings = ProjectSettings()
    generator = ProjectGenerator(settings)
    args.func(generator, settings, args)

if __name__ == '__main__':
    main()

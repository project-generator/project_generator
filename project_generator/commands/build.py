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
from . import argparse_filestring_type, argparse_string_type, split_options

help = 'Build a project'

def run(args):
    # Export if we know how, otherwise return
    combined_projects = args.projects + args.project or ['']
    kwargs = split_options(args.options)
    generator = Generator(args.file)
    any_build_failed = False
    any_export_failed = False
    for project_name in combined_projects:
        for project in generator.generate(project_name):
            clean_failed = False
            if args.clean and project.clean(args.tool) == -1:
                clean_failed = True # So we don't attempt to generate or build this project.
                any_build_failed = True
            if not clean_failed:
                if project.generate(args.tool, args.copy) == -1:
                    any_export_failed = True
                if project.build(args.tool, jobs=args.jobs, **kwargs) == -1:
                    any_build_failed = True
            if args.stop_on_failure and (any_build_failed or any_export_failed):
                break

    if any_build_failed or any_export_failed:
        return -1
    else:
        return 0

def setup(subparser):
    subparser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help='Increase the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument('-q', dest='quietness', action='count', default=0,
                        help='Decrease the verbosity of the output (repeat for less verbose output)')
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml',
        type=argparse_filestring_type)
    subparser.add_argument(
        "-p", "--project", dest="projects", action='append', default=[], help="Name of the project to build")
    subparser.add_argument(
        "-t", "--tool", help="Build a project files for provided tool",
        type=argparse_string_type(str.lower, False), choices=list(ToolsSupported.TOOLS_DICT.keys()) + list(ToolsSupported.TOOLS_ALIAS.keys()))
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")
    subparser.add_argument(
        "-k", "--clean", action="store_true", help="Clean project before building")
    subparser.add_argument(
        "-o", "--options", action="append", help="Toolchain options")
    subparser.add_argument(
        "-x", "--stop-on-failure", action="store_true", help="Stop on first failure")
    subparser.add_argument(
        "-j", "--jobs", action="store", type=int, default=1,
        help="Number of concurrent build jobs (not supported by all tools)")
    subparser.add_argument("project", nargs='*',
                        help="Specify projects to be generated and built")

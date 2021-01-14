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
import multiprocessing as mp

from ..tools_supported import ToolsSupported
from ..generate import Generator
from . import argparse_filestring_type, argparse_string_type, split_options

logger = logging.getLogger('progen.generate')

help = 'Generate a project record'

def _setup_logging(args):
    verbosity = args.verbosity - args.quietness

    logging_level = max(logging.INFO - (10 * verbosity), 0)
    logging.basicConfig(format="%(name)s %(levelname)s\t%(message)s", level=logging_level)
    return logging.getLogger('progen.generate')

def _generate_project(project, args):
    logger = _setup_logging(args)
    build_failed = False
    export_failed = False
    generated = False
    if hasattr(project, 'workspace_name') and (project.workspace_name is not None):
        logger.info("Generating %s for %s in workspace %s", args.tool, project.name, project.workspace_name)
    else:
        logger.info("Generating %s for %s", args.tool, project.name)
    if project.generate(args.tool, copied=args.copy, copy=args.copy) == -1:
        export_failed = True
    if args.build:
        kwargs = split_options(args.options)
        if project.build(args.tool, **kwargs) == -1:
            build_failed = True
    return (build_failed, export_failed)

def run(args):
    combined_projects = args.projects + args.project or ['']
    generator = Generator(args.file)
    build_failed = False
    export_failed = False
    generated = False

    try:
        # Create a pool of processes to run generators.
        pool = mp.Pool(args.jobs)

        # Issue jobs.
        results = [pool.apply_async(_generate_project, (project, args))
                    for project_name in combined_projects
                    for project in generator.generate(project_name)]

        # Gather results
        for r in results:
            build_failed, export_failed = r.get(timeout=20.0)
            if build_failed or export_failed:
                # Force termination of running jobs.
                pool.terminate()
                break
            else:
                generated = True

        if build_failed or export_failed or not generated:
            return -1
        else:
            return 0
    finally:
        pool.close()
        pool.join()

def _get_default_jobs():
    # Get number of CPUs.
    try:
        return mp.cpu_count()
    except NotImplementedError:
        # Default of 2 if we can't get the actual count.
        return 2

def setup(subparser):
    subparser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help='Increase the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument('-q', dest='quietness', action='count', default=0,
                        help='Decrease the verbosity of the output (repeat for more verbose output)')
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml', type=argparse_filestring_type)
    subparser.add_argument(
        "-p", "--project", dest="projects", action='append', default=[], help="Project to be generated")
    subparser.add_argument(
        "-t", "--tool", help="Create project files for provided tool",
        type=argparse_string_type(str.lower, False), choices=list(ToolsSupported.TOOLS_DICT.keys()) + list(ToolsSupported.TOOLS_ALIAS.keys()))
    subparser.add_argument(
        "-b", "--build", action="store_true", help="Build defined projects")
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")
    subparser.add_argument(
        "-o", "--options", action="append", help="Toolchain options")
    num_cpus = _get_default_jobs()
    subparser.add_argument(
        "-j", "--jobs", action="store", type=int, default=num_cpus,
                help=("Number of concurrent jobs to use for generating projects (default is %d)" % num_cpus))
    subparser.add_argument("project", nargs='*',
                        help="Specify projects to be generated")

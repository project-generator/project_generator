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

from .commands import build, clean, export, init, list_projects, import_command

subcommands = {
    'init': init,
    'export': export,
    'clean': clean,
    'list': list_projects,
    'build': build,
    'import': import_command,
}

def main():
    # Parse Options
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help='Increase the verbosity of the output (repeat for more verbose output)')
    parser.add_argument('-q', dest='quietness', action='count', default=0,
                        help='Decrease the verbosity of the output (repeat for more verbose output)')

    parser.add_argument("--version", action='version',
                        version=pkg_resources.require("project_generator")[0].version, help="Display version")

    subparsers = parser.add_subparsers(help='commands')

    for name, module in subcommands.items():
        subparser = subparsers.add_parser(name, help=module.help)

        module.setup(subparser)
        subparser.set_defaults(func=module.run)

    args = parser.parse_args()

    # set the verbosity
    verbosity = args.verbosity - args.quietness

    logging_level = max(logging.INFO - (10 * verbosity), 0)

    logging.basicConfig(format="%(levelname)s\t%(message)s", level=logging_level)

    logging.debug('This should be the project root: %s', os.getcwd())

    return args.func(args)

if __name__ == '__main__':
    main()

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
import sys
import logging

from .project import Project

help = 'Create a project record'


def run(args):
    logging.debug("Generating the records.")

    root = os.getcwd()

    directory = root if not args.directory else os.path.join(root, args.directory)
    Project.scrape_dir(root, directory, args.name, args.target, args.sources)


def setup(subparser):
    subparser.add_argument(
        'name', help='Project name')
    subparser.add_argument(
        '-tar', '--target', action='store', help='Target definition')
    subparser.add_argument(
        '-dir', '--directory', action='store', help='Directory selection', default=None)
    subparser.add_argument(
        '-s', '--sources', action='store_true', help='List all files, otherwise only folders for sources.')

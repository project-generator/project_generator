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
from ..init_yaml import create_yaml

help = 'Create a project record'


def run(args):
    logging.debug("Generating the records.")

    root = os.getcwd()
    directory = root if not args.directory else os.path.join(root, args.directory)
    name = os.path.split(directory)[1] if not args.name else args.name
    return create_yaml(root, directory, name, args.target.lower(), args.files)


def setup(subparser):
    subparser.add_argument(
        '-name', help='Project name')
    subparser.add_argument(
        '-tar', '--target', action='store', help='Target definition', default = "cortex-m0")
    subparser.add_argument(
        '-dir', '--directory', action='store', help='Directory selection', default=None)
    subparser.add_argument(
        '-files', '--files', action='store_true', help='List file names', default=None)

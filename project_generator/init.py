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

import sys
import logging

help = 'Create a project record'


def run(generator, settings, args, root):
    logging.debug("Generating the records.")
    generator.scrape_dir(args.board, args.directory, args.sources, root)
    sys.exit()


def setup(subparser):
    subparser.add_argument(
        '-bd', '--board', action='store', help='Board definition')
    subparser.add_argument(
        '-dir', '--directory', action='store', help='Directory selection')
    subparser.add_argument(
        '-s', '--sources', action='store_true', help='List all files, otherwise only folders for sources.')

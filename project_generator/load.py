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
import shutil
import os.path
import distutils.util

help = 'Load definition files'


def run(generator, settings, args, root):
    config_directory = os.path.expanduser('~/.pg')
    definitions_directory = os.path.join(config_directory, 'definitions')

    if not os.path.isdir(config_directory):
        logging.debug("Config directory does not exist.")
        logging.debug("Creating config directory: %s" % config_directory)
        os.path.mkdir(config_directory)

    overwrite = True

    if os.path.isdir(definitions_directory):
        # this should be print, not logging
        print("Definitions directory already exists.")

        while True:
            answer = input('Should I overwrite it? (Y/n)')

            try:
                overwrite = distutils.util.strtobool(answer)
                break
            except ValueError:
                continue

    if overwrite:
        shutil.rmtree(os.path.join(config_directory, 'definitions'))

        if os.path.isdir(definitions_directory):
            # it shouldn't exist any more
            logging.error("Unable to remove existing definitions directory.")
            return -1

        command = ['git', 'clone', args.directory, 'definitions']

        subprocess.call(command, cwd=config_directory)


def setup(subparser):
    subparser.add_argument(
        "-dir", "--directory", help="Locations of definitions repository")

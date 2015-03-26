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
import shutil
import logging
import subprocess

from .util import rmtree_if_exists

help = 'Update definitions source repository'

def run(args):
    config_directory = os.path.expanduser(os.path.join('~', '.pg'))
    definitions_location = os.path.join(config_directory, 'definitions')

    if not os.path.exists(config_directory):
        os.mkdir(config_directory)

    if args.source:
        # is source remote or local?
        if args.force:
            rmtree_if_exists(definitions_location)
        elif os.path.exists(definitions_location):
            logging.critical('Definitions location already exists.')
            return

        if os.path.exists(args.source):
            # local
            if args.copy:
                # copy contents of directory
                logging.debug('Copying contents of %s to %s' % (args.source, definitions_location))
                shutil.copytree(args.source, definitions_location)
            else:
                if os.name == 'nt' and not args.copy:
                    logging.warning('Symlink only supported on unix systems')
                    logging.info('Copying directory')
                    shutil.copytree(args.source, definitions_location)

                    return

                os.symlink(source, definitions_location)
        else:
            # remote
            cmd = ('git', 'clone', '--quiet', args.source, 'definitions')

            subprocess.call(cmd, cwd=config_directory)
    else:
        if not os.path.exists(definitions_location):
            cmd = ('git', 'clone', '--quiet', 'https://github.com/0xc0170/project_generator_definitions.git', 'definitions')
            subprocess.call(cmd, cwd=config_directory)
        else:
            cmd = ('git', 'pull', '--rebase', '--quiet', 'origin', 'master')
            subprocess.call(cmd, cwd=definitions_location)

        

def setup(subparser):
    subparser.add_argument('-f', '--force', action='store_true', help='Force update of the directory')
    subparser.add_argument('-c', '--copy', action='store_true',
                            help='Copy contents directory instead of symlinking (only for local directories)')
    subparser.add_argument('source', help='Where to get the updates from', nargs='?')

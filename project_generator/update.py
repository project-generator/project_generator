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
from .settings import ProjectSettings

help = 'Update definitions source repository'

def update(source=None, force=False, copy=False, settings=ProjectSettings()):
    defdir_exists = True
    if not os.path.exists(settings.paths['definitions']):
        defdir_exists = False
        os.mkdir(settings.paths['definitions'])

    if source:
        # is source remote or local?
        if force:
            rmtree_if_exists(settings.paths['definitions'])
        elif os.path.exists(settings.paths['definitions']):
            logging.critical('Definitions location already exists.')
            return

        if os.path.exists(source):
            # local
            if copy:
                # copy contents of directory
                logging.debug('Copying contents of %s to %s' % (source, settings.paths['definitions']))
                shutil.copytree(source, settings.paths['definitions'])
            else:
                if os.name == 'nt' and not copy:
                    logging.warning('Symlink only supported on unix systems')
                    logging.info('Copying directory')
                    shutil.copytree(source, settings.paths['definitions'])

                    return

                os.symlink(source, settings.paths['definitions'])
        else:
            # remote
            cmd = ('git', 'clone', '--quiet', source, 'definitions')

            subprocess.call(cmd, cwd=settings.paths['definitions'])
    else:
        if not defdir_exists:
            cmd = ('git', 'clone', '--quiet', 'https://github.com/0xc0170/project_generator_definitions.git', '.')
            subprocess.call(cmd, cwd=settings.paths['definitions'])
        elif force:
            # rebase only if force, otherwise use the current version
            cmd = ('git', 'pull', '--rebase', '--quiet', 'origin', 'master')
            subprocess.call(cmd, cwd=settings.paths['definitions'])


def run(args):
    update(args.source, args.force, args.copy)
        

def setup(subparser):
    subparser.add_argument('-f', '--force', action='store_true', help='Force update of the directory', default=True)
    subparser.add_argument('-c', '--copy', action='store_true',
                            help='Copy contents directory instead of symlinking (only for local directories)')
    subparser.add_argument('source', help='Where to get the updates from', nargs='?')

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
import subprocess

from .settings import ProjectSettings

help = 'Update definitions source repository'


def update(force=False, settings=ProjectSettings()):
    defdir_exists = True
    if not os.path.exists(settings.paths['definitions']):
        defdir_exists = False
        os.mkdir(settings.paths['definitions'])

    # For default, use up to date repo from github
    if settings.get_env_settings('definitions') == settings.get_env_settings('definitions_default'):
        if not defdir_exists:
            cmd = ('git', 'clone', '--quiet',
                   'https://github.com/project-generator/project_generator_definitions.git', '.')
            subprocess.call(cmd, cwd=settings.paths['definitions'])
        elif force:
            # rebase only if force, otherwise use the current version
            cmd = ('git', 'pull', '--rebase', '--quiet', 'origin', 'master')
            subprocess.call(cmd, cwd=settings.paths['definitions'])
        else:
            # check if we are on top of origin/master
            cmd = ('git', 'fetch', 'origin','master', '--quiet')
            subprocess.call(cmd, cwd=settings.paths['definitions'])
            cmd = ('git', 'diff', 'master', 'origin/master', '--quiet')
            p = subprocess.call(cmd, cwd=settings.paths['definitions'])
            # any output means we are behind the master, update
            if p:
                logging.debug("Definitions are behind the origin/master, rebasing.")
                cmd = ('git', 'pull', '--rebase', '--quiet', 'origin', 'master')
                subprocess.call(cmd, cwd=settings.paths['definitions'])


def run(args):
    update(args.source, args.force, args.copy)


def setup(subparser):
    subparser.add_argument('-f', '--force', action='store_true',
                           help='Force update of the remote directory', default=True)

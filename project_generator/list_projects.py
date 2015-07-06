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

from .workspace import PgenWorkspace
from .util import unicode_available

help = 'List all projects'


def run(args):
    if args.file:
        workspace = PgenWorkspace(args.file, os.getcwd())

        if args.section == 'targets':
            print(workspace.list_targets())
        elif args.section == 'projects':
            if not args.no_unicode and unicode_available():
                print(workspace.list_projects())
            else:
                print(workspace.list_projects(use_unicode=False))
        elif args.section == 'tools':
            print(workspace.list_tools())
    else:
        print(PgenWorkspace.pgen_list(args.section.lower()))


def setup(subparser):
    subparser.add_argument("section", choices = ['targets','tools','projects'],
                           help="What section you would like listed", default='projects')
    subparser.add_argument("-f", "--file", help="YAML projects file")
    subparser.add_argument("-u", "--no-unicode", help="Use ASCII characters only", action='store_true')

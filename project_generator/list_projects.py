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
from .workspace import Workspace

help = 'List all projects'


def run(args):
    if args.file != "X":
        workspace = Workspace(args.file, os.getcwd())
        workspace.list(args.section.lower())
    else:
        Workspace.pgen_list(args.section.lower())


def setup(subparser):
    subparser.add_argument("section", choices =['targets','tools','projects'],    help="What section you would like listed", default='projects')
    subparser.add_argument("-f", "--file", help="YAML projects file", default='X')

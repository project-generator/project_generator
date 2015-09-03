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

from ..tools_supported import ToolsSupported
from ..generate import Generator
from ..util import unicode_available

help = 'List general pgen data as projects, tools or targets'


def run(args):
    if args.file and os.path.exists(args.file):
        generator = Generator(args.file)
        for project in generator.generate():
            if args.section == 'targets':
                print("%s supports: %s"%(project.project['name'],project.project['target']))
            elif args.section == 'projects':
                print (project.project['name'])
            elif args.section == 'tools':
                tools = [tool for tool, value in project.tool_specific.items() if value.linker_file is not None]
                tools = ", ".join(tools)
                print("%s supports: %s\n"%(project.project['name'], tools))
    else:
        print("\nPgen supports the following tools:\n")
        print("\n".join(ToolsSupported().get_supported()))
    return 0


def setup(subparser):
    subparser.add_argument("section", choices = ['targets','tools','projects'],
                           help="What section you would like listed", default='projects')
    subparser.add_argument("-f", "--file", help="YAML projects file")
    subparser.add_argument("-u", "--no-unicode", help="Use ASCII characters only", action='store_true')

# Copyright 2015 0xc0170
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

import argparse
import os
import yaml
import shutil

from unittest import TestCase
from nose.tools import *

from project_generator.commands import import_command

class TestImportCommand(TestCase):

    """test import command"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/template_file'), 'wt') as f:
            f.write(yaml.dump('Hello', default_flow_style=False))

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = subparsers.add_parser('import', help=import_command.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)

    @raises(SystemExit)
    def test_import_empty_command(self):
        import_command.setup(self.subparser)
        args = self.parser.parse_args(['import'])
        result = import_command.run(args)

        # this should fail
        assert result == -1

    # TODO 0xc0170: add all tools import and also template files
    # def test_import_uvision(self):
    #     # Should raise None
    #     import_command.setup(self.subparser)
    #     args = self.parser.parse_args(['import', '-t', 'uvision'])
    #     import_command.run(args)

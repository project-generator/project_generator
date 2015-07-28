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

from project_generator.commands import init

class TestInitCommand(TestCase):

    """test init command"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')

        # create 3 files to test init
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header1.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/linker.ld'), 'wt') as f:
            pass

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = subparsers.add_parser('init', help=init.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        os.remove('projects.yaml')
        os.remove('project.yaml')

    def test_init_empty_project(self):
        init.setup(self.subparser)
        args = self.parser.parse_args(['init'])
        result = init.run(args)

        assert result == 0
        # Should create 2 files
        assert os.path.isfile('projects.yaml')
        assert os.path.isfile('project.yaml')

    def test_init_small_project(self):
        init.setup(self.subparser)
        args = self.parser.parse_args(['init', '-dir', 'test_workspace'])
        result = init.run(args)

        assert result == 0
        # Should create 2 files
        assert os.path.isfile('projects.yaml')
        assert os.path.isfile('project.yaml')

        # TODO 0xc0170: add checking yaml files if they contain 3 files we created.
        # we should also export using those to check validity (or export bugs :) )

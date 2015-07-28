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

from project_generator.commands import list_projects
from .simple_project import project_1_yaml, projects_yaml, project_2_yaml

class TestListCommand(TestCase):

    """test list command"""

    def setUp(self):
        # we produce some files, to check if list projects listing the projects we defined
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_yaml, default_flow_style=False))

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = subparsers.add_parser('list', help=list_projects.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)

    def test_list_projects(self):
        # For now list projects should not fail, we should add checking stdout if projects match
        list_projects.setup(self.subparser)
        args = self.parser.parse_args(['list','projects'])
        result = list_projects.run(args)

        assert result == 0

    def test_list_targets(self):
        # For now list projects should not fail, we should add checking stdout if targets match
        list_projects.setup(self.subparser)
        args = self.parser.parse_args(['list','targets'])
        result = list_projects.run(args)

        assert result == 0

    def test_list_tools(self):
        # For now list projects should not fail, we should add checking stdout if tools match
        list_projects.setup(self.subparser)
        args = self.parser.parse_args(['list','tools'])
        result = list_projects.run(args)

        assert result == 0

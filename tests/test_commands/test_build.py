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

from project_generator.commands import build
from .simple_project import project_1_yaml, projects_yaml, project_2_yaml

class TestBuildCommand(TestCase):

    """test build command"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_2.yaml'), 'wt') as f:
            f.write(yaml.dump(project_2_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_yaml, default_flow_style=False))

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = subparsers.add_parser('build', help=build.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    @raises(RuntimeError)
    def test_build_project_unknown_tool(self):
        # we pass unknown tool which should raise RuntimeError
        build.setup(self.subparser)
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2'])
        result = build.run(args)

        # TODO 0xc0170: we need to return valid values, then we enable this assert
        # assert result == 0

    def test_build_project_uvision_tool(self):
        # we pass unknown tool which should raise RuntimError
        build.setup(self.subparser)
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'uvision'])
        result = build.run(args)

        # TODO 0xc0170: we need to return valid values, then we enable this assert
        # assert result == 0

    def test_build_project_iar_arm_tool(self):
        # we pass unknown tool which should raise RuntimError
        build.setup(self.subparser)
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'iar_arm'])
        result = build.run(args)

        # TODO 0xc0170: we need to return valid values, then we enable this assert
        # assert result == 0

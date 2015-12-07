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

from project_generator.commands import generate, clean
from .simple_project import project_1_yaml, projects_yaml, project_2_yaml

class TestCleanCommand(TestCase):

    """test clean command"""

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
        self.export_subparser = subparsers.add_parser('generate', help=generate.help)
        self.clean_subparser = subparsers.add_parser('clean', help=clean.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)


    def test_clean_one_project(self):
        # We first generate project, then clean it
        generate.setup(self.export_subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'uvision'])
        result = generate.run(args)

        # this should generate a project to generated_projects/uvision_project_2/project_2.uvproj
        assert os.path.isfile('generated_projects/uvision_project_2/project_2.uvproj')
        assert result == 0

        # now clean
        clean.setup(self.clean_subparser)
        args = self.parser.parse_args(['clean','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'uvision'])
        result = clean.run(args)

        assert not os.path.isfile('generated_projects/uvision_project_2/project_2.uvproj')
        assert not os.path.isdir('generated_projects/uvision_project_2')
        assert result == 0

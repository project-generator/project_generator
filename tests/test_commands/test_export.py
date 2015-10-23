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

from project_generator.commands import generate
from .simple_project import project_1_yaml, projects_yaml, project_2_yaml

class TestExportCommand(TestCase):

    """test generate command"""

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
        self.subparser = subparsers.add_parser('generate', help=generate.help)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_generate_project3_all_tools(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_3'])
        result = generate.run(args)

        # one of the tools is unknown , should return -1
        assert result == -1

    def test_generate_project2_all_tools(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2'])
        result = generate.run(args)

        # No tools defined
        assert result == -1

    def test_generate_one_project_uvision(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'uvision'])
        result = generate.run(args)

        assert result == 0

        # this should generate a project to generated_projects/uvision_project_2/project_2.uvproj
        assert os.path.isfile('generated_projects/uvision_project_2/project_2.uvproj')

    def test_generate_one_project_iar_arm(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'iar_arm'])
        result = generate.run(args)

        assert result == 0

        # this should generate a project to generated_projects/uvision_project_2/project_2.ewp/ewd/eww
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.ewp')
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.ewd')
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.eww')

    def test_generate_one_project_make_gcc_arm(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'make_gcc_arm'])
        result = generate.run(args)

        assert result == 0
        # this should generate a project to generated_projects/uvision_project_2/Makefile
        assert os.path.isfile('generated_projects/make_gcc_arm_project_2/Makefile')

    def test_generate_one_project_coide(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'coide'])
        result = generate.run(args)

        assert result == 0

        # this should generate a project to generated_projects/uvision_project_2/project_2.coproj
        assert os.path.isfile('generated_projects/coide_project_2/project_2.coproj')

    def test_generate_one_project_arm_none_eabi_gdb(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'arm_none_eabi_gdb'])
        result = generate.run(args)

        assert result == 0

    def test_generate_one_project_sublime_make_gcc_arm(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'sublime_make_gcc_arm'])
        result = generate.run(args)

        assert result == 0

    def test_generate_one_project_eclipse_make_gcc_arm(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'eclipse_make_gcc_arm'])
        result = generate.run(args)

        assert result == 0

    def test_generate_workspace_all_tools(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p',
            'project_workspace'])
        result = generate.run(args)

        # we dont specify tool to generate, which is not valid for workspace.
        # we don't know which tool we should build worksapce for as it consists
        # of projects, and each can speficify tools supported.
        assert result == -1

    def test_generate_workspace_uvision(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p',
            'project_workspace', '-t', 'uvision'])
        result = generate.run(args)

        assert result == 0

    def test_generate_workspace_iar_arm(self):
        generate.setup(self.subparser)
        args = self.parser.parse_args(['generate','-f','test_workspace/projects.yaml','-p',
            'project_workspace', '-t', 'iar_arm'])
        result = generate.run(args)

        assert result == 0

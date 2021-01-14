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
        with open(os.path.join(os.getcwd(), 'test_workspace/linker.ld'), 'wt'):
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            f.write("int __bss_start__ = 0;\nint __bss_end__ = 0;\nint _exit = 0;\nint main() {}\n")

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = subparsers.add_parser('build', help=build.help)
        build.setup(self.subparser)

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_build_project_unknown_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2'])
        result = build.run(args)

        assert result == -1

    def test_build_project_uvision_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'uvision'])
        result = build.run(args)

        # not valid project, should fail with errors
        assert result == -1

    def test_build_workspace_uvision_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_workspace', '-t', 'uvision'])
        result = build.run(args)

        # workspace build not supported for now
        assert result == -1

    def test_build_project_iar_arm_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'iar_arm'])
        result = build.run(args)

        # CI does not have IAR ARM tool installed should fail , or even a project is not valid
        assert result == -1

    @raises(NotImplementedError)
    def test_build_project_coide_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'coide'])
        result = build.run(args)

    def test_build_project_make_gcc_arm_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'make_gcc_arm'])
        result = build.run(args)

    def test_build_project_cmake_gcc_arm_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'cmake_gcc_arm'])
        result = build.run(args)

    def test_build_project_make_armcc_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'make_armcc'])
        result = build.run(args)

        assert result == -1

    @raises(NotImplementedError)
    def test_build_project_eclipse_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'eclipse_make_gcc_arm'])
        result = build.run(args)

    @raises(NotImplementedError)
    def test_build_project_gdb_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'gdb'])
        result = build.run(args)

    @raises(NotImplementedError)
    def test_build_project_arm_none_eabi_gdb_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'arm_none_eabi_gdb'])
        result = build.run(args)

    def test_build_project_sublime_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'sublime'])
        result = build.run(args)

        assert result == -1

    def test_build_project_sublime_tool(self):
        args = self.parser.parse_args(['build','-f','test_workspace/projects.yaml','-p',
            'project_2', '-t', 'sublime_make_gcc_arm'])
        result = build.run(args)

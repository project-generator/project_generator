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

from project_generator.commands import export
from .simple_project import project_1_yaml, projects_yaml, project_2_yaml

class TestExportCommand(TestCase):

    """test export command"""

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
        self.subparser = subparsers.add_parser('export', help=export.help)

    def tearDown(self):
        # remove created directory
        pass
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_export_one_project_uvision(self):
        export.setup(self.subparser)
        args = self.parser.parse_args(['export','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'uvision'])
        export.run(args)

        # this should export a project to generated_projects/uvision_project_2/project_2.uvproj
        assert os.path.isfile('generated_projects/uvision_project_2/project_2.uvproj')

    def test_export_one_project_iar_arm(self):
        export.setup(self.subparser)
        args = self.parser.parse_args(['export','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'iar_arm'])
        export.run(args)

        # this should export a project to generated_projects/uvision_project_2/project_2.ewp/ewd/eww
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.ewp')
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.ewd')
        assert os.path.isfile('generated_projects/iar_arm_project_2/project_2.eww')

    def test_export_one_project_make_gcc_arm(self):
        export.setup(self.subparser)
        args = self.parser.parse_args(['export','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'make_gcc_arm'])
        export.run(args)

        # this should export a project to generated_projects/uvision_project_2/Makefile
        assert os.path.isfile('generated_projects/make_gcc_arm_project_2/Makefile')

    def test_export_one_project_coide(self):
        export.setup(self.subparser)
        args = self.parser.parse_args(['export','-f','test_workspace/projects.yaml','-p','project_2',
            '-t', 'coide'])
        export.run(args)

        # this should export a project to generated_projects/uvision_project_2/project_2.coproj
        assert os.path.isfile('generated_projects/coide_project_2/project_2.coproj')


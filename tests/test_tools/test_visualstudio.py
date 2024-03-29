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
import os
import yaml
import shutil

from unittest import TestCase

from project_generator.generate import Generator
from project_generator.project import Project
from project_generator.settings import ProjectSettings
from project_generator.tools.visual_studio import VisualStudioMakeGCCARM

from .simple_project import project_1_yaml, project_2_yaml, projects_1_yaml

class TestProject(TestCase):

    """test things related to the visual studio tool"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        with open(os.path.join(os.getcwd(), 'test_workspace/project_2.yaml'), 'wt') as f:
            f.write(yaml.dump(project_2_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_1_yaml, default_flow_style=False))

        self.project = next(Generator(projects_1_yaml).generate('project_1'))
        self.project2 = next(Generator(projects_1_yaml).generate('project_2'))

        self.vs = VisualStudioMakeGCCARM(self.project.project, ProjectSettings())

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_export_project(self):
        result = self.project.generate('visual_studio_make_gcc_arm', False)
        # TODO: add project files test once implemted
        # projectfiles = self.project.get_generated_project_files('visual_studio_make_gcc_arm')

        assert result == 0
        # assert projectfiles
        # assert os.path.splitext(projectfiles['files'][0])[1] == '.vcxproj.filters'

        result = self.project.generate('visual_studio_gdb', False)
        # TODO: add project files test once implemted
        # projectfiles = self.project.get_generated_project_files('visual_studio_make_gcc_arm')

        assert result == 0
        # assert projectfiles
        # assert os.path.splitext(projectfiles['files'][0])[1] == '.vcxproj.filters'

    def test_export_project_to_diff_directory(self):
        project_1_yaml['common']['export_dir'] = ['create_this_folder']
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        for project in Generator(projects_1_yaml).generate('project_1'):
            result = project.generate('visual_studio_make_gcc_arm', False)

        assert result == 0
        assert os.path.isdir('create_this_folder')
        shutil.rmtree('create_this_folder')

    def test_template(self):
        # should fail as template does not exists, and neither visual studio supports it
        result = self.project2.generate('visual_studio_make_gcc_arm', False)
        assert result == 0

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
import shutil

import yaml
from unittest import TestCase

from project_generator.generate import Generator
from project_generator.project import Project, ProjectWorkspace
from project_generator.settings import ProjectSettings

project_1_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['target1'],
        'core': ['core1'],
        'tools_supported': ['iar_arm', 'uvision', 'coide', 'unknown'],
        'output_type': ['exe'],
        'debugger': ['debugger_1'],
        'linker_file': ['test_workspace/linker.ld'],
    }
}

projects_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml']
    },
    'workspaces': {
        'projects': ['project_1']
    }
}

class TestWorkspace(TestCase):

    """test things related to the PgenWorkspace class"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_yaml, default_flow_style=False))

        self.project = Project('project_1',[project_1_yaml],
            ProjectSettings())

        self.workspace = ProjectWorkspace('workspace_project_1', [self.project],
            ProjectSettings(), {})


        # create 3 files to test project
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header1.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/linker.ld'), 'wt') as f:
            pass

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_member_variables(self):
        # basic test if name and projects are set properly
        assert self.workspace.name == 'workspace_project_1'
        assert self.workspace.projects == [self.project]
        assert bool(self.workspace.generated_files) == False

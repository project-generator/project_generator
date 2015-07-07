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
from unittest import TestCase

from project_generator.workspace import PgenWorkspace

project_1_yaml = {
    'common': {
        'sources': ['sources/main.cpp'],
        'includes': ['includes/header1.h']
    }
}

projects_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml']
    },
    'settings' : {
        'definitions_dir': ['notpg/path/somewhere'],
        'export_dir': ['not_generated_projects']
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
        self.workspace = PgenWorkspace('test_workspace/projects.yaml')

    def test_settings(self):
        # only check things which are affected by projects.yaml
        assert self.workspace.settings.paths['definitions'] == os.path.normpath('notpg/path/somewhere')
        assert self.workspace.settings.generated_projects_dir == 'not_generated_projects'

    def test_list_projects(self):
        # assert self.workspace.list_projects(width=1, False) == 'project_1'


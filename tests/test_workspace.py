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
from unittest import TestCase

from project_generator.workspace import Workspace

class TestWorkspace(TestCase):

    """test things related to the Workspace class"""

    def setUp(self):
        self.workspace = Workspace('test_projects/test_workspace/projects.yaml')

    def test_settings(self):
        # only check things which are affected by projects.yaml
        assert self.workspace.settings.paths['definitions'] == '~/.notpg'
        assert self.workspace.settings.generated_projects_dir == 'not_generated_projects'

    # def test_load_definitions(self):
    #     self.workspace.load_definitions()

    #     assert os.path.exists(os.path.expanduser(self.workspace.settings.paths['definitions']))

    def test_list_projects(self):
        assert self.workspace.list('projects', 'raw') == set()


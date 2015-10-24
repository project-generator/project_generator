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

from project_generator.settings import ProjectSettings

settings_dict = {
    'tools': {
        'iar': {
            'path' : ['path_to_iar'],
            'template': ['template_iar']
        },
        'uvision': {
            'path': ['path_to_uvision'],
            'template': ['template_uvision'],
        }
    },
    'definitions_dir': ['path_to_definitions'],
    'export_dir': ['path_to_export'],
}

class TestProject(TestCase):

    """test things related to the Project class"""

    def setUp(self):
        self.settings = ProjectSettings()

    def test_update(self):
        self.settings.update(settings_dict)

        assert self.settings.get_env_settings('iar') == settings_dict['tools']['iar']['path'][0]
        assert self.settings.get_env_settings('uvision') == settings_dict['tools']['uvision']['path'][0]
        assert self.settings.export_location_format == settings_dict['export_dir'][0]

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

import copy

from .tool import Tool, Exporter
from .gccarm import MakefileGccArm

class CMake(Tool,Exporter):

    generated_project = {
        'path': '',
        'files': {
            'cmakelist': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.workspace = workspace
        self.exporter = MakefileGccArm(workspace, env_settings)
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['cmake', 'gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def export_project(self):
        generated_projects = {}
        output = copy.deepcopy(self.generated_project)

        data_for_make = self.workspace.copy()
        self.exporter.process_data_for_makefile(data_for_make)

        project_path, output['files']['cproj'] = self.gen_file_jinja(
            'cmakelist.tmpl', data_for_make, 'CMakeLists.txt', data_for_make['output_dir']['path'])

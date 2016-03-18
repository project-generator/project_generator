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
from os import getcwd

from .tool import Tool, Exporter
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

class CMakeGccArm(Tool,Exporter):

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
        return ['cmake_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def fix_paths_unix(self, data):
        # cmake seems to require unix paths
        # This might do proper handling in the gcc arm, pass there a param (force normpath to unix)
        for key in SOURCE_KEYS:
            paths = []
            for value in data[key]:
                # TODO: this needs to be fixed
                paths.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + value.replace('\\', '/'))
            data[key] = paths
        # fix includes
        includes = []
        for key in data['include_paths']:
            includes.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + key.replace('\\', '/'))
        data['include_paths'] = includes
        data['linker_file'] = getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + data['linker_file'].replace('\\', '/')
        lib_paths = []
        for path in data['lib_paths']:
            lib_paths.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + path.replace('\\', '/'))
        data['lib_paths'] = lib_paths

    def export_project(self):
        generated_projects = {}
        generated_projects = copy.deepcopy(self.generated_project)

        data_for_make = self.workspace.copy()
        # Warning: we dont use rel path for cmake, we inject there root and use paths within root
        data_for_make['output_dir']['rel_path'] = ""
        self.exporter.process_data_for_makefile(data_for_make)
        try:
            data_for_make['misc'] = data_for_make['misc']
        except:
            pass

        self.fix_paths_unix(data_for_make)

        generated_projects['path'], generated_projects['files']['cmakelist'] = self.gen_file_jinja(
            'cmakelistgccarm.tmpl', data_for_make, 'CMakeLists.txt', data_for_make['output_dir']['path'])
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['cmakelist']]}

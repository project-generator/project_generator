# Copyright 2014-2015 sg-, 0xc0170
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

from .gccarm import MakefileGccArm

class SublimeTextMakeGccARM(MakefileGccArm):

    generated_project = {
        'path': '',
        'files': {
            'sublimetext': '',
            'makefile': '',
        }
    }

    def __init__(self, workspace, env_settings):
        super(SublimeTextMakeGccARM, self).__init__(workspace, env_settings)

    @staticmethod
    def get_toolnames():
        return ['sublime_make_gcc_arm', 'make_gcc_arm', 'sublime']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def _fix_sublime_paths(self, data):
        fixed_paths = []
        for path in data['source_paths']:
            # TODO - fix, using only posix paths
            fixed_paths.append(path.replace('\\', '/'))
        data['source_paths'] = fixed_paths

    def export_project(self):
        """ Processes misc options specific for GCC ARM, and run generator. """
        output = copy.deepcopy(self.generated_project)
        self.process_data_for_makefile(self.workspace)
        self._fix_sublime_paths(self.workspace)
        self.workspace['linker_options'] =[]

        output['path'], output['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', self.workspace, 'Makefile', self.workspace['output_dir']['path'])

        self.workspace['buildsys_name'] = 'Make'
        self.workspace['buildsys_cmd'] = 'make all'

        path, output['files']['sublimetext'] = self.gen_file_jinja(
            'sublimetext.sublime-project.tmpl', self.workspace, '%s.sublime-project' % self.workspace['name'], self.workspace['output_dir']['path'])
        generated_projects = output
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['sublimetext'], self.workspace['files']['makefile']]}

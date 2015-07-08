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

from .gccarm import MakefileGccArm


class SublimeTextMakeGccARM(MakefileGccArm):

    def __init__(self, workspace, env_settings):
        super(SublimeTextMakeGccARM, self).__init__(workspace, env_settings)

    def _fix_sublime_paths(self, data):
        fixed_paths = []
        for path in data['source_paths']:
            # TODO - fix, using only posix paths
            fixed_paths.append(path.replace('\\', '/'))
        data['source_paths'] = fixed_paths

    def export_project(self):
        """ Processes misc options specific for GCC ARM, and run generator. """
        for project in self.workspace['projects']:
            self.process_data_for_makefile(project, "sublime_make_gcc_arm")
            self._fix_sublime_paths(project)
            project['linker_options'] =[]

            project_path, makefile = self.gen_file_jinja('makefile_gcc.tmpl', project, 'Makefile', project['output_dir']['path'])

            project['buildsys_name'] = 'Make'
            project['buildsys_cmd'] = 'make all'

            sublimeproject = self.gen_file_jinja(
                'sublimetext.sublime-project.tmpl', project, '%s.sublime-project' % project['name'], project['output_dir']['path'])

        return project_path, [makefile, sublimeproject]

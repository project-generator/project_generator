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

from os.path import basename, normpath, join

from .gccarm import MakefileGccArmExporter
from .exporter import Exporter
from ..targets import Targets

class SublimeTextMakeGccARMExporter(MakefileGccArmExporter):

    def fix_sublime_paths(self, data):
        fixed_paths = []
        for path in data['source_paths']:
            # TODO - fix, using only posix paths
            fixed_paths.append(path.replace('\\', '/'))
        data['source_paths'] = fixed_paths

    def generate(self, data, env_settings):
        """ Processes misc options specific for GCC ARM, and run generator. """
        self.process_data_for_makefile(data, env_settings, "sublime_make_gcc_arm")
        self.fix_sublime_paths(data)
        data['linker_options'] =[]

        project_path, makefile = self.gen_file('makefile_gcc.tmpl', data, 'Makefile',
            data['dest_path'])

        data['buildsys_name'] = 'Make'
        data['buildsys_cmd'] = 'make all'

        sublimeproject = self.gen_file('sublimetext.sublime-project.tmpl', data,
            '%s.sublime-project' % data['name'], data['dest_path'])

        return project_path, [makefile, sublimeproject]

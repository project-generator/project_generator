# Copyright 2014-2015 sg-
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

from os.path import basename, relpath, join

from .gccarm import MakefileGccArmExporter
from .exporter import Exporter
from ..targets import Targets

class SublimeTextExporter(MakefileGccArmExporter):

    def generate(self, data, env_settings):
        """ Processes misc options specific for GCC ARM, and run generator. """
        self.process_data_for_makefile(data, env_settings)

        data['linker_options'] =[]

        project_path, makefile = self.gen_file('makefile_gcc.tmpl', data, 'Makefile', "sublime_gcc_arm", data[
            'project_dir']['path'], data['project_dir']['name'])

        sublimeproject = self.gen_file('sublimetext.sublime-project.tmpl', data, '%s.sublime-project' % data['name'], "sublime_gcc_arm", data[
            'project_dir']['path'], data['project_dir']['name'])

        return project_path, [makefile, sublimeproject]


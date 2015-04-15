# Copyright 2014-2015 0xc0170
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

from os.path import basename, relpath, join, normpath

from .exporter import Exporter
from ..targets import Targets

class MakefileGccArmExporter(Exporter):

    optimization_options = ['O0', 'O1', 'O2', 'O3', 'Os']

    def list_files(self, data, attribute, rel_path):
        """ Creates a list of all files based on the attribute. """
        file_list = []
        for groups in data[attribute]:
            try:
                for k, v in groups.items():
                    for file in v:
                        file_list.append(join(rel_path, normpath(file)))
            except:
                continue
        data[attribute] = file_list

    def libraries(self, key, value, data):
        """ Add defined GCC libraries. """
        for option in value:
            if key == "libraries":
                data['source_files_lib'].append(option)

    def compiler_options(self, key, value, data):
        """ Compiler flags """
        for option in value:
            if key == "compiler_options":
                data['compiler_options'].append(option)

    def linker_options(self, key, value, data):
        """ Linker flags """
        for option in value:
            if key == "linker_options":
                data['linker_options'].append(option)

    def optimization(self, key, value, data):
        """ Optimization setting. """
        for option in value:
            if option in self.optimization_options:
                data['optimization_level'] = option

    def cc_standard(self, key, value, data):
        """ C++ Standard """
        if key == "cc_standard":
            data['cc_standard'] = value

    def c_standard(self, key, value, data):
        """ C Standard """
        if key == "c_standard":
            data['c_standard'] = value

    def parse_specific_options(self, data):
        """ Parse all uvision specific setttings. """
        data['compiler_options'] = []
        for dic in data['misc']:
            for k, v in dic.items():
                self.libraries(k, v, data)
                self.compiler_options(k, v, data)
                self.optimization(k, v, data)
                self.cc_standard(k, v, data)
                self.c_standard(k, v, data)

        data['linker_options'] = []
        for dic in data['misc']:
            for k, v in dic.items():
                self.linker_options(k, v, data)

    def fix_paths(self, data, name):
        # get relative path and fix all paths within a project
        data.update(self.get_dest_path(data, name, data['project_dir']['path'], data['project_dir']['name']))
        fixed_paths = []
        for path in data['include_paths']:
            fixed_paths.append(join(data['rel_path'], normpath(path)))
        data['include_paths'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_lib']:
            fixed_paths.append(join(data['rel_path'], normpath(path)))
        data['source_files_lib'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_obj']:
            fixed_paths.append(join(data['rel_path'], normpath(path)))
        data['source_files_obj'] = fixed_paths
        fixed_paths = []
        for path in data['source_paths']:
            fixed_paths.append(join(data['rel_path'], normpath(path)))
        data['source_paths'] = fixed_paths
        if data['linker_file']:
            data['linker_file'] = join(data['rel_path'], normpath(data['linker_file']))

    def generate(self, data, env_settings):
        """ Processes misc options specific for GCC ARM, and run generator. """
        self.process_data_for_makefile(data, env_settings, "make_gcc_arm")
        project_path, makefile = self.gen_file('makefile_gcc.tmpl', data, 'Makefile', data['dest_path'])
        return project_path, [makefile]

    def process_data_for_makefile(self, data, env_settings, name):
        self.fix_paths(data, name)
        self.list_files(data, 'source_files_c', data['rel_path'])
        self.list_files(data, 'source_files_cpp', data['rel_path'])
        self.list_files(data, 'source_files_s', data['rel_path'])

        self.parse_specific_options(data)
        data['toolchain'] = 'arm-none-eabi-'
        data['toolchain_bin_path'] = env_settings.get_env_settings('gcc')

        target = Targets(env_settings.get_env_settings('definitions'))

        if target.get_mcu_core(data['target']):
            data['core'] = target.get_mcu_core(data['target'])[0]
        else:
            raise RuntimeError(
                "Target: %s not found, Please add them to https://github.com/0xc0170/project_generator_definitions" % data['target'].lower())

        # gcc arm is funny about cortex-m4f.
        if data['core'] == 'cortex-m4f':
            data['core'] = 'cortex-m4'

        # change cortex-m0+ to cortex-m0plus
        if data['core'] == 'cortex-m0+':
            data['core'] = 'cortex-m0plus'

        # set default values
        if 'optimization_level' not in data:
            data['optimization_level'] = self.optimization_options[0]

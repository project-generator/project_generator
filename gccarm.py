# Copyright 2014 0xc0170
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
from os.path import basename
from export_generator import Exporter

class GccArm(Exporter):
    optimization_options = ['O0', 'O1', 'O2', 'O3', 'Os']

    def list_files(self, data, attribute):
        """ Creates a list of all files based on the attribute. """
        file_list = []
        for groups in data[attribute]:
            try:
                for k,v in groups.items():
                    for file in v:
                        file_list.append(file)
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

    def parse_specific_options(self, data):
        """ Parse all uvision specific setttings. """
        data['compiler_options'] = []
        for dic in data['misc']:
            for k,v in dic.items():
                self.libraries(k, v, data)
                self.compiler_options(k, v, data)
                self.optimization(k, v, data)

    def generate(self, data, ide):
        """ Processes misc options specific for GCC ARM, and run generator. """
        self.list_files(data, 'source_files_c')
        self.list_files(data, 'source_files_cpp')
        self.list_files(data, 'source_files_s')

        self.parse_specific_options(data)

        self.gen_file('gcc_arm.tmpl', data, 'Makefile', ide)

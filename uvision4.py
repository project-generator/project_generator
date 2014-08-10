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


class Uvision4(Exporter):
    NAME = 'uVision4'

    optimization_options = ['O0', 'O1', 'O2', 'O3']
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']

    def __init__(self):
        self.data = []

    def expand_data(self, old_data, new_data, attribute, group):
        # data expansion - uvision needs filename and path separately
        # if group == None:
        #     group = attribute

        new_data['groups'][group][attribute] = []
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_file = {"path" : file, "name" : basename(file)}
                new_data['groups'][group][attribute].append(new_file)

    def iterate(self, data, expanded_data):
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group)

    def parse_specific_options(self, data):
        for dic in data['misc']:
            for k,v in dic.items():
                self.optimization(k,v,data)
                self.c_misc(k,v,data)
                self.one_elf_per_fun(k,v,data)

    def optimization(self, key, value, data):
        for option in value:
            if option in self.optimization_options:
                data['optimization_level'] = int(option[1]) + 1

    def c_misc(self, key,value, data):
        if key == 'c_command_line':
            data['c_command_line'] = value

    def one_elf_per_fun(self, key, value, data):
        for option in value:
            if option == 'one_elf_per_function':
                data['one_elf_per_function'] = 1

    def get_groups(self, data):
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        k = 'Sources'
                    if k not in groups:
                        groups.append(k)
        return groups

    def generate(self, data, ide):
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = {}
        self.iterate(data, expanded_dic)

        self.parse_specific_options(expanded_dic)

        # Project file
        self.gen_file('uvision4_%s.uvproj.tmpl' % data['mcu'], expanded_dic, '%s.uvproj' % data['name'], ide)
        self.gen_file('uvision4_%s.uvopt.tmpl' % data['mcu'], expanded_dic, '%s.uvopt' % data['name'], ide)

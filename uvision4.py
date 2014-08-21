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
    optimization_options = ['O0', 'O1', 'O2', 'O3']
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 8, 'c' : 1, 's' : 2 ,'obj' : 3, 'lib' : 4}

    def __init__(self):
        self.data = []

    def expand_data(self, old_data, new_data, attribute, group):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {"path" : file, "name" : basename(file), "filetype" : self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def iterate(self, data, expanded_data):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group)

    def parse_specific_options(self, data):
        """ Parse all uvision specific setttings. """
        for dic in data['misc']:
            for k,v in dic.items():
                self.optimization(k,v,data)
                self.c_misc(k,v,data)
                self.one_elf_per_fun(k,v,data)
                self.c99mode(k,v,data)

    def optimization(self, key, value, data):
        """ Optimization setting. """
        for option in value:
            if option in self.optimization_options:
                data['optimization_level'] = int(option[1]) + 1

    def c_misc(self, key,value, data):
        """ Command line commands. """
        if key == 'c_command_line':
            data['c_command_line'] = value

    def one_elf_per_fun(self, key, value, data):
        """ Checkbox - One Elf Per Function. """
        for option in value:
            if option == 'one_elf_per_function':
                data['one_elf_per_function'] = 1

    def c99mode(self, key, value, data):
        """ Checkbox - C99 ."""
        for option in value:
            if option == 'c99':
                data['c99'] = 1

    def get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                if dic:
                    for k,v in dic.items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def generate(self, data, ide):
        """ Processes groups and misc options specific for uVision, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)

        self.parse_specific_options(expanded_dic)

        # Project file
        self.gen_file('uvision4.uvproj.tmpl', expanded_dic, '%s.uvproj' % data['name'], ide)
        self.gen_file('uvision4.uvopt.tmpl', expanded_dic, '%s.uvopt' % data['name'], ide)

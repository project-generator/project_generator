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
from export_generator import Exporter

class IAR(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']
    core_dic = {
        "cortex-m0" : 34,
        "cortex-m0+" : 35,
        "cortex-m3" : 38,
        "cortex-m4" : 39,
        "cortex-m4f" : 40,
    }

    def __init__(self):
        self.data = []

    def expand_data(self, old_data, new_data, attribute, group):
        # data expansion - uvision needs filename and path separately
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_data['groups'][group].append(file)

    def iterate(self, data, expanded_data):
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group)

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

    def find_target_core(self, data):
        for k,v in self.core_dic.items():
            if k == data['core']:
                return v
        return core_dic['cortex-m0'] #def cortex-m0 if not defined otherwise

    def generate(self, data, ide):
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)
        expanded_dic['target_core'] = self.find_target_core(expanded_dic)

        self.gen_file('iar.ewp.tmpl' , expanded_dic, '%s.ewp' % data['name'], ide)
        self.gen_file('iar.eww.tmpl' , expanded_dic, '%s.eww' % data['name'], ide)


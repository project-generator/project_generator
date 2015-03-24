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

import copy

from os.path import basename, join, relpath

from .exporter import Exporter
from .coide_definitions import CoIDEdefinitions
from ..targets import Targets

class CoideExporter(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1}

    def __init__(self):
        self.definitions = CoIDEdefinitions()

    def expand_data(self, old_data, new_data, attribute, group):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {"path": file, "name": basename(
                    file), "type": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                if dic:
                    for k, v in dic.items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def iterate(self, data, expanded_data):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k, v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group)

    def parse_specific_options(self, data):
        """ Parse all CoIDE specific setttings. """
        data['coide_settings'].update(copy.deepcopy(
            self.definitions.coide_settings))  # set specific options to default values
        for dic in data['misc']:
            for k, v in dic.items():
                for option in v:
                    data['coide_settings'][k][option] = v[option]

    def normalize_mcu_def(self, mcu_def):
        for k,v in mcu_def['Device'].items():
            mcu_def['Device'][k] = v[0]
        for k,v in mcu_def['DebugOption'].items():
            mcu_def['DebugOption'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IROM1'].items():
            mcu_def['MemoryAreas']['IROM1'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IROM2'].items():
            mcu_def['MemoryAreas']['IROM2'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IRAM1'].items():
            mcu_def['MemoryAreas']['IRAM1'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IRAM2'].items():
            mcu_def['MemoryAreas']['IRAM2'][k] = v[0]

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for CoIDE, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)

        expanded_dic['coide_settings'] = {}
        self.parse_specific_options(expanded_dic)

        target = Targets(env_settings.get_env_settings('definitions'))
        mcu_def_dic = target.get_tool_def(expanded_dic['target'], 'coide')
        if not mcu_def_dic:
             raise RuntimeError("Mcu definitions were not found for %s" % expanded_dic['target'])
        self.normalize_mcu_def(mcu_def_dic)
        expanded_dic['coide_settings'].update(mcu_def_dic)

        # Project file
        project_path, projfile = self.gen_file(
            'coide.coproj.tmpl', expanded_dic, '%s.coproj' % data['name'], "coide", data['project_dir']['path'], data['project_dir']['name'])
        return project_path, [projfile]

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
from iar_mcu_definitions import get_mcu_definition

class IAR(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']
    core_dic = {
        "cortex-m0" : 34,
        "cortex-m0+" : 35,
        "cortex-m3" : 38,
        "cortex-m4" : 39,
        "cortex-m4f" : 40,
    }

    iar_settings = {
        'GEndianMode' : {
            'state' : 0,
        },
        'Input variant' : {
            'version' : 0,
            'state' : 0,
        },
        'Output variant' : {
            'state' : 0,
        },
        'GOutputBinary' : {
            'state' : 0,
        },
        'FPU' : {
            'version' : 2,
            'state' : 0,
        },
        'OGCoreOrChip' : {
            'state' : 0,
        },
        'GRuntimeLibSelect' : {
            'version' : 0,
            'state' : 0,
        },
        'GRuntimeLibSelectSlave' : {
            'version' : 0,
            'state' : 0,
        },
        'GeneralEnableMisra' : {
            'state' : 0,
        },
        'GeneralMisraVerbose' : {
            'state' : 0,
        },
        'OGChipSelectEditMenu' : {
            'state' : 0,
        },
        'GenLowLevelInterface' : {
            'state' : 0,
        },
        'GEndianModeBE' : {
            'state' : 0,
        },
        'OGBufferedTerminalOutput' : {
            'state' : 0,
        },
        'GenStdoutInterface' : {
            'state' : 0,
        },
        'GeneralMisraVer' : {
            'state' : 0,
        },
        'GFPUCoreSlave' : {
            'state' : 0,
        },
        'GBECoreSlave' : {
            'state' : 0,
        },
        'OGUseCmsis' : {
            'state' : 0,
        },
        'OGUseCmsisDspLib' : {
            'state' : 0,
        },
    }

    def expand_data(self, old_data, new_data, attribute, group):
        """ Groups expansion for Sources. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_data['groups'][group].append(file)

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

    def get_groups(self, data):
        """ Get all groups defined. """
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
        """ Sets Target core. """
        for k,v in self.core_dic.items():
            if k == data['core']:
                return v
        return core_dic['cortex-m0'] #def cortex-m0 if not defined otherwise

    def generate(self, data, ide):
        """ Processes groups and misc options specific for IAR, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)
        # expanded_dic['target_core'] = self.find_target_core(expanded_dic)
        expanded_dic['iar_settings'] = {}
        expanded_dic['iar_settings'].update(get_mcu_definition(expanded_dic['mcu']))

        self.gen_file('iar.ewp.tmpl' , expanded_dic, '%s.ewp' % data['name'], ide)
        self.gen_file('iar.eww.tmpl' , expanded_dic, '%s.eww' % data['name'], ide)


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

    uvision_settings = {
        # C/C++ settings
        'Cads' : {
            'interw' : 0,
            'Optim' : 0,
            'oTime' : 0,
            'SplitLS' : 0,
            'OneElfS' : 0,
            'Strict' : 0,
            'EnumInt' : 0,
            'PlainCh' : 0,
            'Ropi' : 0,
            'Rwpi' : 0,
            'wLevel' : 0,
            'uThumb' : 0,
            'uSurpInc' : 0,
            'uC99' : 0,
            'MiscControls': [],
        },

        # Linker settings
        'LDads' : {
           'umfTarg' : 0,
           'Ropi' : 0,
           'Rwpi' : 0,
           'noStLib' : 0,
           'RepFail' : 0,
           'useFile' : 0,
           'TextAddressRange' : 0,
           'DataAddressRange' : 0,
           'IncludeLibs' : 0,
           'IncludeLibsPath' : 0,
           'Misc' : 0,
           'LinkerInputFile' : 0,
           'DisabledWarnings' : [],
        },

        # Assembly settings
        'Aads' : {
            'interw' : 0,
            'Ropi' : 0,
            'Rwpi' : 0,
            'thumb' : 0,
            'SplitLS' : 0,
            'SwStkChk' : 0,
            'NoWarn' : 0,
            'uSurpInc' : 0,
            'VariousControls' : 0,
            'MiscControls' : 0,
            'Define' : [],
            'Undefine' : 0,
            'IncludePath' : [],
            'VariousControls' : 0,
        },

        # User settings
        'TargetOption' : {
            'CreateExecutable' : 0,
            'CreateLib' : 0,
            'CreateHexFile' : 0,
            'DebugInformation' : 0,
            'BrowseInformation' : 0,
            'CreateBatchFile' : 0,
            'BeforeCompile' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            },
            'BeforeMake' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            },
            'AfterMake' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            }
        },

        # Target settings
        'ArmAdsMisc' : {
            'useUlib' : 0,
            'NoZi1' : 0,
            'NoZi2' : 0,
            'NoZi3' : 0,
            'NoZi4' : 0,
            'NoZi5' : 0,
            'OCR_RVCT1' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT2' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT3' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT4' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT5' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT6' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT7' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT8' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT9' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT10' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            }
            
        }
    }

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
                if k == 'ArmAdsMisc':
                    self.set_target_options(v, data, k)
                elif k == 'TargetOption':
                    self.set_user_options(v, data, k)
                else:
                    self.set_specific_settings(v, data, k)

    def set_specific_settings(self, value_list, data, uvision_dic):
        data[uvision_dic] = self.uvision_settings[uvision_dic]
        for option in value_list:
            if value_list[option][0] == 'enable':
                value_list[option] = 1
            elif value_list[option][0] == 'disable':
                value_list[option] = 0
            data[uvision_dic][option] = value_list[option]

    def set_target_options(self, value_list, data, uvision_dic):
        data[uvision_dic] = self.uvision_settings[uvision_dic]
        for option in value_list:
            if option.startswith('OCR_'):
                for k,v in value_list[option].items():
                    if v[0] == 'enable':
                        value_list[option][k] = 1
                    elif v[0] == 'disable':
                        value_list[option][k] = 0
                    data[uvision_dic][option][k] = value_list[option][k]
            else:
                if value_list[option][0] == 'enable':
                    value_list[option] = 1
                elif value_list[option][0] == 'disable':
                    value_list[option] = 0
                data[uvision_dic][option] = value_list[option]

    def set_user_options(self, value_list, data, uvision_dic):
        data[uvision_dic] = self.uvision_settings[uvision_dic]
        for option in value_list:
            if option.startswith('Before'):
                for k,v in value_list[option].items():
                    if v[0] == 'enable':
                        value_list[option][k] = 1
                    elif v[0] == 'disable':
                        value_list[option][k] = 0
                    data[uvision_dic][option][k] = value_list[option][k]
            else:
                if value_list[option][0] == 'enable':
                    value_list[option] = 1
                elif value_list[option][0] == 'disable':
                    value_list[option] = 0
                data[uvision_dic][option] = value_list[option]

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

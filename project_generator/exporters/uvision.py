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
import shutil

from os.path import basename, join, relpath

# from . import board_definitions

from .exporter import Exporter
from .uvision_definitions import uVisionDefinitions
from ..targets import Targets

class UvisionExporter(Exporter):
    optimization_options = ['O0', 'O1', 'O2', 'O3']
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 8, 'c': 1, 's': 2, 'obj': 3, 'lib': 4}

    def __init__(self):
        self.definitions = uVisionDefinitions()

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
                    file), "filetype": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

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
        """ Parse all uvision specific setttings. """
        default_set = copy.deepcopy(self.definitions.uvision_settings)
        data.update(default_set)  # set specific options to default values
        for dic in data['misc']:
            for k, v in dic.items():
                if k == 'ArmAdsMisc':
                    self.set_target_options(v, data, k)
                elif k == 'TargetOption':
                    self.set_user_options(v, data, k)
                elif k == 'DebugOption':
                    raise RuntimeError("Option not supported yet.")
                elif k == 'Utilities':
                    raise RuntimeError("Option not supported yet.")
                else:
                    self.set_specific_settings(v, data, k)

    def set_specific_settings(self, value_list, data, uvision_dic):
        for option in value_list:
            if value_list[option][0] == 'enable':
                value_list[option] = 1
            elif value_list[option][0] == 'disable':
                value_list[option] = 0
            data[uvision_dic][option] = value_list[option]

    def set_target_options(self, value_list, data, uvision_dic):
        for option in value_list:
            if option.startswith('OCR_'):
                for k, v in value_list[option].items():
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
        for option in value_list:
            if option.startswith('Before') or option.startswith('After'):
                for k, v in value_list[option].items():
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
                    for k, v in dic.items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def append_mcu_def(self, data, mcu_def):
        """ Get MCU definitons as Flash algo, RAM, ROM size , etc. """
        try:
            data['TargetOption'].update(mcu_def['TargetOption'])
        except KeyError:
            # does not exist, create it
            data['TargetOption'] = mcu_def['TargetOption']

    def normalize_mcu_def(self, mcu_def):
        for k,v in mcu_def['TargetOption'].items():
            mcu_def['TargetOption'][k] = v[0]

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for uVision, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)

        self.parse_specific_options(expanded_dic)

        target = Targets(env_settings.get_env_settings('definitions'))

        mcu_def_dic = target.get_tool_def(expanded_dic['target'], 'uvision')
        if not mcu_def_dic:
             raise RuntimeError("Mcu definitions were not found for %s" % expanded_dic['target'])
        self.normalize_mcu_def(mcu_def_dic)
        self.append_mcu_def(expanded_dic, mcu_def_dic)

        # set default build directory if unset
        if not 'output_dir' in expanded_dic:
            expanded_dic['output_dir'] = '.\\build\\' + data['name'] + '\\'

        # optimization set to correct value, default not used
        expanded_dic['Cads']['Optim'][0] += 1

        # Project file
        project_path, projfile = self.gen_file(
            'uvision4.uvproj.tmpl', expanded_dic, '%s.uvproj' % data['name'], "uvision", data['project_dir']['path'], data['project_dir']['name'])
        project_path, optfile = self.gen_file(
            'uvision4.uvopt.tmpl', expanded_dic, '%s.uvopt' % data['name'], "uvision", data['project_dir']['path'], data['project_dir']['name'])
        return project_path, [projfile, optfile]

    def fixup_executable(self, exe_path):
        new_exe_path = exe_path + '.axf'
        shutil.copy(exe_path, new_exe_path)
        return new_exe_path

    def supports_target(self, target):
        return target in self.definitions.mcu_def

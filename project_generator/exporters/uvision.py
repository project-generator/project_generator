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

import copy
import shutil
import logging

from os.path import basename, join, relpath, normpath
from os import getcwd
import xmltodict

from .exporter import Exporter
from .uvision_definitions import uVisionDefinitions
from ..targets import Targets
from ..utils import xmldict

class UvisionExporter(Exporter):
    optimization_options = ['O0', 'O1', 'O2', 'O3']
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp','source_files_lib','source_files_obj']
    file_types = {'cpp': 8, 'c': 1, 's': 2, 'obj': 3,'o':3, 'lib': 4, 'ar': 4}

    def __init__(self):
        self.definitions = uVisionDefinitions()

    def expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {"FilePath": rel_path + normpath(file), "FileName": basename(
                    file), "FileType": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k, v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group, rel_path)

    # def parse_specific_options(self, data):
    #     """ Parse all uvision specific setttings. """
    #     default_set = copy.deepcopy(self.definitions.uvision_settings)
    #     data['uvision_settings'].update(default_set)  # set specific options to default values
    #     for dic in data['misc']:
    #         for k, v in dic.items():
    #             if k == 'ArmAdsMisc':
    #                 self.set_target_options(v, data, k)
    #             elif k == 'TargetOption':
    #                 self.set_user_options(v, data, k)
    #             elif k == 'DebugOption':
    #                 # TODO implement
    #                 raise RuntimeError("Option not supported yet.")
    #             elif k == 'Utilities':
    #                 # TODO implement
    #                 raise RuntimeError("Option not supported yet.")
    #             else:
    #                 self.set_specific_settings(v, data, k)

    # def set_specific_settings(self, value_list, data, uvision_dic):
    #     for option in value_list:
    #         if value_list[option][0] == 'enable':
    #             value_list[option] = 1
    #         elif value_list[option][0] == 'disable':
    #             value_list[option] = 0
    #         data['uvision_settings'][uvision_dic][option] = value_list[option]

    # def set_target_options(self, value_list, data, uvision_dic):
    #     for option in value_list:
    #         if option.startswith('OCR_'):
    #             for k, v in value_list[option].items():
    #                 if v[0] == 'enable':
    #                     value_list[option][k] = 1
    #                 elif v[0] == 'disable':
    #                     value_list[option][k] = 0
    #                 data[uvision_dic][option][k] = value_list[option][k]
    #         else:
    #             if value_list[option][0] == 'enable':
    #                 value_list[option] = 1
    #             elif value_list[option][0] == 'disable':
    #                 value_list[option] = 0
    #             data[uvision_dic][option] = value_list[option]

    # def set_user_options(self, value_list, data, uvision_dic):
    #     for option in value_list:
    #         if option.startswith('Before') or option.startswith('After'):
    #             for k, v in value_list[option].items():
    #                 if v[0] == 'enable':
    #                     value_list[option][k] = 1
    #                 elif v[0] == 'disable':
    #                     value_list[option][k] = 0
    #                 try:
    #                     data[uvision_dic][option][k] = value_list[option][k]
    #                 except KeyError:
    #                     logging.info("Tool specific option: %s not recognized" % uvision_dic)
    #         else:
    #             if value_list[option][0] == 'enable':
    #                 value_list[option] = 1
    #             elif value_list[option][0] == 'disable':
    #                 value_list[option] = 0
    #             data[uvision_dic][option] = value_list[option]

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
            data['uvision_settings'].update(mcu_def['TargetOption'])
        except KeyError:
            # does not exist, create it
            data['uvision_settings'] = mcu_def['TargetOption']

    def normalize_mcu_def(self, mcu_def):
        for k,v in mcu_def['TargetOption'].items():
            mcu_def['TargetOption'][k] = v[0]

    def fix_paths(self, data, rel_path):
        data['includes'] = [join(rel_path, normpath(path)) for path in data['includes']]

        if type(data['source_files_lib'][0]) == type(dict()):
            for k in data['source_files_lib'][0].keys():
                data['source_files_lib'][0][k] = [join(rel_path,normpath(path)) for path in data['source_files_lib'][0][k]]
        else:
            data['source_files_lib'][0] = [join(rel_path,normpath(path)) for path in data['source_files_lib'][0]]

        if type(data['source_files_obj'][0]) == type(dict()):
            for k in data['source_files_obj'][0].keys():
                data['source_files_obj'][0][k] = [join(rel_path,normpath(path)) for path in data['source_files_obj'][0][k]]
        else:
            data['source_files_obj'][0] = [join(rel_path,normpath(path)) for path in data['source_files_obj'][0]]

        if data['linker_file']:
            data['linker_file'] = join(rel_path, normpath(data['linker_file']))

    def _uvproj_clean_xmldict(self, uvproj_dic):
        for k,v in uvproj_dic.items():
            if v is None:
                uvproj_dic[k] = ''

    def _uvproj_set_CommonProperty(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_set_DebugOption(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_set_DllOption(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_set_TargetArmAds(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic['Aads'])
        self._uvproj_clean_xmldict(uvproj_dic['ArmAdsMisc'])
        self._uvproj_clean_xmldict(uvproj_dic['Cads'])
        self._uvproj_clean_xmldict(uvproj_dic['LDads'])
        uvproj_dic['LDads']['ScatterFile'] = project_dic['linker_file']

        uvproj_dic['Cads']['VariousControls']['IncludePath'] = ';'.join(project_dic['includes']).encode('utf-8')
        uvproj_dic['Cads']['VariousControls']['Define'] = ';'.join(project_dic['macros']).encode('utf-8')
        uvproj_dic['Aads']['VariousControls']['Define'] = ','.join(project_dic['macros']).encode('utf-8')


    def _uvproj_set_TargetCommonOption(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)
        uvproj_dic['OutputDirectory'] = project_dic['output_dir']
        uvproj_dic['OutputName'] = project_dic['name']
        uvproj_dic['CreateExecutable'] = 1 if project_dic['output_type'] == 'exe' else 0
        uvproj_dic['CreateLib'] = 1 if project_dic['output_type'] == 'lib' else 0

    def _uvproj_set_Utilities(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_files_set(self, uvproj_dic, project_dic):
        uvproj_dic['Project']['Targets']['Target']['Groups'] = {}
        uvproj_dic['Project']['Targets']['Target']['Groups']['Group'] = []
        i = 0
        for group_name, files in project_dic['groups'].items():
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'].append({'GroupName' : group_name})
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files'] = []
            for file in files:
                uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files'].append(file)
            i = i + 1

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for uVision, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []


        # get relative path and fix all paths within a project
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        expanded_dic['build_dir'] = '.\\' + expanded_dic['build_dir'] + '\\'

        # generic tool template specified or project
        if expanded_dic['template']:
            project_file = join(getcwd(), expanded_dic['template'][0]) #TODO 0xc0170: template list !
            uvproj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        elif 'uvision' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            project_file = join(getcwd(), env_settings.templates['uvision']['path'][0], env_settings.templates['uvision']['name'][0] + '.ewp')
            uvproj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        else:
            uvproj_dic = self.definitions.uvproj_file

        # TODO 0xc0170: support uvopt parsing
        uvopt_dic = self.definitions.uvopt_file
        uvopt_dic['ProjectOpt']['Target']['TargetName'] = expanded_dic['name']

        self._uvproj_files_set(uvproj_dic, expanded_dic)
        self._uvproj_set_CommonProperty(uvproj_dic['Project']['Targets']['Target']['TargetOption']['CommonProperty'], expanded_dic)
        self._uvproj_set_DebugOption(uvproj_dic['Project']['Targets']['Target']['TargetOption']['CommonProperty'], expanded_dic)
        self._uvproj_set_DllOption(uvproj_dic['Project']['Targets']['Target']['TargetOption']['DllOption'], expanded_dic)
        self._uvproj_set_TargetArmAds(uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetArmAds'], expanded_dic)
        self._uvproj_set_TargetCommonOption(uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption'], expanded_dic)
        self._uvproj_set_Utilities(uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities'], expanded_dic)

        target = Targets(env_settings.get_env_settings('definitions'))
        if not target.is_supported(expanded_dic['target'].lower(), 'uvision'):
            raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
        mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'uvision')
        if not mcu_def_dic:
             raise RuntimeError(
                "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                % expanded_dic['target'].lower())
        # self.normalize_mcu_def(mcu_def_dic)
        logging.debug("Mcu definitions: %s" % mcu_def_dic)
        # self.append_mcu_def(expanded_dic, mcu_def_dic)

        # load debugger
        if expanded_dic['debugger']:
            try:
                expanded_dic['uvision_settings']['TargetDlls']['Driver'] = self.definitions.debuggers[expanded_dic['debugger']]['TargetDlls']['Driver']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # if there's template parse + use it
        # TODO add project, which would overwrite parents template
        if 'uvision' in env_settings.templates.keys():
            project_file = join(getcwd(), env_settings.templates['uvision']['path'][0], env_settings.templates['uvision']['name'][0] + '.uvproj')
            proj_dic = xmltodict.parse(file(project_file))
            TargetOption = proj_dic['Project']['Targets']['Target']['TargetOption']
            # we need to inject only attributes we know are relevant (not overwrite mcu for example)
            expanded_dic['uvision_settings']['CommonProperty'] = TargetOption['CommonProperty']
            # fix default dic is wronG !
            expanded_dic['uvision_settings']['BeforeCompile'] = TargetOption['TargetCommonOption']['BeforeCompile']
            expanded_dic['uvision_settings']['BeforeMake'] = TargetOption['TargetCommonOption']['BeforeMake']
            expanded_dic['uvision_settings']['AfterMake'] = TargetOption['TargetCommonOption']['AfterMake']
            expanded_dic['uvision_settings']['Cads'] = TargetOption['TargetArmAds']['Cads']
        else:
            # optimization set to correct value, default not used
            expanded_dic['uvision_settings']['Cads']['Optim'][0] += 1

        # Project file
        uvproj_xml = xmldict.dict2xml(uvproj_dic)
        project_path, projfile = self.gen_file(
            uvproj_xml.prettyxml(), expanded_dic, '%s.uvproj' % data['name'], expanded_dic['output_dir']['path'])

        uvopt_xml = xmldict.dict2xml(uvopt_dic)
        project_path, optfile = self.gen_file(
            uvopt_xml.prettyxml(), expanded_dic, '%s.uvopt' % data['name'], expanded_dic['output_dir']['path'])
        return project_path, [projfile, optfile]

    def fixup_executable(self, exe_path):
        new_exe_path = exe_path + '.axf'
        shutil.copy(exe_path, new_exe_path)
        return new_exe_path

    def supports_target(self, target):
        return target in self.definitions.mcu_def

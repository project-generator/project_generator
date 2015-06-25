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
from collections import OrderedDict

from .exporter import Exporter
from .uvision_definitions import uVisionDefinitions
from ..targets import Targets

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
        self._uvproj_clean_xmldict(uvproj_dic['SimDlls'])
        self._uvproj_clean_xmldict(uvproj_dic['Simulator'])
        self._uvproj_clean_xmldict(uvproj_dic['Target'])
        self._uvproj_clean_xmldict(uvproj_dic['TargetDlls'])

    def _uvproj_set_DllOption(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_set_TargetArmAds(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic['Aads'])
        self._uvproj_clean_xmldict(uvproj_dic['Aads']['VariousControls'])
        self._uvproj_clean_xmldict(uvproj_dic['ArmAdsMisc'])
        self._uvproj_clean_xmldict(uvproj_dic['Cads'])
        self._uvproj_clean_xmldict(uvproj_dic['Cads']['VariousControls'])
        self._uvproj_clean_xmldict(uvproj_dic['LDads'])
        uvproj_dic['LDads']['ScatterFile'] = project_dic['linker_file']

        uvproj_dic['Cads']['VariousControls']['IncludePath'] = '; '.join(project_dic['includes']).encode('utf-8')
        uvproj_dic['Cads']['VariousControls']['Define'] = ', '.join(project_dic['macros']).encode('utf-8')
        uvproj_dic['Aads']['VariousControls']['Define'] = ', '.join(project_dic['macros']).encode('utf-8')


    def _uvproj_set_TargetCommonOption(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)
        self._uvproj_clean_xmldict(uvproj_dic['AfterMake'])
        self._uvproj_clean_xmldict(uvproj_dic['BeforeCompile'])
        self._uvproj_clean_xmldict(uvproj_dic['BeforeMake'])
        self._uvproj_clean_xmldict(uvproj_dic['TargetStatus'])
        uvproj_dic['OutputDirectory'] = project_dic['build_dir']
        uvproj_dic['OutputName'] = project_dic['name']
        uvproj_dic['CreateExecutable'] = 1 if project_dic['output_type'] == 'exe' else 0
        uvproj_dic['CreateLib'] = 1 if project_dic['output_type'] == 'lib' else 0

    def _uvproj_set_Utilities(self, uvproj_dic, project_dic):
        self._uvproj_clean_xmldict(uvproj_dic)

    def _uvproj_files_set(self, uvproj_dic, project_dic):
        uvproj_dic['Project']['Targets']['Target']['Groups'] = OrderedDict()
        uvproj_dic['Project']['Targets']['Target']['Groups']['Group'] = []
        i = 0
        for group_name, files in project_dic['groups'].items():
            # Why OrderedDict() - uvision project requires an order. GroupName must be before Files,
            # otherwise it does not sense any file. Same applies for other attributes, like VariousControl.
            # Therefore be aware that order matters in this exporter
            group = OrderedDict()
            group['GroupName'] = group_name
            # group['Files'] = {}
            group['Files'] = {'File' : []}
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'].append(group)
            for file in files:
                uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files']['File'].append(file)
            i = i + 1

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for uVision, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []

        # TODO 0xc0170: fix misc , its a list with a dictionary
        if 'misc' in expanded_dic and bool(expanded_dic['misc'][0]):
            print "Using deprecated misc options for uvision. Please use template project files."

        # get relative path and fix all paths within a project
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        expanded_dic['build_dir'] = '.\\' + expanded_dic['build_dir'] + '\\'

        # generic tool template specified or project
        if expanded_dic['template']:
            project_file = join(getcwd(), expanded_dic['template'][0]) #TODO 0xc0170: template list !
            uvproj_dic = xmltodict.parse(file(project_file))
        elif 'uvision' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extensions for templates - support multiple files and get their extension
            # and check if user defined them correctly
            project_file = join(getcwd(), env_settings.templates['uvision'][0])
            uvproj_dic = xmltodict.parse(file(project_file))
        else:
            uvproj_dic = self.definitions.uvproj_file

        # TODO 0xc0170: support uvopt parsing
        uvopt_dic = self.definitions.uvopt_file
        uvopt_dic['ProjectOpt']['Target']['TargetName'] = expanded_dic['name']
        uvproj_dic['Project']['Targets']['Target']['TargetName'] = expanded_dic['name']

        self._uvproj_files_set(uvproj_dic, expanded_dic)
        self._uvproj_set_CommonProperty(uvproj_dic['Project']['Targets']['Target']['TargetOption']['CommonProperty'], expanded_dic)
        self._uvproj_set_DebugOption(uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption'], expanded_dic)
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
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Device'] = mcu_def_dic['TargetOption']['Device'][0]
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Vendor'] = mcu_def_dic['TargetOption']['Vendor'][0]
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Cpu'] = mcu_def_dic['TargetOption']['Cpu'][0].encode('utf-8')
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['DeviceId'] = mcu_def_dic['TargetOption']['DeviceId'][0]
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['FlashDriverDll'] = str(mcu_def_dic['TargetOption']['FlashDriverDll'][0]).encode('utf-8')
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile'] = mcu_def_dic['TargetOption']['SFDFile'][0]

        # load debugger
        if expanded_dic['debugger']:
            try:
                uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption']['TargetDlls']['Driver'] = self.definitions.debuggers[expanded_dic['debugger']]['TargetDlls']['Driver']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        uvproj_xml = xmltodict.unparse(uvproj_dic, pretty=True)
        project_path, projfile = self.gen_file_raw(
            uvproj_xml, '%s.uvproj' % data['name'], expanded_dic['output_dir']['path'])

        uvopt_xml = xmltodict.unparse(uvopt_dic, pretty=True)
        project_path, optfile = self.gen_file_raw(
            uvopt_xml, '%s.uvopt' % data['name'], expanded_dic['output_dir']['path'])
        return project_path, [projfile, optfile]

    def fixup_executable(self, exe_path):
        new_exe_path = exe_path + '.axf'
        shutil.copy(exe_path, new_exe_path)
        return new_exe_path

    def supports_target(self, target):
        return target in self.definitions.mcu_def

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

from os.path import basename, join, relpath, normpath
from os import getcwd

import copy
import logging
import xmltodict

from .exporter import Exporter
from .iar_definitions import IARDefinitions
from ..targets import Targets

class IAREWARMExporter(Exporter):

    def __init__(self):
        self.definitions = IARDefinitions()

    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj', 'source_files_lib']
    core_dic = {
        "cortex-m0": 34,
        "cortex-m0+": 35,
        "cortex-m3": 38,
        "cortex-m4": 39,
        "cortex-m4f": 40,
    }

    def expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ Groups expansion for Sources. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_data['groups'][group].append(join('$PROJ_DIR$', rel_path, normpath(file)))

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
                for k, v in dic.items():
                    if k == None:
                        k = 'Sources'
                    if k not in groups:
                        groups.append(k)
        return groups

    def find_target_core(self, data):
        """ Sets Target core. """
        for k, v in self.core_dic.items():
            if k == data['core']:
                return v
        return core_dic['cortex-m0']  # def cortex-m0 if not defined otherwise

    def parse_specific_options(self, data):
        """ Parse all IAR specific setttings. """
        data['iar_settings'].update(copy.deepcopy(
            self.definitions.iar_settings))  # set specific options to default values
        for dic in data['misc']:
            # for k,v in dic.items():
            self.set_specific_settings(dic, data)

    def set_specific_settings(self, value_list, data):
        for k, v in value_list.items():
            for option in v.items():
                for key,value in v['data']['option'].items():
                    result = 0
                    if value[0] == 'enable':
                        result = 1
                    data['iar_settings'][k]['data']['option'][key]['state'] = result

    def normalize_mcu_def(self, mcu_def):
        # hack to insert tab as IAR using tab for MCU definitions
        mcu_def['OGChipSelectEditMenu']['state'] = mcu_def['OGChipSelectEditMenu']['state'][0].replace(' ', '\t', 1)
        mcu_def['OGCoreOrChip']['state'] = mcu_def['OGCoreOrChip']['state'][0]

    def fix_paths(self, data, rel_path):
        data['includes'] = [join('$PROJ_DIR$', rel_path, normpath(path)) for path in data['includes']]

        for k in data['source_files_lib'][0].keys():
            data['source_files_lib'][0][k] = [join('$PROJ_DIR$',rel_path,normpath(path)) for path in data['source_files_lib'][0][k]]

        for k in data['source_files_obj'][0].keys():
            data['source_files_obj'][0][k] = [join('$PROJ_DIR$',rel_path,normpath(path)) for path in data['source_files_obj'][0][k]]
            
        if data['linker_file']:
            data['linker_file'] = join('$PROJ_DIR$', rel_path, normpath(data['linker_file']))

    def _get_option(self, settings, find_key):
        for option in settings:
            if option['name'] == find_key:
                return settings.index(option)

    def _set_option(self, settings, value):
        settings['state'] = value

    def _set_multiple_option(self, settings, value_list):
        settings['state'] = []
        for value in value_list:
            settings['state'].append(value)

    def _ewp_general_set(self, ewp_dic, project_dic):
        index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ExePath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'] ,'Exe'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ObjPath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'] ,'Obj'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ListPath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'] ,'List'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'GOutputBinary')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], 0 if project_dic['output_type'] == 'exe' else 1 )

    def _ewp_iccarm_set(self, ewp_dic, project_dic):
        index_iccarm = self._get_option(ewp_dic['project']['configuration']['settings'], 'ICCARM')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_iccarm]['data']['option'], 'CCDefines')
        self._set_multiple_option(ewp_dic['project']['configuration']['settings'][index_iccarm]['data']['option'][index_option], project_dic['macros'])
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_iccarm]['data']['option'], 'CCIncludePath2')
        self._set_multiple_option(ewp_dic['project']['configuration']['settings'][index_iccarm]['data']['option'][index_option], project_dic['includes'])

    def _ewp_aarm_set(self, ewp_dic, project_dic):
        # not used yet
        pass

    def _ewp_ilink_set(self, ewp_dic, project_dic):
        index_ilink = self._get_option(ewp_dic['project']['configuration']['settings'], 'ILINK')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'], 'IlinkIcfFile')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'][index_option], project_dic['linker_file'])
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'], 'IlinkAdditionalLibs')
        self._set_multiple_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'][index_option], project_dic['source_files_lib'])
        self._set_multiple_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'][index_option], project_dic['source_files_obj'])

    def _ewp_files_set(self, ewp_dic, project_dic):
        ewp_dic['project']['group'] = []
        i = 0
        for group_name, files in project_dic['groups'].items():
            ewp_dic['project']['group'].append({'name': group_name, 'file' : []})
            for file in files:
                ewp_dic['project']['group'][i]['file'].append({ 'name' : file})
            i = i + 1

    def _clean_xmldict_option(self, dictionary):
            for option in dictionary['data']['option']:
                if option['state'] is None:
                    option['state'] = ''

    def _clean_xmldict_single_dic(self, dictionary):
            for k,v in dictionary.items():
                if v is None:
                    dictionary[k] = ''

    def _clean_xmldict_ewp(self, ewp_dic):
        for setting in ewp_dic['project']['configuration']['settings']:
            if setting['name'] == 'BICOMP' or setting['name'] == 'BILINK':
                self._clean_xmldict_single_dic(setting)
            elif setting['name'] == 'BUILDACTION' or setting['name'] == 'CUSTOM':
                self._clean_xmldict_single_dic(setting['data'])
            elif 'option' in setting['data']:
                self._clean_xmldict_option(setting)


    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for IAR, and run generator """
        expanded_dic = data.copy()

        # TODO 0xc0170: fix misc , its a list with a dictionary
        if 'misc' in expanded_dic and bool(expanded_dic['misc'][0]):
            print "Using deprecated misc options for iar. Please use template project files."

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        # generic tool template specified or project
        if expanded_dic['template']:
            project_file = join(getcwd(), expanded_dic['template'][0]) #TODO 0xc0170: template list !
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        elif 'iar' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), env_settings.templates['iar'][0])
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        else:
            ewp_dic = self.definitions.ewp_file

        # TODO 0xc0170: add ewd file parsing and support
        ewd_dic = self.definitions.ewd_file
        eww_dic = self.definitions.eww_file

        # replace all None with empty strings ''
        self._clean_xmldict_ewp(ewp_dic)
        #self._clean_xmldict_ewd(ewd_dic)

        # set ARM toolchain and project name
        ewp_dic['project']['configuration']['toolchain']['name'] = 'ARM'
        ewp_dic['project']['configuration']['name'] = expanded_dic['name']

        # set eww
        eww_dic['workspace']['project']['path'] = join('$WS_DIR$', expanded_dic['name'] + '.ewp')

        # set common things we have for IAR
        self._ewp_general_set(ewp_dic, expanded_dic)
        self._ewp_iccarm_set(ewp_dic, expanded_dic)
        self._ewp_aarm_set(ewp_dic, expanded_dic)
        self._ewp_ilink_set(ewp_dic, expanded_dic)
        self._ewp_files_set(ewp_dic, expanded_dic)

        # get target definition (target + mcu)
        target = Targets(env_settings.get_env_settings('definitions'))
        if not target.is_supported(expanded_dic['target'].lower(), 'iar'):
            raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
        mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'iar')
        if not mcu_def_dic:
             raise RuntimeError(
                "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                % expanded_dic['target'].lower())
        self.normalize_mcu_def(mcu_def_dic)
        logging.debug("Mcu definitions: %s" % mcu_def_dic)
        index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OGChipSelectEditMenu')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], mcu_def_dic['OGChipSelectEditMenu']['state'])
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OGCoreOrChip')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], mcu_def_dic['OGCoreOrChip']['state'])

        # overwrite debugger only if defined in the project file, otherwise use either default or from template
        if expanded_dic['debugger']:
            try:
                debugger = self.definitions.debuggers[expanded_dic['debugger']]
                index_cspy = self._get_option(ewd_dic['project']['configuration']['settings'], 'C-SPY')
                index_option = self._get_option(ewd_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OCDynDriverList')
                self._set_option(ewd_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], debugger['OCDynDriverList']['state'])
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        ewp_xml = xmltodict.unparse(ewp_dic, pretty=True)
        project_path, ewp = self.gen_file_raw(ewp_xml, '%s.ewp' %
            expanded_dic['name'], expanded_dic['output_dir']['path'])

        eww_xml = xmltodict.unparse(eww_dic, pretty=True)
        project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' %
            expanded_dic['name'], expanded_dic['output_dir']['path'])

        ewd_xml = xmltodict.unparse(ewd_dic, pretty=True)
        project_path, ewd = self.gen_file_raw(ewd_xml, '%s.ewd' %
                    expanded_dic['name'], expanded_dic['output_dir']['path'])
        return project_path, [ewp, eww, ewd]

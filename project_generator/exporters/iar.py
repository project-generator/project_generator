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
        mcu_def['General']['data']['option']['OGChipSelectEditMenu']['state'] = mcu_def['General']['data']['option']['OGChipSelectEditMenu']['state'][0].replace(' ', '\t', 1)
        mcu_def['General']['data']['option']['OGCoreOrChip']['state'] = mcu_def['General']['data']['option']['OGCoreOrChip']['state'][0]

    def fix_paths(self, data, rel_path):
        fixed_paths = []
        for path in data['includes']:
            fixed_paths.append(join('$PROJ_DIR$', rel_path, normpath(path)))
        data['includes'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_lib']:
            fixed_paths.append(join('$PROJ_DIR$', rel_path, normpath(path)))
        data['source_files_lib'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_obj']:
            fixed_paths.append(join('$PROJ_DIR$', rel_path, normpath(path)))
        data['source_files_obj'] = fixed_paths
        if data['linker_file']:
            data['linker_file'] = join('$PROJ_DIR$', rel_path, normpath(data['linker_file']))

    def _iar_option_dictionarize(self, option_group , iar_settings):
        dictionarized = {}
        for option in iar_settings[option_group]['data']['option']:
            dictionarized[option['name']] = {}
            dictionarized[option['name']].update(option)
        return dictionarized

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for IAR, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        expanded_dic['iar_settings'] = {
            'toolchain' : 'ARM',
        }

        # generic tool template specified or project
        if 'iar' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            project_file = join(getcwd(), env_settings.templates['iar']['path'][0], env_settings.templates['iar']['name'][0] + '.ewp')
            proj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
            # form valid iar settings dictionary
            iar_settings = {
                'General' : {},
                'ICCARM' : {},
                'AARM' : {},
                'OBJCOPY' : {},
                'CUSTOM' : {},
                'BICOMP' : {},
                'BUILDACTION' : {},
                'ILINK' : {},
                'IARCHIVE' : {},
                'BILINK' : {},
            }
            for settings in proj_dic['project']['configuration']['settings']:
                iar_settings[settings['name']].update(settings)
            iar_settings['AARM']['data']['option'] = self._iar_option_dictionarize('AARM', iar_settings)
            iar_settings['General']['data']['option'] = self._iar_option_dictionarize('General', iar_settings)
            iar_settings['IARCHIVE']['data']['option'] = self._iar_option_dictionarize('IARCHIVE', iar_settings)
            iar_settings['ICCARM']['data']['option'] = self._iar_option_dictionarize('ICCARM', iar_settings)
            iar_settings['ILINK']['data']['option'] = self._iar_option_dictionarize('ILINK', iar_settings)
            iar_settings['OBJCOPY']['data']['option'] = self._iar_option_dictionarize('OBJCOPY', iar_settings)
            expanded_dic['iar_settings'] = iar_settings
        else:
            # setting values from the yaml files
            self.parse_specific_options(expanded_dic)

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
        expanded_dic['iar_settings']['General']['data']['option']['OGChipSelectEditMenu'] = mcu_def_dic['General']['data']['option']['OGChipSelectEditMenu']
        expanded_dic['iar_settings']['General']['data']['option']['OGCoreOrChip'] = mcu_def_dic['General']['data']['option']['OGCoreOrChip']

        # get debugger definitions
        try:
            expanded_dic['iar_settings'].update(self.definitions.debuggers[expanded_dic['debugger']])
        except KeyError:
            raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        project_path, ewp = self.gen_file('iar.ewp.tmpl', expanded_dic, '%s.ewp' %
            data['name'], expanded_dic['output_dir']['path'])
        project_path, eww = self.gen_file('iar.eww.tmpl', expanded_dic, '%s.eww' %
            data['name'], expanded_dic['output_dir']['path'])
        project_path, ewd = self.gen_file('iar.ewd.tmpl', expanded_dic, '%s.ewd' %
                    data['name'], expanded_dic['output_dir']['path'])
        return project_path, [ewp, eww, ewd]

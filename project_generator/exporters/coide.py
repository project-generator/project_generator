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
import logging

from os.path import basename, join, relpath, normpath
from os import getcwd
import xmltodict

from .exporter import Exporter
from .coide_definitions import CoIDEdefinitions
from ..targets import Targets

class CoideExporter(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1}

    def __init__(self):
        self.definitions = CoIDEdefinitions()

    def expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {"path": rel_path + normpath(file), "name": basename(
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

    def parse_specific_options(self, data):
        """ Parse all CoIDE specific setttings. """
        data['coide_settings'].update(copy.deepcopy(
            self.definitions.coide_settings))  # set specific options to default values
        for dic in data['misc']:
            for k, v in dic.items():
                for option in v:
                    data['coide_settings'][k][option].update(v[option])

    def normalize_mcu_def(self, mcu_def):
        for k,v in mcu_def['Target']['Device'].items():
            mcu_def['Target']['Device'][k] = v[0]
        for k,v in mcu_def['Target']['DebugOption'].items():
            mcu_def['Target']['DebugOption'][k] = v[0]
        for k,v in mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IROM1'].items():
            mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IROM1'][k] = v[0]
        for k,v in mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IROM2'].items():
            mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IROM2'][k] = v[0]
        for k,v in mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IRAM1'].items():
            mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IRAM1'][k] = v[0]
        for k,v in mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IRAM2'].items():
            mcu_def['Target']['BuildOption']['Link']['MemoryAreas']['Memory']['IRAM2'][k] = v[0]

    def fix_paths(self, data, rel_path):
        fixed_paths = []
        for path in data['includes']:
            fixed_paths.append(join(rel_path, normpath(path)))
        data['includes'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_lib']:
            fixed_paths.append(join(rel_path, normpath(path)))
        data['source_files_lib'] = fixed_paths
        fixed_paths = []
        for path in data['source_files_obj']:
            fixed_paths.append(join(rel_path, normpath(path)))
        if data['linker_file']:
            data['linker_file'] = join(rel_path, normpath(data['linker_file']))

    def _coide_option_dictionarize(self, key, coide_settings):
        dictionarized = {}
        for option in coide_settings[key]:
            dictionarized[option['@name']] = {}
            dictionarized[option['@name']].update(option)
        return dictionarized

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for CoIDE, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        expanded_dic['coide_settings'] = {}

        # generic tool template specified or project
        if 'coide' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            project_file = join(getcwd(), env_settings.templates['coide']['path'][0], env_settings.templates['coide']['name'][0] + '.coproj')
            proj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
            coide_settings = {
                    'Target' : {
                        'Device' : {},
                        'BuildOption' : {
                            'Compile' : {
                                'Option' : {}
                            },
                            'Link' : {
                                'Option' : {}
                            },
                            'Output' : {
                                'Option' : {}
                            },
                            'User': {
                                'UserRun' : {}
                            }
                        },
                        'DebugOption' : {
                            'Option' : {}
                        },
                    }
            }
            coide_settings['Target']['BuildOption']['Compile']['Option'] = self._coide_option_dictionarize('Option', proj_dic['Project']['Target']['BuildOption']['Compile'])
            coide_settings['Target']['BuildOption']['Link'].update(proj_dic['Project']['Target']['BuildOption']['Link'])
            coide_settings['Target']['BuildOption']['Link']['Option'] = self._coide_option_dictionarize('Option', proj_dic['Project']['Target']['BuildOption']['Link'])
            coide_settings['Target']['BuildOption']['Output'].update(proj_dic['Project']['Target']['BuildOption']['Output'])
            coide_settings['Target']['BuildOption']['Output']['Option'] = self._coide_option_dictionarize('Option', proj_dic['Project']['Target']['BuildOption']['Output'])
            coide_settings['Target']['BuildOption']['User'].update(proj_dic['Project']['Target']['BuildOption']['User'])
            # Run#1 is an exception, oh
            dictionarized = {}
            dictionarized[proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0]['@name']] = {
                proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0]['@type'] : {},
                proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][1]['@type'] : {}
            }
            dictionarized[proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0]['@name']][proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0]['@type']].update(proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0])
            dictionarized[proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][0]['@name']][proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][1]['@type']].update(proj_dic['Project']['Target']['BuildOption']['User']['UserRun'][1])
            coide_settings['Target']['BuildOption']['User']['UserRun'] = dictionarized

            coide_settings['Target']['DebugOption'].update(proj_dic['Project']['Target']['DebugOption'])
            coide_settings['Target']['DebugOption']['Option'] = {}
            coide_settings['Target']['DebugOption']['Option'].update(self._coide_option_dictionarize('Option', proj_dic['Project']['Target']['DebugOption']))
            # merge in current settings with the parser one
            expanded_dic['coide_settings'] = {key: dict(expanded_dic['coide_settings'].get(key, {}).items() + coide_settings.get(key, {}).items()) for key in expanded_dic['coide_settings'].keys() + coide_settings.keys()}
        else:
            # setting values from the yaml files
            self.parse_specific_options(expanded_dic)

        target = Targets(env_settings.get_env_settings('definitions'))
        if not target.is_supported(expanded_dic['target'].lower(), 'coide'):
            raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
        mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'coide')
        if not mcu_def_dic:
             raise RuntimeError(
                "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                % expanded_dic['target'].lower())
        self.normalize_mcu_def(mcu_def_dic)
        logging.debug("Mcu definitions: %s" % mcu_def_dic)
        expanded_dic['coide_settings']['Target']['Device'].update(mcu_def_dic['Target']['Device'])
        expanded_dic['coide_settings']['Target']['DebugOption'].update(mcu_def_dic['Target']['DebugOption'])
        expanded_dic['coide_settings']['Target']['BuildOption']['Link']['MemoryAreas'].update(mcu_def_dic['Target']['BuildOption']['Link']['MemoryAreas'])

        # get debugger definitions
        try:
            expanded_dic['coide_settings']['Target']['DebugOption']['org.coocox.codebugger.gdbjtag.core.adapter'] = self.definitions.debuggers[expanded_dic['debugger']]['Target']['DebugOption']['org.coocox.codebugger.gdbjtag.core.adapter']
        except KeyError:
            raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        project_path, projfile = self.gen_file(
            'coide.coproj.tmpl', expanded_dic, '%s.coproj' % data['name'], expanded_dic['output_dir']['path'])
        return project_path, [projfile]

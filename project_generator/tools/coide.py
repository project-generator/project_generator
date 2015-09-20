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

import logging
import xmltodict
from collections import OrderedDict
import copy

from os.path import basename, join, normpath
from os import getcwd

from .tool import Tool, Builder, Exporter
from ..targets import Targets

class CoIDEdefinitions():

    coproj_file = OrderedDict([(u'Project', OrderedDict([(u'@version', u'2G - 1.7.5'), (u'@name', u''), (u'Target', OrderedDict([(u'@name', u''), (u'@isCurrent', u'1'), (u'Device', OrderedDict([(u'@manufacturerId', u'7'), (u'@manufacturerName', u'NXP'), (u'@chipId', u'165'), (u'@chipName', u'LPC1768'), (u'@boardId', u''), (u'@boardName', u'')])), (u'BuildOption', OrderedDict([(u'Compile', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OptimizationLevel'), (u'@value', u'4')]), OrderedDict([(u'@name', u'UseFPU'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditCompiler'), (u'@value', u'-fno-common;-fmessage-length=0;-Wall;-fno-strict-aliasing;-fno-rtti;-fno-exceptions;-ffunction-sections;-fdata-sections;-std=gnu++98;')])]), (u'Includepaths', OrderedDict([(u'Includepath', OrderedDict([(u'@path', u'')]))])), (u'DefinedSymbols', OrderedDict([(u'Define', OrderedDict([(u'@name', u'')]))]))])), (u'Link', OrderedDict([(u'@useDefault', u'0'), (u'Option', [OrderedDict([(u'@name', u'DiscardUnusedSection'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinkder'), (u'@value', u'1')]), OrderedDict([(u'@name', u'UseMemoryLayout'), (u'@value', u'0')]), OrderedDict([(u'@name', u'LTO'), (u'@value', u'')]), OrderedDict([(u'@name', u'IsNewStartupCode'), (u'@value', u'')]), OrderedDict([(u'@name', u'Library'), (u'@value', u'Use nano C Library')]), OrderedDict([(u'@name', u'nostartfiles'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinker'), (u'@value', u'')]), OrderedDict([(u'@name', u'Printf'), (u'@value', u'1')]), OrderedDict([(u'@name', u'Scanf'), (u'@value', u'1')])]), (u'LinkedLibraries', OrderedDict([(u'Libset', [OrderedDict([(u'@dir', u''), (u'@libs', u'stdc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'supc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'm')]), OrderedDict([(u'@dir', u''), (u'@libs', u'gcc')]), OrderedDict([(u'@dir', u''), (u'@libs', u'c')]), OrderedDict([(u'@dir', u''), (u'@libs', u'nosys')])])])), (u'MemoryAreas', OrderedDict([(u'@debugInFlashNotRAM', u'1'), (u'Memory', [OrderedDict([(u'@name', u'IROM1'), (u'@type', u'ReadOnly'), (u'@size', u'524288'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM1'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'268435456')]), OrderedDict([(u'@name', u'IROM2'), (u'@type', u'ReadOnly'), (u'@size', u'0'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM2'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'537378816')])])])), (u'LocateLinkFile', OrderedDict([(u'@path', u''), (u'@type', u'0')]))])), (u'Output', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OutputFileType'), (u'@value', u'0')]), OrderedDict([(u'@name', u'Path'), (u'@value', u'./')]), OrderedDict([(u'@name', u'Name'), (u'@value', u'')]), OrderedDict([(u'@name', u'HEX'), (u'@value', u'1')]), OrderedDict([(u'@name', u'BIN'), (u'@value', u'1')])])])), (u'User', OrderedDict([(u'UserRun', [OrderedDict([(u'@name', u'Run#1'), (u'@type', u'Before'), (u'@checked', u'0'), (u'@value', u'')]), OrderedDict([(u'@name', u'Run#1'), (u'@type', u'After'), (u'@checked', u'0'), (u'@value', u'')])])]))])), (u'DebugOption', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.adapter'), (u'@value', u'J-Link')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.debugMode'), (u'@value', u'SWD')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.clockDiv'), (u'@value', u'1M')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.corerunToMain'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkgdbserver'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.userDefineGDBScript'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.targetEndianess'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkResetMode'), (u'@value', u'Type 0: Normal')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.resetMode'), (u'@value', u'SYSRESETREQ')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifSemihost'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifCacheRom'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ipAddress'), (u'@value', u'127.0.0.1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.portNumber'), (u'@value', u'2009')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.autoDownload'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.verify'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.downloadFuction'), (u'@value', u'Erase Effected')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.defaultAlgorithm'), (u'@value', u'')])])])), (u'ExcludeFile', None)])), (u'Components', OrderedDict([(u'@path', u'./')])), (u'Files', None)]))])

    debuggers = {
        'cmsis-dap' : {
            'Target': {
                'DebugOption' : {
                    'org.coocox.codebugger.gdbjtag.core.adapter' : 'CMSIS-DAP',
                }
            }
        },
        'j-link' : {
            'Target': {
                'DebugOption' : {
                    'org.coocox.codebugger.gdbjtag.core.adapter' : 'J-Link',
                }
            }
        },
    }

class Coide(Tool, Exporter, Builder):

    source_files_dic = [
        'source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1}

    generated_project = {
        'path': '',
        'files': {
            'coproj': ''
        }
    }

    def __init__(self, workspace, env_settings):
        self.definitions = CoIDEdefinitions()
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'coide'

    def _expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group

        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {
                    '@path': rel_path + normpath(file), '@name': basename(file), '@type': str(self.file_types[extension.lower()])
                }
                new_data['groups'][group].append(new_file)

    def _get_groups(self):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
                for k, v in self.workspace[attribute].items():
                    if k == None:
                        k = 'Sources'
                    if k not in groups:
                        groups.append(k)
        return groups

    def _iterate(self, data, expanded_data, rel_path):
        """ _Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                self._expand_data(data[attribute], expanded_data, attribute, group, rel_path)

    def _normalize_mcu_def(self, mcu_def):
        for k, v in mcu_def['Device'].items():
            mcu_def['Device'][k] = v[0]
        for k, v in mcu_def['DebugOption'].items():
            mcu_def['DebugOption'][k] = v[0]
        for k, v in mcu_def['MemoryAreas']['IROM1'].items():
            mcu_def['MemoryAreas']['IROM1'][k] = v[0]
        for k, v in mcu_def['MemoryAreas']['IROM2'].items():
            mcu_def['MemoryAreas']['IROM2'][k] = v[0]
        for k, v in mcu_def['MemoryAreas']['IRAM1'].items():
            mcu_def['MemoryAreas']['IRAM1'][k] = v[0]
        for k, v in mcu_def['MemoryAreas']['IRAM2'].items():
            mcu_def['MemoryAreas']['IRAM2'][k] = v[0]

    def _fix_paths(self, data, rel_path):
        data['includes'] = [join(rel_path, normpath(path)) for path in data['includes']]

        for k in data['source_files_lib'].keys():
            data['source_files_lib'][k] = [join(rel_path,normpath(path)) for path in data['source_files_lib'][k]]

        for k in data['source_files_obj'].keys():
            data['source_files_obj'][k] = [join(rel_path,normpath(path)) for path in data['source_files_obj'][k]]
        if data['linker_file']:
            data['linker_file'] = join(rel_path, normpath(data['linker_file']))

    def _coide_option_dictionarize(self, option, key, coide_settings):
        dictionarized = {}
        for option in coide_settings[option]:
            dictionarized[option[key]] = {}
            dictionarized[option[key]].update(option)
        return dictionarized

    def _coproj_set_files(self, coproj_dic, project_dic):
        coproj_dic['Project']['Files'] = {}
        coproj_dic['Project']['Files']['File'] = []
        for group,files in project_dic['groups'].items():
            # TODO 0xc0170: this might not be needed
            # coproj_dic['Project']['Files']['File'].append({u'@name': group, u'@path': '', u'@type' : '2' })
            for file in files:
                if group:
                    file['@name'] = group + '/' + file['@name']
                coproj_dic['Project']['Files']['File'].append(file)

    def _coproj_set_macros(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'] = []
        for macro in project_dic['macros']:
            coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'].append({'@name': macro})

    def _coproj_set_includepaths(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['Includepaths']['Includepath'] = []
        for include in project_dic['includes']:
            coproj_dic['Project']['Target']['BuildOption']['Compile']['Includepaths']['Includepath'].append({'@path': include})

    def _coproj_set_linker(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Link']['LocateLinkFile']['@path'] = project_dic['linker_file']

    def _coproj_find_option(self, option_dic, key_to_find, value_to_match):
        i = 0
        for option in option_dic:
            for k,v in option.items():
                if k == key_to_find and value_to_match == v:
                    return i
            i += 1
        return None

    def _export_single_project(self):
        """ Processes groups and misc options specific for CoIDE, and run generator """
        expanded_dic = self.workspace.copy()

        # TODO 0xc0170: fix misc , its a list with a dictionary
        if 'misc' in expanded_dic and bool(expanded_dic['misc']):
            print ("Using deprecated misc options for coide. Please use template project files.")

        groups = self._get_groups()
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self._iterate(self.workspace, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self._fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        # generic tool template specified or project
        if expanded_dic['template']:
            project_file = join(getcwd(), expanded_dic['template'][0])
            coproj_dic = xmltodict.parse(file(project_file))
        elif 'coide' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), self.env_settings.templates['coide'][0])
            coproj_dic = xmltodict.parse(file(project_file))
        else:
            # setting values from the yaml files
            coproj_dic = self.definitions.coproj_file

        # set name and target
        try:
            coproj_dic['Project']['@name'] = expanded_dic['name']
        except KeyError:
            raise RuntimeError("The coide template is not valid .coproj file")

        coproj_dic['Project']['Target']['@name'] = expanded_dic['name']
        # library/exe
        coproj_dic['Project']['Target']['BuildOption']['Output']['Option'][0]['@value'] = 0 if expanded_dic['output_type'] == 'exe' else 1

        # Fill in pgen data to the coproj_dic
        self._coproj_set_files(coproj_dic, expanded_dic)
        self._coproj_set_macros(coproj_dic, expanded_dic)
        self._coproj_set_includepaths(coproj_dic, expanded_dic)
        self._coproj_set_linker(coproj_dic, expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if expanded_dic['target']:
            target = Targets(self.env_settings.get_env_settings('definitions'))
            if not target.is_supported(expanded_dic['target'].lower(), 'coide'):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'coide')
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                    % expanded_dic['target'].lower())
            self._normalize_mcu_def(mcu_def_dic)
            logging.debug("Mcu definitions: %s" % mcu_def_dic)
            # correct attributes from definition, as yaml does not allowed multiple keys (=dict), we need to
            # do this magic.
            for k, v in mcu_def_dic['Device'].items():
                del mcu_def_dic['Device'][k]
                mcu_def_dic['Device']['@' + k] = str(v)
            memory_areas = []
            for k, v in mcu_def_dic['MemoryAreas'].items():
                # ??? duplicate use of k
                for k, att in v.items():
                    del v[k]
                    v['@' + k] = str(att)
                memory_areas.append(v)

            coproj_dic['Project']['Target']['Device'].update(mcu_def_dic['Device'])
            # TODO 0xc0170: fix debug options
            # coproj_dic['Project']['Target']['DebugOption'].update(mcu_def_dic['DebugOption'])
            coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'] = memory_areas

        # get debugger definitions
        if expanded_dic['debugger']:
            try:
                # find debugger definitions in the list of options
                index = 0
                for option in coproj_dic['Project']['Target']['DebugOption']['Option']:
                    # ??? k, v not used ???
                    for k, v in option.items():
                        if option['@name'] == 'org.coocox.codebugger.gdbjtag.core.adapter':
                            found = index
                index += 1
                coproj_dic['Project']['Target']['DebugOption']['Option'][found]['@value'] = self.definitions.debuggers[expanded_dic['debugger']]['Target']['DebugOption']['org.coocox.codebugger.gdbjtag.core.adapter']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        # somehow this xml is not compatible with coide, coide v2.0 changing few things, lets use jinja
        # for now, more testing to get xml output right. Jinja template follows the xml dictionary,which is
        # what we want anyway.
        # coproj_xml = xmltodict.unparse(coproj_dic, pretty=True)
        project_path, projfile = self.gen_file_jinja(
            'coide.coproj.tmpl', coproj_dic, '%s.coproj' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        return project_path, projfile

    def export_workspace(self):
        logging.debug("Current version of CoIDE does not support workspaces")

    def export_project(self):
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'], generated_projects['files']['coproj'] = self._export_single_project()
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['coproj']]}

    def get_mcu_definition(self, project_file):
        """ Parse project file to get mcu definition """
        project_file = join(getcwd(), project_file)
        coproj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)

        mcu = Targets().get_mcu_definition()

        IROM1_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IROM1')
        IROM2_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IROM2')
        IRAM1_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IRAM1')
        IRAM2_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IRAM2')
        defaultAlgorithm_index = self._coproj_find_option(coproj_dic['Project']['Target']['DebugOption']['Option'], '@name', 'org.coocox.codebugger.gdbjtag.core.defaultAlgorithm')

        mcu['tool_specific'] = {
            'coide' : {
                'Device' : {
                    'manufacturerId' : [coproj_dic['Project']['Target']['Device']['@manufacturerId']],
                    'manufacturerName': [coproj_dic['Project']['Target']['Device']['@manufacturerName']],
                    'chipId': [coproj_dic['Project']['Target']['Device']['@chipId']],
                    'chipName': [coproj_dic['Project']['Target']['Device']['@chipName']],
                },
                'DebugOption': {
                    'defaultAlgorithm': [coproj_dic['Project']['Target']['DebugOption']['Option'][defaultAlgorithm_index]['@value']],
                },
                'MemoryAreas': {
                    'IROM1': {
                        'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@name']],
                        'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@size']],
                        'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@startValue']],
                        'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@type']],
                    },
                    'IRAM1': {
                        'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@name']],
                        'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@size']],
                        'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@startValue']],
                        'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@type']],
                    },
                    'IROM2': {
                        'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@name']],
                        'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@size']],
                        'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@startValue']],
                        'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@type']],
                    },
                    'IRAM2': {
                        'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@name']],
                        'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@size']],
                        'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@startValue']],
                        'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@type']],
                    }
                }
            }
        }
        return mcu

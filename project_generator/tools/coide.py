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
import re

from os.path import basename, join, normpath, splitext
from os import getcwd
from project_generator_definitions.definitions import ProGenDef

from .tool import Tool, Builder, Exporter
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.coide')

class CoIDEdefinitions():

    coproj_file = OrderedDict([(u'Project', OrderedDict([(u'@version', u'2G - 1.7.5'), (u'@name', u''), (u'Target', OrderedDict([(u'@name', u''), (u'@isCurrent', u'1'), (u'Device', OrderedDict([(u'@manufacturerId', u'7'), (u'@manufacturerName', u'NXP'), (u'@chipId', u'165'), (u'@chipName', u'LPC1768'), (u'@boardId', u''), (u'@boardName', u'')])), (u'BuildOption', OrderedDict([(u'Compile', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OptimizationLevel'), (u'@value', u'4')]), OrderedDict([(u'@name', u'UseFPU'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditCompiler'), (u'@value', u'-fno-common;-fmessage-length=0;-Wall;-fno-strict-aliasing;-fno-rtti;-fno-exceptions;-ffunction-sections;-fdata-sections;-std=gnu++98;')])]), (u'Includepaths', OrderedDict([(u'Includepath', OrderedDict([(u'@path', u'')]))])), (u'DefinedSymbols', OrderedDict([(u'Define', OrderedDict([(u'@name', u'')]))]))])), (u'Link', OrderedDict([(u'@useDefault', u'0'), (u'Option', [OrderedDict([(u'@name', u'DiscardUnusedSection'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinkder'), (u'@value', u'1')]), OrderedDict([(u'@name', u'UseMemoryLayout'), (u'@value', u'0')]), OrderedDict([(u'@name', u'LTO'), (u'@value', u'')]), OrderedDict([(u'@name', u'IsNewStartupCode'), (u'@value', u'')]), OrderedDict([(u'@name', u'Library'), (u'@value', u'Use nano C Library')]), OrderedDict([(u'@name', u'nostartfiles'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinker'), (u'@value', u'')]), OrderedDict([(u'@name', u'Printf'), (u'@value', u'1')]), OrderedDict([(u'@name', u'Scanf'), (u'@value', u'1')])]), (u'LinkedLibraries', OrderedDict([(u'Libset', [OrderedDict([(u'@dir', u''), (u'@libs', u'stdc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'supc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'm')]), OrderedDict([(u'@dir', u''), (u'@libs', u'gcc')]), OrderedDict([(u'@dir', u''), (u'@libs', u'c')]), OrderedDict([(u'@dir', u''), (u'@libs', u'nosys')])])])), (u'MemoryAreas', OrderedDict([(u'@debugInFlashNotRAM', u'1'), (u'Memory', [OrderedDict([(u'@name', u'IROM1'), (u'@type', u'ReadOnly'), (u'@size', u'524288'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM1'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'268435456')]), OrderedDict([(u'@name', u'IROM2'), (u'@type', u'ReadOnly'), (u'@size', u'0'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM2'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'537378816')])])])), (u'LocateLinkFile', OrderedDict([(u'@path', u''), (u'@type', u'0')]))])), (u'Output', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OutputFileType'), (u'@value', u'0')]), OrderedDict([(u'@name', u'Path'), (u'@value', u'./')]), OrderedDict([(u'@name', u'Name'), (u'@value', u'')]), OrderedDict([(u'@name', u'HEX'), (u'@value', u'1')]), OrderedDict([(u'@name', u'BIN'), (u'@value', u'1')])])])), (u'User', OrderedDict([(u'UserRun', [OrderedDict([(u'@name', u'Run#1'), (u'@type', u'Before'), (u'@checked', u'0'), (u'@value', u'')]), OrderedDict([(u'@name', u'Run#1'), (u'@type', u'After'), (u'@checked', u'0'), (u'@value', u'')])])]))])), (u'DebugOption', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.adapter'), (u'@value', u'CMSIS-DAP')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.debugMode'), (u'@value', u'SWD')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.clockDiv'), (u'@value', u'1M')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.corerunToMain'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkgdbserver'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.userDefineGDBScript'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.targetEndianess'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkResetMode'), (u'@value', u'Type 0: Normal')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.resetMode'), (u'@value', u'SYSRESETREQ')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifSemihost'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifCacheRom'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ipAddress'), (u'@value', u'127.0.0.1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.portNumber'), (u'@value', u'2009')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.autoDownload'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.verify'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.downloadFuction'), (u'@value', u'Erase Effected')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.defaultAlgorithm'), (u'@value', u'')])])])), (u'ExcludeFile', None)])), (u'Components', OrderedDict([(u'@path', u'./')])), (u'Files', None)]))])

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

    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1, 'h': 1}

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
        return ['coide']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def _expand_one_file(self, source, new_data, extension):
        return {'@path': source, '@name': basename(source), '@type': str(self.file_types[extension.lower()])}

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
        coproj_dic['Project']['Files']['File'] = sorted(coproj_dic['Project']['Files']['File'], key=lambda x: basename(x['@path'].lower()))

    def _coproj_set_macros(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'] = []
        for macro in project_dic['macros']:
            coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'].append({'@name': macro})

    def _coproj_set_includepaths(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['Includepaths']['Includepath'] = []
        for include in project_dic['include_paths']:
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

        groups = self._get_groups(self.workspace)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self._iterate(self.workspace, expanded_dic)

        # generic tool template specified or project
        if expanded_dic['template']:
            for template in expanded_dic['template']:
                template = join(getcwd(), template)
                if splitext(template)[1] == '.coproj' or re.match('.*\.coproj.tmpl$', template):
                    try:
                        coproj_dic = xmltodict.parse(open(template))
                    except IOError:
                        logger.info("Template file %s not found. Using default template" % template)
                        coproj_dic = self.definitions.coproj_file
                else:
                    logger.info("Template file %s contains unknown template extension (.coproj/.coproj.tmpl are valid). Using default one" % template)
                    coproj_dic = self.definitions.coproj_file
        elif 'coide' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            for template in self.env_settings.templates['coide']:
                template = join(getcwd(), template)
                if splitext(template)[1] == '.coproj' or re.match('.*\.coproj.tmpl$', template):
                    try:
                        coproj_dic = xmltodict.parse(open(template))
                    except IOError:
                        logger.info("Template file %s not found. Using default template" % template)
                        coproj_dic = self.definitions.coproj_file
                else:
                    logger.info("Template file %s contains unknown template extension (.coproj/.coproj.tmpl are valid). Using default one" % template)
                    coproj_dic = self.definitions.coproj_file
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

        # Fill in progen data to the coproj_dic
        self._coproj_set_files(coproj_dic, expanded_dic)
        self._coproj_set_macros(coproj_dic, expanded_dic)
        self._coproj_set_includepaths(coproj_dic, expanded_dic)
        self._coproj_set_linker(coproj_dic, expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if expanded_dic['target']:
            pro_def = ProGenDef('coide')
            if not pro_def.is_supported(expanded_dic['target'].lower()):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = pro_def.get_tool_definition(expanded_dic['target'].lower())
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                    % expanded_dic['target'].lower())
            self._normalize_mcu_def(mcu_def_dic)
            logger.debug("Mcu definitions: %s" % mcu_def_dic)
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

            # TODO 0xc0170: create a method and look at finding that option if we can reuse already defined method
            try:
                # find debugger definitions in the list of options
                index = 0
                for option in coproj_dic['Project']['Target']['DebugOption']['Option']:
                    # ??? k, v not used ???
                    for k, v in option.items():
                        if option['@name'] == 'org.coocox.codebugger.gdbjtag.core.adapter':
                            found = index
                index += 1
                debugger_name =pro_def.get_debugger(expanded_dic['target'])['name']
                coproj_dic['Project']['Target']['DebugOption']['Option'][found]['@value'] = self.definitions.debuggers[debugger_name]['Target']['DebugOption']['org.coocox.codebugger.gdbjtag.core.adapter']
            except (TypeError, KeyError) as err:
                pass


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
        logger.debug("Current version of CoIDE does not support workspaces")

    def export_project(self):
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'], generated_projects['files']['coproj'] = self._export_single_project()
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['coproj']]}

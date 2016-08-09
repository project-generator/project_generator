# Copyright 2015 0xc0170
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
import xmltodict
import subprocess
from subprocess import Popen, PIPE
import time
import copy
import re

import os
from os import getcwd
from os.path import join, normpath
from collections import OrderedDict
from project_generator_definitions.definitions import ProGenDef

from .tool import Tool, Builder, Exporter
from ..util import SOURCE_KEYS, FILES_EXTENSIONS, fix_paths

logger = logging.getLogger('progen.tools.iar')

class IARDefinitions():
    """ Definitions for IAR Workbench IDE """

    # TODO: Fix this with the parser!
    debuggers = {
        'cmsis-dap': {
            'OCDynDriverList': {
                'state' : 'CMSISDAP_ID',
            },
            'interface': {
                'name' : 'CMSISDAPInterfaceRadio', # each debuger has own names for th1s
                'jtag' : 0, # TODO: verify that jtag maches for all debuggers to have it just defined once
                'swd' : 1,
            }
        },
        'j-link': {
            'OCDynDriverList': {
                'state' : 'JLINK_ID',
            },
            'interface': {
                'name' : 'CCJLinkInterfaceRadio',
                'jtag' : 0,
                'swd' : 1,
            }
        },
        'st-link': {
            'OCDynDriverList': {
                'state' : 'STLINK_ID',
            },
            'interface': {
                'name' : 'CCSTLinkInterfaceRadio',
                'jtag' : 0,
                'swd' : 1,
            }
        },
    }


class IAREmbeddedWorkbenchProject:
    """ This class handles all related project settings """

    # IAR misc contains enable check and then state. Therefore we map here
    # each flag to dict to know which one to enable and set those options
    FLAG_TO_IAR = {
        'asm_flags' : {
            'enable': 'AExtraOptionsCheckV2',
            'set' : 'AExtraOptionsV2',
        },
        'c_flags' : {
            'enable': 'IExtraOptionsCheck',
            'set' : 'IExtraOptions',
        },
        'cxx_flags' : {
            'enable': 'IExtraOptionsCheck',
            'set' : 'IExtraOptions',
        },
        'ld_flags' : {
            'enable': 'IlinkUseExtraOptions',
            'set' : 'IlinkExtraOptions',
        },
    }

    def _set_option(self, settings, value):
        """ Set option (state) """
        settings['state'] = value

    def _get_option(self, settings, find_key):
        """ Return index for provided key """
        # This is used as in IAR template, everything 
        # is as an array with random positions. We look for key with an index
        for option in settings:
            if option['name'] == find_key:
                return settings.index(option)

    def _set_multiple_option(self, settings, value_list):
        settings['state'] = []
        for value in value_list:
            settings['state'].append(value)

    def _ewp_general_set(self, ewp_dic, project_dic):
        index_general = self._get_option(ewp_dic, 'General')
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'ExePath')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'Exe'))
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'ObjPath')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'Obj'))
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'ListPath')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'List'))
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'GOutputBinary')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], 0 if project_dic['output_type'] == 'exe' else 1)

    def _ewp_iccarm_set(self, ewp_dic, project_dic):
        """ C/C++ options (ICCARM) """
        index_iccarm = self._get_option(ewp_dic, 'ICCARM')
        index_option = self._get_option(ewp_dic[index_iccarm]['data']['option'], 'CCDefines')
        self._set_multiple_option(ewp_dic[index_iccarm]['data']['option'][index_option], project_dic['macros'])
        index_option = self._get_option(ewp_dic[index_iccarm]['data']['option'], 'CCIncludePath2')
        self._set_multiple_option(ewp_dic[index_iccarm]['data']['option'][index_option], project_dic['include_paths'])

        iccarm_dic = ewp_dic[index_iccarm]['data']['option']
        self._ewp_flags_set(iccarm_dic, project_dic, 'cxx_flags', self.FLAG_TO_IAR['cxx_flags'])
        self._ewp_flags_set(iccarm_dic, project_dic, 'c_flags', self.FLAG_TO_IAR['c_flags'])

    def _ewp_aarm_set(self, ewp_dic, project_dic):
        """ Assembly options (AARM) """
        index_aarm = self._get_option(ewp_dic, 'AARM')

        aarm_dic = ewp_dic[index_aarm]['data']['option']
        self._ewp_flags_set(aarm_dic, project_dic, 'asm_flags', self.FLAG_TO_IAR['asm_flags'])

    def _ewp_ilink_set(self, ewp_dic, project_dic):
        """ Linker options (ILINK) """
        index_ilink = self._get_option(ewp_dic, 'ILINK')
        index_option = self._get_option(ewp_dic[index_ilink]['data']['option'], 'IlinkIcfFile')
        self._set_option(ewp_dic[index_ilink]['data']['option'][index_option], project_dic['linker_file'])

        ilink_dic = ewp_dic[index_ilink]['data']['option']
        self._ewp_flags_set(ilink_dic, project_dic, 'ld_flags', self.FLAG_TO_IAR['ld_flags'])

    def _ewp_flags_set(self, ewp_dic_subset, project_dic, flag_type, flag_dic):
        """ Flags from misc to set to ewp project """
        try:
            if flag_type in project_dic['misc'].keys():
                # enable commands
                index_option = self._get_option(ewp_dic_subset, flag_dic['enable'])
                self._set_option(ewp_dic_subset[index_option], '1')

                index_option = self._get_option(ewp_dic_subset, flag_dic['set'])
                if type(ewp_dic_subset[index_option]['state']) != list:
                    # if it's string, only one state
                    previous_state = ewp_dic_subset[index_option]['state']
                    ewp_dic_subset[index_option]['state'] = []
                    ewp_dic_subset[index_option]['state'].append(previous_state)

                for item in project_dic['misc'][flag_type]:
                    ewp_dic_subset[index_option]['state'].append(item)
        except KeyError:
            return

    def _ewp_files_set(self, ewp_dic, project_dic):
        """ Fills files in the ewp dictionary """
        # empty any files in the template which are not grouped
        try:
            ewp_dic['project']['file'] = []
        except KeyError:
            pass
        # empty groups
        ewp_dic['project']['group'] = []
        i = 0
        for group_name, files in project_dic['groups'].items():
            ewp_dic['project']['group'].append({'name': group_name, 'file': []})
            for file in files:
                ewp_dic['project']['group'][i]['file'].append({'name': file})
            ewp_dic['project']['group'][i]['file'] = sorted(ewp_dic['project']['group'][i]['file'], key=lambda x: os.path.basename(x['name'].lower()))
            i += 1

    def _clean_xmldict_option(self, dictionary):
        """ xml parser puts None to empty fields, this functions replaces them with empty strings """
        for option in dictionary['data']['option']:
            if option['state'] is None:
                option['state'] = ''

    def _clean_xmldict_single_dic(self, dictionary):
        """ Every None replace by '' in the dic, as xml parsers puts None in those fiels, which is not valid for IAR """
        for k, v in dictionary.items():
            if v is None:
                dictionary[k] = ''

    def _clean_xmldict_ewp(self, ewp_dic):
        for setting in ewp_dic['settings']:
            if setting['name'] == 'BICOMP' or setting['name'] == 'BILINK':
                self._clean_xmldict_single_dic(setting)
            elif setting['name'] == 'BUILDACTION' or setting['name'] == 'CUSTOM':
                self._clean_xmldict_single_dic(setting['data'])
            elif 'option' in setting['data']:
                self._clean_xmldict_option(setting)

    def _ewp_set_toolchain(self, ewp_dic, toolchain):
        ewp_dic['toolchain']['name'] = toolchain

    def _ewp_set_name(self, ewp_dic, name):
        ewp_dic['name'] = name

    def _ewd_set_name(self, ewd_dic, name):
        ewd_dic['name'] = name

    def _eww_set_path_single_project(self, eww_dic, name):
        eww_dic['workspace']['project']['path'] = join('$WS_DIR$', name + '.ewp')

    def _eww_set_path_multiple_project(self, eww_dic):
        eww_dic['workspace']['project'] = []
        for project in self.workspace['projects']:
            # We check how far is project from root and workspace. IF they dont match,
            # get relpath for project and inject it into workspace
            path_project = os.path.dirname(project['files']['ewp'])
            path_workspace = os.path.dirname(self.workspace['settings']['path'] + '\\')
            destination =  os.path.join(os.path.relpath(os.getcwd(), path_project), project['files']['ewp'])
            if path_project != path_workspace:
                destination = os.path.join(os.path.relpath(os.getcwd(), path_workspace), project['files']['ewp'])
            eww_dic['workspace']['project'].append( { 'path' : join('$WS_DIR$', destination) })

    def _ewp_set_target(self, ewp_dic, mcu_def_dic):
        index_general = self._get_option(ewp_dic, 'General')
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'OGChipSelectEditMenu')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], mcu_def_dic['OGChipSelectEditMenu']['state'])
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'OGCoreOrChip')
        self._set_option(ewp_dic[index_general]['data']['option'][index_option], mcu_def_dic['OGCoreOrChip']['state'])

        # get version based on FPU
        index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'FPU2')
        if index_option == None:
            fileVersion = 1
        else:
            fileVersion = 2

        def _get_mcu_option(option):
            try:
                return mcu_def_dic[option]['state']
            except KeyError:
                return None

        # Get variant 
        Variant = _get_mcu_option('Variant')
        if not Variant:
            Variant = _get_mcu_option('CoreVariant')
        GFPUCoreSlave = _get_mcu_option('GFPUCoreSlave') 
        if not GFPUCoreSlave:
            GFPUCoreSlave = _get_mcu_option('GFPUCoreSlave2')
        GBECoreSlave = _get_mcu_option('GBECoreSlave')

        if fileVersion == 1:
            index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'Variant')
            self._set_option(ewp_dic[index_general]['data']['option'][index_option], Variant)
            index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'GFPUCoreSlave')
            self._set_option(ewp_dic[index_general]['data']['option'][index_option], GFPUCoreSlave)
        elif fileVersion == 2:
            index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'CoreVariant')
            self._set_option(ewp_dic[index_general]['data']['option'][index_option], Variant)
            index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'GFPUCoreSlave2')
            self._set_option(ewp_dic[index_general]['data']['option'][index_option], GFPUCoreSlave)
            if GBECoreSlave:
                index_option = self._get_option(ewp_dic[index_general]['data']['option'], 'GBECoreSlave')
                self._set_option(ewp_dic[index_general]['data']['option'][index_option], mcu_def_dic['GBECoreSlave']['state'])
            GFPUDeviceSlave = {
                'state': mcu_def_dic['OGChipSelectEditMenu']['state'], # should be same
                'name': 'GFPUDeviceSlave',
            }
            ewp_dic[index_general]['data']['option'].append(GFPUDeviceSlave)

    def _ewd_set_debugger(self, ewd_dic, debugger):
        try:
            debugger_def = self.definitions.debuggers[debugger['name']]
        except TypeError:
            return
        index_cspy = self._get_option(ewd_dic, 'C-SPY')
        index_option = self._get_option(ewd_dic[index_cspy]['data']['option'], 'OCDynDriverList')
        self._set_option(ewd_dic[index_cspy]['data']['option'][index_option], debugger_def['OCDynDriverList']['state'])

        # find InterfaceRadio (jtag or swd)
        try:
            debugger_interface = self.definitions.debuggers[debugger['name']]['interface']
            index_debugger_settings = self._get_option(ewd_dic, debugger_def['OCDynDriverList']['state'])
            index_option = self._get_option(ewd_dic[index_debugger_settings]['data']['option'], debugger_interface['name'])
            self._set_option(ewd_dic[index_debugger_settings]['data']['option'][index_option], debugger_def['interface'][debugger['interface']])
        except TypeError as e:
            # use default
            pass
        
class IAREmbeddedWorkbench(Tool, Builder, Exporter, IAREmbeddedWorkbenchProject):

    generated_project = {
        'path': '',
        'files': {
            'ewp': '',
            'ewd': '',
            'eww': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.definitions = IARDefinitions()
        self.workspace = workspace
        self.env_settings = env_settings
        self.ewp_file = join(self.TEMPLATE_DIR, "iar.ewp")
        self.eww_file = join(self.TEMPLATE_DIR, "iar.eww")
        self.ewd_file = join(self.TEMPLATE_DIR, "iar.ewd")

    @staticmethod
    def get_toolnames():
        return ['iar_arm']

    @staticmethod
    def get_toolchain():
        return 'iar'

    def _normalize_mcu_def(self, mcu_def):
        """ Normalizes mcu definitions to the required format """
        # hack to insert tab as IAR using tab for MCU definitions
        mcu_def['OGChipSelectEditMenu']['state'] = mcu_def['OGChipSelectEditMenu']['state'][0].replace(' ', '\t', 1)
        mcu_def['OGCoreOrChip']['state'] = mcu_def['OGCoreOrChip']['state'][0]

    def _fix_paths(self, data):
        """ All paths needs to be fixed - add PROJ_DIR prefix + normalize """
        data['include_paths'] = [join('$PROJ_DIR$', path) for path in data['include_paths']]

        if data['linker_file']:
            data['linker_file'] = join('$PROJ_DIR$', data['linker_file'])

        data['groups'] = {}
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k not in data['groups']:
                    data['groups'][k] = []
                data['groups'][k].extend([join('$PROJ_DIR$', file) for file in v])
        for k,v in data['include_files'].items():
            if k not in data['groups']:
                data['groups'][k] = []
            data['groups'][k].extend([join('$PROJ_DIR$', file) for file in v])

        # sort groups
        data['groups'] = OrderedDict(sorted(data['groups'].items(), key=lambda t: t[0]))

    def _get_default_templates(self):
        ewp_dic = xmltodict.parse(open(self.ewp_file).read())
        ewd_dic = xmltodict.parse(open(self.ewd_file).read())
        return ewp_dic, ewd_dic

    def _export_single_project(self):
        """ A single project export """
        expanded_dic = self.workspace.copy()

        self._fix_paths(expanded_dic)

        # generic tool template specified or project
        if expanded_dic['template']:
            template_ewp = False
            template_ewd = False
            # process each template file
            for template in expanded_dic['template']:
                template = join(getcwd(), template)
                # we support .ewp or .ewp.tmpl templates
                if os.path.splitext(template)[1] == '.ewp' or re.match('.*\.ewp.tmpl$', template):
                    try:
                        ewp_dic = xmltodict.parse(open(template), dict_constructor=dict)
                        template_ewp = True
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        ewp_dic = xmltodict.parse(open(self.ewp_file).read())
                if os.path.splitext(template)[1] == '.ewd' or re.match('.*\.ewd.tmpl$', template):
                    try:
                        ewd_dic = xmltodict.parse(open(template), dict_constructor=dict)
                        template_ewd = True
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        ewd_dic = xmltodict.parse(open(self.ewd_file).read())
                # handle non valid template files or not specified
                if not template_ewp and template_ewd:
                    ewp_dic, _ = self._get_default_templates() 
                elif not template_ewd and template_ewp:
                    _, ewd_dic = self._get_default_templates()
                else:
                    ewp_dic, ewd_dic = self._get_default_templates()
        elif 'iar' in self.env_settings.templates.keys():
            template_ewp = False
            template_ewd = False
            # template overrides what is set in the yaml files
            for template in self.env_settings.templates['iar']:
                template = join(getcwd(), template)
                if os.path.splitext(template)[1] == '.ewp' or re.match('.*\.ewp.tmpl$', template):
                    try:
                        ewp_dic = xmltodict.parse(open(template), dict_constructor=dict)
                        template_ewp = True
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        ewp_dic = xmltodict.parse(open(self.ewp_file).read())
                if os.path.splitext(template)[1] == '.ewd' or re.match('.*\.ewd.tmpl$', template):
                    # get ewd template
                    try:
                        ewd_dic = xmltodict.parse(open(template), dict_constructor=dict)
                        template_ewd = True
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        ewd_dic = xmltodict.parse(open(self.ewd_file).read())
                # handle non valid template files or not specified
                if not template_ewp and template_ewd:
                    ewp_dic, _ = self._get_default_templates() 
                elif not template_ewd and template_ewp:
                    _, ewd_dic = self._get_default_templates()
                else:
                    ewp_dic, ewd_dic = self._get_default_templates()
        else:
            ewp_dic, ewd_dic = self._get_default_templates()

        eww = None
        if self.workspace['singular']:
            # TODO 0xc0170: if we use here self.definitions.eww, travis fails. I cant reproduce it and dont see
            # eww used anywhere prior to exporting this.
            eww_dic = {u'workspace': {u'project': {u'path': u''}, u'batchBuild': None}}
            # set eww
            self._eww_set_path_single_project(eww_dic, expanded_dic['name'])
            eww_xml = xmltodict.unparse(eww_dic, pretty=True)
            project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' % expanded_dic['name'], expanded_dic['output_dir']['path'])


        try:
            ewp_configuration = ewp_dic['project']['configuration'][0]
            logging.debug("Provided .ewp file has multiple configuration, we use only the first one")
            ewp_dic['project']['configuration'] = ewp_dic['project']['configuration'][0]
        except KeyError:
            ewp_configuration = ewp_dic['project']['configuration']

        try:
            ewp_configuration = ewp_dic['project']['configuration'][0]
            logging.debug("Provided .ewp file has multiple configuration, we use only the first one")
            ewp_dic['project']['configuration'] = ewp_dic['project']['configuration'][0]
        except KeyError:
            ewp_configuration = ewp_dic['project']['configuration']

        # replace all None with empty strings ''
        self._clean_xmldict_ewp(ewp_configuration)
        #self._clean_xmldict_ewd(ewd_dic)

        try:
            self._ewp_set_name(ewp_configuration, expanded_dic['name'])
        except KeyError:
            raise RuntimeError("The IAR template is not valid .ewp file")

        # set ARM toolchain and project name\
        self._ewp_set_toolchain(ewp_configuration, 'ARM')

        # set common things we have for IAR
        self._ewp_general_set(ewp_configuration['settings'], expanded_dic)
        self._ewp_iccarm_set(ewp_configuration['settings'], expanded_dic)
        self._ewp_aarm_set(ewp_configuration['settings'], expanded_dic)
        self._ewp_ilink_set(ewp_configuration['settings'], expanded_dic)
        self._ewp_files_set(ewp_dic, expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if expanded_dic['target']:
            # get target definition (target + mcu)
            proj_def = ProGenDef('iar')
            if not proj_def.is_supported(expanded_dic['target'].lower()):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = proj_def.get_tool_definition(expanded_dic['target'].lower())
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
            self._normalize_mcu_def(mcu_def_dic)
            logger.debug("Mcu definitions: %s" % mcu_def_dic)
            self._ewp_set_target(ewp_configuration['settings'], mcu_def_dic)

            try:
                debugger = proj_def.get_debugger(expanded_dic['target'])
                self._ewd_set_debugger(ewd_dic['project']['configuration']['settings'], debugger)
            except KeyError as err:
                # TODO: worth reporting?
                pass

        # overwrite debugger only if defined in the project file, otherwise use either default or from template
        if expanded_dic['debugger']:
            try:
                self._ewd_set_debugger(ewd_dic['project']['configuration']['settings'], expanded_dic['debugger'])
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        self._ewd_set_name(ewd_dic['project']['configuration'], expanded_dic['name'])

        # IAR uses ident 2 spaces, encoding iso-8859-1
        ewp_xml = xmltodict.unparse(ewp_dic, encoding='iso-8859-1', pretty=True, indent='  ')
        project_path, ewp = self.gen_file_raw(ewp_xml, '%s.ewp' % expanded_dic['name'], expanded_dic['output_dir']['path'])

        ewd_xml = xmltodict.unparse(ewd_dic, encoding='iso-8859-1', pretty=True, indent='  ')
        project_path, ewd = self.gen_file_raw(ewd_xml, '%s.ewd' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        return project_path, [ewp, eww, ewd]

    def _generate_eww_file(self):
        eww_dic = xmltodict.parse(open(self.eww_file).read())
        self._eww_set_path_multiple_project(eww_dic)

        # generate the file
        eww_xml = xmltodict.unparse(eww_dic, pretty=True)
        project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' % self.workspace['settings']['name'], self.workspace['settings']['path'])
        return project_path, [eww]

    def _parse_subprocess_output(self, output):
        num_errors = 0
        lines = output.split("\n")
        error_re = '\s*Total number of errors:\s*(\d+)\s*'
        for line in lines:
            m = re.match(error_re, line)
            if m is not None:
                num_errors = m.group(1)
        return int(num_errors)

    def export_workspace(self):
        """ Export a workspace file """
        # we got a workspace defined, therefore one ewp generated only
        path, workspace = self._generate_eww_file()
        return path, [workspace]

    def export_project(self):
        """ Processes groups and misc options specific for IAR, and run generator """
        path, files = self._export_single_project()
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'] = path
        generated_projects['files']['ewp'] = files[0]
        generated_projects['files']['eww'] = files[1]
        generated_projects['files']['ewd'] = files[2]
        return generated_projects

    def build_project(self):
        """ Build IAR project """
        # > IarBuild [project_path] -build [project_name]
        proj_path = join(getcwd(), self.workspace['files']['ewp'])
        if proj_path.split('.')[-1] != 'ewp':
            proj_path += '.ewp'
        if not os.path.exists(proj_path):
            logger.debug("The file: %s does not exists, exported prior building?" % proj_path)
            return -1
        logger.debug("Building IAR project: %s" % proj_path)

        args = [join(self.env_settings.get_env_settings('iar'), 'IarBuild.exe'), proj_path, '-build', os.path.splitext(os.path.basename(self.workspace['files']['ewp']))[0]]
        logger.debug(args)

        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
        except:
            logger.error("Project: %s build failed. Please check IARBUILD path in the user_settings.py file." % self.workspace['files']['ewp'])
            return -1
        else:
            build_log_path = os.path.join(os.path.dirname(proj_path),'build_log.txt')
            with open(build_log_path, 'w') as f:
                f.write(output)
            num_errors = self._parse_subprocess_output(output)
            if num_errors == 0:
                logger.info("Project: %s build completed." % self.workspace['files']['ewp'])
                return 0
            else:
                logger.error("Project: %s build failed with %d errors" %
                             (self.workspace['files']['ewp'], num_errors))
                return -1

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['ewp'], self.workspace['files']['eww'],
            self.workspace['files']['ewd']]}

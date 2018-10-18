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

import os
import subprocess
import shutil
import logging
import xmltodict
import copy
import re
from codecs import open

from os import getcwd
from os.path import basename, join, normpath
from collections import OrderedDict
from project_generator_definitions.definitions import ProGenDef

from .tool import Tool, Builder, Exporter
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.uvision')

class uVisionDefinitions():

    debuggers = {
        'ulink2-me': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'BIN\\UL2CM3.dll',
                },
                'Utilities': {
                    'Flash2': 'BIN\\UL2CM3.DLL',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '1',
                    'pMon': 'BIN\\UL2CM3.DLL',
                },
                'SetRegEntry' : {
                    'Key' : 'UL2CM3',
                },
            },
        },
        'cmsis-dap': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'BIN\\CMSIS_AGDI.dll',
                },
                'Utilities': {
                    'Flash2': 'BIN\\CMSIS_AGDI.dll',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '12',
                    'pMon': 'BIN\\CMSIS_AGDI.dll',
                },
                'SetRegEntry' : {
                    'Key' : 'CMSIS_AGDI',
                },
            },
        },
        'j-link': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'Segger\\JL2CM3.dll',
                },
                'Utilities': {
                    'Flash2': 'Segger\\JL2CM3.dll',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '6',
                    'pMon': 'Segger\\JL2CM3.dll',
                },
                'SetRegEntry' : {
                    'Key' : 'JL2CM3',
                },
            },
        },
        'ulink-pro': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'BIN\\ULP2CM3.dll',
                },
                'Utilities': {
                    'Flash2': 'BIN\\ULP2CM3.dll',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '7',
                    'pMon': 'BIN\\ULP2CM3.DLL',
                },
                'SetRegEntry' : {
                    'Key' : 'ULP2CM3',
                },
            },
        },
        'st-link': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'STLink\\ST-LINKIII-KEIL_SWO.dll',
                },
                'Utilities': {
                    'Flash2': 'STLink\\ST-LINKIII-KEIL_SWO.dll',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '11',
                    'pMon': 'STLink\\ST-LINKIII-KEIL_SWO.dll',
                },
                'SetRegEntry' : {
                    'Key' : 'ST-LINKIII-KEIL_SWO',
                },
            },
        },
        'nu-link': {
            'uvproj': {
                'TargetDlls': {
                    'Driver': 'BIN\\Nu_Link.dll',
                },
                'Utilities': {
                    'Flash2': 'BIN\\Nu_Link.dll',
                },
            },
            'uvoptx' : {
                'DebugOpt' : {
                    'nTsel' : '9',
                    'pMon': 'NULink\\Nu_Link.dll',
                },
                'SetRegEntry' : {
                    'Key' : 'Nu_Link',
                },
            },
        },
    }

    # use cmsis-dap debugger as default
    debuggers_default = 'cmsis-dap'


class Uvision(Tool, Builder, Exporter):

    optimization_options = ['O0', 'O1', 'O2', 'O3']
    file_types = {'cpp': 8, 'c': 1, 's': 2, 'obj': 3,'o':3, 'lib': 4, 'ar': 4, 'h': 5}

    # flags mapping to uvision uvproj dics
    # for available flags, check armcc/armasm/armlink command line guide
    # this does not provide all options within a project, most usable options are
    # exposed via command line, the rest is covered via template project files
    FLAGS_TO_UVISION = {
        'asm_flags': 'Aads',
        'c_flags': 'Cads',
        'cxx_flags': 'Cads',
        'ld_flags':  'LDads',
    }

    ERRORLEVEL = {
        0: 'success (0 warnings, 0 errors)',
        1: 'warnings',
        2: 'errors',
        3: 'fatal errors',
        11: 'cant write to project file',
        12: 'device error',
        13: 'error writing',
        15: 'error reading xml file',
    }

    SUCCESSVALUE = 0
    WARNVALUE = 1

    generated_project = {
        'path': '',
        'files': {
            'uvproj': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.definitions = uVisionDefinitions()
        # workspace or project
        self.workspace = workspace
        self.env_settings = env_settings
        self.uvproj_file = join(self.TEMPLATE_DIR, "uvision.uvproj")
        self.uvmpw_file = join(self.TEMPLATE_DIR, "uvision.uvmpw")
        self.uvoptx_file = join(self.TEMPLATE_DIR, "uvision.uvoptx")

    @staticmethod
    def get_toolnames():
        return ['uvision']

    @staticmethod
    def get_toolchain():
        return 'uvision'

    def _expand_one_file(self, source, new_data, extension):
        ordered = OrderedDict() 
        ordered["FileType"] = self.file_types[extension]
        ordered["FileName"] = basename(source)
        ordered["FilePath"] = source
        return ordered

    def _normalize_mcu_def(self, mcu_def):
        for k, v in mcu_def['TargetOption'].items():
            mcu_def['TargetOption'][k] = v[0]

    def _uvproj_clean_xmldict(self, uvproj_dic):
        for k, v in uvproj_dic.items():
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

        uvproj_dic['Cads']['VariousControls']['IncludePath'] = '; '.join(project_dic['include_paths'])
        uvproj_dic['Cads']['VariousControls']['Define'] = ', '.join(project_dic['macros'])
        if project_dic['macros']:
            uvproj_dic['Aads']['VariousControls']['MiscControls'] = '--cpreproc --cpreproc_opts=-D' + ',-D'.join(project_dic['macros'])

        for misc_keys in project_dic['misc'].keys():
            # ld-flags dont follow the same as asm/c flags, why?!? Please KEIL fix this
            if misc_keys == 'ld_flags':
                for item in project_dic['misc'][misc_keys]:
                    uvproj_dic[self.FLAGS_TO_UVISION[misc_keys]]['Misc'] += ' ' + item
            else:
                for item in project_dic['misc'][misc_keys]:
                    uvproj_dic[self.FLAGS_TO_UVISION[misc_keys]]['VariousControls']['MiscControls'] += ' ' + item

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
            group['Files'] = {'File': []}
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'].append(group)
            for file in files:
                uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files']['File'].append(file)
            files = uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files']['File']
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files']['File'] = sorted(files, key=lambda x: x['FileName'].lower())
            i += 1

    def _generate_uvmpw_file(self):
        uvmpw_dic = xmltodict.parse(open(self.uvmpw_file, "rb"))
        uvmpw_dic['ProjectWorkspace']['project'] = []

        for project in self.workspace['projects']:
            # We check how far is project from root and workspace. IF they dont match,
            # get relpath for project and inject it into workspace
            path_project = os.path.dirname(project['files']['uvproj'])
            path_workspace = os.path.dirname(self.workspace['settings']['path'] + '\\')
            destination = os.path.join(os.path.relpath(self.env_settings.root, path_project), project['files']['uvproj'])
            if path_project != path_workspace:
                destination = os.path.join(os.path.relpath(self.env_settings.root, path_workspace), project['files']['uvproj'])
            uvmpw_dic['ProjectWorkspace']['project'].append({'PathAndName': destination})

        # generate the file
        uvmpw_xml = xmltodict.unparse(uvmpw_dic, pretty=True)
        project_path, uvmpw = self.gen_file_raw(uvmpw_xml, '%s.uvmpw' % self.workspace['settings']['name'], self.workspace['settings']['path'])
        return project_path, uvmpw

    def _set_target(self, expanded_dic, uvproj_dic, tool_name):
        pro_def = ProGenDef(tool_name)
        if not pro_def.is_supported(expanded_dic['target'].lower()):
            raise RuntimeError("Target %s is not supported. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
        mcu_def_dic = pro_def.get_tool_definition(expanded_dic['target'].lower())
        if not mcu_def_dic:
             raise RuntimeError(
                "Target definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
        logger.debug("Mcu definitions: %s" % mcu_def_dic)
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Device'] = mcu_def_dic['TargetOption']['Device'][0]
        uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['DeviceId'] = mcu_def_dic['TargetOption']['DeviceId'][0]
        try:
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Vendor'] = mcu_def_dic['TargetOption']['Vendor'][0]
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Cpu'] = mcu_def_dic['TargetOption']['Cpu'][0]
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['FlashDriverDll'] = str(mcu_def_dic['TargetOption']['FlashDriverDll'][0])
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile'] = mcu_def_dic['TargetOption']['SFDFile'][0]
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['RegisterFile'] = mcu_def_dic['TargetOption']['RegisterFile'][0]
        except KeyError:
            pass

        # overwrite the template if target has defined debugger
        # later progen can overwrite this if debugger is set in project data
        try:
            debugger_name = pro_def.get_debugger(expanded_dic['target'])['name']
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption']['TargetDlls']['Driver'] = self.definitions.debuggers[debugger_name]['uvproj']['TargetDlls']['Driver']
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities']['Flash2'] = self.definitions.debuggers[debugger_name]['uvproj']['Utilities']['Flash2']
        except (TypeError, KeyError) as err:
            pass
        # Support new device packs
        if 'PackID' in  mcu_def_dic['TargetOption']:
            if tool_name != 'uvision5':
                # using software packs require v5
                logger.info("The target might not be supported in %s, requires uvision5" % tool_name)
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['PackID'] = mcu_def_dic['TargetOption']['PackID'][0]

    def _uvoptx_set_debugger(self, expanded_dic, uvoptx_dic, tool_name):
        pro_def = ProGenDef(tool_name)
        if not pro_def.is_supported(expanded_dic['target'].lower()):
            raise RuntimeError("Target %s is not supported. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
        mcu_def_dic = pro_def.get_tool_definition(expanded_dic['target'].lower())
        if not mcu_def_dic:
             raise RuntimeError(
                "Target definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
        logger.debug("Mcu definitions: %s" % mcu_def_dic)

        # set the same target name FlashDriverDll config as in uvprojx file
        try:
            uvoptx_dic['ProjectOpt']['Target']['TargetName'] = expanded_dic['name']
            uvoptx_dic['ProjectOpt']['Target']['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']['Name'] = str(mcu_def_dic['TargetOption']['FlashDriverDll'][0])
        except KeyError:
            return 

        # load debugger from target dictionary or use default debugger
        try:
            debugger_dic = pro_def.get_debugger(expanded_dic['target'])
            if debugger_dic is None:
                debugger_name = self.definitions.debuggers_default
            else:
                debugger_name = debugger_dic['name']
            uvoptx_dic['ProjectOpt']['Target']['TargetOption']['DebugOpt']['nTsel'] = self.definitions.debuggers[debugger_name]['uvoptx']['DebugOpt']['nTsel']
            uvoptx_dic['ProjectOpt']['Target']['TargetOption']['DebugOpt']['pMon'] = self.definitions.debuggers[debugger_name]['uvoptx']['DebugOpt']['pMon']
            uvoptx_dic['ProjectOpt']['Target']['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']['Key'] = self.definitions.debuggers[debugger_name]['uvoptx']['SetRegEntry']['Key']
        except KeyError:
            raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

    def _export_single_project(self, tool_name):
        expanded_dic = self.workspace.copy()

        groups = self._get_groups(self.workspace)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []

        # get relative path and fix all paths within a project
        self._iterate(self.workspace, expanded_dic)

        expanded_dic['build_dir'] = '.\\' + expanded_dic['build_dir'] + '\\'

        # generic tool template specified or project
        if expanded_dic['template']:
            for template in expanded_dic['template']:
                template = join(getcwd(), template)
                if os.path.splitext(template)[1] == '.uvproj' or os.path.splitext(template)[1] == '.uvprojx' or \
                    re.match('.*\.uvproj.tmpl$', template) or re.match('.*\.uvprojx.tmpl$', template):
                    try:
                        uvproj_dic = xmltodict.parse(open(template, encoding="utf8").read())
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        return None, None
                else:
                    logger.info("Template file %s contains unknown template extension (.uvproj/x are valid). Using default one" % template)
                    uvproj_dic = xmltodict.parse(open(self.uvproj_file, "rb"))
        elif 'uvision' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            for template in self.env_settings.templates['uvision']:
                template = join(getcwd(), template)
                if os.path.splitext(template)[1] == '.uvproj' or os.path.splitext(template)[1] == '.uvprojx' or \
                    re.match('.*\.uvproj.tmpl$', template) or re.match('.*\.uvprojx.tmpl$', template):
                    try:
                        uvproj_dic = xmltodict.parse(open(template, encoding="utf8").read())
                    except IOError:
                        logger.info("Template file %s not found. Using default template" % template)
                        uvproj_dic = xmltodict.parse(open(self.uvproj_file, "rb"))
                else:
                    logger.info("Template file %s contains unknown template extension (.uvproj/x are valid). Using default one" % template)
                    uvproj_dic = xmltodict.parse(open(self.uvproj_file))
        else:
            uvproj_dic = xmltodict.parse(open(self.uvproj_file, "rb"))

        try:
            uvproj_dic['Project']['Targets']['Target']['TargetName'] = expanded_dic['name']
        except KeyError:
            raise RuntimeError("The uvision template is not valid .uvproj file")

        self._uvproj_files_set(uvproj_dic, expanded_dic)
        self._uvproj_set_CommonProperty(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['CommonProperty'], expanded_dic)
        self._uvproj_set_DebugOption(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption'], expanded_dic)
        self._uvproj_set_DllOption(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['DllOption'], expanded_dic)
        self._uvproj_set_TargetArmAds(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetArmAds'], expanded_dic)
        self._uvproj_set_TargetCommonOption(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption'], expanded_dic)
        self._uvproj_set_Utilities(
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities'], expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if tool_name == 'uvision5':
            extension = 'uvprojx'
            uvproj_dic['Project']['SchemaVersion'] = '2.1'
        else:
            extension = 'uvproj'
            uvproj_dic['Project']['SchemaVersion'] = '1.1'

        if expanded_dic['target']:
            self._set_target(expanded_dic, uvproj_dic, tool_name)

        # load debugger
        if expanded_dic['debugger']:
            try:
                uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption']['TargetDlls']['Driver'] = self.definitions.debuggers[expanded_dic['debugger']]['uvproj']['TargetDlls']['Driver']
                uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities']['Flash2'] = self.definitions.debuggers[expanded_dic['debugger']]['uvproj']['Utilities']['Flash2']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        uvproj_xml = xmltodict.unparse(uvproj_dic, pretty=True)
        project_path, uvproj = self.gen_file_raw(uvproj_xml, '%s.%s' % (expanded_dic['name'], extension), expanded_dic['output_dir']['path'])

        uvoptx = None

        # generic tool template specified
        uvoptx_dic = xmltodict.parse(open(self.uvoptx_file, "rb"))

        self._uvoptx_set_debugger(expanded_dic, uvoptx_dic, tool_name)

        # set target only if defined, otherwise use from template/default one
        if tool_name == 'uvision5':
            extension = 'uvoptx'
        else:
            extension = 'uvopt'

        # Project file
        uvoptx_xml = xmltodict.unparse(uvoptx_dic, pretty=True)
        project_path, uvoptx = self.gen_file_raw(uvoptx_xml, '%s.%s' % (expanded_dic['name'], extension), expanded_dic['output_dir']['path'])

        return project_path, [uvproj, uvoptx]

    def export_workspace(self):
        path, workspace = self._generate_uvmpw_file()
        return path, [workspace]

    def export_project(self):
        path, files = self._export_single_project('uvision') #todo: uvision will switch to uv4
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'] = path
        generated_projects['files']['uvproj'] = files[0]
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['uvproj']]}

    def _build_project(self, tool_name, extension):
        # > UV4 -b [project_path]
        path = join(self.env_settings.root, self.workspace['files'][extension])
        if path.split('.')[-1] != extension:
            path = path + extension

        if not os.path.exists(path):
            logger.debug("The file: %s does not exists, exported prior building?" % path)
            return -1

        logger.debug("Building uVision project: %s" % path)

        build_log_path = join(os.path.dirname(path),'build','build_log.txt')
        args = [self.env_settings.get_env_settings(tool_name), '-r', '-j0', '-o', build_log_path, path]
        logger.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logger.error(
                "Error whilst calling UV4: '%s'. Please set uvision path in the projects.yaml file." % self.env_settings.get_env_settings('uvision'))
            return -1
        else:
            if ret_code != self.SUCCESSVALUE and ret_code != self.WARNVALUE:
                # Seems like something went wrong.
                logger.error("Project: %s build failed with the status: %s" % (self.workspace['files'][extension], self.ERRORLEVEL.get(ret_code, "Unknown")))
                return -1
            else:
                logger.info("Project: %s build succeeded with the status: %s" % (self.workspace['files'][extension], self.ERRORLEVEL.get(ret_code, "Unknown")))
                return 0

    def build_project(self):
        return self._build_project('uvision', 'uvproj')

class Uvision5(Uvision):

    generated_project = {
        'path': '',
        'files': {
            'uvprojx': '',
            'uvoptx': '',
        }
    }

    def __init__(self, workspace, env_settings):
        super(Uvision5, self).__init__(workspace, env_settings)

    @staticmethod
    def get_toolnames():
        return ['uvision5']

    def export_project(self):
        path, files = self._export_single_project('uvision5')
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'] = path
        generated_projects['files']['uvprojx'] = files[0]
        generated_projects['files']['uvoptx'] = files[1]
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['uvprojx'], self.workspace['files']['uvoptx']]}

    def build_project(self):
        # tool_name uvision as uv4 is still used in uv5
        return self._build_project('uvision', 'uvprojx')

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

from os import getcwd
from os.path import basename, join, normpath
from collections import OrderedDict
from project_generator_definitions.definitions import ProGenDef

from .tool import Tool, Builder, Exporter
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.uvision')

class uVisionDefinitions():

    uvproj_file = OrderedDict([(u'Project', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xsi:noNamespaceSchemaLocation', u'project_proj.xsd'), (u'SchemaVersion', u'1.1'), (u'Header', u'### uVision Project, (C) Keil Software'), (u'Targets', OrderedDict([(u'Target', OrderedDict([(u'TargetName', u''), (u'ToolsetNumber', u'0x4'), (u'ToolsetName', u'ARM-ADS'), (u'TargetOption', OrderedDict([(u'TargetCommonOption', OrderedDict([(u'Device', u'LPC1768'), (u'Vendor', u'NXP'), (u'Cpu', u'IRAM(0x10000000-0x10007FFF) IRAM2(0x2007C000-0x20083FFF) IROM(0-0x7FFFF) CLOCK(12000000) CPUTYPE("Cortex-M3")'), (u'FlashUtilSpec', None), (u'StartupFile', None), (u'FlashDriverDll', u'UL2CM3(-O463 -S0 -C0 -FO7 -FD10000000 -FC800 -FN1 -FF0LPC_IAP_512 -FS00 -FL080000)'), (u'DeviceId', u'4868'), (u'RegisterFile', None), (u'MemoryEnv', None), (u'Cmp', None), (u'Asm', None), (u'Linker', None), (u'OHString', None), (u'InfinionOptionDll', None), (u'SLE66CMisc', None), (u'SLE66AMisc', None), (u'SLE66LinkerMisc', None), (u'SFDFile', u'SFD\\NXP\\LPC176x5x\\LPC176x5x.SFR'), (u'bCustSvd', u'0'), (u'UseEnv', u'0'), (u'BinPath', None), (u'IncludePath', None), (u'LibPath', None), (u'RegisterFilePath', None), (u'DBRegisterFilePath', None), (u'TargetStatus', OrderedDict([(u'Error', u'0'), (u'ExitCodeStop', u'0'), (u'ButtonStop', u'0'), (u'NotGenerated', u'0'), (u'InvalidFlash', u'1')])), (u'OutputDirectory', u'.\\build\\'), (u'OutputName', u''), (u'CreateExecutable', u'0'), (u'CreateLib', u'1'), (u'CreateHexFile', u'0'), (u'DebugInformation', u'1'), (u'BrowseInformation', u'1'), (u'ListingPath', u'.\\build'), (u'HexFormatSelection', u'1'), (u'Merge32K', u'0'), (u'CreateBatchFile', u'0'), (u'BeforeCompile', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0'), (u'nStopU1X', u'0'), (u'nStopU2X', u'0')])), (u'BeforeMake', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0'), (u'nStopB1X', u'0'), (u'nStopB2X', u'0')])), (u'AfterMake', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0')])), (u'SelectedForBatchBuild', u'0'), (u'SVCSIdString', None)])), (u'CommonProperty', OrderedDict([(u'UseCPPCompiler', u'0'), (u'RVCTCodeConst', u'0'), (u'RVCTZI', u'0'), (u'RVCTOtherData', u'0'), (u'ModuleSelection', u'0'), (u'IncludeInBuild', u'0'), (u'AlwaysBuild', u'0'), (u'GenerateAssemblyFile', u'0'), (u'AssembleAssemblyFile', u'0'), (u'PublicsOnly', u'0'), (u'StopOnExitCode', u'0'), (u'CustomArgument', None), (u'IncludeLibraryModules', None), (u'ComprImg', u'1')])), (u'DllOption', OrderedDict([(u'SimDllName', u'SARMCM3.DLL'), (u'SimDllArguments', None), (u'SimDlgDll', u'DCM.DLL'), (u'SimDlgDllArguments', u'-pCM4'), (u'TargetDllName', u'SARMCM3.DLL'), (u'TargetDllArguments', u'-MPU'), (u'TargetDlgDll', u'TCM.DLL'), (u'TargetDlgDllArguments', u'-pCM4')])), (u'DebugOption', OrderedDict([(u'OPTHX', OrderedDict([(u'HexSelection', u'1'), (u'HexRangeLowAddress', u'0'), (u'HexRangeHighAddress', u'0'), (u'HexOffset', u'0'), (u'Oh166RecLen', u'16')])), (u'Simulator', OrderedDict([(u'UseSimulator', u'0'), (u'LoadApplicationAtStartup', u'1'), (u'RunToMain', u'1'), (u'RestoreBreakpoints', u'1'), (u'RestoreWatchpoints', u'1'), (u'RestoreMemoryDisplay', u'1'), (u'RestoreFunctions', u'1'), (u'RestoreToolbox', u'1'), (u'LimitSpeedToRealTime', u'0'), (u'RestoreSysVw', u'1')])), (u'Target', OrderedDict([(u'UseTarget', u'1'), (u'LoadApplicationAtStartup', u'1'), (u'RunToMain', u'1'), (u'RestoreBreakpoints', u'1'), (u'RestoreWatchpoints', u'1'), (u'RestoreMemoryDisplay', u'1'), (u'RestoreFunctions', u'0'), (u'RestoreToolbox', u'1'), (u'RestoreTracepoints', u'0'), (u'RestoreSysVw', u'1')])), (u'RunDebugAfterBuild', u'0'), (u'TargetSelection', u'12'), (u'SimDlls', OrderedDict([(u'CpuDll', None), (u'CpuDllArguments', None), (u'PeripheralDll', None), (u'PeripheralDllArguments', None), (u'InitializationFile', None)])), (u'TargetDlls', OrderedDict([(u'CpuDll', None), (u'CpuDllArguments', None), (u'PeripheralDll', None), (u'PeripheralDllArguments', None), (u'InitializationFile', None), (u'Driver', u'BIN\\CMSIS_AGDI.dll')]))])), (u'Utilities', OrderedDict([(u'Flash1', OrderedDict([(u'UseTargetDll', u'1'), (u'UseExternalTool', u'0'), (u'RunIndependent', u'0'), (u'UpdateFlashBeforeDebugging', u'1'), (u'Capability', u'1'), (u'DriverSelection', u'4100')])), (u'bUseTDR', u'1'), (u'Flash2', u''), (u'Flash3', u''), (u'Flash4', u''), (u'pFcarmOut', None), (u'pFcarmGrp', None), (u'pFcArmRoot', None), (u'FcArmLst', u'0')])), (u'TargetArmAds', OrderedDict([(u'ArmAdsMisc', OrderedDict([(u'GenerateListings', u'0'), (u'asHll', u'1'), (u'asAsm', u'1'), (u'asMacX', u'1'), (u'asSyms', u'1'), (u'asFals', u'1'), (u'asDbgD', u'1'), (u'asForm', u'1'), (u'ldLst', u'0'), (u'ldmm', u'1'), (u'ldXref', u'1'), (u'BigEnd', u'0'), (u'AdsALst', u'1'), (u'AdsACrf', u'1'), (u'AdsANop', u'0'), (u'AdsANot', u'0'), (u'AdsLLst', u'1'), (u'AdsLmap', u'1'), (u'AdsLcgr', u'1'), (u'AdsLsym', u'1'), (u'AdsLszi', u'1'), (u'AdsLtoi', u'1'), (u'AdsLsun', u'1'), (u'AdsLven', u'1'), (u'AdsLsxf', u'1'), (u'RvctClst', u'0'), (u'GenPPlst', u'0'), (u'AdsCpuType', u'"Cortex-M3"'), (u'RvctDeviceName', None), (u'mOS', u'0'), (u'uocRom', u'0'), (u'uocRam', u'0'), (u'hadIROM', u'1'), (u'hadIRAM', u'1'), (u'hadXRAM', u'0'), (u'uocXRam', u'0'), (u'RvdsVP', u'0'), (u'hadIRAM2', u'1'), (u'hadIROM2', u'0'), (u'StupSel', u'8'), (u'useUlib', u'0'), (u'EndSel', u'0'), (u'uLtcg', u'0'), (u'RoSelD', u'3'), (u'RwSelD', u'3'), (u'CodeSel', u'0'), (u'OptFeed', u'0'), (u'NoZi1', u'0'), (u'NoZi2', u'0'), (u'NoZi3', u'0'), (u'NoZi4', u'0'), (u'NoZi5', u'0'), (u'Ro1Chk', u'0'), (u'Ro2Chk', u'0'), (u'Ro3Chk', u'0'), (u'Ir1Chk', u'1'), (u'Ir2Chk', u'0'), (u'Ra1Chk', u'0'), (u'Ra2Chk', u'0'), (u'Ra3Chk', u'0'), (u'Im1Chk', u'1'), (u'Im2Chk', u'0'), (u'OnChipMemories', OrderedDict([(u'Ocm1', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm2', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm3', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm4', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm5', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm6', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'IRAM', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x10000000'), (u'Size', u'0x8000')])), (u'IROM', OrderedDict([(u'Type', u'1'), (u'StartAddress', u'0x0'), (u'Size', u'0x80000')])), (u'XRAM', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT1', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT2', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT3', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT4', OrderedDict([(u'Type', u'1'), (u'StartAddress', u'0x0'), (u'Size', u'0x80000')])), (u'OCR_RVCT5', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT6', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT7', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT8', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT9', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x10000000'), (u'Size', u'0x8000')])), (u'OCR_RVCT10', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x2007c000'), (u'Size', u'0x8000')]))])), (u'RvctStartVector', None)])), (u'Cads', OrderedDict([(u'interw', u'0'), (u'Optim', u'2'), (u'oTime', u'0'), (u'SplitLS', u'0'), (u'OneElfS', u'0'), (u'Strict', u'0'), (u'EnumInt', u'0'), (u'PlainCh', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'wLevel', u'0'), (u'uThumb', u'0'), (u'uSurpInc', u'0'), (u'uC99', u'1'), (u'useXO', u'0'), (u'VariousControls', OrderedDict([(u'MiscControls', u''), (u'Define', None), (u'Undefine', None), (u'IncludePath', None)]))])), (u'Aads', OrderedDict([(u'interw', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'thumb', u'0'), (u'SplitLS', u'0'), (u'SwStkChk', u'0'), (u'NoWarn', u'0'), (u'uSurpInc', u'0'), (u'useXO', u'0'), (u'VariousControls', OrderedDict([(u'MiscControls', None), (u'Define', None), (u'Undefine', None), (u'IncludePath', None)]))])), (u'LDads', OrderedDict([(u'umfTarg', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'noStLib', u'0'), (u'RepFail', u'0'), (u'useFile', u'0'), (u'TextAddressRange', u'0'), (u'DataAddressRange', u'0'), (u'pXoBase', None), (u'ScatterFile', None), (u'IncludeLibs', None), (u'IncludeLibsPath', None), (u'Misc', None), (u'LinkerInputFile', None), (u'DisabledWarnings', None)]))]))])), (u'Groups', OrderedDict([(u'Group', OrderedDict([(u'GroupName', u'default'), (u'Files', None)]))]))]))]))]))])

    uvmpw_file = OrderedDict([(u'ProjectWorkspace', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xsi:noNamespaceSchemaLocation', u'project_mpw.xsd'), (u'SchemaVersion', u'1.0'), (u'Header', u'### uVision Project, (C) Keil Software'), (u'WorkspaceName', u'WorkSpace'), (u'project', OrderedDict([(u'PathAndName', None)]))]))])

    debuggers = {
        'cmsis-dap': {
            'TargetDlls': {
                'Driver': 'BIN\\CMSIS_AGDI.dll',
            },
            'Utilities': {
                'Flash2': 'BIN\\CMSIS_AGDI.dll',
            },
        },
        'j-link': {
            'TargetDlls': {
                'Driver': 'Segger\\JL2CM3.dll',
            },
            'Utilities': {
                'Flash2': 'Segger\\JL2CM3.dll',
            },
        },
        'ulink-pro': {
            'TargetDlls': {
                'Driver': 'BIN\\ULP2CM3.dll',
            },
            'Utilities': {
                'Flash2': 'BIN\\ULP2CM3.dll',
            },
        },
        'st-link': {
            'TargetDlls': {
                'Driver': 'STLink\\ST-LINKIII-KEIL_SWO.dll',
            },
            'Utilities': {
                'Flash2': 'STLink\\ST-LINKIII-KEIL_SWO.dll',
            },
        },
        'nu-link': {
            'TargetDlls': {
                'Driver': 'BIN\\Nu_Link.dll',
            },
            'Utilities': {
                'Flash2': 'BIN\\Nu_Link.dll',
            },
        },
    }


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

    @staticmethod
    def get_toolnames():
        return ['uvision']

    @staticmethod
    def get_toolchain():
        return 'uvision'

    def _expand_data(self, old_data, new_data, attribute, group):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1].lower()
                if not extension in self.file_types.keys():
                    logger.debug("Filetype for file %s not recognized" % file)
                    continue
                new_file = {"FilePath": file, "FileName": basename(file),
                            "FileType": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def _iterate(self, data, expanded_data):
        """ Iterate through all sources/includes, store the result expansion in extended dictionary. """
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                self._expand_data(data[attribute], expanded_data, attribute, group)
        for k, v in data['include_files'].items():
            if k == None:
                group = 'Includes'
            else:
                group = k
            self._expand_data(data['include_files'], expanded_data, attribute, group)

        # sort groups
        expanded_data['groups'] = OrderedDict(sorted(expanded_data['groups'].items(), key=lambda t: t[0]))

    def _get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    k = 'Sources'
                if k not in groups:
                    groups.append(k)
            for k, v in data['include_files'].items():
                if k == None:
                    k = 'Includes'
                if k not in groups:
                    groups.append(k)
        return groups

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

        uvproj_dic['Cads']['VariousControls']['IncludePath'] = '; '.join(project_dic['include_paths']).encode('utf-8')
        uvproj_dic['Cads']['VariousControls']['Define'] = ', '.join(project_dic['macros']).encode('utf-8')
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
        uvmpw_dic = self.definitions.uvmpw_file
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
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Cpu'] = mcu_def_dic['TargetOption']['Cpu'][0].encode('utf-8')
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['FlashDriverDll'] = str(mcu_def_dic['TargetOption']['FlashDriverDll'][0]).encode('utf-8')
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile'] = mcu_def_dic['TargetOption']['SFDFile'][0]
        except KeyError:
            # TODO: remove for next patch
            logger.debug("Using old definitions which are faulty for uvision, please update >v0.1.3.")

        # overwrite the template if target has defined debugger
        # later progen can overwrite this if debugger is set in project data
        try:
            debugger_name = pro_def.get_debugger(expanded_dic['target'])['name']
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption']['TargetDlls']['Driver'] = self.definitions.debuggers[debugger_name]['TargetDlls']['Driver']
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities']['Flash2'] = self.definitions.debuggers[debugger_name]['Utilities']['Flash2']
        except (TypeError, KeyError) as err:
            pass
        # Support new device packs
        if 'PackID' in  mcu_def_dic['TargetOption']:
            if tool_name != 'uvision5':
                # using software packs require v5
                logger.info("The target might not be supported in %s, requires uvision5" % tool_name)
            uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['PackID'] = mcu_def_dic['TargetOption']['PackID'][0]

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
                        uvproj_dic = xmltodict.parse(open(template))
                    except IOError:
                        logger.info("Template file %s not found" % template)
                        return None, None
                else:
                    logger.info("Template file %s contains unknown template extension (.uvproj/x are valid). Using default one" % template)
                    uvproj_dic = self.definitions.uvproj_file
        elif 'uvision' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            for template in self.env_settings.templates['uvision']:
                template = join(getcwd(), template)
                if os.path.splitext(template)[1] == '.uvproj' or os.path.splitext(template)[1] == '.uvprojx' or \
                    re.match('.*\.uvproj.tmpl$', template) or re.match('.*\.uvprojx.tmpl$', template):
                    try:
                        uvproj_dic = xmltodict.parse(open(template))
                    except IOError:
                        logger.info("Template file %s not found. Using default template" % template)
                        uvproj_dic = self.definitions.uvproj_file
                else:
                    logger.info("Template file %s contains unknown template extension (.uvproj/x are valid). Using default one" % template)
                    uvproj_dic = self.definitions.uvproj_file
        else:
            uvproj_dic = self.definitions.uvproj_file

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
                uvproj_dic['Project']['Targets']['Target']['TargetOption']['DebugOption']['TargetDlls']['Driver'] = self.definitions.debuggers[expanded_dic['debugger']]['TargetDlls']['Driver']
                uvproj_dic['Project']['Targets']['Target']['TargetOption']['Utilities']['Flash2'] = self.definitions.debuggers[expanded_dic['debugger']]['Utilities']['Flash2']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        uvproj_xml = xmltodict.unparse(uvproj_dic, pretty=True)
        path, files = self.gen_file_raw(uvproj_xml, '%s.%s' % (expanded_dic['name'], extension), expanded_dic['output_dir']['path'])
        return path, files

    def export_workspace(self):
        path, workspace = self._generate_uvmpw_file()
        return path, [workspace]

    def export_project(self):
        path, files = self._export_single_project('uvision') #todo: uvision will switch to uv4
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'] = path
        generated_projects['files']['uvproj'] = files
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

        args = [self.env_settings.get_env_settings(tool_name), '-r', '-j0', '-o', './build/build_log.txt', path]
        logger.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logger.error(
                "Error whilst calling UV4: '%s'. Please set uvision path in the projects.yaml file." % self.env_settings.get_env_settings('uvision'))
            return -1
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                logger.error("Project: %s build failed with the status: %s" % (self.ERRORLEVEL[ret_code], self.workspace['files'][extension]))
                return -1
            else:
                logger.info("Project: %s build succeeded with the status: %s" % (self.ERRORLEVEL[ret_code], self.workspace['files'][extension]))
                return 0

    def build_project(self):
        return self._build_project('uvision', 'uvproj')

class Uvision5(Uvision):

    generated_project = {
        'path': '',
        'files': {
            'uvprojx': '',
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
        generated_projects['files']['uvprojx'] = files
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['uvprojx']]}

    def build_project(self):
        # tool_name uvision as uv4 is still used in uv5
        return self._build_project('uvision', 'uvprojx')

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

from os.path import basename, join, normpath
from os import getcwd
from collections import OrderedDict
from .exporter import Exporter
from .builder import Builder
from ..targets import Targets

class uVisionDefinitions():

    uvproj_file = OrderedDict([(u'Project', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xsi:noNamespaceSchemaLocation', u'project_proj.xsd'), (u'SchemaVersion', u'1.1'), (u'Header', u'### uVision Project, (C) Keil Software'), (u'Targets', OrderedDict([(u'Target', OrderedDict([(u'TargetName', u''), (u'ToolsetNumber', u'0x4'), (u'ToolsetName', u'ARM-ADS'), (u'TargetOption', OrderedDict([(u'TargetCommonOption', OrderedDict([(u'Device', u'LPC1768'), (u'Vendor', u'NXP'), (u'Cpu', u'IRAM(0x10000000-0x10007FFF) IRAM2(0x2007C000-0x20083FFF) IROM(0-0x7FFFF) CLOCK(12000000) CPUTYPE("Cortex-M3")'), (u'FlashUtilSpec', None), (u'StartupFile', None), (u'FlashDriverDll', u'UL2CM3(-O463 -S0 -C0 -FO7 -FD10000000 -FC800 -FN1 -FF0LPC_IAP_512 -FS00 -FL080000)'), (u'DeviceId', u'4868'), (u'RegisterFile', None), (u'MemoryEnv', None), (u'Cmp', None), (u'Asm', None), (u'Linker', None), (u'OHString', None), (u'InfinionOptionDll', None), (u'SLE66CMisc', None), (u'SLE66AMisc', None), (u'SLE66LinkerMisc', None), (u'SFDFile', u'SFD\\NXP\\LPC176x5x\\LPC176x5x.SFR'), (u'bCustSvd', u'0'), (u'UseEnv', u'0'), (u'BinPath', None), (u'IncludePath', None), (u'LibPath', None), (u'RegisterFilePath', None), (u'DBRegisterFilePath', None), (u'TargetStatus', OrderedDict([(u'Error', u'0'), (u'ExitCodeStop', u'0'), (u'ButtonStop', u'0'), (u'NotGenerated', u'0'), (u'InvalidFlash', u'1')])), (u'OutputDirectory', u'.\\build\\'), (u'OutputName', u''), (u'CreateExecutable', u'0'), (u'CreateLib', u'1'), (u'CreateHexFile', u'0'), (u'DebugInformation', u'1'), (u'BrowseInformation', u'1'), (u'ListingPath', u'.\\build'), (u'HexFormatSelection', u'1'), (u'Merge32K', u'0'), (u'CreateBatchFile', u'0'), (u'BeforeCompile', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0'), (u'nStopU1X', u'0'), (u'nStopU2X', u'0')])), (u'BeforeMake', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0'), (u'nStopB1X', u'0'), (u'nStopB2X', u'0')])), (u'AfterMake', OrderedDict([(u'RunUserProg1', u'0'), (u'RunUserProg2', u'0'), (u'UserProg1Name', None), (u'UserProg2Name', None), (u'UserProg1Dos16Mode', u'0'), (u'UserProg2Dos16Mode', u'0')])), (u'SelectedForBatchBuild', u'0'), (u'SVCSIdString', None)])), (u'CommonProperty', OrderedDict([(u'UseCPPCompiler', u'0'), (u'RVCTCodeConst', u'0'), (u'RVCTZI', u'0'), (u'RVCTOtherData', u'0'), (u'ModuleSelection', u'0'), (u'IncludeInBuild', u'0'), (u'AlwaysBuild', u'0'), (u'GenerateAssemblyFile', u'0'), (u'AssembleAssemblyFile', u'0'), (u'PublicsOnly', u'0'), (u'StopOnExitCode', u'0'), (u'CustomArgument', None), (u'IncludeLibraryModules', None), (u'ComprImg', u'1')])), (u'DllOption', OrderedDict([(u'SimDllName', u'SARMCM3.DLL'), (u'SimDllArguments', None), (u'SimDlgDll', u'DCM.DLL'), (u'SimDlgDllArguments', u'-pCM4'), (u'TargetDllName', u'SARMCM3.DLL'), (u'TargetDllArguments', u'-MPU'), (u'TargetDlgDll', u'TCM.DLL'), (u'TargetDlgDllArguments', u'-pCM4')])), (u'DebugOption', OrderedDict([(u'OPTHX', OrderedDict([(u'HexSelection', u'1'), (u'HexRangeLowAddress', u'0'), (u'HexRangeHighAddress', u'0'), (u'HexOffset', u'0'), (u'Oh166RecLen', u'16')])), (u'Simulator', OrderedDict([(u'UseSimulator', u'0'), (u'LoadApplicationAtStartup', u'1'), (u'RunToMain', u'1'), (u'RestoreBreakpoints', u'1'), (u'RestoreWatchpoints', u'1'), (u'RestoreMemoryDisplay', u'1'), (u'RestoreFunctions', u'1'), (u'RestoreToolbox', u'1'), (u'LimitSpeedToRealTime', u'0'), (u'RestoreSysVw', u'1')])), (u'Target', OrderedDict([(u'UseTarget', u'1'), (u'LoadApplicationAtStartup', u'1'), (u'RunToMain', u'1'), (u'RestoreBreakpoints', u'1'), (u'RestoreWatchpoints', u'1'), (u'RestoreMemoryDisplay', u'1'), (u'RestoreFunctions', u'0'), (u'RestoreToolbox', u'1'), (u'RestoreTracepoints', u'0'), (u'RestoreSysVw', u'1')])), (u'RunDebugAfterBuild', u'0'), (u'TargetSelection', u'12'), (u'SimDlls', OrderedDict([(u'CpuDll', None), (u'CpuDllArguments', None), (u'PeripheralDll', None), (u'PeripheralDllArguments', None), (u'InitializationFile', None)])), (u'TargetDlls', OrderedDict([(u'CpuDll', None), (u'CpuDllArguments', None), (u'PeripheralDll', None), (u'PeripheralDllArguments', None), (u'InitializationFile', None), (u'Driver', u'BIN\\CMSIS_AGDI.dll')]))])), (u'Utilities', OrderedDict([(u'Flash1', OrderedDict([(u'UseTargetDll', u'1'), (u'UseExternalTool', u'0'), (u'RunIndependent', u'0'), (u'UpdateFlashBeforeDebugging', u'1'), (u'Capability', u'1'), (u'DriverSelection', u'4105')])), (u'bUseTDR', u'1'), (u'Flash2', u'BIN\\CMSIS_AGDI.dll'), (u'Flash3', u'"" ()'), (u'Flash4', None), (u'pFcarmOut', None), (u'pFcarmGrp', None), (u'pFcArmRoot', None), (u'FcArmLst', u'0')])), (u'TargetArmAds', OrderedDict([(u'ArmAdsMisc', OrderedDict([(u'GenerateListings', u'0'), (u'asHll', u'1'), (u'asAsm', u'1'), (u'asMacX', u'1'), (u'asSyms', u'1'), (u'asFals', u'1'), (u'asDbgD', u'1'), (u'asForm', u'1'), (u'ldLst', u'0'), (u'ldmm', u'1'), (u'ldXref', u'1'), (u'BigEnd', u'0'), (u'AdsALst', u'1'), (u'AdsACrf', u'1'), (u'AdsANop', u'0'), (u'AdsANot', u'0'), (u'AdsLLst', u'1'), (u'AdsLmap', u'1'), (u'AdsLcgr', u'1'), (u'AdsLsym', u'1'), (u'AdsLszi', u'1'), (u'AdsLtoi', u'1'), (u'AdsLsun', u'1'), (u'AdsLven', u'1'), (u'AdsLsxf', u'1'), (u'RvctClst', u'0'), (u'GenPPlst', u'0'), (u'AdsCpuType', u'"Cortex-M3"'), (u'RvctDeviceName', None), (u'mOS', u'0'), (u'uocRom', u'0'), (u'uocRam', u'0'), (u'hadIROM', u'1'), (u'hadIRAM', u'1'), (u'hadXRAM', u'0'), (u'uocXRam', u'0'), (u'RvdsVP', u'0'), (u'hadIRAM2', u'1'), (u'hadIROM2', u'0'), (u'StupSel', u'8'), (u'useUlib', u'0'), (u'EndSel', u'0'), (u'uLtcg', u'0'), (u'RoSelD', u'3'), (u'RwSelD', u'3'), (u'CodeSel', u'0'), (u'OptFeed', u'0'), (u'NoZi1', u'0'), (u'NoZi2', u'0'), (u'NoZi3', u'0'), (u'NoZi4', u'0'), (u'NoZi5', u'0'), (u'Ro1Chk', u'0'), (u'Ro2Chk', u'0'), (u'Ro3Chk', u'0'), (u'Ir1Chk', u'1'), (u'Ir2Chk', u'0'), (u'Ra1Chk', u'0'), (u'Ra2Chk', u'0'), (u'Ra3Chk', u'0'), (u'Im1Chk', u'1'), (u'Im2Chk', u'0'), (u'OnChipMemories', OrderedDict([(u'Ocm1', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm2', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm3', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm4', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm5', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'Ocm6', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'IRAM', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x10000000'), (u'Size', u'0x8000')])), (u'IROM', OrderedDict([(u'Type', u'1'), (u'StartAddress', u'0x0'), (u'Size', u'0x80000')])), (u'XRAM', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT1', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT2', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT3', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT4', OrderedDict([(u'Type', u'1'), (u'StartAddress', u'0x0'), (u'Size', u'0x80000')])), (u'OCR_RVCT5', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT6', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT7', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT8', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x0'), (u'Size', u'0x0')])), (u'OCR_RVCT9', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x10000000'), (u'Size', u'0x8000')])), (u'OCR_RVCT10', OrderedDict([(u'Type', u'0'), (u'StartAddress', u'0x2007c000'), (u'Size', u'0x8000')]))])), (u'RvctStartVector', None)])), (u'Cads', OrderedDict([(u'interw', u'0'), (u'Optim', u'2'), (u'oTime', u'0'), (u'SplitLS', u'0'), (u'OneElfS', u'0'), (u'Strict', u'0'), (u'EnumInt', u'0'), (u'PlainCh', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'wLevel', u'0'), (u'uThumb', u'0'), (u'uSurpInc', u'0'), (u'uC99', u'1'), (u'useXO', u'0'), (u'VariousControls', OrderedDict([(u'MiscControls', u''), (u'Define', None), (u'Undefine', None), (u'IncludePath', None)]))])), (u'Aads', OrderedDict([(u'interw', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'thumb', u'0'), (u'SplitLS', u'0'), (u'SwStkChk', u'0'), (u'NoWarn', u'0'), (u'uSurpInc', u'0'), (u'useXO', u'0'), (u'VariousControls', OrderedDict([(u'MiscControls', None), (u'Define', None), (u'Undefine', None), (u'IncludePath', None)]))])), (u'LDads', OrderedDict([(u'umfTarg', u'0'), (u'Ropi', u'0'), (u'Rwpi', u'0'), (u'noStLib', u'0'), (u'RepFail', u'0'), (u'useFile', u'0'), (u'TextAddressRange', u'0'), (u'DataAddressRange', u'0'), (u'pXoBase', None), (u'ScatterFile', None), (u'IncludeLibs', None), (u'IncludeLibsPath', None), (u'Misc', None), (u'LinkerInputFile', None), (u'DisabledWarnings', None)]))]))])), (u'Groups', OrderedDict([(u'Group', OrderedDict([(u'GroupName', u'default'), (u'Files', None)]))]))]))]))]))])
        # u'Project': {u'SchemaVersion': u'1.1', u'Header': u'### uVision Project, (C) Keil Software', u'Targets': {u'Target': {u'ToolsetNumber': u'0x4', u'ToolsetName': u'ARM-ADS', u'TargetName': u'lpc1768_blinky', u'TargetOption': {u'TargetCommonOption': {u'UseEnv': u'0', u'TargetStatus': {u'InvalidFlash': u'1', u'ExitCodeStop': u'0', u'NotGenerated': u'0', u'ButtonStop': u'0', u'Error': u'0'}, u'RegisterFile': None, u'LibPath': None, u'SFDFile': u'SFD\\NXP\\LPC176x5x\\LPC176x5x.SFR', u'BinPath': None, u'AfterMake': {u'RunUserProg2': u'0', u'UserProg1Dos16Mode': u'0', u'RunUserProg1': u'0', u'UserProg2Name': None, u'UserProg2Dos16Mode': u'0', u'UserProg1Name': None}, u'DBRegisterFilePath': None, u'BeforeMake': {u'RunUserProg2': u'0', u'UserProg1Dos16Mode': u'0', u'RunUserProg1': u'0', u'UserProg2Name': None, u'nStopB1X': u'0', u'nStopB2X': u'0', u'UserProg2Dos16Mode': u'0', u'UserProg1Name': None}, u'MemoryEnv': None, u'Vendor': u'NXP', u'SLE66AMisc': None, u'StartupFile': None, u'FlashUtilSpec': None, u'SLE66LinkerMisc': None, u'SVCSIdString': None, u'InfinionOptionDll': None, u'DebugInformation': u'1', u'Device': u'LPC1768', u'Asm': None, u'BrowseInformation': u'1', u'OutputName': u'lpc1768_blinky', u'bCustSvd': u'0', u'HexFormatSelection': u'1', u'ListingPath': u'.\\build\\lpc1768_blinky\\', u'CreateExecutable': u'0', u'BeforeCompile': {u'RunUserProg2': u'0', u'nStopU2X': u'0', u'UserProg1Dos16Mode': u'0', u'RunUserProg1': u'0', u'UserProg2Name': None, u'UserProg2Dos16Mode': u'0', u'nStopU1X': u'0', u'UserProg1Name': None}, u'OHString': None, u'CreateLib': u'1', u'SelectedForBatchBuild': u'0', u'OutputDirectory': u'.\\build\\', u'Cpu': u'IRAM(0x10000000-0x10007FFF) IRAM2(0x2007C000-0x20083FFF) IROM(0-0x7FFFF) CLOCK(12000000) CPUTYPE("Cortex-M3")', u'Merge32K': u'0', u'Cmp': None, u'CreateHexFile': u'0', u'CreateBatchFile': u'0', u'Linker': None, u'SLE66CMisc': None, u'DeviceId': u'4868', u'FlashDriverDll': u'UL2CM3(-O463 -S0 -C0 -FO7 -FD10000000 -FC800 -FN1 -FF0LPC_IAP_512 -FS00 -FL080000)', u'RegisterFilePath': None, u'IncludePath': None}, u'CommonProperty': {u'RVCTCodeConst': u'0', u'PublicsOnly': u'0', u'IncludeInBuild': u'0', u'CustomArgument': None, u'RVCTZI': u'0', u'GenerateAssemblyFile': u'0', u'ModuleSelection': u'0', u'ComprImg': u'1', u'RVCTOtherData': u'0', u'StopOnExitCode': u'0', u'UseCPPCompiler': u'0', u'AlwaysBuild': u'0', u'IncludeLibraryModules': None, u'AssembleAssemblyFile': u'0'}, u'DebugOption': {u'Target': {u'RestoreWatchpoints': u'1', u'RestoreTracepoints': u'0', u'UseTarget': u'1', u'LoadApplicationAtStartup': u'1', u'RunToMain': u'1', u'RestoreBreakpoints': u'1', u'RestoreFunctions': u'0', u'RestoreSysVw': u'1', u'RestoreToolbox': u'1', u'RestoreMemoryDisplay': u'1'}, u'Simulator': {u'RestoreWatchpoints': u'1', u'UseSimulator': u'0', u'LimitSpeedToRealTime': u'0', u'LoadApplicationAtStartup': u'1', u'RunToMain': u'1', u'RestoreBreakpoints': u'1', u'RestoreFunctions': u'1', u'RestoreSysVw': u'1', u'RestoreToolbox': u'1', u'RestoreMemoryDisplay': u'1'}, u'SimDlls': {u'CpuDll': None, u'CpuDllArguments': None, u'InitializationFile': None, u'PeripheralDllArguments': None, u'PeripheralDll': None}, u'TargetSelection': u'12', u'TargetDlls': {u'PeripheralDll': None, u'PeripheralDllArguments': None, u'CpuDll': None, u'InitializationFile': None, u'Driver': u'BIN\\CMSIS_AGDI.dll', u'CpuDllArguments': None}, u'RunDebugAfterBuild': u'0', u'OPTHX': {u'HexRangeLowAddress': u'0', u'HexSelection': u'1', u'HexRangeHighAddress': u'0', u'Oh166RecLen': u'16', u'HexOffset': u'0'}}, u'Utilities': {u'FcArmLst': u'0', u'pFcarmGrp': None, u'bUseTDR': u'1', u'Flash2': u'BIN\\CMSIS_AGDI.dll', u'Flash4': None, u'pFcArmRoot': None, u'Flash1': {u'Capability': u'1', u'DriverSelection': u'4105', u'RunIndependent': u'0', u'UpdateFlashBeforeDebugging': u'1', u'UseExternalTool': u'0', u'UseTargetDll': u'1'}, u'pFcarmOut': None, u'Flash3': u'"" ()'}, u'DllOption': {u'TargetDllName': u'SARMCM3.DLL', u'TargetDllArguments': u'-MPU', u'TargetDlgDll': u'TCM.DLL', u'TargetDlgDllArguments': u'-pCM4', u'SimDllName': u'SARMCM3.DLL', u'SimDllArguments': None, u'SimDlgDllArguments': u'-pCM4', u'SimDlgDll': u'DCM.DLL'}, u'TargetArmAds': {u'Aads': {u'SplitLS': u'0', u'SwStkChk': u'0', u'thumb': u'0', u'interw': u'0', u'VariousControls': {u'MiscControls': None, u'Define': None,  u'Undefine': None, u'IncludePath': None}, u'uSurpInc': u'0', u'NoWarn': u'0', u'Rwpi': u'0', u'useXO': u'0', u'Ropi': u'0'}, u'LDads': {u'noStLib': u'0', u'IncludeLibs': None, u'TextAddressRange': u'0', u'DisabledWarnings': None, u'RepFail': u'0', u'Misc': None, u'IncludeLibsPath': None, u'LinkerInputFile': None, u'pXoBase': None, u'ScatterFile': None, u'Rwpi': u'0', u'useFile': u'0', u'DataAddressRange': u'0', u'Ropi': u'0', u'umfTarg': u'0'}, u'Cads': {u'SplitLS': u'0', u'oTime': u'0', u'uThumb': u'0', u'Optim': u'2', u'wLevel': u'0', u'interw': u'0', u'VariousControls': {u'MiscControls': u'--debug -g --gnu', u'Define': None, u'Undefine': None, u'IncludePath': None}, u'uSurpInc': u'0', u'Strict': u'0', u'Rwpi': u'0', u'OneElfS': u'0', u'PlainCh': u'0', u'useXO': u'0', u'Ropi': u'0', u'uC99': u'1', u'EnumInt': u'0'}, u'ArmAdsMisc': {u'RvctStartVector': None, u'Ro1Chk': u'0', u'uocRom': u'0', u'mOS': u'0', u'hadIROM2': u'0', u'Ra3Chk': u'0', u'ldmm': u'1', u'AdsLszi': u'1', u'AdsLcgr': u'1', u'GenerateListings': u'0', u'RoSelD': u'3', u'asForm': u'1', u'asDbgD': u'1', u'Ro3Chk': u'0', u'hadIRAM': u'1', u'asSyms': u'1', u'Ra2Chk': u'0', u'AdsLsxf': u'1', u'AdsANop': u'0', u'AdsANot': u'0', u'uLtcg': u'0', u'Ra1Chk': u'0', u'NoZi4': u'0', u'RvctDeviceName': None, u'AdsACrf': u'1', u'AdsALst': u'1', u'OptFeed': u'0', u'AdsLmap': u'1', u'asMacX': u'1', u'Im2Chk': u'0', u'GenPPlst': u'0', u'AdsLtoi': u'1', u'AdsLsun': u'1', u'asAsm': u'1', u'AdsLven': u'1', u'RvdsVP': u'0', u'Ir2Chk': u'0', u'EndSel': u'0', u'Ir1Chk': u'1', u'hadIROM': u'1', u'ldLst': u'0', u'hadXRAM': u'0', u'StupSel': u'8', u'asFals': u'1', u'uocXRam': u'0', u'Ro2Chk': u'0', u'AdsCpuType': u'"Cortex-M3"', u'AdsLLst': u'1', u'ldXref': u'1', u'asHll': u'1', u'uocRam': u'0', u'AdsLsym': u'1', u'hadIRAM2': u'1', u'Im1Chk': u'1', u'NoZi5': u'0', u'NoZi2': u'0', u'NoZi3': u'0', u'RvctClst': u'0', u'NoZi1': u'0', u'useUlib': u'0', u'RwSelD': u'3', u'CodeSel': u'0', u'BigEnd': u'0'}}}, u'Groups': {u'Group': {u'Files': None, u'GroupName': u'default'}}}}}

    uvmpw_file = OrderedDict([(u'ProjectWorkspace', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xsi:noNamespaceSchemaLocation', u'project_mpw.xsd'), (u'SchemaVersion', u'1.0'), (u'Header', u'### uVision Project, (C) Keil Software'), (u'WorkspaceName', u'WorkSpace'), (u'project', OrderedDict([(u'PathAndName', None)]))]))])

    debuggers = {
        'cmsis-dap': {
            'TargetDlls': {
                'Driver' : 'BIN\CMSIS_AGDI.dll',
            },
        },
        'j-link': {
            'TargetDlls': {
                'Driver' : 'Segger\JL2CM3.dll',
            },
        }
    }


class Uvision(Builder, Exporter):

    optimization_options = ['O0', 'O1', 'O2', 'O3']
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_lib', 'source_files_obj']
    file_types = {'cpp': 8, 'c': 1, 's': 2, 'obj': 3,'o':3, 'lib': 4, 'ar': 4}

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

    def _expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {"FilePath": rel_path + normpath(file), "FileName": basename(file),
                            "FileType": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def _iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k, v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self._expand_data(dic, expanded_data, attribute, group, rel_path)

    def _get_groups(self, data):
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

    def _normalize_mcu_def(self, mcu_def):
        for k, v in mcu_def['TargetOption'].items():
            mcu_def['TargetOption'][k] = v[0]

    def _fix_paths(self, data, rel_path):
        data['includes'] = [join(rel_path, normpath(path)) for path in data['includes']]

        if type(data['source_files_lib'][0]) == type(dict()):
            for k in data['source_files_lib'][0].keys():
                data['source_files_lib'][0][k] = [
                    join(rel_path, normpath(path)) for path in data['source_files_lib'][0][k]]
        else:
            data['source_files_lib'][0] = [
                join(rel_path, normpath(path)) for path in data['source_files_lib'][0]]

        if type(data['source_files_obj'][0]) == type(dict()):
            for k in data['source_files_obj'][0].keys():
                data['source_files_obj'][0][k] = [
                    join(rel_path, normpath(path)) for path in data['source_files_obj'][0][k]]
        else:
            data['source_files_obj'][0] = [
                join(rel_path, normpath(path)) for path in data['source_files_obj'][0]]

        if data['linker_file']:
            data['linker_file'] = join(rel_path, normpath(data['linker_file']))

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
            group['Files'] = {'File': []}
            uvproj_dic['Project']['Targets']['Target']['Groups']['Group'].append(group)
            for file in files:
                uvproj_dic['Project']['Targets']['Target']['Groups']['Group'][i]['Files']['File'].append(file)
            i += 1

    def _generate_uvmpw_file(self):
        uvmpw_dic = self.definitions.uvmpw_file
        uvmpw_dic['ProjectWorkspace']['project'] = []

        for project in self.workspace['projects']:
            # We check how far is project from root and workspace. IF they dont match,
            # get relpath for project and inject it into workspace
            path_project = os.path.dirname(project['files']['uvproj'])
            path_workspace = os.path.dirname(self.workspace['settings']['path'] + '\\')
            if path_project != path_workspace:
                rel_path = os.path.relpath(os.getcwd(), path_workspace)
            uvmpw_dic['ProjectWorkspace']['project'].append({'PathAndName': os.path.join(rel_path, project['path'])})

        # generate the file
        uvmpw_xml = xmltodict.unparse(uvmpw_dic, pretty=True)
        project_path, uvmpw = self.gen_file_raw(uvmpw_xml, '%s.uvmpw' % self.workspace['settings']['name'], self.workspace['settings']['path'])
        return project_path, uvmpw

    def _export_single_project(self):
        expanded_dic = self.workspace.copy()

        groups = self._get_groups(self.workspace)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []

        # get relative path and fix all paths within a project
        self._iterate(self.workspace, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self._fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        expanded_dic['build_dir'] = '.\\' + expanded_dic['build_dir'] + '\\'

        # generic tool template specified or project
        if expanded_dic['template']:
            # TODO 0xc0170: template list !
            project_file = join(getcwd(), expanded_dic['template'][0])
            uvproj_dic = xmltodict.parse(file(project_file))
        elif 'uvision' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extensions for templates - support multiple files and get their extension
            # and check if user defined them correctly
            project_file = join(getcwd(), self.env_settings.templates['uvision'][0])
            uvproj_dic = xmltodict.parse(file(project_file))
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
        if expanded_dic['target']:
            target = Targets(self.env_settings.get_env_settings('definitions'))
            if not target.is_supported(expanded_dic['target'].lower(), 'uvision'):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'uvision')
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
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
        path, files = self.gen_file_raw(uvproj_xml, '%s.uvproj' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        return path, files

    def export_workspace(self):
        path, workspace = self._generate_uvmpw_file()
        return path, [workspace]

    def export_project(self):
        path, files = self._export_single_project()
        generated_projects = copy.deepcopy(self.generated_project)
        generated_projects['path'] = path
        generated_projects['files']['uvproj'] = files
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['uvproj']]}

    def supports_target(self, target):
        return target in self.definitions.mcu_def

    def build_project(self):
        # > UV4 -b [project_path]
        path = join(os.getcwd(), self.workspace['files']['uvproj'])
        if path.split('.')[-1] != 'uvproj':
            path = path + '.uvproj'
        if not os.path.exists(path):
            logging.debug("The file: %s does not exists, exported prior building?" % path)
            return

        logging.debug("Building uVision project: %s" % path)

        args = [self.env_settings.get_env_settings('uvision'), '-r', '-j0', '-o', './build/build_log.txt', path]
        logging.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error(
                "Error whilst calling UV4: '%s'. Please set uvision path in the projects.yaml file." % self.env_settings.get_env_settings('uvision'))
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                logging.error("Build failed with the status: %s" % self.ERRORLEVEL[ret_code])
            else:
                logging.info("Build succeeded with the status: %s" % self.ERRORLEVEL[ret_code])

    def get_mcu_definition(self, project_file):
        """ Parse project file to get target definition """
        project_file = join(getcwd(), project_file)
        uvproj_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        # Generic Target, should get from Target class !
        mcu = Targets().get_mcu_definition()

        mcu['tool_specific'] = {
            # legacy device
            'uvision' : {
                'TargetOption' : {
                    'Device' : [uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Device']],
                    'Vendor' : [uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Vendor']],
                    'Cpu' : [uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Cpu']],
                    'FlashDriverDll' : [uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['FlashDriverDll']],
                    'DeviceId' : [int(uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['DeviceId'])],
                    'SFDFile' : [uvproj_dic['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile']],
                }
            }
        }
        return mcu

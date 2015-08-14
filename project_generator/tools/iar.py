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
import logging
import time
import copy

import os
from os import getcwd
from os.path import join, normpath

from .tool import Tool, Builder, Exporter
from ..targets import Targets


class IARDefinitions():

    # EWP file template
    ewp_file = {
        u'project': {u'configuration': {u'debug': u'1', u'toolchain': {u'name': u''}, u'name': None, u'settings': [{u'archiveVersion': u'3', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'22', u'option': [{u'state': u'$PROJ_DIR$\\build\\Exe', u'name': u'ExePath'}, {u'state': u'$PROJ_DIR$\\build\\Obj', u'name': u'ObjPath'}, {u'state': u'$PROJ_DIR$\\build\\List', u'name': u'ListPath'}, {u'state': u'0', u'version': None, u'name': u'Variant'}, {u'state': u'0', u'name': u'GEndianMode'}, {u'state': u'0', u'version': None, u'name': u'Input variant'}, {u'state': u'Full formatting.', u'name': u'Input description'}, {u'state': u'1', u'version': None, u'name': u'Output variant'}, {u'state': u'Full formatting.', u'name': u'Output description'}, {u'state': u'0', u'name': u'GOutputBinary'}, {u'state': u'0', u'version': u'2', u'name': u'FPU'}, {u'state': u'1', u'name': u'OGCoreOrChip'}, {u'state': u'2', u'version': u'0', u'name': u'GRuntimeLibSelect'}, {u'state': u'0', u'version': u'0', u'name': u'GRuntimeLibSelectSlave'}, {u'state': u'Use the full configuration of the C/C++ runtime library. Full locale interface, C locale, file descriptor support, multibytes in printf and scanf, and hex floats in strtod.', u'name': u'RTDescription'}, {u'state': u'5.10.0.159', u'name': u'OGProductVersion'}, {u'state': u'6.30.6.53380', u'name': u'OGLastSavedByProductVersion'}, {u'state': u'0', u'name': u'GeneralEnableMisra'}, {u'state': u'0', u'name': u'GeneralMisraVerbose'}, {u'state': u'LPC1768\tNXP LPC1768', u'name': u'OGChipSelectEditMenu'}, {u'state': u'0', u'name': u'GenLowLevelInterface'}, {u'state': u'0', u'name': u'GEndianModeBE'}, {u'state': u'0', u'name': u'OGBufferedTerminalOutput'}, {u'state': u'0', u'name': u'GenStdoutInterface'}, {u'state': u'1000111110110101101110011100111111101110011011000101110111101101100111111111111100110011111001110111001111111111111111111111111', u'version': u'0', u'name': u'GeneralMisraRules98'}, {u'state': u'0', u'name': u'GeneralMisraVer'}, {u'state': u'111101110010111111111000110111111111111111111111111110010111101111010101111111111111111111111111101111111011111001111011111011111111111111111', u'version': u'0', u'name': u'GeneralMisraRules04'}, {u'state': u'$TOOLKIT_DIR$\\INC\\c\\DLib_Config_Full.h', u'name': u'RTConfigPath2'}, {u'state': u'0', u'version': None, u'name': u'GFPUCoreSlave'}, {u'state': u'0', u'version': None, u'name': u'GBECoreSlave'}, {u'state': u'0', u'name': u'OGUseCmsis'}, {u'state': u'0', u'name': u'OGUseCmsisDspLib'}]}, u'name': u'General'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'28', u'option': [{u'state': None, u'name': u'CCDefines'}, {u'state': u'0', u'name': u'CCPreprocFile'}, {u'state': u'0', u'name': u'CCPreprocComments'}, {u'state': u'0', u'name': u'CCPreprocLine'}, {u'state': u'0', u'name': u'CCListCFile'}, {u'state': u'0', u'name': u'CCListCMnemonics'}, {u'state': u'0', u'name': u'CCListCMessages'}, {u'state': u'0', u'name': u'CCListAssFile'}, {u'state': u'0', u'name': u'CCListAssSource'}, {u'state': u'[]', u'name': u'CCEnableRemarks'}, {u'state': None, u'name': u'CCDiagSuppress'}, {u'state': None, u'name': u'CCDiagRemark'}, {u'state': None, u'name': u'CCDiagWarning'}, {u'state': None, u'name': u'CCDiagError'}, {u'state': u'1', u'name': u'CCObjPrefix'}, {u'state': u'1111111', u'version': u'1', u'name': u'CCAllowList'}, {u'state': u'1', u'name': u'CCDebugInfo'}, {u'state': u'1', u'name': u'IEndianMode'}, {u'state': u'1', u'name': u'IProcessor'}, {u'state': u'0', u'name': u'IExtraOptionsCheck'}, {u'state': u'0', u'name': u'IExtraOptions'}, {u'state': u'0', u'name': u'CCLangConformance'}, {u'state': u'1', u'name': u'CCSignedPlainChar'}, {u'state': u'0', u'name': u'CCRequirePrototypes'}, {u'state': u'0', u'name': u'CCMultibyteSupport'}, {u'state': u'0', u'name': u'CCDiagWarnAreErr'}, {u'state': u'0', u'name': u'CCCompilerRuntimeInfo'}, {u'state': u'0', u'name': u'IFpuProcessor'}, {u'state': u'$FILE_BNAME$.o', u'name': u'OutputFile'}, {u'state': u'0', u'name': u'CCLibConfigHeader'}, {u'state': None, u'name': u'PreInclude'}, {u'state': u'0', u'name': u'CompilerMisraOverride'}, {u'state': None, u'name': u'CCIncludePath2'}, {u'state': u'0', u'name': u'CCStdIncCheck'}, {u'state': u'.text', u'name': u'CCCodeSection'}, {u'state': u'0', u'name': u'IInterwork2'}, {u'state': u'0', u'name': u'IProcessorMode2'}, {u'state': u'1', u'name': u'CCOptLevel'}, {u'state': u'0', u'version': u'0', u'name': u'CCOptStrategy'}, {u'state': u'0', u'name': u'CCOptLevelSlave'}, {u'state': u'1000111110110101101110011100111111101110011011000101110111101101100111111111111100110011111001110111001111111111111111111111111', u'version': u'0', u'name': u'CompilerMisraRules98'}, {u'state': u'111101110010111111111000110111111111111111111111111110010111101111010101111111111111111111111111101111111011111001111011111011111111111111111', u'version': u'0', u'name': u'CompilerMisraRules04'}, {u'state': u'0', u'name': u'CCPosIndRopi'}, {u'state': u'0', u'name': u'CCPosIndRwpi'}, {u'state': u'0', u'name': u'CCPosIndNoDynInit'}, {u'state': u'1', u'name': u'IccLang'}, {u'state': u'1', u'name': u'IccCDialect'}, {u'state': u'0', u'name': u'IccAllowVLA'}, {u'state': u'2', u'name': u'IccCppDialect'}, {u'state': u'0', u'name': u'IccExceptions'}, {u'state': u'0', u'name': u'IccRTTI'}, {u'state': u'1', u'name': u'IccStaticDestr'}, {u'state': u'0', u'name': u'IccCppInlineSemantics'}, {u'state': u'1', u'name': u'IccCmsis'}, {u'state': u'0', u'name': u'IccFloatSemantics'}]}, u'name': u'ICCARM'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'8', u'option': [{u'state': u'1', u'name': u'AObjPrefix'}, {u'state': u'0', u'name': u'AEndian'}, {u'state': u'1', u'name': u'ACaseSensitivity'}, {u'state': u'0', u'version': u'0', u'name': u'MacroChars'}, {u'state': u'0', u'name': u'AWarnEnable'}, {u'state': u'0', u'name': u'AWarnWhat'}, {u'state': u'0', u'name': u'AWarnOne'}, {u'state': u'0', u'name': u'AWarnRange1'}, {u'state': u'0', u'name': u'AWarnRange2'}, {u'state': u'1', u'name': u'ADebug'}, {u'state': u'0', u'name': u'AltRegisterNames'}, {u'state': None, u'name': u'ADefines'}, {u'state': u'0', u'name': u'AList'}, {u'state': u'0', u'name': u'AListHeader'}, {u'state': u'0', u'name': u'AListing'}, {u'state': u'0', u'name': u'Includes'}, {u'state': u'0', u'name': u'MacDefs'}, {u'state': u'1', u'name': u'MacExps'}, {u'state': u'0', u'name': u'MacExec'}, {u'state': u'0', u'name': u'OnlyAssed'}, {u'state': u'0', u'name': u'MultiLine'}, {u'state': u'0', u'name': u'PageLengthCheck'}, {u'state': u'80', u'name': u'PageLength'}, {u'state': u'4', u'name': u'TabSpacing'}, {u'state': u'0', u'name': u'AXRef'}, {u'state': u'0', u'name': u'AXRefDefines'}, {u'state': u'0', u'name': u'AXRefInternal'}, {u'state': u'0', u'name': u'AXRefDual'}, {u'state': u'0', u'name': u'AProcessor'}, {u'state': u'0', u'name': u'AFpuProcessor'}, {u'state': u'$FILE_BNAME$.o', u'name': u'AOutputFile'}, {u'state': u'0', u'name': u'AMultibyteSupport'}, {u'state': u'0', u'name': u'ALimitErrorsCheck'}, {u'state': u'100', u'name': u'ALimitErrorsEdit'}, {u'state': u'0', u'name': u'AIgnoreStdInclude'}, {u'state': None, u'name': u'AUserIncludes'}, {u'state': u'0', u'name': u'AExtraOptionsCheckV2'}, {u'state': u'0', u'name': u'AExtraOptionsV2'}]}, u'name': u'AARM'}, {u'archiveVersion': u'0', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'1', u'option': [{u'state': u'0', u'version': u'0', u'name': u'OOCOutputFormat'}, {u'state': u'0', u'name': u'OCOutputOverride'}, {u'state': u'lpc1768_blinky.bin', u'name': u'OOCOutputFile'}, {u'state': u'0', u'name': u'OOCCommandLineProducer'}, {u'state': u'1', u'name': u'OOCObjCopyEnable'}]}, u'name': u'OBJCOPY'}, {u'archiveVersion': u'3', u'data': {u'cmdline': None, u'extensions': None}, u'name': u'CUSTOM'}, {u'archiveVersion': u'0', u'data': None, u'name': u'BICOMP'}, {u'archiveVersion': u'1', u'data': {u'prebuild': None, u'postbuild': None}, u'name': u'BUILDACTION'}, {u'archiveVersion': u'0', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'14', u'option': [{u'state': None, u'name': u'IlinkOutputFile'}, {u'state': u'1', u'name': u'IlinkLibIOConfig'}, {u'state': u'0', u'name': u'XLinkMisraHandler'}, {u'state': u'0', u'name': u'IlinkInputFileSlave'}, {u'state': u'1', u'name': u'IlinkDebugInfoEnable'}, {u'state': None, u'name': u'IlinkKeepSymbols'}, {u'state': None, u'name': u'IlinkRawBinaryFile'}, {u'state': None, u'name': u'IlinkRawBinarySymbol'}, {u'state': None, u'name': u'IlinkRawBinarySegment'}, {u'state': None, u'name': u'IlinkRawBinaryAlign'}, {u'state': None, u'name': u'IlinkDefines'}, {u'state': None, u'name': u'IlinkConfigDefines'}, {u'state': u'0', u'name': u'IlinkMapFile'}, {u'state': u'0', u'name': u'IlinkLogFile'}, {u'state': u'0', u'name': u'IlinkLogInitialization'}, {u'state': u'0', u'name': u'IlinkLogModule'}, {u'state': u'0', u'name': u'IlinkLogSection'}, {u'state': u'0', u'name': u'IlinkLogVeneer'}, {u'state': u'1', u'name': u'IlinkIcfOverride'}, {u'state': None, u'name': u'IlinkIcfFile'}, {u'state': None, u'name': u'IlinkIcfFileSlave'}, {u'state': u'0', u'name': u'IlinkEnableRemarks'}, {u'state': None, u'name': u'IlinkSuppressDiags'}, {u'state': None, u'name': u'IlinkTreatAsRem'}, {u'state': None, u'name': u'IlinkTreatAsWarn'}, {u'state': None, u'name': u'IlinkTreatAsErr'}, {u'state': u'0', u'name': u'IlinkWarningsAreErrors'}, {u'state': u'0', u'name': u'IlinkUseExtraOptions'}, {u'state': None, u'name': u'IlinkExtraOptions'}, {u'state': u'1', u'name': u'IlinkLowLevelInterfaceSlave'}, {u'state': u'1', u'name': u'IlinkAutoLibEnable'}, {u'state': None, u'name': u'IlinkAdditionalLibs'}, {u'state': u'0', u'name': u'IlinkOverrideProgramEntryLabel'}, {u'state': u'0', u'name': u'IlinkProgramEntryLabelSelect'}, {u'state': u'__iar_program_start', u'name': u'IlinkProgramEntryLabel'}, {u'state': u'0', u'name': u'DoFill'}, {u'state': u'0xFF', u'name': u'FillerByte'}, {u'state': u'0x0', u'name': u'FillerStart'}, {u'state': u'0x0', u'name': u'FillerEnd'}, {u'state': u'1', u'version': u'0', u'name': u'CrcSize'}, {u'state': u'1', u'name': u'CrcAlign'}, {u'state': u'1', u'name': u'CrcAlgo'}, {u'state': u'0x11021', u'name': u'CrcPoly'}, {u'state': u'0', u'version': u'0', u'name': u'CrcCompl'}, {u'state': u'0', u'version': u'0', u'name': u'CrcBitOrder'}, {u'state': u'0x0', u'name': u'CrcInitialValue'}, {u'state': u'0', u'name': u'DoCrc'}, {u'state': u'1', u'name': u'IlinkBE8Slave'}, {u'state': u'1', u'name': u'IlinkBufferedTerminalOutput'}, {u'state': u'1', u'name': u'IlinkStdoutInterfaceSlave'}, {u'state': u'0', u'name': u'CrcFullSize'}, {u'state': u'0', u'name': u'IlinkIElfToolPostProcess'}, {u'state': u'0', u'name': u'IlinkLogAutoLibSelect'}, {u'state': u'0', u'name': u'IlinkLogRedirSymbols'}, {u'state': u'0', u'name': u'IlinkLogUnusedFragments'}, {u'state': u'0', u'name': u'IlinkCrcReverseByteOrder'}, {u'state': u'1', u'name': u'IlinkCrcUseAsInput'}, {u'state': u'0', u'name': u'IlinkOptInline'}, {u'state': u'0', u'name': u'IlinkOptExceptionsAllow'}, {u'state': u'0', u'name': u'IlinkOptExceptionsForce'}, {u'state': u'1', u'name': u'IlinkCmsis'}, {u'state': u'0', u'name': u'IlinkOptMergeDuplSections'}, {u'state': u'1', u'name': u'IlinkOptUseVfe'}, {u'state': u'0', u'name': u'IlinkOptForceVfe'}, {u'state': u'0', u'name': u'IlinkStackAnalysisEnable'}, {u'state': None, u'name': u'IlinkStackControlFile'}, {u'state': None, u'name': u'IlinkStackCallGraphFile'}]}, u'name': u'ILINK'}, {u'archiveVersion': u'0', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'0', u'option': [{u'state': None, u'name': u'IarchiveInputs'}, {u'state': u'0', u'name': u'IarchiveOverride'}, {u'state': u'###Unitialized###', u'name': u'IarchiveOutput'}]}, u'name': u'IARCHIVE'}, {u'archiveVersion': u'0', u'data': None, u'name': u'BILINK'}]}, u'fileVersion': u'2'}
    }

    # eww file template
    eww_file = {
        u'workspace': {u'project': {u'path': u''}, u'batchBuild': None}
    }

    # ewd file template
    ewd_file = {
        u'project': {u'configuration': {u'debug': u'1', u'debuggerPlugins': {u'plugin': [{u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\middleware\\HCCWare\\HCCWare.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\AVIX\\AVIX.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\CMX\\CmxArmPlugin.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\CMX\\CmxTinyArmPlugin.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\embOS\\embOSPlugin.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\MQX\\MQXRtosPlugin.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\OpenRTOS\\OpenRTOSPlugin.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\SafeRTOS\\SafeRTOSPlugin.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\ThreadX\\ThreadXArmPlugin.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\TI-RTOS\\tirtosplugin.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-II\\uCOS-II-286-KA-CSpy.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-II\\uCOS-II-KA-CSpy.ewplugin'}, {u'loadFlag': u'0', u'file': u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-III\\uCOS-III-KA-CSpy.ewplugin'}, {u'loadFlag': u'1', u'file': u'$EW_DIR$\\common\\plugins\\CodeCoverage\\CodeCoverage.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$EW_DIR$\\common\\plugins\\Orti\\Orti.ENU.ewplugin'}, {u'loadFlag': u'1', u'file': u'$EW_DIR$\\common\\plugins\\SymList\\SymList.ENU.ewplugin'}, {u'loadFlag': u'0', u'file': u'$EW_DIR$\\common\\plugins\\uCProbe\\uCProbePlugin.ENU.ewplugin'}]}, u'toolchain': {u'name': u'ARM'}, u'name': u'lpc1768_blinky', u'settings': [{u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'26', u'option': [{u'state': u'1', u'name': u'CInput'}, {u'state': u'1', u'name': u'CEndian'}, {u'state': u'1', u'name': u'CProcessor'}, {u'state': u'0', u'name': u'OCVariant'}, {u'state': u'0', u'name': u'MacOverride'}, {u'state': None, u'name': u'MacFile'}, {u'state': u'0', u'name': u'MemOverride'}, {u'state': None, u'name': u'MemFile'}, {u'state': u'1', u'name': u'RunToEnable'}, {u'state': u'main', u'name': u'RunToName'}, {u'state': u'0', u'name': u'CExtraOptionsCheck'}, {u'state': None, u'name': u'CExtraOptions'}, {u'state': u'1', u'name': u'CFpuProcessor'}, {u'state': None, u'name': u'OCDDFArgumentProducer'}, {u'state': u'0', u'name': u'OCDownloadSuppressDownload'}, {u'state': u'0', u'name': u'OCDownloadVerifyAll'}, {u'state': u'7.10.3.6927', u'name': u'OCProductVersion'}, {u'state': u'CMSISDAP_ID', u'name': u'OCDynDriverList'}, {u'state': u'7.10.3.6927', u'name': u'OCLastSavedByProductVersion'}, {u'state': u'0', u'name': u'OCDownloadAttachToProgram'}, {u'state': u'0', u'name': u'UseFlashLoader'}, {u'state': u'1', u'name': u'CLowLevel'}, {u'state': u'1', u'name': u'OCBE8Slave'}, {u'state': None, u'name': u'MacFile2'}, {u'state': u'1', u'name': u'CDevice'}, {u'state': u'$TOOLKIT_DIR$\\config\\flashloader\\NXP\\FlashNXPLPC512K_Cortex.board', u'name': u'FlashLoadersV3'}, {u'state': u'0', u'name': u'OCImagesSuppressCheck1'}, {u'state': None, u'name': u'OCImagesPath1'}, {u'state': u'0', u'name': u'OCImagesSuppressCheck2'}, {u'state': None, u'name': u'OCImagesPath2'}, {u'state': u'0', u'name': u'OCImagesSuppressCheck3'}, {u'state': None, u'name': u'OCImagesPath3'}, {u'state': u'0', u'name': u'OverrideDefFlashBoard'}, {u'state': None, u'name': u'OCImagesOffset1'}, {u'state': None, u'name': u'OCImagesOffset2'}, {u'state': None, u'name': u'OCImagesOffset3'}, {u'state': u'0', u'name': u'OCImagesUse1'}, {u'state': u'0', u'name': u'OCImagesUse2'}, {u'state': u'0', u'name': u'OCImagesUse3'}, {u'state': u'1', u'name': u'OCDeviceConfigMacroFile'}, {u'state': u'1', u'name': u'OCDebuggerExtraOption'}, {u'state': u'1', u'name': u'OCAllMTBOptions'}, {u'state': u'1', u'name': u'OCMulticoreNrOfCores'}, {u'state': u'0', u'name': u'OCMulticoreMaster'}, {u'state': u'53461', u'name': u'OCMulticorePort'}, {u'state': None, u'name': u'OCMulticoreWorkspace'}, {u'state': None, u'name': u'OCMulticoreSlaveProject'}, {u'state': None, u'name': u'OCMulticoreSlaveConfiguration'}]}, u'name': u'C-SPY'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'1', u'option': [{u'state': u'1', u'name': u'OCSimDriverInfo'}, {u'state': u'0', u'name': u'OCSimEnablePSP'}, {u'state': u'0', u'name': u'OCSimPspOverrideConfig'}, {u'state': None, u'name': u'OCSimPspConfigFile'}]}, u'name': u'ARMSIM_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'0', u'option': [{u'state': u'1', u'name': u'CCAngelHeartbeat'}, {u'state': u'1', u'name': u'CAngelCommunication'}, {u'state': u'3', u'version': u'0', u'name': u'CAngelCommBaud'}, {u'state': u'0', u'version': u'0', u'name': u'CAngelCommPort'}, {u'state': u'aaa.bbb.ccc.ddd', u'name': u'ANGELTCPIP'}, {u'state': u'0', u'name': u'DoAngelLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'AngelLogFile'}, {u'state': u'1', u'name': u'OCDriverInfo'}]}, u'name': u'ANGEL_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'2', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'1', u'name': u'CMSISDAPAttachSlave'}, {u'state': u'1', u'name': u'OCIarProbeScriptFile'}, {u'state': u'7', u'version': u'1', u'name': u'CMSISDAPResetList'}, {u'state': u'300', u'name': u'CMSISDAPHWResetDuration'}, {u'state': u'200', u'name': u'CMSISDAPHWResetDelay'}, {u'state': u'0', u'name': u'CMSISDAPDoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CMSISDAPLogFile'}, {u'state': u'0', u'name': u'CMSISDAPInterfaceRadio'}, {u'state': u'0', u'name': u'CMSISDAPInterfaceCmdLine'}, {u'state': u'0', u'name': u'CMSISDAPMultiTargetEnable'}, {u'state': u'0', u'name': u'CMSISDAPMultiTarget'}, {u'state': u'0', u'version': u'0', u'name': u'CMSISDAPJtagSpeedList'}, {u'state': u'0', u'name': u'CMSISDAPBreakpointRadio'}, {u'state': u'0', u'name': u'CMSISDAPRestoreBreakpointsCheck'}, {u'state': u'_call_main', u'name': u'CMSISDAPUpdateBreakpointsEdit'}, {u'state': u'0', u'name': u'RDICatchReset'}, {u'state': u'1', u'name': u'RDICatchUndef'}, {u'state': u'0', u'name': u'RDICatchSWI'}, {u'state': u'1', u'name': u'RDICatchData'}, {u'state': u'1', u'name': u'RDICatchPrefetch'}, {u'state': u'0', u'name': u'RDICatchIRQ'}, {u'state': u'0', u'name': u'RDICatchFIQ'}, {u'state': u'0', u'name': u'CatchCORERESET'}, {u'state': u'1', u'name': u'CatchMMERR'}, {u'state': u'1', u'name': u'CatchNOCPERR'}, {u'state': u'1', u'name': u'CatchCHKERR'}, {u'state': u'1', u'name': u'CatchSTATERR'}, {u'state': u'1', u'name': u'CatchBUSERR'}, {u'state': u'1', u'name': u'CatchINTERR'}, {u'state': u'1', u'name': u'CatchHARDERR'}, {u'state': u'0', u'name': u'CatchDummy'}, {u'state': u'0', u'name': u'CMSISDAPMultiCPUEnable'}, {u'state': u'0', u'name': u'CMSISDAPMultiCPUNumber'}, {u'state': u'0', u'name': u'OCProbeCfgOverride'}, {u'state': None, u'name': u'OCProbeConfig'}, {u'state': u'0', u'name': u'CMSISDAPProbeConfigRadio'}, {u'state': u'0', u'name': u'CMSISDAPSelectedCPUBehaviour'}, {u'state': None, u'name': u'ICpuName'}, {u'state': u'1', u'name': u'OCJetEmuParams'}]}, u'name': u'CMSISDAP_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'0', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'aaa.bbb.ccc.ddd', u'name': u'TCPIP'}, {u'state': u'0', u'name': u'DoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'LogFile'}, {u'state': u'0', u'name': u'CCJTagBreakpointRadio'}, {u'state': u'0', u'name': u'CCJTagDoUpdateBreakpoints'}, {u'state': u'_call_main', u'name': u'CCJTagUpdateBreakpoints'}]}, u'name': u'GDBSERVER_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'1', u'option': [{u'state': u'0', u'name': u'CRomLogFileCheck'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CRomLogFileEditB'}, {u'state': u'0', u'version': u'0', u'name': u'CRomCommPort'}, {u'state': u'7', u'version': u'0', u'name': u'CRomCommBaud'}, {u'state': u'1', u'name': u'OCDriverInfo'}]}, u'name': u'IARROM_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'3', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'1', u'name': u'IjetAttachSlave'}, {u'state': u'1', u'name': u'OCIarProbeScriptFile'}, {u'state': u'10', u'version': u'1', u'name': u'IjetResetList'}, {u'state': u'300', u'name': u'IjetHWResetDuration'}, {u'state': u'200', u'name': u'IjetHWResetDelay'}, {u'state': u'1', u'name': u'IjetPowerFromProbe'}, {u'state': u'0', u'name': u'IjetPowerRadio'}, {u'state': u'0', u'name': u'IjetDoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'IjetLogFile'}, {u'state': u'0', u'name': u'IjetInterfaceRadio'}, {u'state': u'0', u'name': u'IjetInterfaceCmdLine'}, {u'state': u'0', u'name': u'IjetMultiTargetEnable'}, {u'state': u'0', u'name': u'IjetMultiTarget'}, {u'state': u'0', u'name': u'IjetScanChainNonARMDevices'}, {u'state': u'0', u'name': u'IjetIRLength'}, {u'state': u'0', u'version': u'0', u'name': u'IjetJtagSpeedList'}, {u'state': u'0', u'name': u'IjetProtocolRadio'}, {u'state': u'0', u'name': u'IjetSwoPin'}, {u'state': u'72.0', u'name': u'IjetCpuClockEdit'}, {u'state': u'0', u'version': u'1', u'name': u'IjetSwoPrescalerList'}, {u'state': u'0', u'name': u'IjetBreakpointRadio'}, {u'state': u'0', u'name': u'IjetRestoreBreakpointsCheck'}, {u'state': u'_call_main', u'name': u'IjetUpdateBreakpointsEdit'}, {u'state': u'0', u'name': u'RDICatchReset'}, {u'state': u'1', u'name': u'RDICatchUndef'}, {u'state': u'0', u'name': u'RDICatchSWI'}, {u'state': u'1', u'name': u'RDICatchData'}, {u'state': u'1', u'name': u'RDICatchPrefetch'}, {u'state': u'0', u'name': u'RDICatchIRQ'}, {u'state': u'0', u'name': u'RDICatchFIQ'}, {u'state': u'0', u'name': u'CatchCORERESET'}, {u'state': u'1', u'name': u'CatchMMERR'}, {u'state': u'1', u'name': u'CatchNOCPERR'}, {u'state': u'1', u'name': u'CatchCHKERR'}, {u'state': u'1', u'name': u'CatchSTATERR'}, {u'state': u'1', u'name': u'CatchBUSERR'}, {u'state': u'1', u'name': u'CatchINTERR'}, {u'state': u'1', u'name': u'CatchHARDERR'}, {u'state': u'0', u'name': u'CatchDummy'}, {u'state': u'0', u'name': u'OCProbeCfgOverride'}, {u'state': None, u'name': u'OCProbeConfig'}, {u'state': u'0', u'name': u'IjetProbeConfigRadio'}, {u'state': u'0', u'name': u'IjetMultiCPUEnable'}, {u'state': u'0', u'name': u'IjetMultiCPUNumber'}, {u'state': u'0', u'name': u'IjetSelectedCPUBehaviour'}, {u'state': None, u'name': u'ICpuName'}, {u'state': u'1', u'name': u'OCJetEmuParams'}]}, u'name': u'IJET_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'15', u'option': [{u'state': u'1000', u'name': u'JLinkSpeed'}, {u'state': u'0', u'name': u'CCJLinkDoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CCJLinkLogFile'}, {u'state': u'0', u'name': u'CCJLinkHWResetDelay'}, {u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'1000', u'name': u'JLinkInitialSpeed'}, {u'state': u'0', u'name': u'CCDoJlinkMultiTarget'}, {u'state': u'0', u'name': u'CCScanChainNonARMDevices'}, {u'state': u'0', u'name': u'CCJLinkMultiTarget'}, {u'state': u'0', u'name': u'CCJLinkIRLength'}, {u'state': u'0', u'name': u'CCJLinkCommRadio'}, {u'state': u'aaa.bbb.ccc.ddd', u'name': u'CCJLinkTCPIP'}, {u'state': u'0', u'name': u'CCJLinkSpeedRadioV2'}, {u'state': u'1', u'version': u'1', u'name': u'CCUSBDevice'}, {u'state': u'0', u'name': u'CCRDICatchReset'}, {u'state': u'0', u'name': u'CCRDICatchUndef'}, {u'state': u'0', u'name': u'CCRDICatchSWI'}, {u'state': u'0', u'name': u'CCRDICatchData'}, {u'state': u'0', u'name': u'CCRDICatchPrefetch'}, {u'state': u'0', u'name': u'CCRDICatchIRQ'}, {u'state': u'0', u'name': u'CCRDICatchFIQ'}, {u'state': u'0', u'name': u'CCJLinkBreakpointRadio'}, {u'state': u'0', u'name': u'CCJLinkDoUpdateBreakpoints'}, {u'state': u'_call_main', u'name': u'CCJLinkUpdateBreakpoints'}, {u'state': u'0', u'name': u'CCJLinkInterfaceRadio'}, {u'state': u'1', u'name': u'OCJLinkAttachSlave'}, {u'state': u'7', u'version': u'6', u'name': u'CCJLinkResetList'}, {u'state': u'0', u'name': u'CCJLinkInterfaceCmdLine'}, {u'state': u'0', u'name': u'CCCatchCORERESET'}, {u'state': u'0', u'name': u'CCCatchMMERR'}, {u'state': u'0', u'name': u'CCCatchNOCPERR'}, {u'state': u'0', u'name': u'CCCatchCHRERR'}, {u'state': u'0', u'name': u'CCCatchSTATERR'}, {u'state': u'0', u'name': u'CCCatchBUSERR'}, {u'state': u'0', u'name': u'CCCatchINTERR'}, {u'state': u'0', u'name': u'CCCatchHARDERR'}, {u'state': u'0', u'name': u'CCCatchDummy'}, {u'state': u'1', u'name': u'OCJLinkScriptFile'}, {u'state': None, u'name': u'CCJLinkUsbSerialNo'}, {u'state': u'0', u'version': u'0', u'name': u'CCTcpIpAlt'}, {u'state': None, u'name': u'CCJLinkTcpIpSerialNo'}, {u'state': u'72.0', u'name': u'CCCpuClockEdit'}, {u'state': u'0', u'name': u'CCSwoClockAuto'}, {u'state': u'2000', u'name': u'CCSwoClockEdit'}, {u'state': u'0', u'name': u'OCJLinkTraceSource'}, {u'state': u'0', u'name': u'OCJLinkTraceSourceDummy'}, {u'state': u'1', u'name': u'OCJLinkDeviceName'}]}, u'name': u'JLINK_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'2', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'500', u'name': u'LmiftdiSpeed'}, {u'state': u'0', u'name': u'CCLmiftdiDoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CCLmiftdiLogFile'}, {u'state': u'0', u'name': u'CCLmiFtdiInterfaceRadio'}, {u'state': u'0', u'name': u'CCLmiFtdiInterfaceCmdLine'}]}, u'name': u'LMIFTDI_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'3', u'option': [{u'state': u'0', u'version': u'0', u'name': u'jtag'}, {u'state': u'1', u'name': u'EmuSpeed'}, {u'state': u'aaa.bbb.ccc.ddd', u'name': u'TCPIP'}, {u'state': u'0', u'name': u'DoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'LogFile'}, {u'state': u'0', u'name': u'DoEmuMultiTarget'}, {u'state': u'0@ARM7TDMI', u'name': u'EmuMultiTarget'}, {u'state': u'0', u'name': u'EmuHWReset'}, {u'state': u'4', u'version': u'0', u'name': u'CEmuCommBaud'}, {u'state': u'0', u'version': u'0', u'name': u'CEmuCommPort'}, {u'state': u'0', u'version': u'0', u'name': u'jtago'}, {u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'0x00800000', u'name': u'UnusedAddr'}, {u'state': None, u'name': u'CCMacraigorHWResetDelay'}, {u'state': u'0', u'name': u'CCJTagBreakpointRadio'}, {u'state': u'0', u'name': u'CCJTagDoUpdateBreakpoints'}, {u'state': u'_call_main', u'name': u'CCJTagUpdateBreakpoints'}, {u'state': u'0', u'name': u'CCMacraigorInterfaceRadio'}, {u'state': u'0', u'name': u'CCMacraigorInterfaceCmdLine'}]}, u'name': u'MACRAIGOR_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'1', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'1', u'name': u'OCPEMicroAttachSlave'}, {u'state': u'0', u'version': u'0', u'name': u'CCPEMicroInterfaceList'}, {u'state': None, u'name': u'CCPEMicroResetDelay'}, {u'state': u'#UNINITIALIZED#', u'name': u'CCPEMicroJtagSpeed'}, {u'state': u'0', u'name': u'CCJPEMicroShowSettings'}, {u'state': u'0', u'name': u'DoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'LogFile'}, {u'state': u'0', u'version': u'0', u'name': u'CCPEMicroUSBDevice'}, {u'state': u'0', u'version': u'0', u'name': u'CCPEMicroSerialPort'}, {u'state': u'1', u'name': u'CCJPEMicroTCPIPAutoScanNetwork'}, {u'state': u'10.0.0.1', u'name': u'CCPEMicroTCPIP'}, {u'state': u'0', u'name': u'CCPEMicroCommCmdLineProducer'}, {u'state': u'0', u'name': u'CCSTLinkInterfaceRadio'}, {u'state': u'0', u'name': u'CCSTLinkInterfaceCmdLine'}]}, u'name': u'PEMICRO_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'2', u'option': [{u'state': u'###Uninitialized###', u'name': u'CRDIDriverDll'}, {u'state': u'0', u'name': u'CRDILogFileCheck'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CRDILogFileEdit'}, {u'state': u'0', u'name': u'CCRDIHWReset'}, {u'state': u'0', u'name': u'CCRDICatchReset'}, {u'state': u'0', u'name': u'CCRDICatchUndef'}, {u'state': u'0', u'name': u'CCRDICatchSWI'}, {u'state': u'0', u'name': u'CCRDICatchData'}, {u'state': u'0', u'name': u'CCRDICatchPrefetch'}, {u'state': u'0', u'name': u'CCRDICatchIRQ'}, {u'state': u'0', u'name': u'CCRDICatchFIQ'}, {u'state': u'1', u'name': u'OCDriverInfo'}]}, u'name': u'RDI_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'2', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'0', u'name': u'CCSTLinkInterfaceRadio'}, {u'state': u'0', u'name': u'CCSTLinkInterfaceCmdLine'}, {u'state': u'0', u'version': u'1', u'name': u'CCSTLinkResetList'}, {u'state': u'72.0', u'name': u'CCCpuClockEdit'}, {u'state': u'0', u'name': u'CCSwoClockAuto'}, {u'state': u'2000', u'name': u'CCSwoClockEdit'}]}, u'name': u'STLINK_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'0', u'option': [{u'state': u'###Uninitialized###', u'name': u'CThirdPartyDriverDll'}, {u'state': u'0', u'name': u'CThirdPartyLogFileCheck'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'CThirdPartyLogFileEditB'}, {u'state': u'1', u'name': u'OCDriverInfo'}]}, u'name': u'THIRDPARTY_ID'}, {u'archiveVersion': u'2', u'data': {u'wantNonLocal': u'1', u'debug': u'1', u'version': u'2', u'option': [{u'state': u'1', u'name': u'OCDriverInfo'}, {u'state': u'1', u'name': u'OCXDS100AttachSlave'}, {u'state': u'0', u'name': u'TIPackageOverride'}, {u'state': None, u'name': u'TIPackage'}, {u'state': u'0', u'version': u'1', u'name': u'CCXds100InterfaceList'}, {u'state': None, u'name': u'BoardFile'}, {u'state': u'0', u'name': u'DoLogfile'}, {u'state': u'$PROJ_DIR$\\cspycomm.log', u'name': u'LogFile'}]}, u'name': u'XDS100_ID'}]}, u'fileVersion': u'2'}
    }

    # TODO: Fix this with the parser!
    debuggers = {
        'cmsis-dap': {
            'OCDynDriverList': {
                'state' : 'CMSISDAP_ID',
            },
        },
        'j-link': {
            'OCDynDriverList': {
                'state' : 'JLINK_ID',
            },
        }
    }


class IAREmbeddedWorkbenchProject:

    def _set_option(self, settings, value):
        settings['state'] = value

    def _set_multiple_option(self, settings, value_list):
        settings['state'] = []
        for value in value_list:
            settings['state'].append(value)

    def _ewp_general_set(self, ewp_dic, project_dic):
        index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ExePath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'Exe'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ObjPath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'Obj'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'ListPath')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], join('$PROJ_DIR$', project_dic['build_dir'], 'List'))
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'GOutputBinary')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], 0 if project_dic['output_type'] == 'exe' else 1)

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
        additional_libs = []
        for k,v in project_dic['source_files_lib'].items():
            if len(v):
                additional_libs.append(v)
        for k,v in project_dic['source_files_obj'].items():
            if len(v):
                additional_libs.append(v)
        if len(additional_libs):
            index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'], 'IlinkAdditionalLibs')
            self._set_multiple_option(ewp_dic['project']['configuration']['settings'][index_ilink]['data']['option'][index_option], additional_libs)

    def _ewp_files_set(self, ewp_dic, project_dic):
        ewp_dic['project']['group'] = []
        i = 0
        for group_name, files in project_dic['groups'].items():
            ewp_dic['project']['group'].append({'name': group_name, 'file': []})
            for file in files:
                ewp_dic['project']['group'][i]['file'].append({'name': file})
            i += 1

    def _clean_xmldict_option(self, dictionary):
            for option in dictionary['data']['option']:
                if option['state'] is None:
                    option['state'] = ''

    def _clean_xmldict_single_dic(self, dictionary):
            for k, v in dictionary.items():
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

    def _ewp_set_toolchain(self, ewp_dic, toolchain):
        ewp_dic['project']['configuration']['toolchain']['name'] = toolchain

    def _ewp_set_name(self, ewp_dic, name):
        ewp_dic['project']['configuration']['name'] = name

    def _eww_set_path_single_project(self, eww_dic, name):
        eww_dic['workspace']['project']['path'] = join('$WS_DIR$', name + '.ewp')

    def _eww_set_path_multiple_project(self, eww_dic):
        eww_dic['workspace']['project'] = []
        for project in self.workspace['projects']:
            # We check how far is project from root and workspace. IF they dont match,
            # get relpath for project and inject it into workspace
            path_project = os.path.dirname(project['files']['ewp'])
            path_workspace = os.path.dirname(self.workspace['settings']['path'] + '\\')
            if path_project != path_workspace:
                rel_path = os.path.relpath(os.getcwd(), path_workspace)
            eww_dic['workspace']['project'].append( { 'path' : join('$WS_DIR$', os.path.join(rel_path, project['files']['ewp'])) })

    def _ewp_set_target(self, ewp_dic, mcu_def_dic):
        index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OGChipSelectEditMenu')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], mcu_def_dic['OGChipSelectEditMenu']['state'])
        index_option = self._get_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OGCoreOrChip')
        self._set_option(ewp_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], mcu_def_dic['OGCoreOrChip']['state'])

    def _ewd_set_debugger(self, ewd_dic, ewp_dic, debugger_def_dic):
        index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
        index_cspy = self._get_option(ewd_dic['project']['configuration']['settings'], 'C-SPY')
        index_option = self._get_option(ewd_dic['project']['configuration']['settings'][index_general]['data']['option'], 'OCDynDriverList')
        self._set_option(ewd_dic['project']['configuration']['settings'][index_general]['data']['option'][index_option], debugger_def_dic['OCDynDriverList']['state'])

class IAREmbeddedWorkbench(Tool, Builder, Exporter, IAREmbeddedWorkbenchProject):

    source_files_dic = [
        'source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']

    core_dic = {
        "cortex-m0":  34,
        "cortex-m0+": 35,
        "cortex-m3":  38,
        "cortex-m4":  39,
        "cortex-m4f": 40,
    }

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

    @staticmethod
    def get_toolnames():
        return ['iar_arm']

    @staticmethod
    def get_toolchain():
        return 'iar'

    def _expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ Groups expansion for Sources. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_data['groups'][group].append(join('$PROJ_DIR$', rel_path, normpath(file)))

    def _iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                self._expand_data(data[attribute], expanded_data, attribute, group, rel_path)

    def _get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for k, v in data[attribute].items():
                if k == None:
                    k = 'Sources'
                if k not in groups:
                    groups.append(k)
        return groups

    def _find_target_core(self, data):
        """ Sets Target core. """
        for k, v in self.core_dic.items():
            if k == data['core']:
                return v
        return IAREmbeddedWorkbench.core_dic['cortex-m0']  # def cortex-m0 if not defined otherwise

    def _parse_specific_options(self, data):
        """ Parse all IAR specific settings. """
        data['iar_settings'].update(copy.deepcopy(
            self.definitions.iar_settings))  # set specific options to default values
        for dic in data['misc']:
            # for k,v in dic.items():
            self.set_specific_settings(dic, data)

    def _set_specific_settings(self, value_list, data):
        for k, v in value_list.items():
            for option in v.items():
                for key, value in v['data']['option'].items():
                    result = 0
                    if value[0] == 'enable':
                        result = 1
                    data['iar_settings'][k]['data']['option'][key]['state'] = result

    def _normalize_mcu_def(self, mcu_def):
        """ Normalizes mcu definitions to the required format """
        # hack to insert tab as IAR using tab for MCU definitions
        mcu_def['OGChipSelectEditMenu']['state'] = mcu_def['OGChipSelectEditMenu']['state'][0].replace(' ', '\t', 1)
        mcu_def['OGCoreOrChip']['state'] = mcu_def['OGCoreOrChip']['state'][0]

    def _fix_paths(self, data, rel_path):
        """ All paths needs to be fixed - add PROJ_DIR prefix + normalize """
        data['includes'] = [join('$PROJ_DIR$', rel_path, normpath(path)) for path in data['includes']]

        for k in data['source_files_lib'].keys():
            data['source_files_lib'][k] = [
                join('$PROJ_DIR$', rel_path, normpath(path)) for path in data['source_files_lib'][k]]

        for k in data['source_files_obj'].keys():
            data['source_files_obj'][k] = [
                join('$PROJ_DIR$', rel_path, normpath(path)) for path in data['source_files_obj'][k]]
            
        if data['linker_file']:
            data['linker_file'] = join('$PROJ_DIR$', rel_path, normpath(data['linker_file']))

    def _get_option(self, settings, find_key):
        for option in settings:
            if option['name'] == find_key:
                return settings.index(option)

    def _export_single_project(self):
        expanded_dic = self.workspace.copy()

        groups = self._get_groups(expanded_dic)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self._iterate(self.workspace, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self._fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        # generic tool template specified or project
        if expanded_dic['template']:
            # TODO 0xc0170: template list !
            project_file = join(getcwd(), expanded_dic['template'][0])
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        elif 'iar' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), self.env_settings.templates['iar'][0])
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        else:
            ewp_dic = self.definitions.ewp_file

        # TODO 0xc0170: add ewd file parsing and support
        ewd_dic = self.definitions.ewd_file

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
            self._ewp_set_name(ewp_dic, expanded_dic['name'])
        except KeyError:
            raise RuntimeError("The IAR template is not valid .ewp file")

        # replace all None with empty strings ''
        self._clean_xmldict_ewp(ewp_dic)
        #self._clean_xmldict_ewd(ewd_dic)

        # set ARM toolchain and project name\
        self._ewp_set_toolchain(ewp_dic, 'ARM')

        # set common things we have for IAR
        self._ewp_general_set(ewp_dic, expanded_dic)
        self._ewp_iccarm_set(ewp_dic, expanded_dic)
        self._ewp_aarm_set(ewp_dic, expanded_dic)
        self._ewp_ilink_set(ewp_dic, expanded_dic)
        self._ewp_files_set(ewp_dic, expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if expanded_dic['target']:
            # get target definition (target + mcu)
            target = Targets(self.env_settings.get_env_settings('definitions'))
            if not target.is_supported(expanded_dic['target'].lower(), 'iar'):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'iar')
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
            self._normalize_mcu_def(mcu_def_dic)
            logging.debug("Mcu definitions: %s" % mcu_def_dic)
            self._ewp_set_target(ewp_dic, mcu_def_dic)

        # overwrite debugger only if defined in the project file, otherwise use either default or from template
        if expanded_dic['debugger']:
            try:
                debugger = self.definitions.debuggers[expanded_dic['debugger']]
                self._ewd_set_debugger(ewd_dic, ewp_dic, debugger)
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        ewp_xml = xmltodict.unparse(ewp_dic, pretty=True)
        project_path, ewp = self.gen_file_raw(ewp_xml, '%s.ewp' % expanded_dic['name'], expanded_dic['output_dir']['path'])

        ewd_xml = xmltodict.unparse(ewd_dic, pretty=True)
        project_path, ewd = self.gen_file_raw(ewd_xml, '%s.ewd' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        return project_path, [ewp, eww, ewd]

    def _generate_eww_file(self):
        eww_dic = self.definitions.eww_file
        self._eww_set_path_multiple_project(eww_dic)

        # generate the file
        eww_xml = xmltodict.unparse(eww_dic, pretty=True)
        project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' % self.workspace['settings']['name'], self.workspace['settings']['path'])
        return project_path, [eww]

    def export_workspace(self):
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
        """ Build IAR project. """
        # > IarBuild [project_path] -build [project_name]
        proj_path = join(getcwd(), self.workspace['files']['ewp'])
        if proj_path.split('.')[-1] != 'ewp':
            proj_path += '.ewp'
        if not os.path.exists(proj_path):
            logging.debug("The file: %s does not exists, exported prior building?" % proj_path)
            return
        logging.debug("Building IAR project: %s" % proj_path)

        args = [join(self.env_settings.get_env_settings('iar'), 'IarBuild.exe'), proj_path, '-build', os.path.splitext(os.path.basename(self.workspace['files']['ewp']))[0]]
        logging.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error("Error whilst calling IarBuild. Please check IARBUILD path in the user_settings.py file.")
        else:
            # no IAR doc describes errors from IarBuild
            logging.info("Build completed.")

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['ewp'], self.workspace['files']['eww'],
            self.workspace['files']['ewd']]}

    def get_mcu_definition(self, project_file):
        """ Parse project file to get mcu definition """
        project_file = join(getcwd(), project_file)
        ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)

        mcu = Targets().get_mcu_definition()

        # we take 0 configuration or just configuration, as multiple configuration possibl
        # debug, release, for mcu - does not matter, try and adjust
        try:
            index_general = self._get_option(ewp_dic['project']['configuration'][0]['settings'], 'General')
            configuration = ewp_dic['project']['configuration'][0]
        except KeyError:
            index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
            configuration = ewp_dic['project']['configuration']
        index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'OGChipSelectEditMenu')
        OGChipSelectEditMenu = configuration['settings'][index_general]['data']['option'][index_option]

        mcu['tool_specific'] = {
            'iar' : {
                'OGChipSelectEditMenu' : {
                    'state' : [OGChipSelectEditMenu['state'].replace('\t', ' ', 1)],
                },
                'OGCoreOrChip' : {
                    'state' : [1],
                },
            }
        }
        return mcu

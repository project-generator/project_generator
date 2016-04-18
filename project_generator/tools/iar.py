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
import time
import copy

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

    # ewp file template
    # Using ordereddict, as IAR template should be ordered as parsed (IAR will reorganize the xml structure if not)
    ewp_file = OrderedDict([(u'project', OrderedDict([(u'fileVersion', u'2'), (u'configuration', OrderedDict([(u'name', None), (u'toolchain', OrderedDict([(u'name', u'ARM')])), (u'debug', u'1'), (u'settings', [OrderedDict([(u'name', u'General'), (u'archiveVersion', u'3'), (u'data', OrderedDict([(u'version', u'22'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'GRuntimeLibThreads'), (u'state', u'0')]), OrderedDict([(u'name', u'ExePath'), (u'state', u'$PROJ_DIR$\\build\\Exe')]), OrderedDict([(u'name', u'ObjPath'), (u'state', u'$PROJ_DIR$\\build\\Obj')]), OrderedDict([(u'name', u'ListPath'), (u'state', u'$PROJ_DIR$\\build\\List')]), OrderedDict([(u'name', u'Variant'), (u'version', u'20'), (u'state', u'40')]), OrderedDict([(u'name', u'GEndianMode'), (u'state', u'0')]), OrderedDict([(u'name', u'Input variant'), (u'version', u'3'), (u'state', u'1')]), OrderedDict([(u'name', u'Input description'), (u'state', u'Full formatting.')]), OrderedDict([(u'name', u'Output variant'), (u'version', u'2'), (u'state', u'3')]), OrderedDict([(u'name', u'Output description'), (u'state', u'No specifier a, A.')]), OrderedDict([(u'name', u'GOutputBinary'), (u'state', u'0')]), OrderedDict([(u'name', u'FPU'), (u'version', u'2'), (u'state', u'5')]), OrderedDict([(u'name', u'OGCoreOrChip'), (u'state', u'1')]), OrderedDict([(u'name', u'GRuntimeLibSelect'), (u'version', u'0'), (u'state', u'2')]), OrderedDict([(u'name', u'GRuntimeLibSelectSlave'), (u'version', u'0'), (u'state', u'2')]), OrderedDict([(u'name', u'RTDescription'), (u'state', u'Use the full configuration of the C/C++ runtime library. Full locale interface, C locale, file descriptor support, multibytes in printf and scanf, and hex floats in strtod.')]), OrderedDict([(u'name', u'OGProductVersion'), (u'state', u'5.10.0.159')]), OrderedDict([(u'name', u'OGLastSavedByProductVersion'), (u'state', u'7.10.3.6927')]), OrderedDict([(u'name', u'GeneralEnableMisra'), (u'state', u'0')]), OrderedDict([(u'name', u'GeneralMisraVerbose'), (u'state', u'0')]), OrderedDict([(u'name', u'OGChipSelectEditMenu'), (u'state', u'MK64FN1M0xxx12\tFreescale MK64FN1M0xxx12')]), OrderedDict([(u'name', u'GenLowLevelInterface'), (u'state', u'0')]), OrderedDict([(u'name', u'GEndianModeBE'), (u'state', u'1')]), OrderedDict([(u'name', u'OGBufferedTerminalOutput'), (u'state', u'0')]), OrderedDict([(u'name', u'GenStdoutInterface'), (u'state', u'0')]), OrderedDict([(u'name', u'GeneralMisraRules98'), (u'version', u'0'), (u'state', u'1000111110110101101110011100111111101110011011000101110111101101100111111111111100110011111001110111001111111111111111111111111')]), OrderedDict([(u'name', u'GeneralMisraVer'), (u'state', u'0')]), OrderedDict([(u'name', u'GeneralMisraRules04'), (u'version', u'0'), (u'state', u'111101110010111111111000110111111111111111111111111110010111101111010101111111111111111111111111101111111011111001111011111011111111111111111')]), OrderedDict([(u'name', u'RTConfigPath2'), (u'state', u'$TOOLKIT_DIR$\\INC\\c\\DLib_Config_Full.h')]), OrderedDict([(u'name', u'GFPUCoreSlave'), (u'version', u'20'), (u'state', u'40')]), OrderedDict([(u'name', u'GBECoreSlave'), (u'version', u'20'), (u'state', u'40')]), OrderedDict([(u'name', u'OGUseCmsis'), (u'state', u'0')]), OrderedDict([(u'name', u'OGUseCmsisDspLib'), (u'state', u'0')])])]))]), OrderedDict([(u'name', u'ICCARM'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'31'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CCOptimizationNoSizeConstraints'), (u'state', u'0')]), OrderedDict([(u'name', u'CCDefines'), (u'state', [u'TARGET_K64F', u'TARGET_M4', u'TARGET_Freescale', u'__CORTEX_M4', u'ARM_MATH_CM4', u'__MBED__=1', u'CPU_MK64FN1M0VMD12', u'FSL_RTOS_MBED'])]), OrderedDict([(u'name', u'CCPreprocFile'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPreprocComments'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPreprocLine'), (u'state', u'0')]), OrderedDict([(u'name', u'CCListCFile'), (u'state', u'0')]), OrderedDict([(u'name', u'CCListCMnemonics'), (u'state', u'0')]), OrderedDict([(u'name', u'CCListCMessages'), (u'state', u'0')]), OrderedDict([(u'name', u'CCListAssFile'), (u'state', u'0')]), OrderedDict([(u'name', u'CCListAssSource'), (u'state', u'0')]), OrderedDict([(u'name', u'CCEnableRemarks'), (u'state', u'0')]), OrderedDict([(u'name', u'CCDiagSuppress'), (u'state', None)]), OrderedDict([(u'name', u'CCDiagRemark'), (u'state', None)]), OrderedDict([(u'name', u'CCDiagWarning'), (u'state', None)]), OrderedDict([(u'name', u'CCDiagError'), (u'state', None)]), OrderedDict([(u'name', u'CCObjPrefix'), (u'state', u'1')]), OrderedDict([(u'name', u'CCAllowList'), (u'version', u'1'), (u'state', u'00000000')]), OrderedDict([(u'name', u'CCDebugInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'IEndianMode'), (u'state', u'1')]), OrderedDict([(u'name', u'IProcessor'), (u'state', u'1')]), OrderedDict([(u'name', u'IExtraOptionsCheck'), (u'state', u'')]), OrderedDict([(u'name', u'IExtraOptions'), (u'state', u'')]), OrderedDict([(u'name', u'CCLangConformance'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSignedPlainChar'), (u'state', u'1')]), OrderedDict([(u'name', u'CCRequirePrototypes'), (u'state', u'0')]), OrderedDict([(u'name', u'CCMultibyteSupport'), (u'state', u'0')]), OrderedDict([(u'name', u'CCDiagWarnAreErr'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCompilerRuntimeInfo'), (u'state', u'0')]), OrderedDict([(u'name', u'IFpuProcessor'), (u'state', u'0')]), OrderedDict([(u'name', u'OutputFile'), (u'state', u'$FILE_BNAME$.o')]), OrderedDict([(u'name', u'CCLibConfigHeader'), (u'state', u'0')]), OrderedDict([(u'name', u'PreInclude'), (u'state', None)]), OrderedDict([(u'name', u'CompilerMisraOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'CCIncludePath2'), (u'state', None)]), OrderedDict([(u'name', u'CCStdIncCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCodeSection'), (u'state', u'.text')]), OrderedDict([(u'name', u'IInterwork2'), (u'state', u'0')]), OrderedDict([(u'name', u'IProcessorMode2'), (u'state', u'1')]), OrderedDict([(u'name', u'CCOptLevel'), (u'state', u'1')]), OrderedDict([(u'name', u'CCOptStrategy'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCOptLevelSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'CompilerMisraRules98'), (u'version', u'0'), (u'state', u'1000111110110101101110011100111111101110011011000101110111101101100111111111111100110011111001110111001111111111111111111111111')]), OrderedDict([(u'name', u'CompilerMisraRules04'), (u'version', u'0'), (u'state', u'111101110010111111111000110111111111111111111111111110010111101111010101111111111111111111111111101111111011111001111011111011111111111111111')]), OrderedDict([(u'name', u'CCPosIndRopi'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPosIndRwpi'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPosIndNoDynInit'), (u'state', u'0')]), OrderedDict([(u'name', u'IccLang'), (u'state', u'1')]), OrderedDict([(u'name', u'IccCDialect'), (u'state', u'1')]), OrderedDict([(u'name', u'IccAllowVLA'), (u'state', u'0')]), OrderedDict([(u'name', u'IccCppDialect'), (u'state', u'2')]), OrderedDict([(u'name', u'IccExceptions'), (u'state', u'0')]), OrderedDict([(u'name', u'IccRTTI'), (u'state', u'0')]), OrderedDict([(u'name', u'IccStaticDestr'), (u'state', u'1')]), OrderedDict([(u'name', u'IccCppInlineSemantics'), (u'state', u'0')]), OrderedDict([(u'name', u'IccCmsis'), (u'state', u'1')]), OrderedDict([(u'name', u'IccFloatSemantics'), (u'state', u'0')]), OrderedDict([(u'name', u'CCNoLiteralPool'), (u'state', u'0')]), OrderedDict([(u'name', u'CCOptStrategySlave'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCGuardCalls'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'AARM'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'9'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'AObjPrefix'), (u'state', u'1')]), OrderedDict([(u'name', u'AEndian'), (u'state', u'0')]), OrderedDict([(u'name', u'ACaseSensitivity'), (u'state', u'1')]), OrderedDict([(u'name', u'MacroChars'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'AWarnEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'AWarnWhat'), (u'state', u'0')]), OrderedDict([(u'name', u'AWarnOne'), (u'state', u'0')]), OrderedDict([(u'name', u'AWarnRange1'), (u'state', u'0')]), OrderedDict([(u'name', u'AWarnRange2'), (u'state', u'0')]), OrderedDict([(u'name', u'ADebug'), (u'state', u'1')]), OrderedDict([(u'name', u'AltRegisterNames'), (u'state', u'0')]), OrderedDict([(u'name', u'ADefines'), (u'state', None)]), OrderedDict([(u'name', u'AList'), (u'state', u'0')]), OrderedDict([(u'name', u'AListHeader'), (u'state', u'0')]), OrderedDict([(u'name', u'AListing'), (u'state', u'0')]), OrderedDict([(u'name', u'Includes'), (u'state', u'0')]), OrderedDict([(u'name', u'MacDefs'), (u'state', u'0')]), OrderedDict([(u'name', u'MacExps'), (u'state', u'1')]), OrderedDict([(u'name', u'MacExec'), (u'state', u'0')]), OrderedDict([(u'name', u'OnlyAssed'), (u'state', u'0')]), OrderedDict([(u'name', u'MultiLine'), (u'state', u'0')]), OrderedDict([(u'name', u'PageLengthCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'PageLength'), (u'state', u'80')]), OrderedDict([(u'name', u'TabSpacing'), (u'state', u'4')]), OrderedDict([(u'name', u'AXRef'), (u'state', u'0')]), OrderedDict([(u'name', u'AXRefDefines'), (u'state', u'0')]), OrderedDict([(u'name', u'AXRefInternal'), (u'state', u'0')]), OrderedDict([(u'name', u'AXRefDual'), (u'state', u'0')]), OrderedDict([(u'name', u'AProcessor'), (u'state', u'0')]), OrderedDict([(u'name', u'AFpuProcessor'), (u'state', u'0')]), OrderedDict([(u'name', u'AOutputFile'), (u'state', u'$FILE_BNAME$.o')]), OrderedDict([(u'name', u'AMultibyteSupport'), (u'state', u'0')]), OrderedDict([(u'name', u'ALimitErrorsCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'ALimitErrorsEdit'), (u'state', u'100')]), OrderedDict([(u'name', u'AIgnoreStdInclude'), (u'state', u'0')]), OrderedDict([(u'name', u'AUserIncludes'), (u'state', None)]), OrderedDict([(u'name', u'AExtraOptionsCheckV2'), (u'state', u'0')]), OrderedDict([(u'name', u'AExtraOptionsV2'), (u'state', u'0')]), OrderedDict([(u'name', u'AsmNoLiteralPool'), (u'state', u'0')])])]))]), OrderedDict([(u'name', u'OBJCOPY'), (u'archiveVersion', u'0'), (u'data', OrderedDict([(u'version', u'1'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OOCOutputFormat'), (u'version', u'2'), (u'state', u'0')]), OrderedDict([(u'name', u'OCOutputOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'OOCOutputFile'), (u'state', u'name.srec')]), OrderedDict([(u'name', u'OOCCommandLineProducer'), (u'state', u'0')]), OrderedDict([(u'name', u'OOCObjCopyEnable'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'CUSTOM'), (u'archiveVersion', u'3'), (u'data', OrderedDict([(u'extensions', None), (u'cmdline', None)]))]), OrderedDict([(u'name', u'BICOMP'), (u'archiveVersion', u'0'), (u'data', None)]), OrderedDict([(u'name', u'BUILDACTION'), (u'archiveVersion', u'1'), (u'data', OrderedDict([(u'prebuild', None), (u'postbuild', None)]))]), OrderedDict([(u'name', u'ILINK'), (u'archiveVersion', u'0'), (u'data', OrderedDict([(u'version', u'16'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'IlinkOutputFile'), (u'state', u'name.out')]), OrderedDict([(u'name', u'IlinkLibIOConfig'), (u'state', u'1')]), OrderedDict([(u'name', u'XLinkMisraHandler'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkInputFileSlave'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkDebugInfoEnable'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkKeepSymbols'), (u'state', None)]), OrderedDict([(u'name', u'IlinkRawBinaryFile'), (u'state', None)]), OrderedDict([(u'name', u'IlinkRawBinarySymbol'), (u'state', None)]), OrderedDict([(u'name', u'IlinkRawBinarySegment'), (u'state', None)]), OrderedDict([(u'name', u'IlinkRawBinaryAlign'), (u'state', None)]), OrderedDict([(u'name', u'IlinkDefines'), (u'state', None)]), OrderedDict([(u'name', u'IlinkConfigDefines'), (u'state', None)]), OrderedDict([(u'name', u'IlinkMapFile'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogFile'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogInitialization'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogModule'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogSection'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogVeneer'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkIcfOverride'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkIcfFile'), (u'state', None)]), OrderedDict([(u'name', u'IlinkIcfFileSlave'), (u'state', None)]), OrderedDict([(u'name', u'IlinkEnableRemarks'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkSuppressDiags'), (u'state', None)]), OrderedDict([(u'name', u'IlinkTreatAsRem'), (u'state', None)]), OrderedDict([(u'name', u'IlinkTreatAsWarn'), (u'state', None)]), OrderedDict([(u'name', u'IlinkTreatAsErr'), (u'state', None)]), OrderedDict([(u'name', u'IlinkWarningsAreErrors'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkUseExtraOptions'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkExtraOptions'), (u'state', None)]), OrderedDict([(u'name', u'IlinkLowLevelInterfaceSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkAutoLibEnable'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkAdditionalLibs'), (u'state', None)]), OrderedDict([(u'name', u'IlinkOverrideProgramEntryLabel'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkProgramEntryLabelSelect'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkProgramEntryLabel'), (u'state', u'__iar_program_start')]), OrderedDict([(u'name', u'DoFill'), (u'state', u'0')]), OrderedDict([(u'name', u'FillerByte'), (u'state', u'0xFF')]), OrderedDict([(u'name', u'FillerStart'), (u'state', u'0x0')]), OrderedDict([(u'name', u'FillerEnd'), (u'state', u'0x0')]), OrderedDict([(u'name', u'CrcSize'), (u'version', u'0'), (u'state', u'1')]), OrderedDict([(u'name', u'CrcAlign'), (u'state', u'1')]), OrderedDict([(u'name', u'CrcPoly'), (u'state', u'0x11021')]), OrderedDict([(u'name', u'CrcCompl'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CrcBitOrder'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CrcInitialValue'), (u'state', u'0x0')]), OrderedDict([(u'name', u'DoCrc'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkBE8Slave'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkBufferedTerminalOutput'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkStdoutInterfaceSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'CrcFullSize'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkIElfToolPostProcess'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogAutoLibSelect'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogRedirSymbols'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkLogUnusedFragments'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkCrcReverseByteOrder'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkCrcUseAsInput'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkOptInline'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkOptExceptionsAllow'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkOptExceptionsForce'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkCmsis'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkOptMergeDuplSections'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkOptUseVfe'), (u'state', u'1')]), OrderedDict([(u'name', u'IlinkOptForceVfe'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkStackAnalysisEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkStackControlFile'), (u'state', None)]), OrderedDict([(u'name', u'IlinkStackCallGraphFile'), (u'state', None)]), OrderedDict([(u'name', u'CrcAlgorithm'), (u'version', u'0'), (u'state', u'1')]), OrderedDict([(u'name', u'CrcUnitSize'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'IlinkThreadsSlave'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'IARCHIVE'), (u'archiveVersion', u'0'), (u'data', OrderedDict([(u'version', u'0'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'IarchiveInputs'), (u'state', None)]), OrderedDict([(u'name', u'IarchiveOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'IarchiveOutput'), (u'state', u'###Unitialized###')])])]))]), OrderedDict([(u'name', u'BILINK'), (u'archiveVersion', u'0'), (u'data', None)])])]))]))])

    # eww file template
    eww_file = {
        u'workspace': {u'project': {u'path': u''}, u'batchBuild': None}
    }

    # ewd file template
    ewd_file = OrderedDict([(u'project', OrderedDict([(u'fileVersion', u'2'), (u'configuration', OrderedDict([(u'name', None), (u'toolchain', OrderedDict([(u'name', u'ARM')])), (u'debug', u'1'), (u'settings', [OrderedDict([(u'name', u'C-SPY'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'26'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CInput'), (u'state', u'1')]), OrderedDict([(u'name', u'CEndian'), (u'state', u'1')]), OrderedDict([(u'name', u'CProcessor'), (u'state', u'1')]), OrderedDict([(u'name', u'OCVariant'), (u'state', u'0')]), OrderedDict([(u'name', u'MacOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'MacFile'), (u'state', None)]), OrderedDict([(u'name', u'MemOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'MemFile'), (u'state', u'$TOOLKIT_DIR$\\CONFIG\\debugger\\Freescale\\MK64FN1M0xxx12.ddf')]), OrderedDict([(u'name', u'RunToEnable'), (u'state', u'1')]), OrderedDict([(u'name', u'RunToName'), (u'state', u'main')]), OrderedDict([(u'name', u'CExtraOptionsCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CExtraOptions'), (u'state', None)]), OrderedDict([(u'name', u'CFpuProcessor'), (u'state', u'1')]), OrderedDict([(u'name', u'OCDDFArgumentProducer'), (u'state', None)]), OrderedDict([(u'name', u'OCDownloadSuppressDownload'), (u'state', u'0')]), OrderedDict([(u'name', u'OCDownloadVerifyAll'), (u'state', u'0')]), OrderedDict([(u'name', u'OCProductVersion'), (u'state', u'7.10.3.6927')]), OrderedDict([(u'name', u'OCDynDriverList'), (u'state', u'CMSISDAP_ID')]), OrderedDict([(u'name', u'OCLastSavedByProductVersion'), (u'state', u'7.10.3.6927')]), OrderedDict([(u'name', u'OCDownloadAttachToProgram'), (u'state', u'0')]), OrderedDict([(u'name', u'UseFlashLoader'), (u'state', u'0')]), OrderedDict([(u'name', u'CLowLevel'), (u'state', u'1')]), OrderedDict([(u'name', u'OCBE8Slave'), (u'state', u'1')]), OrderedDict([(u'name', u'MacFile2'), (u'state', None)]), OrderedDict([(u'name', u'CDevice'), (u'state', u'1')]), OrderedDict([(u'name', u'FlashLoadersV3'), (u'state', u'$TOOLKIT_DIR$\\config\\flashloader\\Freescale\\FlashK64Fxxx128K.board')]), OrderedDict([(u'name', u'OCImagesSuppressCheck1'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesPath1'), (u'state', None)]), OrderedDict([(u'name', u'OCImagesSuppressCheck2'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesPath2'), (u'state', None)]), OrderedDict([(u'name', u'OCImagesSuppressCheck3'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesPath3'), (u'state', None)]), OrderedDict([(u'name', u'OverrideDefFlashBoard'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesOffset1'), (u'state', None)]), OrderedDict([(u'name', u'OCImagesOffset2'), (u'state', None)]), OrderedDict([(u'name', u'OCImagesOffset3'), (u'state', None)]), OrderedDict([(u'name', u'OCImagesUse1'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesUse2'), (u'state', u'0')]), OrderedDict([(u'name', u'OCImagesUse3'), (u'state', u'0')]), OrderedDict([(u'name', u'OCDeviceConfigMacroFile'), (u'state', u'1')]), OrderedDict([(u'name', u'OCDebuggerExtraOption'), (u'state', u'1')]), OrderedDict([(u'name', u'OCAllMTBOptions'), (u'state', u'1')]), OrderedDict([(u'name', u'OCMulticoreNrOfCores'), (u'state', u'1')]), OrderedDict([(u'name', u'OCMulticoreMaster'), (u'state', u'0')]), OrderedDict([(u'name', u'OCMulticorePort'), (u'state', u'53461')]), OrderedDict([(u'name', u'OCMulticoreWorkspace'), (u'state', None)]), OrderedDict([(u'name', u'OCMulticoreSlaveProject'), (u'state', None)]), OrderedDict([(u'name', u'OCMulticoreSlaveConfiguration'), (u'state', None)])])]))]), OrderedDict([(u'name', u'ARMSIM_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'1'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCSimDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'OCSimEnablePSP'), (u'state', u'0')]), OrderedDict([(u'name', u'OCSimPspOverrideConfig'), (u'state', u'0')]), OrderedDict([(u'name', u'OCSimPspConfigFile'), (u'state', None)])])]))]), OrderedDict([(u'name', u'ANGEL_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'0'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CCAngelHeartbeat'), (u'state', u'1')]), OrderedDict([(u'name', u'CAngelCommunication'), (u'state', u'1')]), OrderedDict([(u'name', u'CAngelCommBaud'), (u'version', u'0'), (u'state', u'3')]), OrderedDict([(u'name', u'CAngelCommPort'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'ANGELTCPIP'), (u'state', u'aaa.bbb.ccc.ddd')]), OrderedDict([(u'name', u'DoAngelLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'AngelLogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'CMSISDAP_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'2'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'CMSISDAPAttachSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'OCIarProbeScriptFile'), (u'state', u'1')]), OrderedDict([(u'name', u'CMSISDAPResetList'), (u'version', u'1'), (u'state', u'10')]), OrderedDict([(u'name', u'CMSISDAPHWResetDuration'), (u'state', u'300')]), OrderedDict([(u'name', u'CMSISDAPHWResetDelay'), (u'state', u'200')]), OrderedDict([(u'name', u'CMSISDAPDoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPLogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CMSISDAPInterfaceRadio'), (u'state', u'1')]), OrderedDict([(u'name', u'CMSISDAPInterfaceCmdLine'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPMultiTargetEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPMultiTarget'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPJtagSpeedList'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPBreakpointRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPRestoreBreakpointsCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPUpdateBreakpointsEdit'), (u'state', u'_call_main')]), OrderedDict([(u'name', u'RDICatchReset'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchUndef'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchSWI'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchData'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchPrefetch'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchIRQ'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchFIQ'), (u'state', u'0')]), OrderedDict([(u'name', u'CatchCORERESET'), (u'state', u'0')]), OrderedDict([(u'name', u'CatchMMERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchNOCPERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchCHKERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchSTATERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchBUSERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchINTERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchHARDERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchDummy'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPMultiCPUEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPMultiCPUNumber'), (u'state', u'0')]), OrderedDict([(u'name', u'OCProbeCfgOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'OCProbeConfig'), (u'state', None)]), OrderedDict([(u'name', u'CMSISDAPProbeConfigRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CMSISDAPSelectedCPUBehaviour'), (u'state', u'0')]), OrderedDict([(u'name', u'ICpuName'), (u'state', None)]), OrderedDict([(u'name', u'OCJetEmuParams'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'GDBSERVER_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'0'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'TCPIP'), (u'state', u'aaa.bbb.ccc.ddd')]), OrderedDict([(u'name', u'DoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'LogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CCJTagBreakpointRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJTagDoUpdateBreakpoints'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJTagUpdateBreakpoints'), (u'state', u'_call_main')])])]))]), OrderedDict([(u'name', u'IARROM_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'1'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CRomLogFileCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CRomLogFileEditB'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CRomCommPort'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CRomCommBaud'), (u'version', u'0'), (u'state', u'7')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'IJET_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'3'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'IjetAttachSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'OCIarProbeScriptFile'), (u'state', u'1')]), OrderedDict([(u'name', u'IjetResetList'), (u'version', u'1'), (u'state', u'10')]), OrderedDict([(u'name', u'IjetHWResetDuration'), (u'state', u'300')]), OrderedDict([(u'name', u'IjetHWResetDelay'), (u'state', u'200')]), OrderedDict([(u'name', u'IjetPowerFromProbe'), (u'state', u'1')]), OrderedDict([(u'name', u'IjetPowerRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetDoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetLogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'IjetInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetInterfaceCmdLine'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetMultiTargetEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetMultiTarget'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetScanChainNonARMDevices'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetIRLength'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetJtagSpeedList'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetProtocolRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetSwoPin'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetCpuClockEdit'), (u'state', u'72.0')]), OrderedDict([(u'name', u'IjetSwoPrescalerList'), (u'version', u'1'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetBreakpointRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetRestoreBreakpointsCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetUpdateBreakpointsEdit'), (u'state', u'_call_main')]), OrderedDict([(u'name', u'RDICatchReset'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchUndef'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchSWI'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchData'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchPrefetch'), (u'state', u'1')]), OrderedDict([(u'name', u'RDICatchIRQ'), (u'state', u'0')]), OrderedDict([(u'name', u'RDICatchFIQ'), (u'state', u'0')]), OrderedDict([(u'name', u'CatchCORERESET'), (u'state', u'0')]), OrderedDict([(u'name', u'CatchMMERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchNOCPERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchCHKERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchSTATERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchBUSERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchINTERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchHARDERR'), (u'state', u'1')]), OrderedDict([(u'name', u'CatchDummy'), (u'state', u'0')]), OrderedDict([(u'name', u'OCProbeCfgOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'OCProbeConfig'), (u'state', None)]), OrderedDict([(u'name', u'IjetProbeConfigRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetMultiCPUEnable'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetMultiCPUNumber'), (u'state', u'0')]), OrderedDict([(u'name', u'IjetSelectedCPUBehaviour'), (u'state', u'0')]), OrderedDict([(u'name', u'ICpuName'), (u'state', None)]), OrderedDict([(u'name', u'OCJetEmuParams'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'JLINK_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'15'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'JLinkSpeed'), (u'state', u'1000')]), OrderedDict([(u'name', u'CCJLinkDoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkLogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CCJLinkHWResetDelay'), (u'state', u'0')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'JLinkInitialSpeed'), (u'state', u'1000')]), OrderedDict([(u'name', u'CCDoJlinkMultiTarget'), (u'state', u'0')]), OrderedDict([(u'name', u'CCScanChainNonARMDevices'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkMultiTarget'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkIRLength'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkCommRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkTCPIP'), (u'state', u'aaa.bbb.ccc.ddd')]), OrderedDict([(u'name', u'CCJLinkSpeedRadioV2'), (u'state', u'0')]), OrderedDict([(u'name', u'CCUSBDevice'), (u'version', u'1'), (u'state', u'1')]), OrderedDict([(u'name', u'CCRDICatchReset'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchUndef'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchSWI'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchData'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchPrefetch'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchIRQ'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchFIQ'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkBreakpointRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkDoUpdateBreakpoints'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkUpdateBreakpoints'), (u'state', u'_call_main')]), OrderedDict([(u'name', u'CCJLinkInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'OCJLinkAttachSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'CCJLinkResetList'), (u'version', u'6'), (u'state', u'5')]), OrderedDict([(u'name', u'CCJLinkInterfaceCmdLine'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchCORERESET'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchMMERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchNOCPERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchCHRERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchSTATERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchBUSERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchINTERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchHARDERR'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCatchDummy'), (u'state', u'0')]), OrderedDict([(u'name', u'OCJLinkScriptFile'), (u'state', u'1')]), OrderedDict([(u'name', u'CCJLinkUsbSerialNo'), (u'state', None)]), OrderedDict([(u'name', u'CCTcpIpAlt'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJLinkTcpIpSerialNo'), (u'state', None)]), OrderedDict([(u'name', u'CCCpuClockEdit'), (u'state', u'72.0')]), OrderedDict([(u'name', u'CCSwoClockAuto'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSwoClockEdit'), (u'state', u'2000')]), OrderedDict([(u'name', u'OCJLinkTraceSource'), (u'state', u'0')]), OrderedDict([(u'name', u'OCJLinkTraceSourceDummy'), (u'state', u'0')]), OrderedDict([(u'name', u'OCJLinkDeviceName'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'LMIFTDI_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'2'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'LmiftdiSpeed'), (u'state', u'500')]), OrderedDict([(u'name', u'CCLmiftdiDoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'CCLmiftdiLogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CCLmiFtdiInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCLmiFtdiInterfaceCmdLine'), (u'state', u'0')])])]))]), OrderedDict([(u'name', u'MACRAIGOR_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'3'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'jtag'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'EmuSpeed'), (u'state', u'1')]), OrderedDict([(u'name', u'TCPIP'), (u'state', u'aaa.bbb.ccc.ddd')]), OrderedDict([(u'name', u'DoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'LogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'DoEmuMultiTarget'), (u'state', u'0')]), OrderedDict([(u'name', u'EmuMultiTarget'), (u'state', u'0@ARM7TDMI')]), OrderedDict([(u'name', u'EmuHWReset'), (u'state', u'0')]), OrderedDict([(u'name', u'CEmuCommBaud'), (u'version', u'0'), (u'state', u'4')]), OrderedDict([(u'name', u'CEmuCommPort'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'jtago'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'UnusedAddr'), (u'state', u'0x00800000')]), OrderedDict([(u'name', u'CCMacraigorHWResetDelay'), (u'state', None)]), OrderedDict([(u'name', u'CCJTagBreakpointRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJTagDoUpdateBreakpoints'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJTagUpdateBreakpoints'), (u'state', u'_call_main')]), OrderedDict([(u'name', u'CCMacraigorInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCMacraigorInterfaceCmdLine'), (u'state', u'0')])])]))]), OrderedDict([(u'name', u'PEMICRO_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'1'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'OCPEMicroAttachSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'CCPEMicroInterfaceList'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPEMicroResetDelay'), (u'state', None)]), OrderedDict([(u'name', u'CCPEMicroJtagSpeed'), (u'state', u'#UNINITIALIZED#')]), OrderedDict([(u'name', u'CCJPEMicroShowSettings'), (u'state', u'0')]), OrderedDict([(u'name', u'DoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'LogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CCPEMicroUSBDevice'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCPEMicroSerialPort'), (u'version', u'0'), (u'state', u'0')]), OrderedDict([(u'name', u'CCJPEMicroTCPIPAutoScanNetwork'), (u'state', u'1')]), OrderedDict([(u'name', u'CCPEMicroTCPIP'), (u'state', u'10.0.0.1')]), OrderedDict([(u'name', u'CCPEMicroCommCmdLineProducer'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSTLinkInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSTLinkInterfaceCmdLine'), (u'state', u'0')])])]))]), OrderedDict([(u'name', u'RDI_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'2'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CRDIDriverDll'), (u'state', u'###Uninitialized###')]), OrderedDict([(u'name', u'CRDILogFileCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CRDILogFileEdit'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'CCRDIHWReset'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchReset'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchUndef'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchSWI'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchData'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchPrefetch'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchIRQ'), (u'state', u'0')]), OrderedDict([(u'name', u'CCRDICatchFIQ'), (u'state', u'0')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'STLINK_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'2'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'CCSTLinkInterfaceRadio'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSTLinkInterfaceCmdLine'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSTLinkResetList'), (u'version', u'1'), (u'state', u'0')]), OrderedDict([(u'name', u'CCCpuClockEdit'), (u'state', u'72.0')]), OrderedDict([(u'name', u'CCSwoClockAuto'), (u'state', u'0')]), OrderedDict([(u'name', u'CCSwoClockEdit'), (u'state', u'2000')])])]))]), OrderedDict([(u'name', u'THIRDPARTY_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'0'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'CThirdPartyDriverDll'), (u'state', u'###Uninitialized###')]), OrderedDict([(u'name', u'CThirdPartyLogFileCheck'), (u'state', u'0')]), OrderedDict([(u'name', u'CThirdPartyLogFileEditB'), (u'state', u'$PROJ_DIR$\\cspycomm.log')]), OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')])])]))]), OrderedDict([(u'name', u'XDS100_ID'), (u'archiveVersion', u'2'), (u'data', OrderedDict([(u'version', u'2'), (u'wantNonLocal', u'1'), (u'debug', u'1'), (u'option', [OrderedDict([(u'name', u'OCDriverInfo'), (u'state', u'1')]), OrderedDict([(u'name', u'OCXDS100AttachSlave'), (u'state', u'1')]), OrderedDict([(u'name', u'TIPackageOverride'), (u'state', u'0')]), OrderedDict([(u'name', u'TIPackage'), (u'state', None)]), OrderedDict([(u'name', u'CCXds100InterfaceList'), (u'version', u'1'), (u'state', u'0')]), OrderedDict([(u'name', u'BoardFile'), (u'state', None)]), OrderedDict([(u'name', u'DoLogfile'), (u'state', u'0')]), OrderedDict([(u'name', u'LogFile'), (u'state', u'$PROJ_DIR$\\cspycomm.log')])])]))])]), (u'debuggerPlugins', OrderedDict([(u'plugin', [OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\middleware\\HCCWare\\HCCWare.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\AVIX\\AVIX.ENU.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\CMX\\CmxArmPlugin.ENU.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\CMX\\CmxTinyArmPlugin.ENU.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\embOS\\embOSPlugin.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\MQX\\MQXRtosPlugin.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\OpenRTOS\\OpenRTOSPlugin.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\SafeRTOS\\SafeRTOSPlugin.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\ThreadX\\ThreadXArmPlugin.ENU.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\TI-RTOS\\tirtosplugin.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-II\\uCOS-II-286-KA-CSpy.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-II\\uCOS-II-KA-CSpy.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$TOOLKIT_DIR$\\plugins\\rtos\\uCOS-III\\uCOS-III-KA-CSpy.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$EW_DIR$\\common\\plugins\\CodeCoverage\\CodeCoverage.ENU.ewplugin'), (u'loadFlag', u'1')]), OrderedDict([(u'file', u'$EW_DIR$\\common\\plugins\\Orti\\Orti.ENU.ewplugin'), (u'loadFlag', u'0')]), OrderedDict([(u'file', u'$EW_DIR$\\common\\plugins\\SymList\\SymList.ENU.ewplugin'), (u'loadFlag', u'1')]), OrderedDict([(u'file', u'$EW_DIR$\\common\\plugins\\uCProbe\\uCProbePlugin.ENU.ewplugin'), (u'loadFlag', u'0')])])]))]))]))])

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
        settings['state'] = value

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

    def _find_target_core(self, data):
        """ Sets Target core """
        for k, v in self.core_dic.items():
            if k == data['core']:
                return v
        return IAREmbeddedWorkbench.core_dic['cortex-m0']  # def cortex-m0 if not defined otherwise

    def _parse_specific_options(self, data):
        """ Parse all IAR specific settings """
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

    def _get_option(self, settings, find_key):
        """ Return index for provided key """
        # This is used as in IAR template, everything 
        # is as an array with random positions. We look for key with an index
        for option in settings:
            if option['name'] == find_key:
                return settings.index(option)

    def _export_single_project(self):
        """ A single project export """
        expanded_dic = self.workspace.copy()

        self._fix_paths(expanded_dic)

        # generic tool template specified or project
        if expanded_dic['template']:
            # TODO 0xc0170: template list !
            project_file = join(getcwd(), expanded_dic['template'][0])
            try:
                ewp_dic = xmltodict.parse(open(project_file), dict_constructor=dict)
            except IOError:
                logger.info("Template file %s not found" % project_file)
                ewp_dic = self.definitions.ewp_file
        elif 'iar' in self.env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), self.env_settings.templates['iar'][0])
            try:
                ewp_dic = xmltodict.parse(open(project_file), dict_constructor=dict)
            except IOError:
                logger.info("Template file %s not found" % project_file)
                ewp_dic = self.definitions.ewp_file
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
        eww_dic = self.definitions.eww_file
        self._eww_set_path_multiple_project(eww_dic)

        # generate the file
        eww_xml = xmltodict.unparse(eww_dic, pretty=True)
        project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' % self.workspace['settings']['name'], self.workspace['settings']['path'])
        return project_path, [eww]

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
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logger.error("Project: %s build failed. Please check IARBUILD path in the user_settings.py file." % self.workspace['files']['ewp'])
            return -1
        else:
            # no IAR doc describes errors from IarBuild
            logger.info("Project: %s build completed." % self.workspace['files']['ewp'])
            return 0

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['ewp'], self.workspace['files']['eww'],
            self.workspace['files']['ewd']]}

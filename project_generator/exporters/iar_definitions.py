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


class IARDefinitions():

    iar_settings = {
        'Variant': {
            'state': 0,
        },
        'GEndianMode': {  # [General Options][Target] Endian mode
            'state': 0,
        },
        'Input variant': {
            'version': 0,
            'state': 0,
        },
        'Output variant': {
            'state': 1,
        },
        'GOutputBinary': {  # [General Options][Output] Executable or library
            'state': 0,    # 1 - library, 0 - executable
        },
        'FPU': {
            'version': 2,
            'state': 0,
        },
        'GRuntimeLibSelect': {  # [General Options] Use runtime library
            'version': 0,
            'state': 0,        # 0 - none, 1 - normal, 2 - full, 3 - custom
        },
        'GRuntimeLibSelectSlave': {
            'version': 0,
            'state': 0,
        },
        'GeneralEnableMisra': {    # [General Options] Enable Misra-C
            'state': 0,
        },
        'GeneralMisraVerbose': {   # [General Options] Misra verbose
            'state': 0,
        },
        'OGChipSelectEditMenu': {  # [General Options] Select MCU (be aware, tabs are needed in some cases)
            'state': 0,
        },
        'GenLowLevelInterface': {  # [General Options] Use semihosting
            # [General Options] 0 - none, 1 - semihosting, 2 - IAR breakpoint
            'state': 0,
        },
        'GEndianModeBE': {
            'state': 0,
        },
        'OGBufferedTerminalOutput': {  # [General Options] Buffered terminal output
            'state': 0,
        },
        'GenStdoutInterface': {    # [General Options] Stdout/err
            'state': 0,            # [General Options] 0 - semihosting, 1 - SWD
        },
        'GeneralMisraVer': {
            'state': 0,
        },
        'GFPUCoreSlave': {
            'state': 0,
        },
        'GBECoreSlave': {
            'state': 0,
        },
        'OGUseCmsis': {        # [General Options][Lib configuration] Use CMSIS Lib
            'state': 0,
        },
        'OGUseCmsisDspLib': {  # [General Options][Lib configuration] Use CMSIS DSP Lib, only valid if CMSIS Lib is selected
            'state': 0,
        },
        'CCPreprocFile': {
            'state': 0,
        },
        'CCPreprocComments': {
            'state': 0,
        },
        'CCPreprocLine': {
            'state': 0,
        },
        'CCListCFile': {  # [C/C++ Compiler][Output] Output list file
            'state': 0,
        },
        'CCListCMnemonics': {
            'state': 0,
        },
        'CCListCMessages': {
            'state': 0,
        },
        'CCListAssFile': {  # [C/C++ Compiler][Output] Output assembler file
            'state': 0,
        },
        'CCListAssSource': {
            'state': 0,
        },
        'CCEnableRemarks': {
            'state': [],
        },
        'CCDiagSuppress': {
            'state': '',
        },
        'CCDiagRemark': {
            'state': '',
        },
        'CCDiagWarning': {
            'state': '',
        },
        'CCDiagError': {
            'state': '',
        },
        'CCObjPrefix': { # Generate object files for C/C++
            'state': 1,
        },
        'CCAllowList': {       # [C/C++ Compiler] Enable transformations (Optimizations)
            'version': 1,
            # Each bit is for one optimization settings. For example second bit
            # is for loop unrolling
            'state': 1111111,
        },
        'CCDebugInfo': {   # [C/C++ Compiler] Generate debug information
            'state': 1,
        },
        'IEndianMode': {
            'state': 1,
        },
        'IProcessor': {
            'state': 1,
        },
        'IExtraOptionsCheck': {
            'state': 0,
        },
        'IExtraOptions': {
            'state': 0,
        },
        'CCLangConformance': {  # [C/C++ Compiler] Language conformance
            # 0 - standard with IAR extensions, 1 - standard, 2 - strict
            'state': 0,
        },
        'CCSignedPlainChar': {  # [C/C++ Compiler] Plain char
            'state': 1,        # 0 - signed, 1 - unsigned
        },
        'CCRequirePrototypes': {  # [C/C++ Compiler] Require prototypes
            'state': 0,
        },
        'CCMultibyteSupport': {
            'state': 0,
        },
        'CCCompilerRuntimeInfo': {
            'state': 0,
        },
        'CCDiagWarnAreErr': {
            'state': 0,
        },
        'IFpuProcessor': {
            'state': 0,
        },
        'OutputFile': {
            'state': '',
        },
        'CCLibConfigHeader': {
            'state': 0,
        },
        'PreInclude': {
            'state': 0,
        },
        'CompilerMisraOverride': {
            'state': 0,
        },
        'CCStdIncCheck': {
            'state': 0,
        },
        'CCCodeSection': {
            'state': '.text',
        },
        'IInterwork2': {
            'state': 0,
        },
        'IProcessorMode2': {
            'state': 0,
        },
        'IInterwork2': {
            'state': 0,
        },
        'CCOptLevel': {   # [C/C++ Compiler] Optimization level
            'state': 0,        # 0 - None, 1 - Low, 2 - Medium , 3 - High
        },
        'CCOptStrategy': {     # [C/C++ Compiler] Valid only for Optimization level High
            'version': 0,
            'state': 0,        # 0 - Balanced, 1 - Size, 2 - Speed
        },
        'CCOptLevelSlave': {
            'state': 0,
        },
        'CompilerMisraRules98': {
            'version': 0,
            'state': 0,
        },
        'CompilerMisraRules04': {
            'version': 0,
            'state': 0,
        },
        'CCPosIndRopi': {  # [C/C++ Compiler][Code] Code and read-only data
            'state': 0,
        },
        'IccLang': {       # [C/C++ Compiler] C/C++ Language selection
            'state': 0,    # 0 - C, 1- C++, 2 - Auto
        },
        'CCPosIndNoDynInit': {  # [C/C++ Compiler][Code]
            'state': 0,
        },
        'CCPosIndRwpi': {  # [C/C++ Compiler][Code] Read write/data
            'state': 0,
        },
        'IccCDialect': {   # [C/C++ Compiler] C dialect
            'state': 1,    # 0 - C89, 1 - C90
        },
        'IccAllowVLA': {   # [C/C++ Compiler] Allow VLA (valid only for C99)
            'state': 0,
        },
        'IccCppDialect': {  # [C/C++ Compiler] C++ dialect
            'state': 0,    # 0 - Embedded C++, 1 - Extended embedded, 2 - C++
        },
        'IccExceptions': {  # [C/C++ Compiler] With exceptions (valid only for C++ dialect 2)
            'state': 0,
        },
        'IccRTTI': {       # [C/C++ Compiler] With RTTI (valid only for C++ dialect 2)
            'state': 0,
        },
        'IccStaticDestr': {
            'state': 1,
        },
        'IccCppInlineSemantics': {  # [C/C++ Compiler] C++ inline semantic (valid only for C99)
            'state': 0,
        },
        'IccCmsis': {
            'state': 1,
        },
        'IccFloatSemantics': {  # [C/C++ Compiler] Floating point semantic
            'state': 0,        # 0 - strict, 1 - relaxed
        },

        'AObjPrefix': { # Generate object files for assembly files
            'state': 1,
        },
        'AEndian': {
            'state': 0,
        },
        'ACaseSensitivity': {
            'state': 0,
        },
        'MacroChars': {
            'state': 0,
        },
        'AWarnEnable': {
            'state': 0,
        },
        'AWarnWhat': {
            'state': 0,
        },
        'AWarnOne': {
            'state': 0,
        },
        'AWarnRange1': {
            'state': 0,
        },
        'AWarnRange2': {
            'state': 0,
        },
        'ADebug': {     # [Assembler] Generate debug info
            'state': 0,
        },
        'AltRegisterNames': {
            'state': 0,
        },
        'ADefines': {   # [Assembler] Preprocessor - Defines
            'state': '',
        },
        'AList': {
            'state': 0,
        },
        'AListHeader': {
            'state': 0,
        },
        'AListing': {
            'state': 0,
        },
        'Includes': {
            'state': '',
        },
        'MacDefs': {
            'state': 0,
        },
        'MacExps': {
            'state': 0,
        },
        'MacExec': {
            'state': 0,
        },
        'OnlyAssed': {
            'state': 0,
        },
        'MultiLine': {
            'state': 0,
        },
        'PageLengthCheck': {
            'state': 0,
        },
        'PageLength': {
            'state': 0,
        },
        'TabSpacing': {
            'state': 0,
        },
        'AXRefDefines': {
            'state': 0,
        },
        'AXRef': {
            'state': 0,
        },
        'AXRefInternal': {
            'state': 0,
        },
        'AXRefDual': {
            'state': 0,
        },
        'AProcessor': {
            'state': 0,
        },
        'AFpuProcessor': {
            'state': 0,
        },
        'AOutputFile': {
            'state': 0,
        },
        'AMultibyteSupport': {
            'state': 0,
        },
        'ALimitErrorsCheck': {
            'state': 0,
        },
        'ALimitErrorsEdit': {
            'state': 100,
        },
        'AIgnoreStdInclude': {
            'state': 0,
        },
        'AUserIncludes': {
            'state': '',
        },
        'AExtraOptionsCheckV2': {
            'state': 0,
        },
        'AExtraOptionsV2': {
            'state': 0,
        },
        'OOCOutputFormat': {
            'state': 0,
        },
        'OCOutputOverride': {
            'state': 0,
        },
        'OOCCommandLineProducer': {
            'state': 0,
        },
        'OOCObjCopyEnable': {
            'state': 1,
        },

        'IlinkOutputFile': {
            'state': 0,
        },
        'IlinkLibIOConfig': {
            'state': 0,
        },
        'XLinkMisraHandler': {
            'state': 0,
        },
        'IlinkInputFileSlave': {
            'state': 0,
        },
        'IlinkDebugInfoEnable': {
            'state': 0,
        },
        'IlinkKeepSymbols': {
            'state': 0,
        },
        'IlinkRawBinaryFile': {
            'state': 0,
        },
        'IlinkRawBinarySymbol': {
            'state': 0,
        },
        'IlinkRawBinarySegment': {
            'state': 0,
        },
        'IlinkRawBinaryAlign': {
            'state': 0,
        },
        'IlinkDefines': {
            'state': 0,
        },
        'IlinkConfigDefines': {
            'state': 0,
        },
        'IlinkMapFile': {
            'state': 0,
        },
        'IlinkLogFile': {
            'state': 0,
        },

        'IlinkLogInitialization': {
            'state': 0,
        },
        'IlinkLogModule': {
            'state': 0,
        },
        'IlinkLogSection': {
            'state': 0,
        },
        'IlinkLogVeneer': {
            'state': 0,
        },
        'IlinkIcfOverride': {
            'state': 0,
        },
        'IlinkEnableRemarks': {
            'state': 0,
        },
        'IlinkSuppressDiags': {
            'state': 0,
        },

        'IlinkTreatAsRem': {
            'state': 0,
        },
        'IlinkTreatAsWarn': {
            'state': 0,
        },
        'IlinkTreatAsErr': {
            'state': 0,
        },
        'IlinkWarningsAreErrors': {
            'state': 0,
        },
        'IlinkUseExtraOptions': {
            'state': 0,
        },
        'IlinkExtraOptions': {
            'state': 0,
        },
        'IlinkLowLevelInterfaceSlave': {
            'state': 0,
        },
        'IlinkAutoLibEnable': {
            'state': 0,
        },
        'IlinkProgramEntryLabelSelect': {
            'state': 0,
        },
        'IlinkProgramEntryLabel': {
            'state': 0,
        },
    }

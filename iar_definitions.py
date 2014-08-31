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

    def get_mcu_definition(self, name):
    """ If MCU found, returns its definition dic, error otherwise. """
        try:
            return self.mcu_def[name]
        except KeyError:
            raise RuntimeError("Mcu was not recognized for IAR. Please check mcu_def dictionary.")

    # MCU definitions which are currently supported. Add a new one, define a name as it is
    # in IAR, create an empty project for that MCU, open the project file (ewp) in any text
    # editor, find out the values of SelectEditMenu, CoreOrChip and FPU if it's not disabled (=0)
    mcu_def = {
        'LPC1768' : {
            'OGChipSelectEditMenu' : {
                'state' : 'LPC1768  NXP LPC1768',
            },
            'OGCoreOrChip' : {
                'state' : 1,
            }
        },
        'MKL25Z128xxx4' : {
            'OGChipSelectEditMenu' : {
                'state' : 'MKL25Z128xxx4    Freescale MKL25Z128xxx4',
            },
            'OGCoreOrChip' : {
                'state' : 1,
            }
        },
        'STM32F401xB' : {
            'OGChipSelectEditMenu' : {
                'state' : 'STM32F401xB  ST STM32F401xB',
            },
            'OGCoreOrChip' : {
                'state' : 1,
            },
            'FPU' : {
                'state' : 5,
            },
        },
    }


    iar_settings = {
        'Variant' : {
            'state' : 0,
        },
        'GEndianMode' : {
            'state' : 0,
        },
        'Input variant' : {
            'version' : 0,
            'state' : 0,
        },
        'Output variant' : {
            'state' : 0,
        },
        'GOutputBinary' : {
            'state' : 0,
        },
        'FPU' : {
            'version' : 2,
            'state' : 0,
        },
        'GRuntimeLibSelect' : {
            'version' : 0,
            'state' : 0,
        },
        'GRuntimeLibSelectSlave' : {
            'version' : 0,
            'state' : 0,
        },
        'GeneralEnableMisra' : {
            'state' : 0,
        },
        'GeneralMisraVerbose' : {
            'state' : 0,
        },
        'OGChipSelectEditMenu' : {
            'state' : 0,
        },
        'GenLowLevelInterface' : {
            'state' : 0,
        },
        'GEndianModeBE' : {
            'state' : 0,
        },
        'OGBufferedTerminalOutput' : {
            'state' : 0,
        },
        'GenStdoutInterface' : {
            'state' : 0,
        },
        'GeneralMisraVer' : {
            'state' : 0,
        },
        'GFPUCoreSlave' : {
            'state' : 0,
        },
        'GBECoreSlave' : {
            'state' : 0,
        },
        'OGUseCmsis' : {
            'state' : 0,
        },
        'OGUseCmsisDspLib' : {
            'state' : 0,
        },
        'CCPreprocFile' : {
            'state' : 0,
        },
        'CCPreprocComments' : {
            'state' : 0,
        },
        'CCPreprocLine' : {
            'state' : 0,
        },
        'CCListCFile' : {
            'state' : 0,
        },
        'CCListCMnemonics' : {
            'state' : 0,
        },
        'CCListCMessages' : {
            'state' : 0,
        },
        'CCListAssFile' : {
            'state' : 0,
        },
        'CCListAssSource' : {
            'state' : 0,
        },
        'CCEnableRemarks' : {
            'state' : [],
        },
        'CCDiagRemark' : {
            'state' : 0,
        },
        'CCDiagWarning' : {
            'state' : 0,
        },
        'CCDiagError' : {
            'state' : 0,
        },
        'CCObjPrefix' : {
            'state' : 0,
        },
        'CCAllowList' : {
            'version' : 1,
            'state' : 1111111,
        },
        'CCDebugInfo' : {
            'state' : 1,
        },
        'IEndianMode' : {
            'state' : 1,
        },
        'IProcessor' : {
            'state' : 1,
        },
        'IExtraOptionsCheck' : {
            'state' : 0,
        },
        'IExtraOptions' : {
            'state' : 0,
        },
        'CCLangConformance' : {
            'state' : 0,
        },
        'CCSignedPlainChar' : {
            'state' : 1,
        },
        'CCRequirePrototypes' : {
            'state' : 0,
        },
        'CCMultibyteSupport' : {
            'state' : 0,
        },
        'CCDiagWarnAreErr' : {
            'state' : 0,
        },
        'IFpuProcessor' : {
            'state' : 0,
        },
        'OutputFile' : {
            'state' : '',
        },
        'CCLibConfigHeader' : {
            'state' : 0,
        },
        'PreInclude' : {
            'state' : 0,
        },
        'CompilerMisraOverride' : {
            'state' : 0,
        },
        'CCStdIncCheck' : {
            'state' : 0,
        },
        'CCCodeSection' : {
            'state' : '.text',
        },
        'IInterwork2' : {
            'state' : 0,
        },
        'IProcessorMode2' : {
            'state' : 0,
        },
        'IInterwork2' : {
            'state' : 0,
        },
        'CCOptStrategy' : {
            'version' : 0,
            'state' : 0,
        },
        'CCOptLevelSlave' : {
            'state' : 0,
        },
        'CompilerMisraRules98' : {
            'version' : 0,
            'state' : 0,
        },
        'CompilerMisraRules04' : {
            'version': 0,
            'state' : 0,
        },
        'CCPosIndRopi' : {
            'state' : 0,
        },
        'IccLang' : {
            'state' : 0,
        },
        'CCPosIndRwpi' : {
            'state' : 0,
        },
        'IccCDialect' : {
            'state' : 1,
        },
        'IccAllowVLA' : {
            'state' : 0,
        },
        'IccCppDialect' : {
            'state' : 0,
        },
        'IccExceptions' : {
            'state' : 0,
        },
        'IccRTTI' : {
            'state' : 0,
        },
        'IccStaticDestr' : {
            'state' : 1,
        },
        'IccCppInlineSemantics' : {
            'state' : 0,
        },
        'IccCmsis' : {
            'state' : 1,
        },
        'IccFloatSemantics' : {
            'state' : 0,
        },
        'AObjPrefix' : {
            'state' : 0,
        },
        'AEndian' : {
            'state' : 0,
        },
        'ACaseSensitivity' : {
            'state' : 0,
        },
        'MacroChars' : {
            'state' : 0,
        },
        'AWarnEnable' : {
            'state' : 0,
        },
        'AWarnWhat' : {
            'state' : 0,
        },
        'AWarnOne' : {
            'state' : 0,
        },
        'AWarnRange1' : {
            'state' : 0,
        },
        'AWarnRange2' : {
            'state' : 0,
        },
        'ADebug' : {
            'state' : 0,
        },
        'AltRegisterNames' : {
            'state' : 0,
        },
        'ADefines' : {
            'state' : 0,
        },
        'AList' : {
            'state' : 0,
        },
        'AListHeader' : {
            'state' : 0,
        },
        'AListing' : {
            'state' : 0,
        },
        'Includes' : {
            'state' : 0,
        },
        'MacDefs' : {
            'state' : 0,
        },
        'MacExps' : {
            'state' : 0,
        },
        'MacExec' : {
            'state' : 0,
        },
        'OnlyAssed' : {
            'state' : 0,
        },
        'MultiLine' : {
            'state' : 0,
        },
        'PageLengthCheck' : {
            'state' : 0,
        },
        'PageLength' : {
            'state' : 0,
        },
        'TabSpacing' : {
            'state' : 0,
        },
        'AXRefDefines' : {
            'state' : 0,
        },
        'AXRefInternal' : {
            'state' : 0,
        },
        'AXRefDual' : {
            'state' : 0,
        },
        'AProcessor' : {
            'state' : 0,
        },
        'AFpuProcessor' : {
            'state' : 0,
        },
        'AOutputFile' : {
            'state' : 0,
        },
        'AMultibyteSupport' : {
            'state' : 0,
        },
        'ALimitErrorsCheck' : {
            'state' : 0,
        },
        'ALimitErrorsEdit' : {
            'state' : 0,
        },
        'AIgnoreStdInclude' : {
            'state' : 0,
        },
        'AUserIncludes' : {
            'state' : 0,
        },
        'AExtraOptionsCheckV2' : {
            'state' : 0,
        },
        'AExtraOptionsV2' : {
            'state' : 0,
        },
        'OOCOutputFormat' : {
            'state' : 0,
        },
        'OCOutputOverride' : {
            'state' : 0,
        },
        'OOCCommandLineProducer' : {
            'state' : 0,
        },
        'OOCObjCopyEnable' : {
            'state' : 1,
        },
    }

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

class uVisionDefinitions():
    def get_mcu_definition(self, name):
        try:
            return self.mcu_def[name]
        except KeyError:
            raise RuntimeError("Mcu was not recognized for uvision. Please check mcu_def dictionary.")

    # definition dictionaries, please visit wiki page for more information
    mcu_def = {
        'MK20DX128xxx5' : {
            'TargetOption' : {
                'Device' : 'MK20DX128xxx5',
                'Vendor' : 'Freescale Semiconductor',
                'Cpu'    : 'IRAM(0x1FFFE000-0x1FFFFFFF) IRAM2(0x20000000-0x20001FFF) IROM(0x0-0x1FFFF) IROM2(0x10000000-0x10007FFF) CLOCK(12000000) CPUTYPE("Cortex-M4") ELITTLE',
                'FlashDriverDll' : 'ULP2CM3(-O2510 -S0 -C0 -FO15 -FD20000000 -FC800 -FN2 -FF0MK_P128_50MHZ -FS00 -FL020000 -FF1MK_D32_50MHZ -FS110000000 -FL108000)',
                'DeviceId' : 6206,
                'SFDFile' : 'SFD\Freescale\Kinetis\MK20D5.sfr',
            }
        },
        'LPC1768' : {
            'TargetOption' : {
                'Device' : 'LPC1768',
                'Vendor' : 'NXP',
                'Cpu'    : 'IRAM(0x10000000-0x10007FFF) IRAM2(0x2007C000-0x20083FFF) IROM(0-0x7FFFF) CLOCK(12000000) CPUTYPE("Cortex-M3")',
                'FlashDriverDll' : 'UL2CM3(-O463 -S0 -C0 -FO7 -FD10000000 -FC800 -FN1 -FF0LPC_IAP_512 -FS00 -FL080000)',
                'DeviceId' : 4868,
                'SFDFile' : 'SFD\NXP\LPC176x5x\LPC176x5x.SFR',
            }
        }
    }

    uvision_settings = {
        # C/C++ settings
        'Cads' : {
            'interw' : 0,
            'Optim' : 0,
            'oTime' : 0,
            'SplitLS' : 0,
            'OneElfS' : 0,
            'Strict' : 0,
            'EnumInt' : 0,
            'PlainCh' : 0,
            'Ropi' : 0,
            'Rwpi' : 0,
            'wLevel' : 0,
            'uThumb' : 0,
            'uSurpInc' : 0,
            'uC99' : 0,
            'MiscControls': [],
        },

        # Linker settings
        'LDads' : {
           'umfTarg' : 0,
           'Ropi' : 0,
           'Rwpi' : 0,
           'noStLib' : 0,
           'RepFail' : 0,
           'useFile' : 0,
           'TextAddressRange' : 0,
           'DataAddressRange' : 0,
           'IncludeLibs' : 0,
           'IncludeLibsPath' : 0,
           'Misc' : 0,
           'LinkerInputFile' : 0,
           'DisabledWarnings' : [],
        },

        # Assembly settings
        'Aads' : {
            'interw' : 0,
            'Ropi' : 0,
            'Rwpi' : 0,
            'thumb' : 0,
            'SplitLS' : 0,
            'SwStkChk' : 0,
            'NoWarn' : 0,
            'uSurpInc' : 0,
            'VariousControls' : 0,
            'MiscControls' : 0,
            'Define' : [],
            'Undefine' : 0,
            'IncludePath' : [],
            'VariousControls' : 0,
        },

        # User settings
        'TargetOption' : {
            'CreateExecutable' : 0,
            'CreateLib' : 0,
            'CreateHexFile' : 0,
            'DebugInformation' : 0,
            'BrowseInformation' : 0,
            'CreateBatchFile' : 0,
            'BeforeCompile' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            },
            'BeforeMake' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            },
            'AfterMake' : {
                'RunUserProg1' : 0,
                'UserProg1Name' : 0,
                'RunUserProg2' : 0,
                'UserProg2Name' : 0,
                'UserProg1Dos16Mode' : 0,
                'UserProg2Dos16Mode' : 0,
            }
        },

        # Target settings
        'ArmAdsMisc' : {
            'useUlib' : 0,
            'NoZi1' : 0,
            'NoZi2' : 0,
            'NoZi3' : 0,
            'NoZi4' : 0,
            'NoZi5' : 0,
            'OCR_RVCT1' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT2' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT3' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT4' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT5' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT6' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT7' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT8' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT9' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            },
            'OCR_RVCT10' : {
                'Type' : 0,
                'StartAddress' : 0,
                'Size' : 0,
            }
        },

        'CommonProperty' : {
            'UseCPPCompile' : 0,
            'RVCTCodeConst' : 0,
            'RVCTZI' : 0,
            'RVCTOtherData' : 0,
            'ModuleSelection' : 0,
            'IncludeInBuild' : 0,
            'AlwaysBuild' : 0,
            'GenerateAssemblyFile' : 0,
            'AssembleAssemblyFile' : 0,
            'PublicsOnly' : 0,
            'StopOnExitCode' : 0,
            'CustomArgument' : 0,
            'IncludeLibraryModules' : 0,
        },

        'DebugOption' : {
            'Simulator' : {
                'UseSimulator' : 0,
                'LoadApplicationAtStartup' : 1,
                'RunToMain' : 1,
                'RestoreBreakpoints' : 1,
                'RestoreWatchpoints' : 1,
                'RestoreMemoryDisplay' : 1,
                'RestoreFunctions' : 1,
                'RestoreToolbox' : 1,
                'LimitSpeedToRealTime' : 0,
            },
            'Target' : {
                'UseTarget' : 1,
                'LoadApplicationAtStartup' : 1,
                'RunToMain' : 1,
                'RestoreBreakpoints' : 1,
                'RestoreWatchpoints' : 1,
                'RestoreMemoryDisplay' : 1,
                'RestoreFunctions' : 1,
                'RestoreToolbox' : 1,
                'RestoreTracepoints' : 1,
                'RestoreTracepoints' : 1,
                'RestoreTracepoints' : 1,
            },
            'RunDebugAfterBuild' : 0,
            'TargetSelection' : 0,
        },

        'Utilities' : {
            'Flash1' : {
                'UseTargetDll' : 0,
                'UseExternalTool' : 0,
                'RunIndependent' : 0,
                'UpdateFlashBeforeDebugging' : 0,
                'Capability' : 0,
                'DriverSelection' : 0,
            },
            'bUseTDR' : 1,
            'Flash2' : 'BIN\CMSIS_AGDI.dll',
            'Flash3' : 0,
            'Flash4' : 0,
            'pFcarmOut' : 0,
            'pFcarmGrp' : 0,
            'pFcArmRoot' : 0,
            'FcArmLst' : 0,
        }
    }

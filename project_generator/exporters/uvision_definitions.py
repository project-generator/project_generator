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
    # # alias mbed standard names to their CPUs:
    # mcu_def['K64F'] = mcu_def['MK64FN1M0xxx12']

    uvision_settings = {
        # C/C++ settings
        'Cads': {
            'interw': 0,   # Execute-only code
            'Optim': [0],  # Optimization level
            'oTime': 0,    # Optimize for time
            'SplitLS': 0,  # Split load and store multiple
            'OneElfS': 0,  # One elf section per function
            'Strict': 0,   # Strict ANSI C
            'EnumInt': 0,  # Enum container always int
            'PlainCh': 0,  # Plain char is signed
            'Ropi': 0,     # Read-only position independent code
            'Rwpi': 0,     # Read-write position independent code
            'wLevel': 0,   # Warnings level
            'uThumb': 0,   # Thumb mode
            'uSurpInc': 0,  # No auto includes
            'uC99': 0,     # C99 mode
            'MiscControls': [],  # Misc controls
        },

        # Linker settings
        'LDads': {
            'umfTarg': 0,           # Use Memory from Target dialog window
            'Ropi': 0,              # Make RO section position independent
            'Rwpi': 0,              # Make RW section position independent
            'noStLib': 0,           # Dont search Standard libraries
            'RepFail': 0,           # Report might fail conditions as errors
            'useFile': 0,
            'TextAddressRange': 0,  # RO address range
            'DataAddressRange': 0,  # RW address range
            'IncludeLibs': 0,
            'IncludeLibsPath': 0,
            'Misc': 0,              # Misc controls
            'LinkerInputFile': 0,   # Scatter file
            'DisabledWarnings': [],  # Disable warnings
        },

        # Assembly settings
        'Aads': {
            'interw': 0,           # Execute-only code
            'Ropi': 0,             # RO position independent
            'Rwpi': 0,             # RW position independent
            'thumb': 0,            # Thumb mode
            'SplitLS': 0,          # Split load and store multiple
            'SwStkChk': 0,
            'NoWarn': 0,           # No warnings
            'uSurpInc': 0,         # No auto includes
            'VariousControls': 0,
            'MiscControls': 0,     # Misc controls
            'Define': [],          # Define
            'Undefine': 0,         # Undefine
            'IncludePath': [],     # Include paths
            'VariousControls': 0,
        },

        # User settings
        'TargetOption': {
            'CreateExecutable': 0,     # Create executable
            'CreateLib': 0,            # Create library
            'CreateHexFile': 0,        # Create hex file
            'DebugInformation': 0,     # Debug information
            'BrowseInformation': 0,    # Browse information
            'CreateBatchFile': 0,      # Create batch file
            'BeforeCompile': {         # Run user program before compilation
                'RunUserProg1': 0,     # Run #1
                'UserProg1Name': 0,    # Program #1 name
                'RunUserProg2': 0,     # Run #2
                'UserProg2Name': 0,    # Program #2 name
                'UserProg1Dos16Mode': 0,   # Dos16 mode for #1
                'UserProg2Dos16Mode': 0,   # Dos16 mode for #2
            },
            'BeforeMake': {                # User programs before build
                'RunUserProg1': 0,         # Run #1
                'UserProg1Name': 0,        # Program #1 name
                'RunUserProg2': 0,         # Run #2
                'UserProg2Name': 0,        # Program #2 name
                'UserProg1Dos16Mode': 0,   # Dos16 mode for #1
                'UserProg2Dos16Mode': 0,   # Dos16 mode for #2
            },
            'AfterMake': {
                'RunUserProg1': 0,         # Run #2
                'UserProg1Name': 0,        # Program #1 name
                'RunUserProg2': 0,         # Run #2
                'UserProg2Name': 0,        # Program #2 name
                'UserProg1Dos16Mode': 0,   # Dos16 mode for #1
                'UserProg2Dos16Mode': 0,   # Dos16 mode for #2
            }
        },

        # Target settings
        'ArmAdsMisc': {
            'useUlib': 0,  # use MicroLIB
            'NoZi1': 0,    #
            'NoZi2': 0,
            'NoZi3': 0,
            'NoZi4': 0,
            'NoZi5': 0,
            'OCR_RVCT1': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT2': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT3': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT4': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT5': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT6': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT7': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT8': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT9': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            },
            'OCR_RVCT10': {
                'Type': 0,
                'StartAddress': 0,
                'Size': 0,
            }
        },

        'CommonProperty': {
            'UseCPPCompile': 0,    # Use CPP compiler for C files
            'RVCTCodeConst': 0,
            'RVCTZI': 0,
            'RVCTOtherData': 0,
            'ModuleSelection': 0,
            'IncludeInBuild': 0,
            'AlwaysBuild': 0,
            'GenerateAssemblyFile': 0,
            'AssembleAssemblyFile': 0,
            'PublicsOnly': 0,
            'StopOnExitCode': 0,
            'CustomArgument': 0,
            'IncludeLibraryModules': 0,
        },

        'DebugOption': {
            'Simulator': {
                'UseSimulator': 0,
                'LoadApplicationAtStartup': 1,
                'RunToMain': 1,
                'RestoreBreakpoints': 1,
                'RestoreWatchpoints': 1,
                'RestoreMemoryDisplay': 1,
                'RestoreFunctions': 1,
                'RestoreToolbox': 1,
                'LimitSpeedToRealTime': 0,
            },
            'Target': {
                'UseTarget': 1,
                'LoadApplicationAtStartup': 1,
                'RunToMain': 1,
                'RestoreBreakpoints': 1,
                'RestoreWatchpoints': 1,
                'RestoreMemoryDisplay': 1,
                'RestoreFunctions': 1,
                'RestoreToolbox': 1,
                'RestoreTracepoints': 1,
                'RestoreTracepoints': 1,
                'RestoreTracepoints': 1,
            },
            'RunDebugAfterBuild': 0,
            'TargetSelection': 0,
        },

        'Utilities': {
            'Flash1': {
                'UseTargetDll': 0,
                'UseExternalTool': 0,
                'RunIndependent': 0,
                'UpdateFlashBeforeDebugging': 0,
                'Capability': 0,
                'DriverSelection': 0,
            },
            'bUseTDR': 1,
            'Flash2': 'BIN\CMSIS_AGDI.dll',
            'Flash3': 0,
            'Flash4': 0,
            'pFcarmOut': 0,
            'pFcarmGrp': 0,
            'pFcArmRoot': 0,
            'FcArmLst': 0,
        }
    }

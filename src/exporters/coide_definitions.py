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


class CoIDEdefinitions():

    def get_mcu_definition(self, name):
        """ If MCU found, returns its definition dic, error otherwise. """
        try:
            return self.mcu_def[name]
        except KeyError:
            raise RuntimeError(
                "Mcu was not recognized for CoIDE. Please check mcu_def dictionary.")

    # MCU definitions which are currently supported. Add a new one, define a name as it is
    # in CoIDE, create an empty project for that MCU, open the project file (.coproj) in any text
    # editor, find out the values of manufacturerId, manufacturerName and
    # others.
    mcu_def = {
        'MKL25Z128VLK4': {
            'Device': {
                'manufacturerId': 4,
                'manufacturerName': 'Freescale',
                'chipId': 86,
                'chipName': 'MKL25Z128VLK4',
            },
            'DebugOption': {
                'defaultAlgorithm': 'KLxx_128_PRG_NO_CFG.elf',
            },
            'MemoryAreas': {
                'IROM1': {
                    'size': 0x00020000,
                    'startValue': 0x00000000,
                },
                'IRAM1': {
                    'size': 0x00001000,
                    'startValue': 0x1FFFF000,
                },
                'IROM2': {
                    'size': 0x0,
                    'startValue': 0x0,
                },
                'IRAM2': {
                    'size': 0x0,
                    'startValue': 0x0,
                },
            }
        },

        'LPC1768': {
            'Device': {
                'manufacturerId': 7,
                'manufacturerName': 'NXP',
                'chipId': 165,
                'chipName': 'LPC1768',
            },
            'DebugOption': {
                'defaultAlgorithm': 'lpc17xx_512.elf',
            },
            'MemoryAreas': {
                'IROM1': {
                    'size': 0x00080000,
                    'startValue': 0x00000000,
                },
                'IRAM1': {
                    'size': 0x00008000,
                    'startValue': 0x10000000,
                },
                'IROM2': {
                    'size': 0x0,
                    'startValue': 0x0,
                },
                'IRAM2': {
                    'size': 0x00008000,
                    'startValue': 0x2007C000,
                },
            }
        },
    }

    coide_settings = {
        'Compile': {
            'OptimizationLevel': 0,
            'UserEditCompiler': [],
        },
        'Link': {
            'DiscardUnusedSection': 0,
            'UseMemoryLayout': 0,
            'LTO': 0,
            'IsNewStartupCode': 1,
            'nostartfiles': 0,
        },
        'User': {
            'UserRun': {
                'Before': '',
                'After': '',
            }
        },
        'Output': {
            'OutputFileType': 0,
            'HEX': 1,
            'BIN': 1,
        }
    }

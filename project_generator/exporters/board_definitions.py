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

class boardDefinitions():

    def get_board_definition(self, name, tool):
        """ If a board is found, returns its definition for a tool, error otherwise. """
        try:
            return self.board_def[name][tool]
        except KeyError:
            raise RuntimeError(
                "The board: %s was not recognized for %s. Please check board_def dictionary." % (name, tool))

    # This is a dictionary of supported boards. Each board defines tools and required data which
    # are retreived by tools generator. For gcc, it's core, for others it's mcu_def which is later
    # used to get proper data to be set for that MCU. More details found in the tools definiton script file.
    board_def = {
        # Freescale FRDM boards
        'frdm-k20d50m': {
            'uvision': 'MK20DX128xxx5',
            'gcc' : 'cortex-m4',
        },
        'frdm-kl25z' : {
            'iar' : 'MKL25Z128xxx4',
            'gcc' : 'cortex-m0+',
        },
        'frdm-k64f' : {
            'uvision' : 'MK64FN1M0xxx12',
            'gcc' : 'cortex-m4f',
        },

        # mbed boards
        'mbed-lpc1768' : {
            'uvision' : 'LPC1768',
            'iar' : 'LPC1768',
            'coide' : 'LPC1768',
            'gcc' : 'cortex-m3',
        },

        # ST Disco boards
        'disco_f407vg' : {
            'coide' : 'STM32F407VG',
            'gcc' : 'cortex-m4',
        },
    }


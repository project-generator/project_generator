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
        """ If a board is found, returns its definition dic, error otherwise. """
        try:
            return self.board_def[name][tool]
        except KeyError:
            raise RuntimeError(
                "The board: %s was not recognized for uvision. Please check board_def dictionary." % name)

    board_def = {
        'frdm-k20d50m': {
            'uvision': 'MK20DX128xxx5',
        },
        'frdm-kl25z' : {
            'iar' : 'MKL25Z128xxx4',
        },
        'mbed-lpc1768' : {
            'uvision' : 'LPC1768',
            'iar' : 'LPC1768',
            'coide' : 'LPC1768',
        },
    }


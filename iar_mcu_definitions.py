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

def get_mcu_definition(name):
    try:
        return MCU_def[name]
    except KeyError:
        raise RuntimeError("Mcu was not recognized for IAR. Please check MCU_def dictionary.")

MCU_def = {
    'LPC1768' : {
            # 'Variant' : {
            #     'version' : 20,
            #     'state' : 0,
            # },
            # 'GFPUCoreSlave' : {
            #     'version' : 20,
            #     'state' : 0,
            # },
            # 'GBECoreSlave' : {
            #     'version' : 20,
            #     'state' : 0,
            # },
            'OGChipSelectEditMenu' : {
                'state' : 'LPC1768	NXP LPC1768',
            },
            'OGCoreOrChip' : {
                'state' : '1'
            }
    }

}

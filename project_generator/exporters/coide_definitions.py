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

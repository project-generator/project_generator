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
from os.path import join, normpath, expanduser
from os import getcwd
import yaml
import logging

class Targets():

    SUPPORTED_TARGETS = [
        'frdm-k20d50m'
        'frdm-k64f',
        'mbed-lpc1768',
    ]
    def __init__(self):
        config_directory = expanduser('~/.pg')
        self.definitions_directory = join(config_directory, 'definitions')

    def load_record(self, file):
        project_file = open(file)
        config = yaml.load(project_file)
        project_file.close()
        return config

    def get_tool_def(self, target, tool):
        if target not in self.SUPPORTED_TARGETS:
            return None
        target_path = join(self.definitions_directory, 'target', target + '.yaml')
        target_record = self.load_record(target_path)
        mcu_path = target_record['target']['mcu']
        mcu_path = normpath(mcu_path[0])
        mcu_path = join(self.definitions_directory, mcu_path) + '.yaml'
        mcu_record = self.load_record(mcu_path)
        return mcu_record['tool_specific'][tool]

    def is_supported(self, target):
        return target in self.SUPPORTED_TARGETS

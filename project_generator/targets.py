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
from os.path import join, normpath, expanduser, splitext, isfile
from os import getcwd, listdir
import yaml
import logging

class Targets:

    def __init__(self, directory):
        self.definitions_directory = directory
        target_dir = join(self.definitions_directory, 'target')
        self.targets = [ splitext(f)[0] for f in listdir(target_dir) if isfile(join(target_dir,f)) ]

    def _load_record(self, file):
        project_file = open(file)
        config = yaml.load(project_file)
        project_file.close()
        return config

    def get_mcu_record(self, target):
        target_path = join(self.definitions_directory, 'target', target + '.yaml')
        target_record = self._load_record(target_path)
        mcu_path = target_record['target']['mcu']
        mcu_path = normpath(mcu_path[0])
        mcu_path = join(self.definitions_directory, mcu_path) + '.yaml'
        return self._load_record(mcu_path)

    def get_mcu_core(self, target):
        if target not in self.targets:
            return None
        mcu_record = self.get_mcu_record(target)
        try:
            return mcu_record['mcu']['core']
        except KeyError:
            return None

    def get_tool_def(self, target, tool):
        if target not in self.targets:
            return None
        mcu_record = self.get_mcu_record(target)
        try:
            return mcu_record['tool_specific'][tool]
        except KeyError:
            return None

    def is_supported(self, target, tool):
        if target not in self.targets:
            return False
        mcu_record = self.get_mcu_record(target)
        # Look at tool specific options which define tools supported for mcu
        try:
            for k,v in mcu_record['tool_specific'].items():
                if k == tool:
                    return True
        except KeyError:
            pass
        return False

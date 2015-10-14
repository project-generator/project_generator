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

import yaml
import subprocess
import logging

from os.path import join, normpath, splitext, isfile, exists
from os import listdir, makedirs, getcwd

from .settings import ProjectSettings

# DEPRECATED entire file, will be removed for new minor version
# replaced by https://pypi.python.org/pypi/project_generator_definitions

class Targets:

    MCU_TEMPLATE = {
        'mcu' : {
            'vendor' : ['Manually add vendor (st, freescale, etc) instead of this text'],
            'name' : [''],
            'core' : ['Manually add core (cortex-mX) instead of this text'],
        },
    }

    def __init__(self, directory=None):
        if directory:
            self.definitions_directory = directory
            target_dir = join(self.definitions_directory, 'target')
            self.targets = [ splitext(f)[0] for f in listdir(target_dir) if isfile(join(target_dir,f)) ]

    def _load_record(self, file):
        project_file = open(file)
        config = yaml.load(project_file)
        project_file.close()
        return config

    def get_targets(self):
        return self.targets

    def get_mcu_definition(self):
        return self.MCU_TEMPLATE

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
        if target.lower() not in self.targets:
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

    def update_definitions(self, force=False, settings=ProjectSettings()):
        # TODO: deprecated
        logging.debug("Definitions are not updated, please use python module project_generator_definitions")
        return

def mcu_create(ToolParser, mcu_name, proj_file, tool):
    # TODO: deprecated
    logging.debug("Definitions are not updated, please use python module project_generator_definitions")
    return

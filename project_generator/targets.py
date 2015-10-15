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
from project_generator_definitions.definitions import ProGenDef, ProGenTargets

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
        pass

    def _load_record(self, file):
        project_file = open(file)
        config = yaml.load(project_file)
        project_file.close()
        return config

    def get_targets(self):
        return ProGenTargets().get_targets()

    def get_mcu_definition(self):
        return self.MCU_TEMPLATE

    def get_mcu_record(self, target):
        return ProGenTargets().get_mcu_record(target)

    def get_mcu_core(self, target):
        return ProGenDef().get_mcu_core()

    def get_tool_def(self, target, tool):
        return ProGenDef(tool).get_tool_definition(target)

    def is_supported(self, target, tool):
        return ProGenDef(tool).is_supported(target)

    def update_definitions(self, force=False, settings=ProjectSettings()):
        # TODO: deprecated
        logging.debug("Definitions are not updated, please use python module project_generator_definitions")
        return

def mcu_create(ToolParser, mcu_name, proj_file, tool):
    # TODO: deprecated
    logging.debug("Definitions are not updated, please use python module project_generator_definitions")
    return

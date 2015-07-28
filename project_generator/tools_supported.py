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

import os
import logging
import subprocess
import yaml

from .targets import Targets
from .tools.iar import IAREmbeddedWorkbench
from .tools.uvision import Uvision
from .tools.coide import Coide
from .tools.eclipse import EclipseGnuARM
from .tools.gccarm import MakefileGccArm
from .tools.sublimetext import SublimeTextMakeGccARM
from .tools.gdb import GDB
from .tools.gdb import ARMNoneEABIGDB

class ToolsSupported:
    """ Represents all tools available """

    # Tools dictionary
    # Each of this tool needs to support at least:
    # - get_toolchain (toolchain is a list of toolchains supported by tool)
    # - get_toolname (returns name string)
    # - export_project (basic functionality to be covered by a tool)
    TOOLS_DICT = {
        'iar_arm':              IAREmbeddedWorkbench,
        'uvision':              Uvision,
        'coide':                Coide,
        'make_gcc_arm':         MakefileGccArm,
        'eclipse_make_gcc_arm': EclipseGnuARM,
        'sublime_make_gcc_arm': SublimeTextMakeGccARM,
        'gdb':                  GDB,
        'arm_none_eabi_gdb':    ARMNoneEABIGDB,
    }

    TOOLCHAINS = list(set([v.get_toolchain() for k, v in TOOLS_DICT.items() if v.get_toolchain() is not None]))
    TOOLS = list(set([v for k, v in TOOLS_DICT.items() if v is not None]))

    def get_tool(self, tool):
        try:
            return self.TOOLS_DICT[tool]
        except KeyError:
            return None

    def get_toolnames(self, tool):
        try:
            return self.TOOLS_DICT[tool].get_toolnames()
        except KeyError:
            return None

    def get_toolchain(self, tool):
        try:
            return self.TOOLS_DICT[tool].get_toolchain()
        except KeyError:
            return None

    def get_supported(self):
        return self.TOOLS_DICT.keys()

def target_supported(exporter, target, tool, env_settings):
    if exporter not in ToolsSupported().get_supported():
        raise RuntimeError("Target does not support specified tool: %s" % tool)
    else:
        supported = exporter.is_supported_by_default(target)
        # target requires further definitions for exporter
        if not supported:
            Target = Targets(env_settings.get_env_settings('definitions'))
            supported = Target.is_supported(target, tool)
        return supported

def mcu_create(ToolParser, mcu_name, proj_file, tool):
    data = ToolParser(None, None).get_mcu_definition(proj_file)
    data['mcu']['name'] = [mcu_name]
    # we got target, now damp it to root using target.yaml file
    # we can make it better, and ask for definitions repo clone, and add it
    # there, at least to MCU folder
    with open(os.path.join(os.getcwd(), mcu_name + '.yaml'), 'wt') as f:
        f.write(yaml.safe_dump(data, default_flow_style=False, width=200))
    return 0

def load_definitions(def_dir=None):
    definitions_directory = def_dir
    if not definitions_directory:
        config_directory = os.path.expanduser('~/.pg')
        definitions_directory = os.path.join(config_directory, 'definitions')

        if not os.path.isdir(config_directory):
            logging.debug("Config directory does not exist.")
            logging.debug("Creating config directory: %s" % config_directory)
            os.mkdir(config_directory)

        if os.path.isdir(definitions_directory):
            command = ['git', 'pull', '--rebase' ,'origin', 'master']
            subprocess.call(command, cwd=definitions_directory)
        else:
            command = ['git', 'clone',
                       'https://github.com/project-generator/project_generator_definitions.git', definitions_directory]
            subprocess.call(command, cwd=config_directory)

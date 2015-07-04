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

    # Tools dictionary, defines toolchain and all tools used
    TOOLS = {
        'iar_arm': {
            'toolchain': 'iar',
            'toolnames': ['iar_arm'],
            'exporter': IAREmbeddedWorkbench,
            'builder': IAREmbeddedWorkbench,
            'flasher': IAREmbeddedWorkbench,
        },
        'uvision': {
            'toolchain': 'uvision',
            'toolnames': ['uvision'],
            'exporter': Uvision,
            'builder': Uvision,
            'flasher': Uvision,
        },
        'coide': {
            'toolchain': 'gcc_arm',
            'toolnames': ['coide'],
            'exporter': Coide,
            'builder': None,
            'flasher': None,
        },
        'make_gcc_arm': {
            'toolchain': 'gcc_arm',
            'toolnames': ['make_gcc_arm'],
            'exporter': MakefileGccArm,
            'builder': MakefileGccArm,
            'flasher': None,
        },
        'eclipse_make_gcc_arm': {
            'toolchain': 'gcc_arm',
            'toolnames': ['eclipse_make_gcc_arm', 'make_gcc_arm'],
            'exporter': EclipseGnuARM,
            'builder': None,
            'flasher': None,
        },
        'sublime_make_gcc_arm': {
            'toolchain': 'gcc_arm',
            'toolnames': ['sublime_make_gcc_arm', 'make_gcc_arm', 'sublime'],
            'exporter': SublimeTextMakeGccARM,
            'builder': MakefileGccArm,
            'flasher': None,
        },
        'sublime': {
            'toolchain': None,
            'toolnames': ['sublime'],
            'exporter': None,
            'builder': None,
            'flasher': None,
        },
        'gdb': {
            'toolchain': None,
            'toolnames': ['gdb'],
            'exporter': GDB,
            'builder': None,
            'flasher': None,
        },
        'arm_none_eabi_gdb': {
            'toolchain': None,
            'toolnames': ['gdb'],
            'exporter': ARMNoneEABIGDB,
            'builder': None,
            'flasher': None,
        },
    }

    TOOLCHAINS = list(set([v['toolchain'] for k, v in TOOLS.items() if v['toolchain'] is not None]))
    EXPORTERS = list(set([v['exporter'] for k, v in TOOLS.items() if v['exporter'] is not None]))
    BUILDERS = list(set([v['builder'] for k, v in TOOLS.items() if v['builder'] is not None]))
    FLASHERS = list(set([v['flasher'] for k, v in TOOLS.items() if v['flasher'] is not None]))

    def get_value(self, tool, key):
        try:
            value = self.TOOLS[tool][key]
        except (KeyError, TypeError):
            raise RuntimeError("%s does not support specified tool: %s" % (key, tool))
        return value

    def get_supported(self):
        return self.TOOLS.keys()

def export(exporter, project_workspace, tool, env_settings):
    """ Invokes tool generator. """
    if exporter not in ToolsSupported().EXPORTERS:
        raise RuntimeError("Exporter does not support specified tool: %s" % tool)
    else:
        return exporter(project_workspace, env_settings).export_project()

def fixup_executable(exporter, executable_path, tool):
    """ Perform any munging of the executable necessary to debug it with the specified tool. """
    if exporter not in ToolsSupported().EXPORTERS:
        raise RuntimeError("Exporter does not support specified tool: %s" % tool)
    else:
        return exporter().fixup_executable(executable_path)

def target_supported(exporter, target, tool, env_settings):
    # TODO 0xc0170: fix, target supported goes to the tool, not exporter
    if exporter not in ToolsSupported().EXPORTERS:
        raise RuntimeError("Target does not support specified tool: %s" % tool)
    else:
        supported = exporter().is_supported_by_default(target)
        # target requires further definitions for exporter
        if not supported:
            Target = Targets(env_settings.get_env_settings('definitions'))
            supported = Target.is_supported(target, tool)
        return supported

def build(builder, project_name, project_files, tool, env_settings):
    """ Invokes builder for specified tool. """
    if builder not in ToolsSupported().BUILDERS:
        raise RuntimeError("Builder does not support specified tool: %s" % tool)
    else:
        builder().build_project(project_name, project_files, env_settings)

def flash(flasher, proj_dic, project_name, project_files, tool, env_settings):
    """ Invokes flasher for specified tool. """
    if flasher not in ToolsSupported().FLASHERS:
        raise RuntimeError("Flasher does not support specified tool: %s" % tool)
    else:
        flasher().flash_project(proj_dic, project_name, project_files, env_settings)

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

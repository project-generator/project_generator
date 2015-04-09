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

from .builders.iar import IARBuilder
from .builders.gccarm import MakefileGccArmBuilder
from .builders.uvision import UvisionBuilder
from .exporters.iar import IAREWARMExporter
from .exporters.coide import CoideExporter
from .exporters.gccarm import MakefileGccArmExporter
from .exporters.uvision import UvisionExporter
from .exporters.eclipse import EclipseGnuARMExporter
from .exporters.gdb import GDBExporter
from .exporters.gdb import ARMNoneEABIGDBExporter
from .exporters.sublimetext import SublimeTextMakeGccARMExporter


class ToolsSupported:
    """ Represents all tools available """

    # Tools dictionary, defines toolchain and all tools used
    TOOLS = {
        'iar_arm': {
            'toolchain' : 'iar',
            'toolnames' : ['iar_arm'],
            'exporter' : IAREWARMExporter,
            'builder' : IARBuilder,
        },
        'uvision': {
            'toolchain' : 'uvision',
            'toolnames' : ['uvision'],
            'exporter' : UvisionExporter,
            'builder' : UvisionBuilder,
        },
        'coide': {
            'toolchain' : 'gcc_arm',
            'toolnames' : ['coide'],
            'exporter' : CoideExporter,
            'builder' : None,
        },
        'make_gcc_arm': {
            'toolchain' : 'gcc_arm',
            'toolnames' : ['make_gcc_arm'],
            'exporter' : MakefileGccArmExporter,
            'builder' : MakefileGccArmBuilder,
        },
        'eclipse_make_gcc_arm': {
            'toolchain' : 'gcc_arm',
            'toolnames' : ['eclipse_make_gcc_arm', 'make_gcc_arm'],
            'exporter' : EclipseGnuARMExporter,
            'builder' : None,
        },
        'sublime_make_gcc_arm' : {
            'toolchain' : 'gcc_arm',
            'toolnames' : ['sublime_make_gcc_arm', 'make_gcc_arm', 'sublime'],
            'exporter' : SublimeTextMakeGccARMExporter,
            'builder' : MakefileGccArmBuilder,
        },
        'sublime' : {
            'toolchain' : None,
            'toolnames' : ['sublime'],
            'exporter' : None,
            'builder' : None,
        },
        'gdb' : {
            'toolchain' : None,
            'toolnames' : ['gdb'],
            'exporter' : GDBExporter,
            'builder' : None,
        },
        'arm_none_eabi_gdb' : {
            'toolchain' : None,
            'toolnames' : ['gdb'],
            'exporter' : ARMNoneEABIGDBExporter,
            'builder' : None,
        },
    }

    TOOLCHAINS = list(set([v['toolchain'] for k,v in TOOLS.items() if v['toolchain'] is not None]))

    def get_value(self, tool, key):
        try:
            value = self.TOOLS[tool][key]
        except (KeyError, TypeError):
            raise RuntimeError("%s does not support specified tool: %s" % (key, tool))
        return value

def export(exporter, data, tool, env_settings):
    """ Invokes tool generator. """
    try:
        project_path, projectfiles = exporter().generate(data, env_settings)
    except TypeError:
        raise RuntimeError("Exporter does not support specified tool: %s" % tool)
    return project_path, projectfiles

def fixup_executable(exporter, executable_path, tool):
    """ Perform any munging of the executable necessary to debug it with the specified tool. """
    try:
        return exporter().fixup_executable(executable_path)
    except TypeError:
        raise RuntimeError("Exporter does not support specified tool: %s" % tool)

def target_supported(exporter, target, tool, env_settings):
    try:
        supported = exporter().is_supported_by_default(target)
    except TypeError:
        raise RuntimeError("Target does not support specified tool: %s" % tool)
    # target requires further definitions for exporter
    if not supported:
        Target = Targets(env_settings.get_env_settings('definitions'))
        supported = Target.is_supported(target, tool)
    return supported

def build(builder, project_name, project_files, tool, env_settings):
    """ Invokes builder for specified tool. """
    try:
        builder().build_project(project_name, project_files, env_settings)
    except TypeError:
        raise RuntimeError("Builder does not support specified tool: %s" % tool)

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
            command = ['git', 'clone', 'https://github.com/0xc0170/project_generator_definitions.git', definitions_directory]
            subprocess.call(command, cwd=config_directory)

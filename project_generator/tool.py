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

# exporters
from .exporters.iar import IAREWARMExporter
from .exporters.coide import CoideExporter
from .exporters.gccarm import MakefileGccArmExporter
from .exporters.uvision import UvisionExporter
from .exporters.eclipse import EclipseGnuARMExporter
from .exporters.gdb import GDBExporter
from .exporters.gdb import ARMNoneEABIGDBExporter
from .targets import Targets
# builders
from .builders.iar import IARBuilder
from .builders.gccarm import MakefileGccArmBuilder
from .builders.uvision import UvisionBuilder

EXPORTERS = {
    'uvision': UvisionExporter,
    'make_gcc_arm': MakefileGccArmExporter,
    'iar_arm': IAREWARMExporter,
    'coide': CoideExporter,
    'eclipse_make_gcc_arm': EclipseGnuARMExporter,
    'gdb' : GDBExporter,
    'arm_none_eabi_gdb' : ARMNoneEABIGDBExporter,
}

BUILDERS = {
    'uvision': UvisionBuilder,
    'make_gcc_arm': MakefileGccArmBuilder,
    'iar_arm': IARBuilder,
}

def export(data, tool, env_settings):
    """ Invokes tool generator. """
    if tool not in EXPORTERS:
        raise RuntimeError("Exporter does not support specified tool: %s" % tool)

    Exporter = EXPORTERS[tool]
    exporter = Exporter()
    project_path, projectfiles = exporter.generate(data, env_settings)
    return project_path, projectfiles

def fixup_executable(executable_path, tool):
    """ Perform any munging of the executable necessary to debug it with the specified tool. """
    exporter = EXPORTERS[tool]()
    return exporter.fixup_executable(executable_path)

def target_supported(target, tool, env_settings):
    Target = Targets(env_settings.get_env_settings('definitions'))
    return Target.is_supported(target, tool)

def build(project_name, project_files, tool, env_settings):
    """ Invokes builder for specified tool. """
    if tool not in BUILDERS:
        raise RuntimeError("Builder does not support specified tool.")

    Builder = BUILDERS[tool]
    builder = Builder()
    builder.build_project(project_name, project_files, env_settings)

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

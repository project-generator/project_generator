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

# TODO - these 4 functions below can be probbly removed completely

def export(exporter, data, tool, env_settings):
    """ Invokes tool generator. """
    project_path, projectfiles = exporter.generate(data, env_settings)
    return project_path, projectfiles

def fixup_executable(exporter, executable_path, tool):
    """ Perform any munging of the executable necessary to debug it with the specified tool. """
    return exporter.fixup_executable(executable_path)

def target_supported(target, tool, env_settings):
    Target = Targets(env_settings.get_env_settings('definitions'))
    return Target.is_supported(target, tool)

def build(builder, project_name, project_files, tool, env_settings):
    """ Invokes builder for specified tool. """
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

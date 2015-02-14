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

"""
Settings needed:
UV4
IARBUILD
PROJECT_ROOT
GCC_BIN_PATH
"""

import os
import yaml

from os.path import join, pardir, sep
from .yaml_parser import YAML_parser, _finditem

class ProjectSettings:
    PROJECT_ROOT = os.environ.get('PROJECT_GENERATOR_ROOT') or join(pardir, pardir)
    DEFAULT_TOOL = os.environ.get('PROJECT_GENERATOR_DEFAULT_TOOL') or 'uvision'

    def __init__(self):
        """ This are default enviroment settings for build tools. To override,
        define them in the projects.yaml file. """
        self.paths = {}
        self.paths['uvision'] = os.environ.get('UV4') or join('C:', sep,
            'Keil', 'UV4', 'UV4.exe')
        self.paths['iar'] = os.environ.get('IARBUILD') or join(
            'C:', sep, 'Program Files (x86)',
            'IAR Systems', 'Embedded Workbench 7.0',
            'common', 'bin', 'IarBuild.exe')
        self.paths['gcc'] = os.environ.get('ARM_GCC_PATH') or ''

    def load_env_settings(self, config_file):
        """ Loads predefined settings if any, otherwise default used. """
        settings = 0
        try:
            for k, v in config_file.items():
                if k == 'settings':
                    settings = v
        except KeyError:
            pass
        if settings:
            uvision = _finditem(settings, 'uvision')
            if uvision:
                self.paths['uvision'] = uvision
            iar = _finditem(settings, 'iar')
            if iar:
                self.paths['iar'] = iar
            gcc = _finditem(settings, 'gcc')
            if gcc:
                self.paths['gcc'] = gcc

    def get_env_settings(self, env_set):
        return self.paths[env_set]


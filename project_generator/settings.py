# Copyright 2014-2015 0xc0170
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

from os.path import normpath, join, pardir, sep

class ProjectSettings:
    PROJECT_ROOT = os.environ.get('PROJECT_GENERATOR_ROOT') or join(pardir, pardir)
    DEFAULT_TOOL = os.environ.get('PROJECT_GENERATOR_DEFAULT_TOOL') or 'uvision'

    DEFAULT_EXPORT_LOCATION_FORMAT = join('generated_projects', '{tool}_{project_name}')
    DEFAULT_ROOT = os.getcwd()

    def __init__(self):
        """ This are default enviroment settings for build tools. To override,
        define them in the projects.yaml file. """

        self.paths = {}
        self.templates = {}
        self.paths['uvision'] = os.environ.get('UV4') or join('C:', sep,
            'Keil', 'UV4', 'UV4.exe')
        self.paths['iar'] = os.environ.get('IARBUILD') or join(
            'C:', sep, 'Program Files (x86)',
            'IAR Systems', 'Embedded Workbench 7.0',
            'common', 'bin')
        self.paths['gcc'] = os.environ.get('ARM_GCC_PATH') or ''

        self.export_location_format = self.DEFAULT_EXPORT_LOCATION_FORMAT
        self.root = os.getcwd()

    def update(self, settings):
        if settings:
            if 'tools' in settings:
                for k, v in settings['tools'].items():
                    if k in self.paths:
                        if 'path' in v.keys():
                            self.paths[k] = v['path'][0]
                    if 'template' in v.keys():
                        self.templates[k] = v['template']

            if 'export_dir' in settings:
                self.export_location_format = normpath(settings['export_dir'][0])
            if 'root' in settings:
                self.root = normpath(settings['root'][0])

    def get_env_settings(self, env_set):
        return self.paths[env_set]

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

import os
import copy
import logging
import subprocess

from copy import deepcopy
from os.path import join, normpath, dirname, exists
from .tool import Tool, Exporter
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.cmake')

class CMake(Tool,Exporter):

    ERRORLEVEL = {
        0: 'no errors',
        1: 'targets not already up to date',
        2: 'errors'
    }

    SUCCESSVALUE = 0

    generated_project = {
        'path': '',
        'files': {
            'cmakelist': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.workspace = workspace
        self.exporter = MakefileGccArm(workspace, env_settings)
        self.env_settings = env_settings
        self.logging = logging

    def get_template(self):
        raise NotImplementedError()

    def get_workspace_template(self):
        raise NotImplementedError()

    def fix_paths_unix(self, data):
        # cmake seems to require unix paths
        # This might do proper handling in the gcc arm, pass there a param (force normpath to unix)
        output_dir = os.path.join(os.getcwd(), data['output_dir']['path'].replace('\\', '/'))
        for key in SOURCE_KEYS:
            paths = []
            for value in data[key]:
                # TODO: this needs to be fixed
                if value:
                    paths.append(normpath(os.path.join(output_dir, value)).replace('\\', '/'))
            data[key] = paths

        for k in ['include_paths', 'lib_paths']:
            paths = [path for path in data[k] if path]
            paths = [normpath(os.path.join(output_dir, path)).replace('\\', '/') for path in paths]
            data[k] = paths

        # Those paths are not fixed
        for k in ['pre_build_script', 'post_build_script']:
            if k not in data:
                continue
            paths = [path for path in data[k] if path]
            paths = [normpath(os.path.join(os.getcwd(), path)).replace('\\', '/') for path in paths]
            data[k] = paths

        if 'linker_file' in data and data['linker_file']:
            data['linker_file'] = normpath(os.path.join(output_dir, data['linker_file'])).replace('\\', '/')

    def export_project(self):
        generated_projects = {}
        generated_projects = copy.deepcopy(self.generated_project)

        data_for_make = self.workspace.copy()
        # Warning: we dont use rel path for cmake, we inject there root and use paths within root
        data_for_make['output_dir']['rel_path'] = ""
        self.exporter.process_data_for_makefile(data_for_make)
        try:
            data_for_make['misc'] = data_for_make['misc']
        except:
            pass

        self.fix_paths_unix(data_for_make)

        generated_projects['path'], generated_projects['files']['cmakelist'] = self.gen_file_jinja(
            self.get_template(), data_for_make, 'CMakeLists.txt', data_for_make['output_dir']['path'])
        return generated_projects

    def export_workspace(self):
        vars = { 'projects': [os.path.basename(p['path']) for p in self.workspace['projects']],
                 'name': self.workspace['settings']['name'] }
        generated_projects = deepcopy(self.generated_project)
        generated_projects['path'], makefile = \
            self.gen_file_jinja(self.get_workspace_template(), vars, 'CMakeLists.txt',
                                os.path.dirname(self.workspace['settings']['path']))
        generated_projects['files']['cmakelist'] = [makefile] + \
            [os.path.basename(p['files']['cmakelist']) for p in self.workspace['projects']]
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['cmakelist']]}

    def build_project(self, **kwargs):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = dirname(self.workspace['files']['cmakelist'])
        self.logging.debug("Building make project: %s" % path)

        build_path = join(path, "build")
        if not exists(build_path):
            os.mkdir(build_path)

        generator = kwargs['generator'] if 'generator' in kwargs else 'make'
        generators = {
            'make': { 'command': 'make', 'generator': 'Unix Makefiles' },
            'mingw-make': { 'command': 'make', 'generator': 'MinGW Makefiles' },
            'msys-make': { 'command': 'make', 'generator': 'MSYS Makefiles' },
            'ninja': { 'command': 'ninja', 'generator': 'Ninja' },
            'nmake': { 'command': 'nmake', 'generator': 'NMake Makefiles' }
        }

        cmd = generators[generator]['command']
        gen = generators[generator]['generator']

        args = ['cmake', '-G', gen, "-S", path, "-B", build_path]
        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            self.logging.error("Project: %s build error whilst calling cmake with '%s' generator. Are all programs needed it in your PATH?" %
                (self.workspace['files']['cmakelist'], gen))
            return -1

        args = [cmd, "-C", build_path]
        if generator == 'ninja':
            if 'verbose' in kwargs and kwargs['verbose']:
                args += ['-v']
            if 'jobs' not in kwargs:
                args += ['-j', '1']
        else:
            if 'jobs' in kwargs:
                args += ['-j', str(kwargs['jobs'])]
            if 'verbose' in kwargs and kwargs['verbose']:
                args += ["VERBOSE=1"]
            args += ['all']

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            self.logging.error("Project: %s build error whilst calling make. Is '%s' in your PATH?" %
                (self.workspace['files']['cmakelist'], cmd))
            return -1
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                if ret_code < 3:
                    self.logging.error("Project: %s build failed with the status: %s" %
                                  (self.ERRORLEVEL[ret_code], self.workspace['files']['cmakelist']))
                else:
                    self.logging.error("Project: %s build failed with unknown error. Returned: %s" %
                                   (ret_code, self.workspace['files']['cmakelist']))
                return -1
            else:
                name = os.path.basename(self.workspace['path'])
                self.logging.info("Built %s with the status: %s" %
                             (name, self.ERRORLEVEL[ret_code]))
                return 0

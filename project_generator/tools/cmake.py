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

from os.path import join, normpath, dirname, exists
from .tool import Tool, Exporter
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.cmake_gcc_arm')

class CMakeGccArm(Tool,Exporter):

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
        self.workspace['preprocess_linker_file'] = True


    @staticmethod
    def get_toolnames():
        return ['cmake_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def fix_paths_unix(self, data):
        # cmake seems to require unix paths
        # This might do proper handling in the gcc arm, pass there a param (force normpath to unix)
        output_dir = os.path.join(os.getcwd(), data['output_dir']['path'].replace('\\', '/'))
        for key in SOURCE_KEYS:
            paths = []
            for value in data[key]:
                # TODO: this needs to be fixed
                if value:
                    v = value.replace('\\', '/')
                    paths.append(normpath(os.path.join(output_dir, v)))
            data[key] = paths
        # fix includes
        includes = []
        for key in data['include_paths']:
            if key:
                k = key.replace('\\', '/')
                includes.append(normpath(os.path.join(output_dir, k)))
        data['include_paths'] = includes

        if 'linker_file' in data and data['linker_file']:
            lf = data['linker_file'].replace('\\', '/')
            data['linker_file'] = normpath(os.path.join(output_dir, lf))

        lib_paths = []
        for path in data['lib_paths']:
            if path:
                p = path.replace('\\', '/')
                lib_paths.append(paths.append(normpath(os.path.join(output_dir, p))))
        data['lib_paths'] = lib_paths

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
            'cmakelistgccarm.tmpl', data_for_make, 'CMakeLists.txt', data_for_make['output_dir']['path'])
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

        use_ninja = True if os.environ.get("USE_NINJA") else False
        gen = 'Ninja' if use_ninja else 'Unix Makefiles'

        args = ['cmake', '-G', gen, "-S", path, "-B", build_path]
        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            self.logging.error("Project: %s build error whilst calling cmake. Is it in your PATH?" % self.workspace['files']['cmakelist'])
            return -1

        if use_ninja:
            args = ['ninja', "-C", build_path]
            if 'verbose' in kwargs and kwargs['verbose']:
                args += '-v'
        else:
            args = ['make', "-C", build_path]
            try:
                args += ['-j', str(kwargs['jobs'])]
            except KeyError:
                pass
            if 'verbose' in kwargs:
                args += ["VERBOSE=%d" % (1 if kwargs['verbose'] else 0)]
            args += ['all']

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            self.logging.error("Project: %s build error whilst calling make. Is it in your PATH?" % self.workspace['files']['cmakelist'])
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

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

import copy
import logging
import subprocess
from os import getcwd
from os.path import dirname

from .tool import Tool, Exporter
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.cmake_gcc_arm')

class CMakeGccArm(Tool,Exporter):

    SUCCESSVALUE = 0
    ERRORLEVEL = {
        0: 'no errors)',
        1: 'targets not already up to date',
        2: 'errors'
    }

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

    @staticmethod
    def get_toolnames():
        return ['cmake_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def fix_paths_unix(self, data):
        # cmake seems to require unix paths
        # This might do proper handling in the gcc arm, pass there a param (force normpath to unix)
        for key in SOURCE_KEYS:
            paths = []
            for value in data[key]:
                # TODO: this needs to be fixed
                paths.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + value.replace('\\', '/'))
            data[key] = paths
        # fix includes
        includes = []
        for key in data['include_paths']:
            includes.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + key.replace('\\', '/'))
        data['include_paths'] = includes
        data['linker_file'] = getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + data['linker_file'].replace('\\', '/')
        lib_paths = []
        for path in data['lib_paths']:
            lib_paths.append(getcwd().replace('\\', '/') + '/' + data['output_dir']['path'].replace('\\', '/') + '/' + path.replace('\\', '/'))
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

    def build_project(self):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = dirname(self.workspace['files']['cmakelist'])
        logging.debug("Building GCC ARM project: %s" % path)

        args = ['cmake', '.']
        logging.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args, cwd=path)
        except:
            logging.error("Project: %s build error whilst calling cmake. Is it in your PATH?" % self.workspace['files']['cmakelist'])
            return -1
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                if ret_code < 3:
                    logging.error("Project: make failed with the status: %s" %
                                  (self.ERRORLEVEL[ret_code]))
                else:
                    logging.error("Project: make failed with unknown error. Returned: %s" %
                                   (ret_code))
                return -1
            else:

                logging.info("CMake succeeded with the status: %s" %
                             self.ERRORLEVEL[ret_code])

                args = ['make', 'all']
                logging.debug(args)

                try:
                    ret_code = None
                    ret_code = subprocess.call(args, cwd=path)
                except:
                    logging.error("Project: build error whilst calling make. Is it in your PATH?")
                    return -1
                else:
                    if ret_code != self.SUCCESSVALUE:
                        # Seems like something went wrong.
                        if ret_code < 3:
                            logging.error("Project: make failed with the status: %s" %
                                        (self.ERRORLEVEL[ret_code]))
                        else:
                            logging.error("Project:make failed with unknown error. Returned: %s" %
                                        (ret_code))
                        return -1
                    else:
                        logging.info("Build succeeded with the status: %s" %
                                    self.ERRORLEVEL[ret_code])
                        return 0

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

import copy
import os
import logging
import ntpath
import subprocess

from os.path import join, normpath,dirname
from .tool import Tool,Exporter
from ..targets import Targets
from .tool import Tool, Exporter

class MakefileGccArm(Tool,Exporter):

    # http://www.gnu.org/software/make/manual/html_node/Running.html
    ERRORLEVEL = {
        0: 'success (0 warnings, 0 errors)',
        1: 'targets not already up to date',
        2: 'errors'
    }

    SUCCESSVALUE = 0

    optimization_options = ['O0', 'O1', 'O2', 'O3', 'Os']

    generated_projects = {
        'path': '',
        'files': {
            'makefile' : '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['make_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def _list_files(self, data, attribute, rel_path):
        """ Creates a list of all files based on the attribute. """
        file_list = []
        for k, v in data[attribute].items():
            for file in v:
                file_list.append(join(rel_path, normpath(file)))
        data[attribute] = file_list

    def _libraries(self, key, value, data):
        """ Add defined GCC libraries. """
        for option in value:
            if key == "libraries":
                data['source_files_lib'].append(option)

    def _compiler_options(self, key, value, data):
        """ Compiler flags """
        for option in value:
            if key == "compiler_options":
                data['compiler_options'].append(option)

    def _linker_options(self, key, value, data):
        """ Linker flags """
        for option in value:
            if key == "linker_options":
                data['linker_options'].append(option)

    def _optimization(self, key, value, data):
        """ Optimization setting. """
        for option in value:
            if option in self.optimization_options:
                data['optimization_level'] = option

    def _cc_standard(self, key, value, data):
        """ C++ Standard """
        if key == "cc_standard":
            data['cc_standard'] = value

    def _c_standard(self, key, value, data):
        """ C Standard """
        if key == "c_standard":
            data['c_standard'] = value

    def _parse_specific_options(self, data):
        """ Parse all uvision specific setttings. """
        data['compiler_options'] = []
        for dic in data['misc']:
            for k, v in dic.items():
                self._libraries(k, v, data)
                self._compiler_options(k, v, data)
                self._optimization(k, v, data)
                self._cc_standard(k, v, data)
                self._c_standard(k, v, data)

        data['linker_options'] = []
        for dic in data['misc']:
            for k, v in dic.items():
                self._linker_options(k, v, data)

    def _lib_names(self, libs):
        for lib in libs:
            head, tail = ntpath.split(lib)
            file = tail
            if (os.path.splitext(file)[1] != ".a"):
                continue
            else:
                file = file.replace(".a","")
                yield ("-L"+head,file.replace("lib","-l"))

    def _fix_paths(self, data):
        # get relative path and fix all paths within a project
        fixed_paths = []
        for path in data['includes']:
            fixed_paths.append(join(data['output_dir']['rel_path'], normpath(path)))

        data['includes'] = fixed_paths

        libs = []
        for k in data['source_files_lib'].keys():
            libs.extend([normpath(join(data['output_dir']['rel_path'], path))
                         for path in data['source_files_lib'][k]])

        data['lib_paths'] =[]
        data['libraries'] =[]
        for path, lib in self._lib_names(libs):
            data['lib_paths'].append(path)
            data['libraries'].append(lib)

        fixed_paths = []
        for path in data['source_paths']:
            fixed_paths.append(join(data['output_dir']['rel_path'], normpath(path)))

        data['source_paths'] = fixed_paths
        if data['linker_file']:
            data['linker_file'] = join(data['output_dir']['rel_path'], normpath(data['linker_file']))

    def export_workspace(self):
        logging.debug("Current version of CoIDE does not support workspaces")

    def export_project(self):
        """ Processes misc options specific for GCC ARM, and run generator. """
        generated_projects = copy.deepcopy(self.generated_projects)
        self.process_data_for_makefile(self.workspace)
        generated_projects['path'], generated_projects['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', self.workspace, 'Makefile', self.workspace['output_dir']['path'])
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['makefile']]}


    def process_data_for_makefile(self, data):
        self._fix_paths(data)
        self._list_files(data, 'source_files_c', data['output_dir']['rel_path'])
        self._list_files(data, 'source_files_cpp', data['output_dir']['rel_path'])
        self._list_files(data, 'source_files_s', data['output_dir']['rel_path'])
        self._list_files(data, 'source_files_obj', data['output_dir']['rel_path'])

        self._parse_specific_options(data)
        data['toolchain'] = 'arm-none-eabi-'
        data['toolchain_bin_path'] = self.env_settings.get_env_settings('gcc')

        target = Targets(self.env_settings.get_env_settings('definitions'))

        if target.get_mcu_core(data['target'].lower()):
            data['core'] = target.get_mcu_core(data['target'].lower())[0]
        else:
            raise RuntimeError(
                "Target: %s not found, Please add them to https://github.com/project-generator/project_generator_definitions" % data['target'].lower())

        # gcc arm is funny about cortex-m4f.
        if data['core'] == 'cortex-m4f':
            data['core'] = 'cortex-m4'

        # change cortex-m0+ to cortex-m0plus
        if data['core'] == 'cortex-m0+':
            data['core'] = 'cortex-m0plus'

        # set default values
        if 'optimization_level' not in data:
            data['optimization_level'] = self.optimization_options[0]

    def build_project(self):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = dirname(self.workspace['files']['makefile'])
        logging.debug("Building GCC ARM project: %s" % path)

        args = ['make', 'all']
        logging.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args, cwd=path)
        except:
            logging.error("Error whilst calling make. Is it in your PATH?")
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                if ret_code < 3:
                    logging.error("Build failed with the status: %s" %
                                  self.ERRORLEVEL[ret_code])
                else:
                    logging.error("Build failed with unknown error. Returned: %s" %
                                   ret_code)
            else:
                logging.info("Build succeeded with the status: %s" %
                             self.ERRORLEVEL[ret_code])

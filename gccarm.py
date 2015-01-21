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
from __future__ import print_function

import logging
import subprocess
from os.path import basename, relpath, join
from exporter import Exporter
from default_settings import gcc_bin_path

from builder import Builder


class MakefileGccArmExporter(Exporter):
    optimization_options = ['O0', 'O1', 'O2', 'O3', 'Os']

    def list_files(self, data, attribute):
        """ Creates a list of all files based on the attribute. """
        file_list = []
        for groups in data[attribute]:
            try:
                for k, v in groups.items():
                    for file in v:
                        file_list.append(file)
            except:
                continue
        data[attribute] = file_list

    def libraries(self, key, value, data):
        """ Add defined GCC libraries. """
        for option in value:
            if key == "libraries":
                data['source_files_lib'].append(option)

    def compiler_options(self, key, value, data):
        """ Compiler flags """
        for option in value:
            if key == "compiler_options":
                data['compiler_options'].append(option)

    def linker_options(self, key, value, data):
        """ Linker flags """
        for option in value:
            if key == "linker_options":
                data['linker_options'].append(option)

    def optimization(self, key, value, data):
        """ Optimization setting. """
        for option in value:
            if option in self.optimization_options:
                data['optimization_level'] = option

    def cc_standard(self, key, value, data):
        """ C++ Standard """
        if key == "cc_standard":
            data['cc_standard'] = value

    def c_standard(self, key, value, data):
        """ C Standard """
        if key == "c_standard":
            data['c_standard'] = value

    def parse_specific_options(self, data):
        """ Parse all uvision specific setttings. """
        data['compiler_options'] = []
        for dic in data['misc']:
            for k, v in dic.items():
                self.libraries(k, v, data)
                self.compiler_options(k, v, data)
                self.optimization(k, v, data)
                self.cc_standard(k, v, data)
                self.c_standard(k, v, data)

    def generate(self, data):
        """ Processes misc options specific for GCC ARM, and run generator. """
        self.process_data_for_makefile(data)

        project_path = self.gen_file('makefile_gcc.tmpl', data, 'Makefile', "gcc_arm", data['project_dir']['path'], data['project_dir']['name'])
        return project_path

    def process_data_for_makefile(self, data):
        self.list_files(data, 'source_files_c')
        self.list_files(data, 'source_files_cpp')
        self.list_files(data, 'source_files_s')

        self.parse_specific_options(data)
        data['toolchain'] = 'arm-none-eabi-'
        data['toolchain_bin_path'] = gcc_bin_path

        # gcc arm is funny about cortex-m4f.
        if data['core'] == 'cortex-m4f':
            data['core'] = 'cortex-m4'

        # change cortex-m0+ to cortex-m0plus
        if data['core'] == 'cortex-m0+':
            data['core'] = 'cortex-m0plus'

class MakefileGccArmBuilder(Builder):
    # http://www.gnu.org/software/make/manual/html_node/Running.html
    ERRORLEVEL = {
        0: 'success (0 warnings, 0 errors)',
        1: 'targets not already up to date',
        2: 'errors'
    }

    SUCCESSVALUE = 0

    def build_project(self, project_path, project):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = relpath(project_path)
        logging.debug("Building GCC ARM project: %s" % path)

        args = ['make', 'all']

        try:
            ret_code = None
            ret_code = subprocess.call(args, cwd=path)
        except:
            logging.error("Error whilst calling make. Is it in your PATH?")
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                logging.error("Build failed with the status: %s" %
                              self.ERRORLEVEL[ret_code])
            else:
                logging.info("Build succeeded with the status: %s" %
                             self.ERRORLEVEL[ret_code])

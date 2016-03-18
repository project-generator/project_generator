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
from itertools import chain

from os.path import join, normpath,dirname
from project_generator_definitions.definitions import ProGenDef

from .tool import Tool,Exporter
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.gccarm')

class MakefileGccArm(Tool, Exporter):

    # http://www.gnu.org/software/make/manual/html_node/Running.html
    ERRORLEVEL = {
        0: 'no errors)',
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

    def _parse_specific_options(self, data):
        """ Parse all specific setttings. """
        data['common_flags'] = []
        data['ld_flags'] = []
        data['c_flags'] = []
        data['cxx_flags'] = []
        data['asm_flags'] = []
        for k, v in data['misc'].items():
            if type(v) is list:
                if k not in data:
                    data[k] = []
                data[k].extend(v)
            else:
                if k not in data:
                    data[k] = ''
                data[k] = v

    def _get_libs(self, project_data):
        project_data['lib_paths'] =[]
        project_data['libraries'] =[]
        for lib in project_data['source_files_lib']:
            head, tail = ntpath.split(lib)
            file = tail
            if (os.path.splitext(file)[1] != ".a"):
                logging.debug("Found %s lib with non-valid extension (!=.a)" % file)
                continue
            else:
                file = file.replace(".a","")
                project_data['lib_paths'].append(head)
                project_data['libraries'].append(file.replace("lib",''))

    def export_workspace(self):
        logger.debug("Makefile GCC ARM currently does not support workspaces")

    def export_project(self):
        """ Processes misc options specific for GCC ARM, and run generator """
        generated_projects = copy.deepcopy(self.generated_projects)
        self.process_data_for_makefile(self.workspace)
        generated_projects['path'], generated_projects['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', self.workspace, 'Makefile', self.workspace['output_dir']['path'])
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['makefile']]}

    def process_data_for_makefile(self, project_data):
        #Flatten our dictionary, we don't need groups
        for key in SOURCE_KEYS:
            project_data[key] = list(chain(*project_data[key].values()))
        self._get_libs(project_data)
        self._parse_specific_options(project_data)

        project_data['toolchain'] = 'arm-none-eabi-'
        project_data['toolchain_bin_path'] = self.env_settings.get_env_settings('gcc')

        pro_def = ProGenDef()

        if pro_def.get_mcu_core(project_data['target'].lower()):
            project_data['core'] = pro_def.get_mcu_core(project_data['target'].lower())[0]
        else:
            raise RuntimeError(
                "Target: %s not found, Please add the target to https://github.com/project-generator/project_generator_definitions" % project_data['target'].lower())

        # gcc arm is funny about cortex-m4f.
        if project_data['core'] == 'cortex-m4f':
            project_data['core'] = 'cortex-m4'

        # change cortex-m0+ to cortex-m0plus
        if project_data['core'] == 'cortex-m0+':
            project_data['core'] = 'cortex-m0plus'

    def build_project(self):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = dirname(self.workspace['files']['makefile'])
        logger.debug("Building GCC ARM project: %s" % path)

        args = ['make', 'all']
        logger.debug(args)

        try:
            ret_code = None
            ret_code = subprocess.call(args, cwd=path)
        except:
            logger.error("Project: %s build error whilst calling make. Is it in your PATH?" % self.workspace['files']['makefile'])
            return -1
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                if ret_code < 3:
                    logger.error("Project: %s build failed with the status: %s" %
                                  (self.ERRORLEVEL[ret_code], self.workspace['files']['makefile']))
                else:
                    logger.error("Project: %s build failed with unknown error. Returned: %s" %
                                   (ret_code, self.workspace['files']['makefile']))
                return -1
            else:
                logger.info("Build succeeded with the status: %s" %
                             self.ERRORLEVEL[ret_code])
                return 0

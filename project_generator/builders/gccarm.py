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

import subprocess
import logging

from .builder import Builder
from os.path import dirname

class MakefileGccArmBuilder(Builder):
    # http://www.gnu.org/software/make/manual/html_node/Running.html
    ERRORLEVEL = {
        0: 'success (0 warnings, 0 errors)',
        1: 'targets not already up to date',
        2: 'errors'
    }

    SUCCESSVALUE = 0

    def build_project(self, project_name, project_files, env_settings):
        # cwd: relpath(join(project_path, ("gcc_arm" + project)))
        # > make all
        path = dirname(project_files[0])
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

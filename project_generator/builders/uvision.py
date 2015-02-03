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

from .builder import Builder
from .. import settings


class UvisionBuilder(Builder):
    ERRORLEVEL = {
        0: 'success (0 warnings, 0 errors)',
        1: 'warnings',
        2: 'errors',
        3: 'fatal errors',
        11: 'cant write to project file',
        12: 'device error',
        13: 'error writing',
        15: ' error reading xml file',
    }

    SUCCESSVALUE = 0

    def build_project(self, project_path, project):
        # > UV4 -b [project_path]
        path = join(self.root_path, project_path, "%s.uvproj" % project)
        logging.debug("Building uVision project: %s" % path)

        args = [settings.UV4, '-r', '-j0', path]

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error(
                "Error whilst calling UV4. Please check UV4 path in the user_settings.py file.")
        else:
            if ret_code != self.SUCCESSVALUE:
                # Seems like something went wrong.
                logging.error("Build failed with the status: %s" %
                              self.ERRORLEVEL[ret_code])
            else:
                logging.info("Build succeeded with the status: %s" %
                             self.ERRORLEVEL[ret_code])

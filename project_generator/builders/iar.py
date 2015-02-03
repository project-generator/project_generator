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

class IARBuilder(Builder):

    def build_project(self, project_path, project):
        # > IarBuild [project_path] -build [project_name]
        path = join(self.root_path, project_path, "%s.ewp" % project)
        logging.debug("Building IAR project: %s" % path)

        args = [settings.IARBUILD, path, '-build', project]

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error("Error whilst calling IarBuild. Please check IARBUILD path in the user_settings.py file.")
        else:
            # no IAR doc describes errors from IarBuild
            logging.info("Build completed.")

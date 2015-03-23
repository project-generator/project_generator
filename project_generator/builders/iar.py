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

import os
import subprocess
import logging

from .builder import Builder
from os.path import join

class IARBuilder(Builder):

    def build_project(self, project_name, project_files, env_settings):
        # > IarBuild [project_path] -build [project_name]
        path = join(os.getcwd(), project_files[0])
        logging.debug("Building IAR project: %s" % path)

        args = [env_settings.get_env_settings('iar'), path, '-build', project_name]

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error("Error whilst calling IarBuild. Please check IARBUILD path in the user_settings.py file.")
        else:
            # no IAR doc describes errors from IarBuild
            logging.info("Build completed.")

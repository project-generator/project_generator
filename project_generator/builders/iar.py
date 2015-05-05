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

import os
import subprocess
import logging
import time

from .builder import Builder
from os.path import join

class IARBuilder(Builder):

    def build_project(self, project_name, project_files, env_settings):
        # > IarBuild [project_path] -build [project_name]
        path = join(os.getcwd(), project_files[0])
        if path.split('.')[-1] != '.ewp':
            path = path + '.ewp'
        if not os.path.exists(path):
            logging.debug("The file: %s does not exists, exported prior building?" % path)
            return
        logging.debug("Building IAR project: %s" % path)

        args = [join(env_settings.get_env_settings('iar'), 'IarBuild.exe'), path, '-build', project_name]

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error("Error whilst calling IarBuild. Please check IARBUILD path in the user_settings.py file.")
        else:
            # no IAR doc describes errors from IarBuild
            logging.info("Build completed.")

    def flash_project(self, proj_dic, project_name, project_files, env_settings):
        # > [project_path]/settings/[project_name].[project_name].bat
        path = join(os.getcwd(), project_files[0])
        if path.split('.')[-1] != '.eww':
            path = path + '.eww'
        # to be able to flash, open and close IAR, to generate .bat - is there other way around this? IAR help
        child = subprocess.Popen([join(env_settings.get_env_settings('iar'), 'IarIdePm.exe'), path])
        time.sleep(5)
        child.terminate()
        path = join(os.path.dirname(path), 'settings', project_name) + '.' + project_name + '.cspy.bat'
        logging.debug("Flashing IAR project: %s" % path)

        args = [path, join('.', proj_dic['build_dir'], 'Exe', project_name + '.out')]

        try:
            ret_code = None
            ret_code = subprocess.call(args)
        except:
            logging.error("Error whilst calling: %s. Please check IARBUILD path in the user_settings.py file." % path)
        else:
            # cspy returns 0 for success, 1 for error
            if ret_code == 0:
                logging.info("Flashing completed.")
            else:
                logging.info("Flashing failed.")

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

from .tool import Tool, Exporter

# This serves as a new guide for upcoming wiki
# steps how to create a new tool
# 1. create a class and inherit frmo Tool and Exporter (at least export should be implemented)
# 2. implement ctor, get_toolnames and get_toolchain, export_project(), def export_workspace(self): methods
# and get_generated_project_files()
# 3. create generated project dictionary (what files will progen generate)
# 4. 

class VisualStudio(Tool, Exporter):

    def __init__(self, workspace, env_settings):
        self.definitions = 0
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['visual_studio']

    @staticmethod
    def get_toolchain():
        return None


class VisualStudioMakefileGCCARM()

   generated_project = {
        'path': '',
        'files': {
            'vcxproj.filters': '',
            'vcxproj': '',
            'vcxproj.user'
            'makefile': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.definitions = 0
        self.exporter = MakefileGccArm(workspace, env_settings)
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['visual_studio']

    @staticmethod
    def get_toolchain():
        return MakefileGccArm.get_toolchain()

    def export_project(self):

    def export_workspace(self):
        logging.debug("Not supported currently")

    def get_generated_project_files(self):
        pass

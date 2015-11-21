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

import logging
import copy
import os

from .tool import Tool, Exporter
from .gccarm import MakefileGccArm

# This serves as a new guide for upcoming wiki
# steps how to create a new tool
# 1. create a class and inherit frmo Tool and Exporter (at least export should be implemented)
# 2. implement ctor, get_toolnames and get_toolchain, export_project(), def export_workspace(self): methods
# and get_generated_project_files()
# 3. create generated project dictionary (what files will progen generate)
# 4. To test the basic methods, like export or progen list tools, add this class to tools_supported
# use logging.debug to print that exporting is happening and other info if you need to

# Not certain if the first step should not be to create templates. Generate a valid project for a tool,
# create a new project there, make it compile for simple hello world and possibly to debug (verifies that
# everything is correctly set up). Once we have a simple project, we can inspect the syntax . Where are files stored,
# include paths, macros, target if any, and other variables. look at project.ProjectTemplate() class which
# defines data needed for progen.
# The fastest way is to copy the manually generated project, and replace data with jinja2 syntax. To fill in
# all data we need (sources, includes, etc). Rename the files to tools_name.extensions.tmpl. They will be used 
# as templates.
# We can later switch to full parsing the file and generate it on the fly, but this often is more time consuming to learn
# how the tool is structured. Thus lets keep it simple for new tool, use jinja2 

class VisualStudio(Tool, Exporter):

    generated_project = {
        'path': '',
        'files': {
            'vcxproj.filters': '',
            'vcxproj': '',
            'vcxproj.user': '',
        }
    }

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


class VisualStudioMakeGCCARM(VisualStudio):

    generated_project = {
        'path': '',
        'files': {
            'vcxproj.filters': '',
            'vcxproj': '',
            'vcxproj.user': '',
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
        output = copy.deepcopy(self.generated_project)
        data_for_make = self.workspace.copy()

        self.exporter.process_data_for_makefile(data_for_make)
        output['path'], output['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', data_for_make, 'Makefile', data_for_make['output_dir']['path'])

        expanded_dic = self.workspace.copy()

        # data for .vcxproj
        expanded_dic['vcxproj'] = {}
        expanded_dic['vcxproj']['build_command'] = 'make all'
        expanded_dic['vcxproj']['rebuild_command'] = 'make clean &amp;&amp; make all'
        expanded_dic['vcxproj']['clean_command'] = 'make clean &amp;&amp; make all'
        expanded_dic['vcxproj']['executable_path'] = ''

        # data for debugger for pyOCD
        expanded_dic['vcxproj_user'] = {}
        expanded_dic['vcxproj_user']['gdb_address'] = 'localhost:3333'
        expanded_dic['vcxproj_user']['debugger_executable'] = 'arm-none-eabi-gdb'
        expanded_dic['vcxproj_user']['local_executable'] = os.path.join(expanded_dic['build_dir'], expanded_dic['name']) + '.elf'

        # Project files
        project_path, output['files']['vcxproj.filters'] = self.gen_file_jinja(
            'visual_studio.vcxproj.filters.tmpl', expanded_dic, '%s.vcxproj.filters' % expanded_dic['name'], data_for_make['output_dir']['path'])
        project_path, output['files']['vcxproj'] = self.gen_file_jinja(
            'visual_studio.vcxproj.tmpl', expanded_dic, '%s.vcxproj' % expanded_dic['name'], data_for_make['output_dir']['path'])
        project_path, output['files']['vcxproj.user'] = self.gen_file_jinja(
            'visual_studio.vcxproj.user.tmpl', expanded_dic, '%s.vcxproj.user' % expanded_dic['name'], data_for_make['output_dir']['path'])

        return output

    def export_workspace(self):
        logging.debug("Not supported currently")

    def get_generated_project_files(self):
        pass

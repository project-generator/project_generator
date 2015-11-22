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
import uuid
import xmltodict
from collections import OrderedDict

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

    linux_nmake_xaml = OrderedDict([(u'Rule', OrderedDict([(u'@Name', u'ConfigurationNMake'), (u'@DisplayName', u'NMake'), (u'@PageTemplate', u'generic'), (u'@Description', u'NMake'), (u'@SwitchPrefix', u'/'), (u'@Order', u'100'), (u'@xmlns', u'http://schemas.microsoft.com/build/2009/properties'), (u'Rule.Categories', OrderedDict([(u'Category', [OrderedDict([(u'@Name', u'General'), (u'@DisplayName', u'General'), (u'@Description', u'General')]), OrderedDict([(u'@Name', u'IntelliSense'), (u'@DisplayName', u'IntelliSense'), (u'@Description', u'IntelliSense')])])])), (u'Rule.DataSource', OrderedDict([(u'DataSource', OrderedDict([(u'@Persistence', u'ProjectFile')]))])), (u'StringProperty', [OrderedDict([(u'@Name', u'NMakeBuildCommandLine'), (u'@DisplayName', u'Build Command Line'), (u'@Description', u"Specifies the command line to run for the 'Build' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.BuildCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeReBuildCommandLine'), (u'@DisplayName', u'Rebuild All Command Line'), (u'@Description', u"Specifies the command line to run for the 'Rebuild All' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.ReBuildCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeCleanCommandLine'), (u'@DisplayName', u'Clean Command Line'), (u'@Description', u"Specifies the command line to run for the 'Clean' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.CleanCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeOutput'), (u'@DisplayName', u'Output'), (u'@Description', u'Specifies the output file to generate.'), (u'@Category', u'General'), (u'@IncludeInCommandLine', u'false'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.Output')]), OrderedDict([(u'@Name', u'AdditionalOptions'), (u'@DisplayName', u'Additional Options'), (u'@Category', u'IntelliSense'), (u'@Description', u'Specifies additional compiler switches to be used by Intellisense when parsing C++ files')])]), (u'StringListProperty', [OrderedDict([(u'@Name', u'NMakePreprocessorDefinitions'), (u'@DisplayName', u'Preprocessor Definitions'), (u'@Category', u'IntelliSense'), (u'@Switch', u'D'), (u'@Description', u'Specifies the preprocessor defines used by the source files.'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.PreprocessorDefinitions')]), OrderedDict([(u'@Name', u'NMakeIncludeSearchPath'), (u'@DisplayName', u'Include Search Path'), (u'@Category', u'IntelliSense'), (u'@Switch', u'I'), (u'@Description', u'Specifies the include search path for resolving included files.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.IncludeSearchPath')]), OrderedDict([(u'@Name', u'NMakeForcedIncludes'), (u'@DisplayName', u'Forced Includes'), (u'@Category', u'IntelliSense'), (u'@Switch', u'FI'), (u'@Description', u'Specifies the files that are forced included.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.ForcedIncludes')]), OrderedDict([(u'@Name', u'NMakeAssemblySearchPath'), (u'@DisplayName', u'Assembly Search Path'), (u'@Category', u'IntelliSense'), (u'@Switch', u'AI'), (u'@Description', u'Specifies the assembly search path for resolving used .NET assemblies.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.AssemblySearchPath')]), OrderedDict([(u'@Name', u'AdditionalSOSearchPaths'), (u'@DisplayName', u'Additional Symbol Search Paths'), (u'@Category', u'IntelliSense'), (u'@Description', u'Locations to identify '), (u'@F1Keyword', u'VC.Project.VCNMakeTool.AdditionalSOSearchPaths')])])]))])

    linux_debugger_xaml = OrderedDict([(u'Rule', OrderedDict([(u'@Name', u'LocalDebugger'), (u'@DisplayName', u'Local GDB'), (u'@PageTemplate', u'debugger'), (u'@Order', u'200'), (u'@Description', u'Debugger options'), (u'@xmlns:sys', u'clr-namespace:System;assembly=mscorlib'), (u'@xmlns:x', u'http://schemas.microsoft.com/winfx/2006/xaml'), (u'@xmlns', u'http://schemas.microsoft.com/build/2009/properties'), (u'Rule.DataSource', OrderedDict([(u'DataSource', OrderedDict([(u'@Persistence', u'UserFile')]))])), (u'Rule.Categories', OrderedDict([(u'Category', OrderedDict([(u'@Name', u'StartOptions'), (u'@DisplayName', u'Start Options'), (u'@Description', u'Start Options')]))])), (u'StringProperty', [OrderedDict([(u'@Name', u'LocalWorkingDirectory'), (u'@DisplayName', u'Local Working Directory'), (u'@Description', u'Local root location where executable runs'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', [OrderedDict([(u'@EditorType', u'DefaultStringPropertyEditor'), (u'@DisplayName', u'<Edit...>')]), OrderedDict([(u'@EditorType', u'DefaultFolderPropertyEditor'), (u'@DisplayName', u'<Browse...>')])])]))]), OrderedDict([(u'@Name', u'LocalExecutable'), (u'@DisplayName', u'Local Executable'), (u'@Description', u'Name of the local executable program'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')]), OrderedDict([(u'@Name', u'LocalExecutableArguments'), (u'@DisplayName', u'Local Executable Arguments'), (u'@Description', u'Optional, arguments to pass to the local executable'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')]), OrderedDict([(u'@Name', u'LocalDebuggerExecutable'), (u'@DisplayName', u'Local Debugger Executable'), (u'@Description', u'Full path to local gdb/lldb executable'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', [OrderedDict([(u'@EditorType', u'DefaultStringPropertyEditor'), (u'@DisplayName', u'<Edit...>')]), OrderedDict([(u'@EditorType', u'DefaultFilePropertyEditor'), (u'@DisplayName', u'<Browse...>')])])]))]), OrderedDict([(u'@Name', u'LocalDebuggerServerAddress'), (u'@DisplayName', u'Local Debugger Server Address'), (u'@Description', u'Optional, local debugger server address if needed'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')])])]))])

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
        return ['visual_studio'] + MakefileGccArm.get_toolnames()

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
        expanded_dic['vcxproj']['uuid'] = str(uuid.uuid5(uuid.NAMESPACE_URL, expanded_dic['name'])).upper()

        # data for debugger for pyOCD
        expanded_dic['vcxproj_user'] = {}
        expanded_dic['vcxproj_user']['gdb_address'] = 'localhost:3333'
        expanded_dic['vcxproj_user']['debugger_executable'] = 'arm-none-eabi-gdb'
        expanded_dic['vcxproj_user']['local_executable'] = os.path.join(expanded_dic['build_dir'], expanded_dic['name'])
        expanded_dic['vcxproj_user']['working_dir'] = os.path.join(os.getcwd(), data_for_make['output_dir']['path'])

        # Project files
        project_path, output['files']['vcxproj.filters'] = self.gen_file_jinja(
            'visual_studio.vcxproj.filters.tmpl', expanded_dic, '%s.vcxproj.filters' % expanded_dic['name'], data_for_make['output_dir']['path'])
        project_path, output['files']['vcxproj'] = self.gen_file_jinja(
            'visual_studio.vcxproj.tmpl', expanded_dic, '%s.vcxproj' % expanded_dic['name'], data_for_make['output_dir']['path'])
        project_path, output['files']['vcxproj.user'] = self.gen_file_jinja(
            'visual_studio.vcxproj.user.tmpl', expanded_dic, '%s.vcxproj.user' % expanded_dic['name'], data_for_make['output_dir']['path'])

        # NMake and debugger assets
        self.gen_file_raw(xmltodict.unparse(self.linux_nmake_xaml, pretty=True), 'linux_nmake.xaml', data_for_make['output_dir']['path'])
        self.gen_file_raw(xmltodict.unparse(self.linux_debugger_xaml, pretty=True), 'LocalDebugger.xaml', data_for_make['output_dir']['path'])

        return output

    def export_workspace(self):
        logging.debug("Not supported currently")

    def get_generated_project_files(self):
        pass

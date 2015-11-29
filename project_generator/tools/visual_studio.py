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
from ..util import SOURCE_KEYS

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

# once jinja2 template is working, we can switch to python and provide a template in python
# for instance using xmltodict for xml tools project
#>> import xmltodict                                                               
#>> print xmltodict.parse(file('lpc1768_blinky.vcxproj.user'))                     
# store the output and create a dict vcxproj.user , where we can injcet progen data

# This file contains 2 classes, VisualStudio gdb project and VisualStudio with gdb project configured for arm gcc
# I recommend doing minimal project when parsing to python. For instance, we just need one source file, one macro , one header file, or
# any other data for progen. To get the syntax, where to inject those data and the syntax. Then we can just loop to get data injected.

class VisualStudioGDB(Tool, Exporter):

    # Asset - linux_nmake.xaml
    linux_nmake_xaml = OrderedDict([(u'Rule', OrderedDict([(u'@Name', u'ConfigurationNMake'), (u'@DisplayName', u'NMake'), (u'@PageTemplate', u'generic'), (u'@Description', u'NMake'), (u'@SwitchPrefix', u'/'), (u'@Order', u'100'), (u'@xmlns', u'http://schemas.microsoft.com/build/2009/properties'), (u'Rule.Categories', OrderedDict([(u'Category', [OrderedDict([(u'@Name', u'General'), (u'@DisplayName', u'General'), (u'@Description', u'General')]), OrderedDict([(u'@Name', u'IntelliSense'), (u'@DisplayName', u'IntelliSense'), (u'@Description', u'IntelliSense')])])])), (u'Rule.DataSource', OrderedDict([(u'DataSource', OrderedDict([(u'@Persistence', u'ProjectFile')]))])), (u'StringProperty', [OrderedDict([(u'@Name', u'NMakeBuildCommandLine'), (u'@DisplayName', u'Build Command Line'), (u'@Description', u"Specifies the command line to run for the 'Build' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.BuildCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeReBuildCommandLine'), (u'@DisplayName', u'Rebuild All Command Line'), (u'@Description', u"Specifies the command line to run for the 'Rebuild All' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.ReBuildCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeCleanCommandLine'), (u'@DisplayName', u'Clean Command Line'), (u'@Description', u"Specifies the command line to run for the 'Clean' command."), (u'@IncludeInCommandLine', u'false'), (u'@Category', u'General'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.CleanCommandLine'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', OrderedDict([(u'@EditorType', u'DefaultCommandPropertyEditor'), (u'@DisplayName', u'<Edit...>')]))]))]), OrderedDict([(u'@Name', u'NMakeOutput'), (u'@DisplayName', u'Output'), (u'@Description', u'Specifies the output file to generate.'), (u'@Category', u'General'), (u'@IncludeInCommandLine', u'false'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.Output')]), OrderedDict([(u'@Name', u'AdditionalOptions'), (u'@DisplayName', u'Additional Options'), (u'@Category', u'IntelliSense'), (u'@Description', u'Specifies additional compiler switches to be used by Intellisense when parsing C++ files')])]), (u'StringListProperty', [OrderedDict([(u'@Name', u'NMakePreprocessorDefinitions'), (u'@DisplayName', u'Preprocessor Definitions'), (u'@Category', u'IntelliSense'), (u'@Switch', u'D'), (u'@Description', u'Specifies the preprocessor defines used by the source files.'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.PreprocessorDefinitions')]), OrderedDict([(u'@Name', u'NMakeIncludeSearchPath'), (u'@DisplayName', u'Include Search Path'), (u'@Category', u'IntelliSense'), (u'@Switch', u'I'), (u'@Description', u'Specifies the include search path for resolving included files.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.IncludeSearchPath')]), OrderedDict([(u'@Name', u'NMakeForcedIncludes'), (u'@DisplayName', u'Forced Includes'), (u'@Category', u'IntelliSense'), (u'@Switch', u'FI'), (u'@Description', u'Specifies the files that are forced included.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.ForcedIncludes')]), OrderedDict([(u'@Name', u'NMakeAssemblySearchPath'), (u'@DisplayName', u'Assembly Search Path'), (u'@Category', u'IntelliSense'), (u'@Switch', u'AI'), (u'@Description', u'Specifies the assembly search path for resolving used .NET assemblies.'), (u'@Subtype', u'folder'), (u'@F1Keyword', u'VC.Project.VCNMakeTool.AssemblySearchPath')]), OrderedDict([(u'@Name', u'AdditionalSOSearchPaths'), (u'@DisplayName', u'Additional Symbol Search Paths'), (u'@Category', u'IntelliSense'), (u'@Description', u'Locations to identify '), (u'@F1Keyword', u'VC.Project.VCNMakeTool.AdditionalSOSearchPaths')])])]))])

    # Asset LocalDebugger.xaml
    linux_debugger_xaml = OrderedDict([(u'Rule', OrderedDict([(u'@Name', u'LocalDebugger'), (u'@DisplayName', u'Local GDB'), (u'@PageTemplate', u'debugger'), (u'@Order', u'200'), (u'@Description', u'Debugger options'), (u'@xmlns:sys', u'clr-namespace:System;assembly=mscorlib'), (u'@xmlns:x', u'http://schemas.microsoft.com/winfx/2006/xaml'), (u'@xmlns', u'http://schemas.microsoft.com/build/2009/properties'), (u'Rule.DataSource', OrderedDict([(u'DataSource', OrderedDict([(u'@Persistence', u'UserFile')]))])), (u'Rule.Categories', OrderedDict([(u'Category', OrderedDict([(u'@Name', u'StartOptions'), (u'@DisplayName', u'Start Options'), (u'@Description', u'Start Options')]))])), (u'StringProperty', [OrderedDict([(u'@Name', u'LocalWorkingDirectory'), (u'@DisplayName', u'Local Working Directory'), (u'@Description', u'Local root location where executable runs'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', [OrderedDict([(u'@EditorType', u'DefaultStringPropertyEditor'), (u'@DisplayName', u'<Edit...>')]), OrderedDict([(u'@EditorType', u'DefaultFolderPropertyEditor'), (u'@DisplayName', u'<Browse...>')])])]))]), OrderedDict([(u'@Name', u'LocalExecutable'), (u'@DisplayName', u'Local Executable'), (u'@Description', u'Name of the local executable program'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')]), OrderedDict([(u'@Name', u'LocalExecutableArguments'), (u'@DisplayName', u'Local Executable Arguments'), (u'@Description', u'Optional, arguments to pass to the local executable'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')]), OrderedDict([(u'@Name', u'LocalDebuggerExecutable'), (u'@DisplayName', u'Local Debugger Executable'), (u'@Description', u'Full path to local gdb/lldb executable'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath'), (u'StringProperty.ValueEditors', OrderedDict([(u'ValueEditor', [OrderedDict([(u'@EditorType', u'DefaultStringPropertyEditor'), (u'@DisplayName', u'<Edit...>')]), OrderedDict([(u'@EditorType', u'DefaultFilePropertyEditor'), (u'@DisplayName', u'<Browse...>')])])]))]), OrderedDict([(u'@Name', u'LocalDebuggerServerAddress'), (u'@DisplayName', u'Local Debugger Server Address'), (u'@Description', u'Optional, local debugger server address if needed'), (u'@F1Keyword', u'VC.Project.LinuxDebugger.PackagePath')])])]))])

    # .vcxproj.user file template
    vcxproj_user_tmpl = OrderedDict([(u'Project', OrderedDict([(u'@ToolsVersion', u'14.0'), (u'@xmlns', u'http://schemas.microsoft.com/developer/msbuild/2003'), (u'PropertyGroup', OrderedDict([(u'@Condition', u"'$(Configuration)|$(Platform)'=='Debug|ARM'"), (u'LocalExecutable', u'$(WorkingDir)build\\lpc1768_blinky'), (u'LocalDebuggerServerAddress', u'localhost:3333'), (u'DebuggerFlavor', u'LocalDebugger'), (u'LocalWorkingDirectory', u'C:\\Code\\git_repo\\github\\project_generator_mbed_examples\\projects\\visual_studio_make_gcc_arm_mbed-lpc1768\\lpc1768_blinky'), (u'LocalDebuggerExecutable', u'arm-none-eabi-gdb')]))]))])

    # .vcxproj.filters file template
    vcxproj_filters_tmpl = OrderedDict([(u'Project', OrderedDict([(u'@ToolsVersion', u'4.0'), (u'@xmlns', u'http://schemas.microsoft.com/developer/msbuild/2003'), (u'ItemGroup', [OrderedDict([(u'Filter', [OrderedDict([(u'@Include', u'Source Files'), (u'UniqueIdentifier', u'{08a26e93-524c-4982-a01c-c8d4f223d6be}'), (u'Extensions', u'cpp;c;cc;cxx;asm;s')]), OrderedDict([(u'@Include', u'Header Files'), (u'UniqueIdentifier', u'{35c51339-ba9d-43c8-bd71-5f3199e89878}'), (u'Extensions', u'h;hh;hpp;hxx;hm;inl;inc')])])]), OrderedDict([(u'ClCompile', OrderedDict([(u'@Include', u''), (u'Filter', u'Source Files')]))]), OrderedDict([(u'ClInclude', OrderedDict([(u'@Include', u''), (u'Filter', u'Include Files')]))])])]))])
    # vcxproj_filters_tmpl = OrderedDict([(u'http://schemas.microsoft.com/developer/msbuild/2003:Project', OrderedDict([(u'@ToolsVersion', u'4.0'), (u'http://schemas.microsoft.com/developer/msbuild/2003:ItemGroup', [OrderedDict([(u'http://schemas.microsoft.com/developer/msbuild/2003:ClCompile', [OrderedDict([(u'@Include', u'..\\..\\..\\mbed\\libraries\\mbed\\targets\\hal\\TARGET_NXP\\TARGET_LPC176X\\analogin_api.c'), (u'http://schemas.microsoft.com/developer/msbuild/2003:Filter', u'Sources')]), OrderedDict([(u'@Include', u'..\\..\\..\\mbed\\libraries\\mbed\\targets\\hal\\TARGET_NXP\\TARGET_LPC176X\\analogout_api.c'), (u'http://schemas.microsoft.com/developer/msbuild/2003:Filter', u'Sources')])])]), OrderedDict([(u'http://schemas.microsoft.com/developer/msbuild/2003:ClInclude', OrderedDict([(u'@Include', u'..\\..\\..\\mbed\\libraries\\mbed\\targets\\cmsis\\core_ca9.h')]))]), OrderedDict([(u'http://schemas.microsoft.com/developer/msbuild/2003:None', OrderedDict([(u'@Include', u'Makefile')]))]), OrderedDict([(u'http://schemas.microsoft.com/developer/msbuild/2003:Filter', OrderedDict([(u'@Include', u'Sources'), (u'http://schemas.microsoft.com/developer/msbuild/2003:UniqueIdentifier', u'{76f35112-2644-4e2a-8007-2fbb45a4edca}')]))])])]))])

    generated_project = {
        'path': '',
        'files': {
            'vcxproj.filters': '',
            'vcxproj': '',
            'vcxproj.user': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['visual_studio']

    @staticmethod
    def get_toolchain():
        return None

    def _set_vcxproj(self, name='', execut='', build='', rebuild='', clean=''):
        proj_dic = {}
        proj_dic['build_command'] = build
        proj_dic['rebuild_command'] = rebuild
        proj_dic['clean_command'] = clean
        proj_dic['executable_path'] = execut
        proj_dic['uuid'] = str(uuid.uuid5(uuid.NAMESPACE_URL, name)).upper()
        return proj_dic

    def _set_vcxproj_user(self, gdb_add, debbuger_exec, local_executable, working_dir):
        vcxproj_user = copy.deepcopy(self.vcxproj_user_tmpl)
        vcxproj_user['Project']['PropertyGroup']['LocalDebuggerServerAddress'] = gdb_add
        vcxproj_user['Project']['PropertyGroup']['arm-none-eabi-gdb'] = 'arm-none-eabi-gdb'
        vcxproj_user['Project']['PropertyGroup']['LocalExecutable'] = local_executable
        vcxproj_user['Project']['PropertyGroup']['LocalWorkingDirectory'] = working_dir
        return vcxproj_user

    def _generate_vcxproj_files(self, proj_dict, name, rel_path, vcxproj_user_dic):
        output = copy.deepcopy(self.generated_project)
        project_path, output['files']['vcxproj.filters'] = self.gen_file_jinja(
            'visual_studio.vcxproj.filters.tmpl', proj_dict, '%s.vcxproj.filters' % name, rel_path)
        project_path, output['files']['vcxproj'] = self.gen_file_jinja(
            'visual_studio.vcxproj.tmpl', proj_dict, '%s.vcxproj' % name, rel_path)
        project_path, output['files']['vcxproj.user'] = self.gen_file_raw(
            xmltodict.unparse(vcxproj_user_dic, pretty=True), '%s.vcxproj.user' % name, rel_path)
        return project_path, output

    def _set_groups(self, proj_dic):
        # each group needs to have own filter with UUID
        proj_dic['source_groups'] = {}
        proj_dic['include_groups'] = {}
        for key in SOURCE_KEYS:
            for group_name, files in proj_dic[key].items():
                proj_dic['source_groups'][group_name] = str(uuid.uuid5(uuid.NAMESPACE_URL, group_name)).upper()
        for k,v in proj_dic['include_files'].items():
            proj_dic['include_groups'][k] = str(uuid.uuid5(uuid.NAMESPACE_URL, k)).upper()

    def export_project(self):
        output = copy.deepcopy(self.generated_project)
        expanded_dic = self.workspace.copy()

        # data for .vcxproj
        expanded_dic['vcxproj'] = {}
        expanded_dic['vcxproj'] = self._set_vcxproj(expanded_dic['name'])

        # data for debugger for pyOCD
        expanded_dic['vcxproj_user'] = {}
        # TODO: localhost and gdb should be misc for VS ! Add misc options
        vcxproj_user_dic = self._set_vcxproj_user('localhost:3333', 'arm-none-eabi-gdb',
            os.path.join(expanded_dic['build_dir'], expanded_dic['name']), os.path.join(os.getcwd(), expanded_dic['output_dir']['path']))

        self._set_groups(expanded_dic)

        # Project files
        project_path, output = self._generate_vcxproj_files(expanded_dic, 
            expanded_dic['name'], expanded_dic['output_dir']['path'], vcxproj_user_dic)

        # NMake and debugger assets
        # TODO: not sure about base class having NMake and debugger. We might want to disable that by default?
        self.gen_file_raw(xmltodict.unparse(self.linux_nmake_xaml, pretty=True), 'linux_nmake.xaml', expanded_dic['output_dir']['path'])
        self.gen_file_raw(xmltodict.unparse(self.linux_debugger_xaml, pretty=True), 'LocalDebugger.xaml', expanded_dic['output_dir']['path'])

        return output

    def export_workspace(self):
        logging.debug("Not supported currently")

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['vcxproj.filters'],
            self.workspace['files']['vcxproj'], self.workspace['files']['vcxproj.user']]}

class VisualStudioMakeGCCARM(VisualStudioGDB):

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
        super(VisualStudioMakeGCCARM, self).__init__(workspace, env_settings)
        self.exporter = MakefileGccArm(workspace, env_settings)

    @staticmethod
    def get_toolnames():
        return VisualStudioGDB.get_toolnames() + MakefileGccArm.get_toolnames()

    @staticmethod
    def get_toolchain():
        return MakefileGccArm.get_toolchain()

    def export_project(self):
        output = copy.deepcopy(self.generated_project)
        data_for_make = self.workspace.copy()

        self.exporter.process_data_for_makefile(data_for_make)
        output['path'], output['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', data_for_make, 'Makefile', data_for_make['output_dir']['path'])

        expanded_dic = self.workspace.copy()

        expanded_dic['makefile'] = True

        # data for .vcxproj
        expanded_dic['vcxproj'] = {}
        expanded_dic['vcxproj'] = self._set_vcxproj(expanded_dic['name'],'make all', 'make clean &amp;&amp; make all',
            'make clean &amp;&amp; make all', '')

        # data for debugger for pyOCD
        expanded_dic['vcxproj_user'] = {}
        # TODO: localhost and gdb should be misc for VS ! Add misc options
        vcxproj_user_dic = self._set_vcxproj_user('localhost:3333', 'arm-none-eabi-gdb',
            os.path.join(expanded_dic['build_dir'], expanded_dic['name']), os.path.join(os.getcwd(), data_for_make['output_dir']['path']))

        self._set_groups(expanded_dic)

        # Project files
        project_path, vcx_files = self._generate_vcxproj_files(expanded_dic, expanded_dic['name'], 
            data_for_make['output_dir']['path'], vcxproj_user_dic)
        output['files']['vcxproj.filters'] = vcx_files['files']['vcxproj.filters']
        output['files']['vcxproj'] = vcx_files['files']['vcxproj']
        output['files']['vcxproj.user'] = vcx_files['files']['vcxproj.user']

        # NMake and debugger assets
        self.gen_file_raw(xmltodict.unparse(self.linux_nmake_xaml, pretty=True), 'linux_nmake.xaml', data_for_make['output_dir']['path'])
        self.gen_file_raw(xmltodict.unparse(self.linux_debugger_xaml, pretty=True), 'LocalDebugger.xaml', data_for_make['output_dir']['path'])

        return output

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['vcxproj.filters'],
            self.workspace['files']['vcxproj'], self.workspace['files']['vcxproj.user'],
            self.workspace['files']['Makefile']]}

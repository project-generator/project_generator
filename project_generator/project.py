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
import yaml
import shutil
import logging
import operator

from collections import defaultdict
from .tool import build, export, flash, fixup_executable, ToolsSupported
from .util import merge_recursive, flatten
from string import Template

try:
    input = raw_input
except:
    pass

FILES_EXTENSIONS = {
    'includes': ['h', 'hpp', 'inc'],
    'source_files_s': ['s'],
    'source_files_c': ['c'],
    'source_files_cpp': ['cpp', 'cc'],
    'source_files_lib': ['lib', 'ar', 'a'],
    'source_files_obj': ['o', 'obj'],
    'linker_file': ['sct', 'ld', 'lin', 'icf'],
}


class ToolSpecificSettings:

    """represents the settings that are specific to targets"""

    def __init__(self):
        self.includes = []
        self.include_files = []
        self.source_paths = []
        self.source_groups = {}
        self.macros = []
        self.misc = {}

        self.linker_file = None
        self.template = None

    def add_settings(self, data_dictionary, group_name):
        if 'sources' in data_dictionary:
            self._process_source_files(
                data_dictionary['sources'], group_name)

        if 'includes' in data_dictionary:
            self._process_include_files(data_dictionary['includes'])

        if 'macros' in data_dictionary:
            self.macros.extend([x for x in data_dictionary['macros'] if x is not None])

        if 'project_dir' in data_dictionary:
            self.project_dir.update(data_dictionary['project_dir'])

        if 'linker_file' in data_dictionary:
            self.linker_file = data_dictionary['linker_file'][0]

        if 'misc' in data_dictionary:
            self.misc.update(data_dictionary['misc'])

        if 'template' in data_dictionary:
            self.template = data_dictionary['template']

    def source_of_type(self, filetype):
        """return a dictionary of groups and the sources of a specified type within them"""
        files = {}
        for group, group_contents in self.source_groups.items():
            files[group] = []
            if filetype in group_contents:
                files[group].extend(group_contents[filetype])

        return files

    def all_sources_of_type(self, filetype):
        """return a list of the sources of a specified type"""
        files = []

        for group, group_contents in self.source_groups.items():
            if filetype in group_contents:
                files.extend(group_contents[filetype])

        return files

    def _process_source_files(self, files, group_name):
        extensions = ['cpp', 'c', 's', 'obj', 'lib']
        mappings = defaultdict(lambda: None)

        mappings['o'] = 'obj'

        mappings['a'] = 'lib'
        mappings['ar'] = 'lib'
        mappings['cc'] = 'cpp'

        if group_name not in self.source_groups:
            self.source_groups[group_name] = {}

        for source_file in files:
            extension = source_file.split('.')[-1]
            extension = mappings[extension] or extension

            if extension not in extensions:
                continue

            if extension not in self.source_groups[group_name]:
                self.source_groups[group_name][extension] = []

            self.source_groups[group_name][extension].append(source_file)

            if os.path.dirname(source_file) not in self.source_paths:
                self.source_paths.append(os.path.dirname(source_file))

    # TODO 0xc0170: remove this and process source files - duplicate. Probably we should reconsider
    # this class
    def _process_include_files(self, files):
        # If it's dic add it , if file, add it to files
        for include_file in files:
            if os.path.isfile(include_file):
                if not include_file in self.include_files:
                    self.include_files.append(os.path.normpath(include_file))
            if not os.path.dirname(include_file) in self.includes:
                self.includes.append(os.path.normpath(include_file))

class ProjectWorkspace:
    """represents a workspace (multiple projects) """

    def __init__(self, proj_name, projects, workspace_settings, pgen_workspace, singular = False):
        self.name = proj_name
        self.projects = projects
        self.pgen_workspace = pgen_workspace # TODO: FIX me please
        self.generated_files = {}
        self.singular = singular

        # These are additional settings defined in yaml under workspace: {workspace_name: {settings: {}
        self.workspace_settings = workspace_settings

    def export(self, tool, copy):
        """ Exports workspace """

        # Update the project settings with settings specific to this workspace
        self.pgen_workspace.settings.update(self.workspace_settings)
        tools = []
        if not tool:
            tools = ToolsSupported()
        else:
            tools = [tool]

        for export_tool in tools:
            exporter = ToolsSupported().get_value(export_tool, 'exporter')
            workspace_dic = {
                'projects': [],
                'settings': {},
            }
            for project in self.projects:
                workspace_dic['projects'].append(project.generate_dic(export_tool, copy))
            #logging.debug("Project workspace dict: %s" % workspace_dic)
            generated_files = export(exporter, workspace_dic, export_tool, self.pgen_workspace.settings)

            self.generated_files[export_tool] = generated_files

class Project:

    """represents a project, which can be formed of many yaml files"""

    def __init__(self, name, project_files, pgen_workspace):
        """initialise a project with a yaml file"""
        self.workspace = pgen_workspace
        self.tool_specific = defaultdict(ToolSpecificSettings)
        self.name = name
        self.output_types = {
            'executable': 'exe',
            'exe': 'exe',
            'library': 'lib',
            'lib': 'lib',
        }
        self.tools = ToolsSupported()
        self.source_groups = {}

        self.project = {}
        self._fill_project_defaults()

        for project_file in project_files:
            try:
                f = open(project_file, 'rt')
                project_file_data = yaml.load(f)
                self._set_project_attributes(project_file_data)
            except IOError:
               raise IOError("The file %s referenced in main yaml doesn't exist."%project_file)

    def _fill_project_defaults(self):

        self.project = {
            'name': self.name,          # project name
            'core': '',                 # core
            'linker_file': None,        # linker command file
            'build_dir' : 'build',      # Build output path
            'debugger' : 'cmsis-dap',   # Debugger
            'includes': [],             # include paths
            'include_files': [],        # [internal] files to be included
            'source_paths': [],         # [internal] source paths
            'source_files_c': [],       # [internal] c source files
            'source_files_cpp': [],     # [internal] c++ source files
            'source_files_s': [],       # [internal] assembly source files
            'source_files_obj': [{}],   # [internal] object files
            'source_files_lib': [{}],   # [internal] libraries
            'macros': [],               # macros (defines)
            'misc': {},                 # misc tools settings, which are parsed by tool
            'project_dir': {            # Name and path for a project
                'name': '.' + os.path.sep,
                'path' : self.workspace.settings.generated_projects_dir_default
            },
            'output_dir': {         # The generated path dict
                'path': '',
                'rel_path': '',
                'rel_count': '',
            },
            'target': '',       # target
            'template' : '',    # tool template
            'output_type': self.output_types['executable'],           # output type, default - exe
            'tools_supported': [self.workspace.settings.DEFAULT_TOOL] # Tools which are supported

        }

    def _set_project_attributes(self,project_file_data):
        if 'common' in project_file_data:
                if 'output' in project_file_data['common']:
                    if project_file_data['common']['output'][0] not in self.output_types:
                        raise RuntimeError("Invalid Output Type.")

                    self.project['output_type'] = self.output_types[project_file_data['common']['output'][0]]

                if 'includes' in project_file_data['common']:
                    self._process_include_files(project_file_data['common']['includes'])
                    # self.project['includes'].extend(
                        # [os.path.normpath(x) for x in project_file_data['common']['includes'] if x is not None])

                if 'sources' in project_file_data['common']:
                    if type(project_file_data['common']['sources']) == type(dict()):
                        for group_name, sources in project_file_data['common']['sources'].items():
                            self._process_source_files(sources, group_name)
                    else:
                        self._process_source_files(project_file_data['common']['sources'], 'default')
                    for source_path in self.project['source_paths']:
                        if os.path.normpath(source_path) not in self.project['includes']:
                            self.project['includes'].extend([source_path])

                if 'macros' in project_file_data['common']:
                    self.project['macros'].extend(
                        [x for x in project_file_data['common']['macros'] if x is not None])

                if 'project_dir' in project_file_data['common']:
                    self.project['project_dir'].update(
                        project_file_data['common']['project_dir'])

                for key in ['debugger','build_dir','mcu','name','target','core', 'linker_file']:
                    if key in project_file_data['common']:
                        self.project[key] = project_file_data['common'][key][0]

                if 'tools_supported' in project_file_data['common']:
                    self.project['tools_supported'] = []
                    self.project['tools_supported'].extend(
                        [x for x in project_file_data['common']['tools_supported'] if x is not None])

        if 'tool_specific' in project_file_data:
            group_name = 'default'
            for tool_name, tool_settings in project_file_data['tool_specific'].items():
                self.tool_specific[tool_name].add_settings(tool_settings, group_name)

    def _process_include_files(self, files):
        # If it's dic add it , if file, add it to files
        for include_file in files:
            if os.path.isfile(include_file):
                # file, add it to the list (for copying or if tool requires it)
                if not include_file in self.project['include_files']:
                    self.project['include_files'].append(os.path.normpath(include_file))
                dir_path = os.path.dirname(include_file)
            else:
                # its a directory
                dir_path = include_file
            if not os.path.dirname(include_file) in self.project['includes']:
                self.project['includes'].append(os.path.normpath(dir_path))

    def _process_source_files(self, files, group_name):
        extensions = ['cpp', 'c', 's', 'obj', 'lib']
        mappings = defaultdict(lambda: None)
        mappings['o'] = 'obj'
        mappings['a'] = 'lib'
        mappings['ar'] = 'lib'
        mappings['cc'] = 'cpp'
        if group_name not in self.source_groups:
            self.source_groups[group_name] = {}

        for source_file in files:
            if os.path.isdir(source_file):
                self.project['source_paths'].append(os.path.normpath(source_file))
                self._process_source_files([os.path.join(os.path.normpath(source_file), f) for f in os.listdir(
                    source_file) if os.path.isfile(os.path.join(os.path.normpath(source_file), f))], group_name)

            extension = source_file.split('.')[-1]
            extension = mappings[extension] or extension

            if extension not in extensions:
                continue

            if extension not in self.source_groups[group_name]:
                self.source_groups[group_name][extension] = []

            self.source_groups[group_name][extension].append(os.path.normpath(source_file))

            if not os.path.dirname(source_file) in self.project['source_paths']:
                self.project['source_paths'].append(os.path.normpath(os.path.dirname(source_file)))

    def _get_workspace_name(self):
        workspaces = self.workspace.workspaces
        for workspace, proj_workspace in workspaces.items():
            for p in proj_workspace.projects:
                if self is p:
                    return workspace

    def clean(self, project_name, tool):
        if tool is None:
            tools = list(self.TOOLCHAINS)
        else:
            tools = [tool]

        for current_tool in tools:
            if self.workspace.settings.generated_projects_dir != self.workspace.settings.generated_projects_dir_default:
                # TODO: same as in exporters.py - create keyword parser
                path = Template(self.workspace.settings.generated_projects_dir)
                path = path.substitute(target=self.project['target'], workspace=self._get_workspace_name(),
                                        project_name=self.name, tool=tool)
            else:
                 path = os.path.join(self.project_dir['path'], "%s_%s" % (current_tool, self.name))
            if os.path.isdir(path):
                logging.info("Cleaning directory %s" % path)

                shutil.rmtree(path)

    def build(self, tool):
        """build the project"""
        tools = []
        if not tool:
            tools = self.project['tools_supported']
        else:
            tools = [tool]

        for build_tool in tools:
            builder = self.tools.get_value(build_tool, 'builder')
            build(builder, self.name, self._get_project_files(), build_tool, self.workspace.settings)

    def flash(self, tool):
        """flash the project"""
        # flashing via various tools does not make much usefulness?
        if not tool:
            tool = self.workspace.settings.DEFAULT_TOOL

        flasher = self.tools.get_value(tool, 'flasher')
        self.customize_project_for_tool(tool)
        flash(flasher, self.project, self.name, self._get_project_files(), tool, self.workspace.settings)

    def generate_dic(self, tool, copy):
        """export the project"""
        self.customize_project_for_tool(tool)
        self.project['copy_sources'] = False
        self.project['output_dir']['rel_path'] = ''

        if copy:
            self.copy_files()
            # TODO: fixme
            self.project['copy_sources'] = True
        else:
            # Get number of how far we are from root, to set paths in the project
            # correctly
            count = 1
            pdir = self.project['output_dir']['path']
            while os.path.split(pdir)[0]:
                pdir = os.path.split(pdir)[0]
                count += 1
            rel_path_output = ''

            self.project['output_dir']['rel_count'] = count
            while count:
                rel_path_output = os.path.join('..', rel_path_output)
                count -= 1
            self.project['output_dir']['rel_path'] = rel_path_output

        return self.project

    def _get_project_files(self):
        if self.project['project_dir']['name'] and self.project['project_dir']['path']:
            return [os.path.join(self.project['project_dir']['path'], self.project['project_dir']['name'])]
        else:
            return [os.path.join(self.project['output_dir']['path'], self.project['name'])]

    def source_of_type(self, filetype):
        """return a dictionary of groups and the sources of a specified type within them"""
        files = {}
        for group, group_contents in self.source_groups.items():
            files[group] = []
            if filetype in group_contents:
                files[group].extend(group_contents[filetype])
        return files

    def all_sources_of_type(self, filetype):
        """return a list of the sources of a specified type"""
        files = []
        for group, group_contents in self.source_groups.items():
            if filetype in group_contents:
                files.extend(group_contents[filetype])
        return files

    def format_source_files(self, ext, tool_specific_settings, toolchain_specific_settings):
        return [merge_recursive(self.source_of_type(ext), {k: v for settings in
                [settings.source_of_type(ext) for settings in tool_specific_settings] for
                k, v in settings.items()},toolchain_specific_settings.source_of_type(ext))]

    def customize_project_for_tool(self, tool):
        """for backwards compatibility"""
        toolchain_specific_settings =  self.tool_specific[self.tools.get_value(tool, 'toolchain')]
        tool_specific_settings = []
        toolnames = self.tools.get_value(tool, 'toolnames')
        for tool_spec in toolnames:
            if self.tools.get_value(tool, 'toolchain') != tool_spec:
                tool_specific_settings.append(self.tool_specific[tool_spec])

        self.project['includes'] =  self.project['includes'] + list(flatten([settings.includes for settings in tool_specific_settings]))
        self.project['include_files'] =  self.project['include_files'] + list(flatten([settings.include_files for settings in tool_specific_settings]))
        self.project['source_paths'] =  self.project['source_paths'] + list(flatten([settings.includes for settings in tool_specific_settings]))
        self.project['source_files'] = merge_recursive(self.source_groups,
                                {k: v for settings in tool_specific_settings for k, v in settings.source_groups.items()},
                                toolchain_specific_settings.source_groups)
        for ext in ["c","cpp","s","lib"]:
           key = "source_files_"+ext
           self.project[key] = self.format_source_files(ext, tool_specific_settings, toolchain_specific_settings)

        self.project['source_files_obj']= merge_recursive(self.format_source_files('obj',tool_specific_settings, toolchain_specific_settings),
            self.format_source_files('o',tool_specific_settings, toolchain_specific_settings))

        self.project['linker_file'] =  self.project['linker_file'] or toolchain_specific_settings.linker_file or [
            tool_settings.linker_file for tool_settings in tool_specific_settings if tool_settings.linker_file]

        self.project['macros'] = self.project['macros'] + list(flatten([settings.macros for settings in tool_specific_settings])) \
            + toolchain_specific_settings.macros

        self.project['misc'] =  [merge_recursive({k: v for settings in tool_specific_settings for k, v in settings.misc.items()},
            toolchain_specific_settings.misc)]

        self.project['template'] = toolchain_specific_settings.template or [
                tool_settings.template for tool_settings in tool_specific_settings if tool_settings.template]

        if len(self.project['linker_file']) == 0 and self.project['output_type'] == 'exe':
            raise RuntimeError("Executable - no linker command found.")

        if self.workspace.settings.generated_projects_dir != self.workspace.settings.generated_projects_dir_default:
            output_dir = Template(self.workspace.settings.generated_projects_dir)
            output_dir = output_dir.substitute(target=self.project['target'], workspace=self._get_workspace_name(),
                                               project_name=self.name, tool=tool)
        else:
            output_dir = os.path.join(self.project['project_dir']['path'], "%s_%s" % (tool, self.name))
        self.project['output_dir']['path'] = os.path.normpath(output_dir)

    @staticmethod
    def fixup_executable(executable_path, tool):
        exporter = ToolsSupported().get_value(tool, 'exporter')
        fixup_executable(exporter, executable_path, tool)

    def _copy_files(self, file, output_dir, valid_files_group):
        file = os.path.normpath(file)
        dest_dir = os.path.join(os.getcwd(), output_dir, os.path.dirname(file))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        if file.split('.')[-1] in valid_files_group:
            shutil.copy2(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), output_dir, file))

    def copy_files(self):
        """" Copies all project files to specified directory - generated dir"""
        for path in self.project['includes']:
            if os.path.isdir(path):
                # directory full of include files
                path = os.path.normpath(path)
                files = os.listdir(path)
            else:
                # includes is a file, make it valid
                files = [os.path.basename(path)]
                path = os.path.dirname(path)
            dest_dir = os.path.join(os.getcwd(), self.project['output_dir']['path'], path)
            if not os.path.exists(dest_dir) and len(files):
                os.makedirs(dest_dir)
            for filename in files:
                if filename.split('.')[-1] in FILES_EXTENSIONS['includes']:
                    shutil.copy2(os.path.join(os.getcwd(), path, filename),
                                 os.path.join(os.getcwd(), self.project['output_dir']['path'], path))

        # all sources are grouped, therefore treat them as dict
        for k, v in self.project['source_files_c'][0].items():
            for file in v:
                self._copy_files(file, self.project['output_dir']['path'], FILES_EXTENSIONS['source_files_c'])

        for k, v in self.project['source_files_cpp'][0].items():
            for file in v:
                self._copy_files(file, self.project['output_dir']['path'], FILES_EXTENSIONS['source_files_cpp'])

        for k, v in self.project['source_files_s'][0].items():
            for file in v:
                self._copy_files(file, self.project['output_dir']['path'], FILES_EXTENSIONS['source_files_s'])

        for k,v in self.project['source_files_obj'][0].items():
            for file in v:
                self._copy_files(file, self.project['output_dir']['path'], FILES_EXTENSIONS['source_files_obj'])

        for k,v in self.project['source_files_lib'][0].items():
            for file in v:
                self._copy_files(file, self.project['output_dir']['path'], FILES_EXTENSIONS['source_files_lib'])

        linker = os.path.normpath(self.project['linker_file'])
        dest_dir = os.path.join(os.getcwd(), self.project['output_dir']['path'], os.path.dirname(linker))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy2(os.path.join(os.getcwd(), linker),
                     os.path.join(os.getcwd(), self.project['output_dir']['path'], linker))

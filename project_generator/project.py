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
import copy

from collections import defaultdict
from .tools_supported import ToolsSupported
from .util import merge_recursive, flatten, PartialFormatter
from string import Template

FILES_EXTENSIONS = {
    'includes': ['h', 'hpp', 'inc'],
    'source_files_s': ['s'],
    'source_files_c': ['c'],
    'source_files_cpp': ['cpp', 'cc'],
    'source_files_lib': ['lib', 'ar', 'a'],
    'source_files_obj': ['o', 'obj'],
    'linker_file': ['sct', 'ld', 'lin', 'icf'],
}

class ProjectWorkspace:
    """represents a workspace (multiple projects) """

    def __init__(self, name, projects, pgen_workspace):
        self.name = name
        self.projects = projects
        self.pgen_workspace = pgen_workspace # TODO: FIX me please
        self.generated_files = {}

    def export(self, tool, copy):
        """ Exports workspace """

        tools = []
        if not tool:
            logging.info("Workspace supports one tool for all projects within.")
            return -1
        else:
            tools = [tool]

        result = 0
        for export_tool in tools:
            tool_export = ToolsSupported().get_tool(export_tool)
            if tool_export is None:
                result = -1
                continue

            # substitute all of the different dynamic values
            location = PartialFormatter().format(self.pgen_workspace.settings.export_location_format, **{
                'project_name': self.name,
                'tool': tool,
                'workspace': self.name
            })

            workspace_dic = {
                'projects': [],
                'settings': {
                    'name': self.name,
                    'path': location,
                },
            }


            for project in self.projects:
                generated_files = {
                    'projects' : [],
                    'workspaces': [],
                }

                # Merge all dics, copy sources if required, correct output dir. This happens here
                # because we need tool to set proper path (tool might be used as string template)
                project._fill_export_dict(export_tool)

                if copy:
                    project._copy_sources_to_generated_destination()
                project.project['singular'] = False
                files = tool_export(project.project['export'], self.pgen_workspace.settings).export_project()
                # we gather all generated files, needed for workspace files
                workspace_dic['projects'].append(files)
                generated_files['projects'].append(files)

            # all projects are genereated, now generate workspace files
            generated_files['workspaces'] = tool_export(workspace_dic, self.pgen_workspace.settings).export_workspace()

            self.generated_files[export_tool] = generated_files
            return result

    def build(self, tool):
        logging.info("Building a workspace is not currently supported")
        return -1

    def clean(self, tool):
        logging.info("Building a workspace is not currently supported")
        return -1

class Project:

    """represents a project, which can be formed of many yaml files"""

    # Common dictionary for project. Tools and commond data shared this structure
    COMMON_DICT = {
        'includes': [],      # include paths
        'macros': [],        # macros
        'linker_file': None, # linker script file
        'source_paths': [],  # [internal] source paths derived from sources
        'include_files': [], # [internal] include files - used in the copy function
        'source_groups': {}, # [internal] sources are here in groups (virtual folders)
    }

    def __init__(self, name, project_dicts, pgen_workspace):
        """initialise a project with a yaml file"""
        self.pgen_workspace = pgen_workspace
        self.name = name
        self.output_types = {
            'executable': 'exe',
            'exe': 'exe',
            'library': 'lib',
            'lib': 'lib',
        }

        # project dictionaries, set them to default values
        self.project = {}
        self.project['common'] = {}
        self.project['tool_specific'] = defaultdict(dict)
        self.project['export'] = defaultdict(dict) # merged common and tool

        self._fill_project_common_defaults()
        self._fill_project_tool_specific_defaults(project_dicts)

        # process all projects dictionaries
        for project in project_dicts:
            self._set_common_attributes(project)
            self._set_tool_attributes(project)
        self.generated_files = {}

    def _fill_project_common_defaults(self):

        # There are public variables which are available to set
        # Those tagged as [internal] are generated by pgen and used internally
        self.project['common'] = {
            'build_dir' : 'build',    # Build output path
            'core': '',               # core
            'debugger' : 'cmsis-dap', # Debugger
            'export_dir': '',         # Export directory path
            'name': self.name,        # project name
            'output_type': self.output_types['executable'], # output type, default - exe
            'output_dir': {           # [internal] The generated path dict
                'path': '',           # path with all name mangling we add to export_dir
                'rel_path': '',       # how far we are from root
                'rel_count': '',      # Contains count of how far we are from root, used for eclipse for example
            },
            'target': '',             # target
            'template' : '',          # tool template
            'tools_supported': [],    # Tools which are supported,
            'singular': True,         # [internal] singular project or part of a workspace
            'source_files_c': {},     # [internal] c source files
            'source_files_cpp': {},   # [internal] c++ source files
            'source_files_s': {},     # [internal] assembly source files
            'source_files_obj': {},   # [internal] object files
            'source_files_lib': {},   # [internal] libraries
        }
        self.project['common'].update(copy.deepcopy(self.COMMON_DICT))

    def _fill_project_tool_specific_defaults(self, project_dicts):
        # set default values for each tool this project supports
        for project in project_dicts:
            if 'tool_specific' in project:
                for tool_name, tool_settings in project['tool_specific'].items():
                    self.project['tool_specific'][tool_name].update(copy.deepcopy(self.COMMON_DICT))

    # Project data have the some keys the same, therefore we process them here
    # and their own keys, are processed in common/tool attributes
    def _set_project_attributes(self, project_dic, key_value , project_file_data):
        if key_value in project_file_data:
            if 'includes' in project_file_data[key_value]:
                self._process_include_files(project_dic, project_file_data[key_value]['includes'])

            if 'sources' in project_file_data[key_value]:
                if type(project_file_data[key_value]['sources']) == type(dict()):
                    for group_name, sources in project_file_data[key_value]['sources'].items():
                        self._process_source_files(project_dic, sources, group_name)
                else:
                    self._process_source_files(project_dic, project_file_data[key_value]['sources'], 'default')
                for source_path in project_dic['source_paths']:
                    if os.path.normpath(source_path) not in project_dic['includes']:
                        project_dic['includes'].extend([source_path])

            if 'macros' in project_file_data[key_value]:
                project_dic['macros'].extend(
                    [x for x in project_file_data[key_value]['macros'] if x is not None])

            if 'export_dir' in project_file_data[key_value]:
                project_dic['export_dir'] = os.path.normpath(project_file_data[key_value]['export_dir'][0])

            if 'linker_file' in project_file_data[key_value]:
                project_dic['linker_file'] = os.path.normpath(project_file_data[key_value]['linker_file'][0])

    def _set_common_attributes(self, project_file_data):
        if 'common' in project_file_data:
            if 'output' in project_file_data['common']:
                if project_file_data['common']['output'][0] not in self.output_types:
                    raise RuntimeError("Invalid Output Type.")

                self.project['common']['output_type'] = self.output_types[project_file_data['common']['output'][0]]

            self._set_project_attributes(self.project['common'], 'common', project_file_data)

            for key in ['debugger','build_dir','mcu','name','target','core']:
                if key in project_file_data['common']:
                    self.project['common'][key] = project_file_data['common'][key][0]

            if 'tools_supported' in project_file_data['common']:
                self.project['common']['tools_supported'] = []
                self.project['common']['tools_supported'].extend(
                    [x for x in project_file_data['common']['tools_supported'] if x is not None])

    def _set_tool_attributes(self, project_file_data):
        if 'tool_specific' in project_file_data:
            for tool_name, tool_settings in project_file_data['tool_specific'].items():
                self._set_project_attributes(self.project['tool_specific'][tool_name], tool_name, project_file_data['tool_specific'])
                if 'misc' in project_file_data['tool_specific'][tool_name]:
                    self.project['tool_specific'][tool_name]['misc'] = project_file_data['tool_specific'][tool_name]['misc']
    @staticmethod
    def _process_include_files(project_dic, files):
        # If it's dic add it , if file, add it to files
        for include_file in files:
            # include might be set to None - empty yaml list
            if include_file:
                if os.path.isfile(include_file):
                    # file, add it to the list (for copying or if tool requires it)
                    if not include_file in project_dic['include_files']:
                        project_dic['include_files'].append(os.path.normpath(include_file))
                    dir_path = os.path.dirname(include_file)
                else:
                    # its a directory
                    dir_path = include_file
                if not os.path.normpath(dir_path) in project_dic['includes']:
                    project_dic['includes'].append(os.path.normpath(dir_path))

    @staticmethod
    def _process_source_files(project_dic, files, group_name):
        extensions = ['cpp', 'c', 's', 'obj', 'lib']
        mappings = defaultdict(lambda: None)
        mappings['o'] = 'obj'
        mappings['a'] = 'lib'
        mappings['ar'] = 'lib'
        mappings['cc'] = 'cpp'
        if group_name not in project_dic['source_groups']:
            project_dic['source_groups'][group_name] = {}

        for source_file in files:
            if os.path.isdir(source_file):
                project_dic['source_paths'].append(os.path.normpath(source_file))
                Project._process_source_files(project_dic, [os.path.join(os.path.normpath(source_file), f) for f in os.listdir(
                    source_file) if os.path.isfile(os.path.join(os.path.normpath(source_file), f))], group_name)

            extension = source_file.split('.')[-1].lower()
            extension = mappings[extension] or extension

            if extension not in extensions:
                continue

            if extension not in project_dic['source_groups'][group_name]:
                project_dic['source_groups'][group_name][extension] = []

            project_dic['source_groups'][group_name][extension].append(os.path.normpath(source_file))

            if not os.path.dirname(source_file) in project_dic['source_paths']:
                project_dic['source_paths'].append(os.path.normpath(os.path.dirname(source_file)))

    def _get_workspace_name(self):
        workspaces = self.pgen_workspace.workspaces
        for workspace, proj_workspace in workspaces.items():
            for p in proj_workspace.projects:
                if self is p:
                    return workspace

    def _validate_tools(self, tool):
        """ Use tool_supported or tool """
        tools = []
        if not tool:
            if len(self.project['common']['tools_supported']) == 0:
                logging.info("No tool defined.")
                return -1
            tools = self.project['common']['tools_supported']
        else:
            tools = [tool]
        return tools

    def clean(self, tool):
        tools = self._validate_tools(tool)
        if tools == -1:
            return -1

        for current_tool in tools:
            # We get the export dict formed, then use it for cleaning
            self._fill_export_dict(current_tool)
            path = self.project['common']['output_dir']['path']

            if os.path.isdir(path):
                logging.info("Cleaning directory %s" % path)

                shutil.rmtree(path)
        return 0

    def export(self, tool, copy):
        """ Exports a project """
        tools = self._validate_tools(tool)
        if tools == -1:
            return -1

        generated_files = {}
        result = 0
        for export_tool in tools:
            exporter = ToolsSupported().get_tool(export_tool)

            # None is an error
            if exporter is None:
                result = -1
                logging.debug("Tool: %s was not found" % export_tool)
                continue

            self._fill_export_dict(export_tool)
            if copy:
                self._copy_sources_to_generated_destination()
            # Print debug info prior exporting
            logging.debug("Project common data: %s" % self.project['common'])
            logging.debug("Project tool_specific data: %s" % self.project['tool_specific'])
            logging.debug("Project export data: %s" % self.project['export'])

            files = exporter(self.project['export'], self.pgen_workspace.settings).export_project()
            generated_files[export_tool] = files
        self.generated_files = generated_files
        return result

    def build(self, tool):
        """build the project"""
        tools = self._validate_tools(tool)
        if tools == -1:
            return -1

        result = 0

        for build_tool in tools:
            builder = ToolsSupported().get_tool(build_tool)
            # None is an error
            if builder is None:
                logging.debug("Tool: %s was not found" % builder)
                result = -1
                continue

            logging.debug("Building for tool: %s", build_tool)
            logging.debug(self.generated_files)
            builder(self.generated_files[build_tool], self.pgen_workspace.settings).build_project()
        return result

    def get_generated_project_files(self, tool):
        # returns list of project files which were generated
        exporter = ToolsSupported().get_tool(tool)
        return exporter(self.generated_files[tool], self.pgen_workspace.settings).get_generated_project_files()

    @staticmethod
    def _generate_output_dir(path):
        """this is a separate function, so that it can be more easily tested."""
        relpath = os.path.relpath(os.getcwd(),path)
        count = relpath.count(os.sep) + 1

        return relpath+os.path.sep, count

    def _source_of_type(self, dict_type, filetype):
        """return a dictionary of groups and the sources of a specified type within them"""
        files = {}
        for group, group_contents in dict_type.items():
            files[group] = []
            if filetype in group_contents:
                files[group].extend(group_contents[filetype])
        return files

    def _get_tool_data(self, key, tool_keywords):
        data = []
        for tool_name in tool_keywords:
            try:
                if self.project['tool_specific'][tool_name][key]:
                    data.append(self.project['tool_specific'][tool_name][key])
            except KeyError:
                continue
        return flatten(data)

    def _get_tool_sources(self, tool_keywords):
        sources = {}
        for tool_name in tool_keywords:
            try:
                sources = merge_recursive(sources, self.project['tool_specific'][tool_name]['source_groups'])
            except KeyError:
                continue
        return sources

    def _fill_export_dict(self, tool):
        tool_keywords = []
        # get all keywords valid for the tool
        tool_keywords.append(ToolsSupported().get_toolchain(tool))
        tool_keywords.append(ToolsSupported().get_toolnames(tool))
        tool_keywords = list(set(flatten(tool_keywords)))

        # Copy common to export, as a base. We then add tool data
        self.project['export'].update(self.project['common'])

        self._set_output_dir_path(tool)
        # Merge common project data with tool specific data
        self.project['export']['includes'] = self.project['export']['includes'] + self._get_tool_data('includes', tool_keywords)
        self.project['export']['include_files'] =  self.project['export']['include_files'] + self._get_tool_data('include_files', tool_keywords)
        self.project['export']['source_paths'] =  self.project['export']['source_paths'] + self._get_tool_data('source_paths', tool_keywords)
        self.project['export']['macros'] = self.project['export']['macros'] + self._get_tool_data('macros', tool_keywords)
        self.project['export']['linker_file'] =  self.project['export']['linker_file'] or self._get_tool_data('linker_file', tool_keywords)
        self.project['export']['template'] = self._get_tool_data('template', tool_keywords)
        self.project['export']['misc'] =  self._get_tool_data('misc', tool_keywords)

        # This is magic with sources as they have groups
        tool_sources = self._get_tool_sources(tool_keywords)
        self.project['export']['source_files'] = merge_recursive(self.project['export']['source_groups'], tool_sources)
        for ext in ["c","cpp","s","lib", "obj"]:
           key = "source_files_" + ext
           self.project['export'][key] = merge_recursive(self._source_of_type(self.project['export']['source_groups'], ext), self._source_of_type(tool_sources, ext))

        # linker checkup
        if len(self.project['export']['linker_file']) == 0 and self.project['export']['output_type'] == 'exe':
            logging.debug("Executable - no linker command found.")

        # There might be a situation when there are more linkers. warn user and choose the first one
        if type(self.project['export']['linker_file']) == type(list()):
            if len(self.project['export']['linker_file']) > 1:
                logging.debug("More than one linker command files: %s" % self.project['export']['linker_file'])
            self.project['export']['linker_file'] = self.project['export']['linker_file'][0]

    def _set_output_dir_path(self, tool):
        if self.pgen_workspace.settings.export_location_format != self.pgen_workspace.settings.DEFAULT_EXPORT_LOCATION_FORMAT:
            location_format = self.pgen_workspace.settings.export_location_format
        else:
            if 'export_dir' in self.project['export'] and self.project['export']['export_dir']:
                location_format = self.project['export']['export_dir']
            else:
                location_format = self.pgen_workspace.settings.export_location_format

        # substitute all of the different dynamic values
        location = PartialFormatter().format(location_format, **{
            'project_name': self.name,
            'tool': tool,
            'target': self.project['export']['target'],
            'workspace': self._get_workspace_name() or '.'
        })

        # TODO (matthewelse): make this return a value directly
        self.project['export']['output_dir']['path'] = os.path.normpath(location)
        path = self.project['export']['output_dir']['path']
        self.project['export']['output_dir']['rel_path'], self.project['export']['output_dir']['rel_count'] = self._generate_output_dir(path)

    def _copy_files(self, file, output_dir, valid_files_group):
        file = os.path.normpath(file)
        dest_dir = os.path.join(os.getcwd(), output_dir, os.path.dirname(file))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        if file.split('.')[-1] in valid_files_group:
            shutil.copy2(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), output_dir, file))

    def _copy_sources_to_generated_destination(self):
        """" Copies all project files to specified directory - generated dir"""
        for path in self.project['export']['includes']:
            if os.path.isdir(path):
                # directory full of include files
                path = os.path.normpath(path)
                files = os.listdir(path)
            else:
                # includes is a file, make it valid
                files = [os.path.basename(path)]
                path = os.path.dirname(path)
            dest_dir = os.path.join(os.getcwd(), self.project['export']['output_dir']['path'], path)
            if not os.path.exists(dest_dir) and len(files):
                os.makedirs(dest_dir)
            for filename in files:
                if filename.split('.')[-1] in FILES_EXTENSIONS['includes']:
                    shutil.copy2(os.path.join(os.getcwd(), path, filename),
                                 os.path.join(os.getcwd(), self.project['export']['output_dir']['path'], path))

        # all sources are grouped, therefore treat them as dict
        for k, v in self.project['export']['source_files_c'].items():
            for file in v:
                self._copy_files(file, self.project['export']['output_dir']['path'], FILES_EXTENSIONS['source_files_c'])

        for k, v in self.project['export']['source_files_cpp'].items():
            for file in v:
                self._copy_files(file, self.project['export']['output_dir']['path'], FILES_EXTENSIONS['source_files_cpp'])

        for k, v in self.project['export']['source_files_s'].items():
            for file in v:
                self._copy_files(file, self.project['export']['output_dir']['path'], FILES_EXTENSIONS['source_files_s'])

        for k,v in self.project['export']['source_files_obj'].items():
            for file in v:
                self._copy_files(file, self.project['export']['output_dir']['path'], FILES_EXTENSIONS['source_files_obj'])

        for k,v in self.project['export']['source_files_lib'].items():
            for file in v:
                self._copy_files(file, self.project['export']['output_dir']['path'], FILES_EXTENSIONS['source_files_lib'])

        linker = os.path.normpath(self.project['export']['linker_file'])
        dest_dir = os.path.join(os.getcwd(), self.project['export']['output_dir']['path'], os.path.dirname(linker))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy2(os.path.join(os.getcwd(), linker),
                     os.path.join(os.getcwd(), self.project['export']['output_dir']['path'], linker))

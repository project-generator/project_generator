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
import shutil
import logging
import operator
import copy
import yaml

from .tools_supported import ToolsSupported
from .tools.tool import get_tool_template
from .util import merge_recursive, PartialFormatter, FILES_EXTENSIONS, VALID_EXTENSIONS, FILE_MAP, OUTPUT_TYPES, SOURCE_KEYS, fix_paths

logger = logging.getLogger('progen.project')

class ProjectWorkspace:
    """ Represents a workspace (multiple projects) """

    def __init__(self, name, projects, settings, workspace_settings):
        self.name = name
        self.projects = projects
        self.settings = settings
        self.workspace_settings = workspace_settings
        self.generated_files = {}

    def generate(self, tool, copied=False, copy=False):
        """ Generates a workspace """

        # copied - already done by external script, copy - do actual copy

        tools = []
        if not tool:
            logger.info("Workspace supports one tool for all projects within.")
            return -1
        else:
            tools = [tool]

        result = 0
        for export_tool in tools:
            tool_export = ToolsSupported().get_tool(export_tool)
            if tool_export is None:
                result = -1
                continue

            project_export_dir_overwrite = False
            if self.settings.export_location_format != self.settings.DEFAULT_EXPORT_LOCATION_FORMAT:
                location_format = self.settings.export_location_format
            else:
                if 'export_dir' in self.workspace_settings:
                    location_format = self.workspace_settings['export_dir'][0]
                    project_export_dir_overwrite = True
                else:
                    location_format = self.settings.export_location_format

            # substitute all of the different dynamic values
            location = PartialFormatter().format(location_format, **{
                'project_name': self.name,
                'tool': tool,
                'workspace_name': self.name
            })

            workspace_dic = {
                'projects': [],
                'settings': {
                    'name': self.name,
                    'path': os.path.normpath(location),
                },
            }

            for project in self.projects:
                generated_files = {
                    'projects' : [],
                    'workspaces': [],
                }

                if project_export_dir_overwrite:
                    project.project['common']['export_dir'] = location
                # Merge all dics, copy sources if required, correct output dir. This happens here
                # because we need tool to set proper path (tool might be used as string template)
                project._fill_export_dict(export_tool, copied)

                if copy:
                    project._copy_sources_to_generated_destination()
                project.project['export']['singular'] = False
                files = tool_export(project.project['export'], self.settings).export_project()
                # we gather all generated files, needed for workspace files
                workspace_dic['projects'].append(files)
                generated_files['projects'].append(files)

            # all projects are genereated, now generate workspace files
            generated_files['workspaces'] = tool_export(workspace_dic, self.settings).export_workspace()

            self.generated_files[export_tool] = generated_files
            return result

    def build(self, tool):
        logger.info("Building a workspace is not currently supported")
        return -1

    def clean(self, tool):
        logger.info("Cleaning a workspace is not currently supported")
        return -1

class ProjectTemplate:
    """ Public data which can be set in yaml files
        Yaml data available are:
            'build_dir' : build_dir,    # Build output path
            'debugger' : debugger,      # Debugger
            'export_dir': '',           # Export directory path
            'includes': [],             # include paths
            'linker_file': None,        # linker script file
            'name': name,               # project name
            'macros': [],               # macros
            'misc': {},                 # misc settings related to tools
            'output_type': output_type, # output type, default - exe
            'sources': [],              # source files/folders
            'target': '',               # target
            'template' : [],            # tool template
            'tools_supported': [],      # Tools which are supported,
    """

    @staticmethod
    def _get_common_data_template():
        """ Data for tool specific """

        data_template = {
            'includes': [],      # include files/folders
            'linker_file': '',   # linker script file
            'macros': [],        # macros
            'sources': [],       # source files/folders
        }
        return data_template

    @staticmethod
    def _get_tool_specific_data_template():
        """ Data for tool specific """

        data_template = {
            'misc': {},     # misc settings related to tools
            'template': [], # template project file
        }
        return data_template

    @staticmethod
    def get_project_template(name="Default", output_type='exe', debugger=None, build_dir='build'):
        """ Project data (+ data) """

        project_template = {
            'build_dir' : build_dir,  # Build output path
            'debugger' : debugger,    # Debugger
            'export_dir': '',         # Export directory path
            'name': name,             # project name
            'output_type': output_type, # output type, default - exe
            'target': '',             # target
            'tools_supported': [],    # Tools which are supported,
        }
        project_template.update(ProjectTemplate._get_common_data_template())
        project_template.update(ProjectTemplate._get_tool_specific_data_template())
        return project_template

class Project:

    """ Represents a project, which can be formed of many yaml files """

    def __init__(self, name, project_dicts, settings, workspace_name=None):
        """ Initialise a project with a yaml file """

        assert type(project_dicts) is list, "Project records/dics must be a list" % project_dicts 

        self.settings = settings
        self.name = name
        self.workspace_name = workspace_name
        self.project = {}
        self.project['common'] = {}
        self.project['export'] = {} # merged common and tool
        self.project['tool_specific'] = {}
        self.project['common'] = ProjectTemplate.get_project_template(self.name, OUTPUT_TYPES['exe'])

        # fill common + tool_specific dics from the project_dicts
        for project_data in project_dicts:
            # project_data might be empty yaml - None
            if project_data:
                if 'common' in project_data:
                    self._set_project_attributes('common', self.project['common'], project_data)
                if 'tool_specific' in project_data:
                    for tool_name, tool_settings in project_data['tool_specific'].items():
                        # if there's no valid tool name, skip that yaml file and report to a user
                        if tool_name not in ToolsSupported().get_supported():
                            logger.error("Project data %s contain non-valid tool: %s" % (project_data, tool_name))
                            continue
                        try:
                            # if dict does not exist, we initialize it
                            bool(self.project['tool_specific'][tool_name])
                        except KeyError:
                            self.project['tool_specific'][tool_name] = ProjectTemplate.get_project_template(self.name, OUTPUT_TYPES['exe'])
                        self._set_project_attributes(tool_name, self.project['tool_specific'][tool_name], project_data['tool_specific'])
        self.generated_files = {}

    @staticmethod
    def _list_elim_none(list_to_clean):
        return [l for l in list_to_clean if l]

    @staticmethod
    def _dict_elim_none(dic_to_clean):
        dic = dic_to_clean
        try:
            for k, v in dic_to_clean.items():
                if type(v) is list:
                    dic[k] = Project._list_elim_none(v)
                elif type(v) is dict:
                    dic[k] = Project._dict_elim_none(v)
        except AttributeError:
            pass
        return dic

    # Project data have the some keys the same, therefore we process them here
    # and their own keys, are processed in common/tool attributes
    def _set_project_attributes(self, key_value, destination, source):
        if key_value in source:
            for attribute, data in source[key_value].items():
                if attribute in ProjectTemplate.get_project_template().keys():
                    if type(destination[attribute]) is list:
                        if type(data) is list:
                            destination[attribute].extend(Project._list_elim_none(data))
                        else:
                            destination[attribute].append(Project._dict_elim_none(data))
                    elif type(destination[attribute]) is dict:
                        destination[attribute] = Project._dict_elim_none(merge_recursive(destination[attribute], data))
                    else:
                        if type(data) is list:
                            if data[0]:
                                destination[attribute] = data[0]
                        else:
                            if data:
                                destination[attribute] = data

    def _set_internal_common_data(self):
        # process here includes, sources and set all internal data related to them
        for files in self.project['common']['sources']:
            self._process_source_files(files)
        for files in self.project['common']['includes']:
            self._process_include_files(files)

    def _set_internal_tool_data(self, tool_keywords):
        # process here includes, sources and set all internal data related to them for tool_keywords
        for tool in tool_keywords:
            if tool in self.project['tool_specific'].keys():
                if 'includes' in self.project['tool_specific'][tool]:
                    for files in self.project['tool_specific'][tool]['includes']:
                        self._process_include_files(files)
                if 'sources' in self.project['tool_specific'][tool]:
                    for files in self.project['tool_specific'][tool]['sources']:
                        self._process_source_files(files)

    def _process_include_files(self, files, use_group_name = 'default'):
        # If it's dic add it , if file, add it to files
        use_includes = []
        if type(files) == dict:
            for group_name, include_files in files.items():
                self._process_include_files(include_files, group_name)
        elif type(files) == list:
            use_includes = files
        else:
            if files:
                use_includes = [files]

        if use_group_name not in self.project['export']['include_files'] and use_includes:
            self.project['export']['include_files'][use_group_name] = []

        for include_file in use_includes:
            include_file = include_file.replace('\\', '/')
            # include might be set to None - empty yaml list
            if include_file:
                if os.path.isdir(include_file):
                   # its a directory
                    dir_path = include_file
                    # get all files from dir
                    include_files = []
                    try:
                        for f in os.listdir(dir_path):
                            if os.path.isfile(os.path.join(os.path.normpath(dir_path), f)) and f.split('.')[-1].lower() in FILES_EXTENSIONS['include_files']:
                                include_files.append(os.path.join(os.path.normpath(dir_path), f))
                    except:
                        # TODO: catch only those exceptions which are relevant
                        logger.debug("The includes is not accessible: %s" % include_file)
                        continue
                    self.project['export']['include_files'][use_group_name] += include_files
                else:
                    # include files are in groups as sources
                    self.project['export']['include_files'][use_group_name].append(os.path.normpath(include_file))
                    dir_path = os.path.dirname(include_file)
                if not os.path.normpath(dir_path) in self.project['export']['include_paths']:
                    self.project['export']['include_paths'].append(os.path.normpath(dir_path))

    def _process_source_files(self, files, use_group_name='default'):
        use_sources = []
        if type(files) == dict:
            for group_name, sources in files.items():
                # process each group name as separate entity
                self._process_source_files(Project._list_elim_none(sources), group_name)
        elif type(files) == list:
            use_sources = Project._list_elim_none(files)
        else:
            if files:
                use_sources = [files]

        for source_file in use_sources:
            source_file = os.path.normpath(source_file)
            if os.path.isdir(source_file):
                self.project['export']['source_paths'].append(source_file)
                self._process_source_files([os.path.join(source_file, f) for f in os.listdir(
                    source_file) if os.path.isfile(os.path.join(source_file, f))], use_group_name)

            # Based on the extension, create a groups inside source_files_(extension)
            extension = source_file.split('.')[-1].lower()
            if extension not in VALID_EXTENSIONS:
                continue
            source_group = FILE_MAP[extension]
            if use_group_name not in self.project['export'][source_group]:
                self.project['export'][source_group][use_group_name] = []

            self.project['export'][source_group][use_group_name].append(source_file)

            if not os.path.dirname(source_file) in self.project['export']['source_paths']:
                self.project['export']['source_paths'].append(os.path.normpath(os.path.dirname(source_file)))

    def _validate_tools(self, tool):
        """ Use tool_supported or tool """

        tools = []
        if not tool:
            if len(self.project['common']['tools_supported']) == 0:
                logger.info("No tool defined.")
                return -1
            tools = self.project['common']['tools_supported']
        else:
            tools = [tool]
        return tools

    @staticmethod
    def _generate_output_dir(settings, path):
        """ This is a separate function, so that it can be more easily tested """

        relpath = os.path.relpath(settings.root,path)
        count = relpath.count(os.sep) + 1

        return relpath+os.path.sep, count

    def _get_tool_data(self, key, tool_keywords):
        data = []
        for tool_name in tool_keywords:
            try:
                if self.project['tool_specific'][tool_name][key]:
                    if type(self.project['tool_specific'][tool_name][key]) is list:
                        data += self.project['tool_specific'][tool_name][key]
                    else:
                        data.append(self.project['tool_specific'][tool_name][key])
            except KeyError:
                continue
        return data

    def _get_tool_sources(self, tool_keywords):
        sources = {}
        for source_key in SOURCE_KEYS:
            sources[source_key] = {}
            for tool_name in tool_keywords:
                try:
                    sources[source_key] = merge_recursive(sources[source_key], self.project['tool_specific'][tool_name][source_key])
                except KeyError:
                    continue
        return sources

    def _get_tool_includes(self, tool_keywords):
        include_files = {}
        for tool_name in tool_keywords:
            try:
                include_files = merge_recursive(include_files, self.project['tool_specific'][tool_name]['include_files'])
            except KeyError:
                continue
        return include_files

    def _set_output_dir_path(self, tool, copied):
        if self.settings.export_location_format != self.settings.DEFAULT_EXPORT_LOCATION_FORMAT:
            location_format = self.settings.export_location_format
        else:
            if 'export_dir' in self.project['export'] and self.project['export']['export_dir']:
                location_format = self.project['export']['export_dir']
            else:
                location_format = self.settings.export_location_format

        # substitute all of the different dynamic values
        location = PartialFormatter().format(location_format, **{
            'project_name': self.name,
            'tool': tool,
            'target': self.project['export']['target'],
            'workspace': self.workspace_name or '.'
        })

        self.project['export']['output_dir']['path'] = os.path.normpath(location)
        path = self.project['export']['output_dir']['path']
        if copied:
            # Sources were copied, therefore they should be in the exported folder
            self.project['export']['output_dir']['rel_path'] = ''
            self.project['export']['output_dir']['rel_count'] = 0
        else:
            self.project['export']['output_dir']['rel_path'], self.project['export']['output_dir']['rel_count'] = self._generate_output_dir(self.settings, path)

    def _fill_export_dict(self, tool, copied=False):
        tool_keywords = []
        # get all keywords valid for the tool
        tool_keywords.append(ToolsSupported().get_toolchain(tool))
        tool_keywords += ToolsSupported().get_toolnames(tool)
        tool_keywords = list(set(tool_keywords))

        # Set the template keys an get the relative path to fix all paths
        self.project['export'] = get_tool_template()
        self.project['export'].update(self.project['common'])

        self._set_output_dir_path(tool, copied)

        self._set_internal_common_data()
        self._set_internal_tool_data(tool_keywords)

        # Merge common project data with tool specific data
        self.project['export']['source_paths'] += self._get_tool_data('source_paths', tool_keywords)
        self.project['export']['include_paths'] += self._get_tool_data('include_paths', tool_keywords)
        self.project['export']['linker_file'] =  self.project['export']['linker_file'] or self._get_tool_data('linker_file', tool_keywords)
        self.project['export']['macros'] += self._get_tool_data('macros', tool_keywords)
        self.project['export']['template'] = self._get_tool_data('template', tool_keywords)

        fix_paths(self.project['export'], self.project['export']['output_dir']['rel_path'], list(FILES_EXTENSIONS.keys()) + ['include_paths', 'source_paths'])

        # misc for tools requires dic merge
        misc = self._get_tool_data('misc', tool_keywords)
        for m in misc:
           self.project['export']['misc'] = merge_recursive(self.project['export']['misc'], m)

        # This is magic with sources/include_files as they have groups
        tool_sources = self._get_tool_sources(tool_keywords)
        for key in SOURCE_KEYS:
            self.project['export'][key] = merge_recursive(self.project['export'][key], tool_sources[key])
            # sort all sources within its own group and own category (=k)
            # the tool needs to do sort files as tools require further processing based on 
            # categories (we can't mix now cpp and c files for instance)
            for k, v in self.project['export'][key].items():
                self.project['export'][key][k] = sorted(v, key=lambda x: os.path.basename(x))

        self.project['export']['include_files'] = merge_recursive(self.project['export']['include_files'], self._get_tool_includes(tool_keywords))

        # linker checkup
        if len(self.project['export']['linker_file']) == 0 and self.project['export']['output_type'] == 'exe':
            logger.debug("Executable - no linker command found.")

        # There might be a situation when there are more linkers. warn user and choose the first one
        if type(self.project['export']['linker_file']) == type(list()):
            if len(self.project['export']['linker_file']) > 1:
                logger.debug("More than one linker command files: %s" % self.project['export']['linker_file'])
            elif len(self.project['export']['linker_file']) == 0:
                logger.debug("No linker found for %s tool" % tool)
                return
            self.project['export']['linker_file'] = self.project['export']['linker_file'][0]

    def _copy_sources_to_generated_destination(self):
        """ Copies all project files to specified directory - generated dir """

        files = []
        for key in FILES_EXTENSIONS.keys():
            if type(self.project['export'][key]) is dict:
                for k,v in self.project['export'][key].items():
                    files.extend(v)
            elif type(self.project['export'][key]) is list:
                files.extend(self.project['export'][key])
            else:
                files.append(self.project['export'][key])

        destination = os.path.join(self.settings.root, self.project['export']['output_dir']['path'])
        if os.path.exists(destination):
            shutil.rmtree(destination)
        for item in files:
            s = os.path.join(self.settings.root, item)
            d = os.path.join(destination, item)
            if os.path.isdir(s):
                shutil.copytree(s,d)
            else:
                if not os.path.exists(os.path.dirname(d)):
                    os.makedirs(os.path.join(self.settings.root, os.path.dirname(d)))
                shutil.copy2(s,d)

    def clean(self, tool):
        """ Clean a project """

        tools = self._validate_tools(tool)
        if tools == -1:
            return -1

        for current_tool in tools:
            # We get the export dict formed, then use it for cleaning
            self._fill_export_dict(current_tool)
            path = self.project['export']['output_dir']['path']

            if os.path.isdir(path):
                logger.info("Cleaning directory %s" % path)

                shutil.rmtree(path)
        return 0

    def generate(self, tool, copied=False, copy=False):
        """ Generates a project """

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
                logger.debug("Tool: %s was not found" % export_tool)
                continue

            self._fill_export_dict(export_tool, copied)
            if copy:
                logger.debug("Copying sources to the output directory")
                self._copy_sources_to_generated_destination()
            # dump a log file if debug is enabled
            if logger.isEnabledFor(logging.DEBUG):
                dump_data = {}
                dump_data['common'] = self.project['common']
                dump_data['tool_specific'] = self.project['tool_specific']
                dump_data['merged'] = self.project['export']
                handler = logging.FileHandler(os.path.join(os.getcwd(), "%s.log" % self.name),"w", encoding=None, delay="true")
                handler.setLevel(logging.DEBUG)
                logger.addHandler(handler)
                logger.debug("\n" + yaml.dump(dump_data))

            files = exporter(self.project['export'], self.settings).export_project()
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
                logger.debug("Tool: %s was not found" % builder)
                result = -1
                continue

            logger.debug("Building for tool: %s", build_tool)
            logger.debug(self.generated_files)
            if builder(self.generated_files[build_tool], self.settings).build_project() == -1:
                # if one fails, set to -1 to report
                result = -1
        return result

    def get_generated_project_files(self, tool):
        """ Get generated project files, the content depends on a tool. Look at tool implementation """

        exporter = ToolsSupported().get_tool(tool)
        return exporter(self.generated_files[tool], self.settings).get_generated_project_files()


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

from .tool import build, export

try:
    input = raw_input
except:
    pass

def merge_recursive(*args):
    if all(isinstance(x, dict) for x in args):
        output = {}
        keys = reduce(operator.or_, [set(x) for x in args])

        for key in keys:
            # merge all of the ones that have them
            output[key] = merge_recursive(*[x[key] for x in args if key in x])

        return output
    else:
        return reduce(operator.add, args)

class ToolSpecificSettings:

    """represents the settings that are specifc to targets"""

    def __init__(self):
        self.include_paths = []
        self.source_paths = []
        self.source_groups = {
            'default': {}
        }
        self.macros = []
        self.misc = {}

        self.linker_file = None

    def add_settings(self, data_dictionary, group_name):
        if 'source_paths' in data_dictionary:
            self.source_paths.extend(data_dictionary['source_paths'])

        if 'source_files' in data_dictionary:
            self._process_source_files(
                data_dictionary['source_files'], group_name)

        if 'include_paths' in data_dictionary:
            self.include_paths.extend([x for x in data_dictionary['include_paths'] if x is not None])

        if 'macros' in data_dictionary:
            self.macros.extend([x for x in data_dictionary['macros'] if x is not None])

        if 'project_dir' in data_dictionary:
            self.project_dir.update(data_dictionary['project_dir'])

        if 'linker_file' in data_dictionary:
            self.linker_file = data_dictionary['linker_file'][0]

        if 'misc' in data_dictionary:
            self.misc.update(data_dictionary['misc'])

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


class Project:

    """represents a project, which can be formed of many yaml files"""

    TOOLCHAINS = {
        'iar_arm': 'iar',
        'uvision': 'uvision',
        'coide': 'gcc_arm',
        'make_gcc_arm': 'gcc_arm',
        'eclipse_make_gcc_arm': 'gcc_arm',
    }

    def __init__(self, name, project_files, workspace):
        """initialise a project with a yaml file"""

        self.workspace = workspace

        logging.debug("Initialising project %s" % name)

        self.name = name

        self.include_paths = []
        self.source_paths = []
        self.source_groups = {
            'default': {}
        }
        self.macros = []
        self.project_dir = {
            'name': '',
            'path': ''
        }

        self.mcu = ''
        self.core = ''
        self.target = ''

        self.output_types = {
            'executable': 'exe',
            'library': 'lib'
        }
        self.output_type = self.output_types['executable']

        self.linker_file = None
        self.tool_specific = defaultdict(ToolSpecificSettings)

        self.project_path = None
        self.project_name = None

        source_paths = []

        for project_file in project_files:
            with open(project_file, 'rt') as f:
                project_file_data = yaml.load(f)

            if 'common' in project_file_data:
                group_name = 'default'
                if 'output' in project_file_data['common']:
                    if project_file_data['common']['output'][0] not in self.output_types:
                        raise RuntimeError("Invalid Output Type.")

                    self.output_type = self.output_types[project_file_data['common']['output'][0]]

                if 'group_name' in project_file_data['common']:
                    group_name = project_file_data['common']['group_name'][0]

                if 'include_paths' in project_file_data['common']:
                    self.include_paths.extend(
                        [x for x in project_file_data['common']['include_paths'] if x is not None])

                if 'source_paths' in project_file_data['common']:
                    self.source_paths.extend(
                        [x for x in project_file_data['common']['source_paths'] if x is not None])

                if 'source_files' in project_file_data['common']:
                    source_paths = self._process_source_files(
                        project_file_data['common']['source_files'], group_name)

                if 'macros' in project_file_data['common']:
                    self.macros.extend(
                        [x for x in project_file_data['common']['macros'] if x is not None])

                if 'project_dir' in project_file_data['common']:
                    self.project_dir.update(
                        project_file_data['common']['project_dir'])

                if 'core' in project_file_data['common']:
                    self.core = project_file_data['common']['core'][0]

                if 'target' in project_file_data['common']:
                    self.target = project_file_data['common']['target'][0]

                if 'name' in project_file_data['common']:
                    self.name = project_file_data['common']['name']

                if 'mcu' in project_file_data['common']:
                    self.mcu = project_file_data['common']['mcu'][0]

            if 'tool_specific' in project_file_data:
                for tool_name, tool_settings in project_file_data['tool_specific'].items():
                    self.tool_specific[tool_name].add_settings(
                        tool_settings, group_name)

        # No include paths - take from source files dir
        if self.include_paths == []:
            self.include_paths = source_paths

        if self.project_dir['path'] == '':
            self.project_dir['path'] = self.workspace.settings.generated_projects_folder

    def _process_source_files(self, files, group_name):
        source_paths = []
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
                source_paths.append(source_file)
                self._process_source_files([os.path.join(source_file, f) for f in os.listdir(
                    source_file) if os.path.isfile(os.path.join(source_file, f))], group_name)

            extension = source_file.split('.')[-1]
            extension = mappings[extension] or extension

            if extension not in extensions:
                continue

            if extension not in self.source_groups[group_name]:
                self.source_groups[group_name][extension] = []

            self.source_groups[group_name][extension].append(source_file)

            if os.path.dirname(source_file) not in self.source_paths:
                self.source_paths.append(os.path.dirname(source_file))

        return source_paths

    def clean(self, tool):
        if tool is None:
            tools = list(self.TOOLCHAINS)
        else:
            tools = [tool]

        for current_tool in tools:
            path = os.path.join(self.project_dir['path'], "%s_%s" % (current_tool, self.name))

            if os.path.isdir(path):
                logging.info("Cleaning directory %s" % path)

                shutil.rmtree(path)

    def build(self, tool):
        """build the project"""
        build(self.name, self.project_files, tool, self.workspace.settings)

    def export(self, tool):
        """export the project"""
        project_path, project_files = export(
            self.generate_dict_for_tool(tool), tool, self.workspace.settings)

        self.project_path = project_path
        self.project_files = project_files

        return project_path, project_files

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

    def generate_dict_for_tool(self, tool):
        """for backwards compatibility"""
        tool_specific_settings = self.tool_specific[self.TOOLCHAINS[tool]]
        toolchain_specific_settings = self.tool_specific[tool]

        if tool == self.TOOLCHAINS[tool]:
            # make sure we don't get duplicates :)
            tool_specific_settings = ToolSpecificSettings()

        d = {
            'name': self.name,
            'mcu': self.mcu,
            'core': self.core,
            'target': self.target,
            'output_type': self.output_type,
            'include_paths': self.include_paths + tool_specific_settings.include_paths,
            'source_paths': self.source_paths + tool_specific_settings.source_paths,
            'source_files': merge_recursive(self.source_groups,
                                            tool_specific_settings.source_groups,
                                            toolchain_specific_settings.source_groups),
            # for backwards compatibility
            'source_files_c': [merge_recursive(self.source_of_type('c'),
                                               tool_specific_settings.source_of_type('c'),
                                               toolchain_specific_settings.source_of_type('c'))],
            'source_files_cpp': [merge_recursive(self.source_of_type('cpp'),
                                                 tool_specific_settings.source_of_type('cpp'),
                                                 toolchain_specific_settings.source_of_type('cpp'))],
            'source_files_s': [merge_recursive(self.source_of_type('s'),
                                               tool_specific_settings.source_of_type('s'),
                                               toolchain_specific_settings.source_of_type('s'))],
            'source_files_obj': self.all_sources_of_type('obj') +
                                tool_specific_settings.all_sources_of_type('obj') +
                                toolchain_specific_settings.all_sources_of_type('obj'),
            'source_files_lib': self.all_sources_of_type('lib') +
                                tool_specific_settings.all_sources_of_type('lib') +
                                toolchain_specific_settings.all_sources_of_type('lib'),
            'linker_file': tool_specific_settings.linker_file
                        or toolchain_specific_settings.linker_file
                        or self.linker_file,
            'macros': self.macros +
                      tool_specific_settings.macros +
                      toolchain_specific_settings.macros,
            'misc': [merge_recursive(tool_specific_settings.misc, toolchain_specific_settings.misc)],
            'project_dir': self.project_dir
        }

        return d

    @staticmethod
    def scrape_dir(root, directory, project_name, board, list_sources):
        data = {
            'common': {
                'linker_file': [],
                'source_files': [],
                'include_paths': [],
                'target': [],
            }
        }

        linker_filetypes = ['sct', 'ld', 'lin', 'icf']
        source_filetypes = ['c', 'cpp', 'cc']
        include_filetypes = ['h', 'hpp', 'inc']

        for dirpath, dirnames, files in os.walk(directory):
            for filename in files:
                extension = filename.split('.')[-1]
                relpath = os.path.relpath(dirpath, root)

                if extension in linker_filetypes:
                    data['common']['linker_file'].append(os.path.join(relpath, filename))
                elif extension in source_filetypes:
                    data['common']['source_files'].append(os.path.join(relpath, filename) if list_sources else relpath)
                elif extension in include_filetypes:
                    data['common']['include_paths'].append(relpath)

        data['common']['source_files'] = list(set(data['common']['source_files']))
        data['common']['include_paths'] = list(set(data['common']['include_paths']))

        if len(data['common']['linker_file']) == 0:
            data['common']['linker_file'].append("No linker file found")

        data['common']['target'].append(board)

        logging.debug('Generating yaml file')

        filename = project_name.replace(' ', '_').lower() + '.yaml'

        #TODO: fix
        if os.path.isfile(os.path.join(directory, filename)):
            # this should be print, not logging
            print("Project file already exists")

            while True:
                answer = input('Should I overwrite it? (Y/n)')

                try:
                    overwrite = answer.lower() in ('y', 'yes')

                    if not overwrite:
                        logging.critical('Unable to save project file')
                        return -1

                    break
                except ValueError:
                    continue

        with open(os.path.join(root, filename), 'wt') as f:
            f.write(yaml.dump(data, default_flow_style=False))

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
import sys
import yaml
import logging
import shutil
import errno

from os.path import join, basename

from .yaml_parser import YAML_parser, _finditem
from .tool import export

class ProjectGenerator:
    # Each tool defines used toolchain.
    TOOLCHAINS = {
        'iar': 'iar',
        'uvision': 'uvision',
        'coide': 'gcc_arm',
        'make_gcc_arm': 'gcc_arm',
        'eclipse_make_gcc_arm': 'gcc_arm',
    }

    PROJECTS_RECORD_TEMPLATE = {
        'projects' : [],
    }

    PROJECT_RECORD_TEMPLATE = {
        'common': {
            'target' : [],
            'include_paths' : [],
            'source_files' : [],
            'linker_file' : [],
        }
    }

    def __init__(self, env_settings):
        self.env_settings = env_settings

    def parse_project(self, dic, project, tool, toolchain):
        project_list = []
        yaml_files = _finditem(dic, project)
        if yaml_files:
            for yaml_file in yaml_files:
                try:
                    file = open(yaml_file)
                except IOError:
                    raise RuntimeError("Cannot open a file: %s" % yaml_file)
                else:
                    loaded_yaml = yaml.load(file)
                    yaml_parser = YAML_parser()
                    project_list.append(
                        yaml_parser.parse_yaml(loaded_yaml, tool, toolchain))
                    file.close()
            yaml_parser_final = YAML_parser()
            process_data = yaml_parser_final.parse_yaml_list(project_list)
            yaml_parser_final.set_name(project)
        else:
            raise RuntimeError("Project: %s was not found." % project)
        return process_data

    def run_generator(self, dic, project, tool, toolchain):
        """ Generates one project. """
        process_data = self.parse_project(dic, project, tool, toolchain)
        logging.debug("Generating project: %s" % project)
        project_path = export(process_data, tool, self.env_settings)
        return project_path

    def process_all_projects(self, dic, tool, toolchain):
        """ Generates all project. """
        projects = []
        projects_paths = []
        for k, v in dic['projects'].items():
            projects.append(k)

        for project in projects:
            projects_paths.append(
                self.run_generator(dic, project, tool, toolchain))
        return (projects, projects_paths)

    def scrape_dir(self, target, path, gen_files, root):
        """ Generates a record for given directory. """
        # recognized files
        exts = ['s', 'c', 'cpp', 'h', 'inc', 'sct', 'ld', 'lin']
        found = {x: [] for x in exts}  # lists of found files
        ignore = '.'
        if path:
            directory = join(root, path)
        else:
            directory = root
        for dirpath, dirnames, files in os.walk(directory):
            # Remove directories in ignore
            # directory names must match exactly!
            for idir in ignore:
                if idir in dirnames:
                    dirnames.remove(idir)
            # Loop through the file names for the current step
            for name in files:
                # Split the name by '.' & get the last element
                ext = name.lower().rsplit('.', 1)[-1]
                # Save the full name if ext matches
                if ext in exts:
                    relpath = os.path.relpath(dirpath, root)
                    found[ext].append(join(relpath, name))
        # Create a directory which will be stored in the project.yaml file
        common = self.PROJECT_RECORD_TEMPLATE
        common['common']['target'].append(target if target else 'No target given')
        for k,v in found.items():
            if k == 's'  or k == 'c' or k == 'cpp':
                for file in v:
                    if gen_files:
                        common['common']['source_files'].append(file)
                    elif os.path.dirname(file) not in common['common']['source_files']:
                        common['common']['source_files'].append(os.path.dirname(file))
            elif k == 'h' or k == 'inc':
                for file in v:
                    path_from_root, filename = os.path.split(file)
                    if path_from_root not in common['common']['include_paths']:
                        common['common']['include_paths'].append(path_from_root)
            elif k == 'sct' or k == 'ld' or k =='lin':
                for file in v:
                    common['common']['linker_file'].append(file)

        if not common['common']['linker_file']:
            common['common']['linker_file'].append('No linker file found')

        source_list_path = os.getcwd()
        if not os.path.exists(source_list_path):
            os.makedirs(source_list_path)
        logging.debug("Generating: %s" % source_list_path)
        with open('gen_project.yaml', 'w') as outfile:
            outfile.write(yaml.dump(common, default_flow_style=False))

    def list_projects(self, dic):
        """ Print all defined project. """
        for k, v in dic['projects'].items():
            logging.info('project: %s' % k)

    def set_toolchain(self, options):
        try:
            options.toolchain = self.TOOLCHAINS[options.tool]
        except KeyError:
            logging.error("The tool was find as unsupported: %s", options.tool)
            sys.exit(-1)

    def load_config(self, options):
        """ Load the project file. """
        logging.debug("Processing projects file.")
        project_file = open(options.file)
        config = yaml.load(project_file)
        project_file.close()
        return config

    def default_settings(self, options, settings):
        if not options.tool:
            options.tool = settings.DEFAULT_TOOL
        if not options.file:
            options.file = 'projects.yaml'

    def run(self, options):
        config = self.load_config(options)

        # update enviroment variables
        self.env_settings.load_env_settings(config)

        projects = []
        projects_paths = []
        if options.project:
            project_path = self.run_generator(
                config, options.project, options.tool, options.toolchain)  # one project
            projects.append(options.project)
            projects_paths.append(project_path)
        else:
            # all projects within project.yaml
            projects, projects_paths = self.process_all_projects(
                config, options.tool, options.toolchain)

        return (projects, projects_paths)

    def clean(self, options):
        # This function is a bit hacky, this needs a proper implementation
        if not options.file:
            options.file = 'projects.yaml'
        if options.tool or options.project:
            self.set_toolchain(options)
        else:
            options.toolchain = None
        config = self.load_config(options)
        projects_paths = []
        if options.project:
            process_data = self.parse_project(config, options.project, options.tool, options.toolchain)
            # now get the path for the project
            # TODO: fix - similarity to gen_file in the Exporter
            if process_data['project_dir']['path'] is '':
                process_data['project_dir']['path'] = 'generated_projects'
            if not os.path.exists(process_data['project_dir']['path']):
                # nothing to clean
                logging.debug("The project does not exist: %s" % process_data['project_dir']['path'])
                return
            if process_data['project_dir']['name'] is '':
                process_data['project_dir']['name'] = options.tool + '_' + process_data['name']
            projects_paths.append(join(process_data['project_dir']['path'], process_data['project_dir']['name']))
        else:
            projects = []
            for k, v in config['projects'].items():
                projects.append(k)

            for project in projects:
                process_data = self.parse_project(config, project, options.tool, options.toolchain)
                # TODO: fix - similarity to gen_file in the Exporter
                generated_dir = process_data['project_dir']['path']
                if generated_dir is '':
                    generated_dir = 'generated_projects'
                if not os.path.exists(generated_dir):
                    # nothing to clean
                    logging.debug("The project does not exist: %s" % generated_dir)
                    continue
                for tools in self.TOOLCHAINS.keys():
                    generated_path = process_data['project_dir']['name']
                    if generated_path is '':
                        generated_path = tools + '_' + process_data['name']
                    projects_paths.append(join(generated_dir, generated_path))

        for project in projects_paths:
            if not os.path.exists(project):
                logging.debug("The project does not exist: %s" % project)
                continue

            try:
                shutil.rmtree(project)
            except OSError as exception:
                if 'cannot call rmtree on a symbolic link' in str(exception).lower():
                    os.unlink(project)
                elif exception.errno != errno.ENOENT:
                    raise

        # try to clean the only folder we might have created
        if os.path.exists('generated_projects') and not os.listdir('generated_projects'):
            try:
                shutil.rmtree('generated_projects')
            except OSError as exception:
                if 'cannot call rmtree on a symbolic link' in str(exception).lower():
                    os.unlink('generated_projects')
                elif exception.errno != errno.ENOENT:
                    raise


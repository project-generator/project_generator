# Copyright 2014 0xc0170
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

    def __init__(self, env_settings):
        self.env_settings = env_settings

    def run_generator(self, dic, project, tool, toolchain):
        """ Generates one project. """
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

        logging.debug("Generating project: %s" % project)
        project_path = export(process_data, tool, self.env_settings)
        return project_path

    def process_all_projects(self, dic, tool, toolchain):
        """ Generates all project. """
        projects = []
        projects_paths = []
        yaml_files = []
        for k, v in dic['projects'].items():
            projects.append(k)

        for project in projects:
            projects_paths.append(
                self.run_generator(dic, project, tool, toolchain))
        return (projects, projects_paths)

    def scrape_dir(self):
        exts = ['s', 'c', 'cpp', 'h', 'inc', 'sct', 'ld']
        found = {x: [] for x in exts}  # lists of found files
        ignore = '.'
        for dirpath, dirnames, files in os.walk(os.getcwd()):
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
                    relpath = dirpath.replace(os.getcwd(), "")
                    found[ext].append(join(relpath, name))
        # The body of our log file
        logbody = ''
        # loop thru results
        for search in found:
            # Concatenate the result from the found dict
            logbody += "<< Results with the extension '%s' >>" % search
            logbody += '\n\n%s\n\n' % '\n'.join(found[search])
        # Write results to the logfile
        source_list_path = join(os.getcwd(), 'tools', 'records')
        if not os.path.exists(source_list_path):
            os.makedirs(source_list_path)
        target_path = join(source_list_path, 'scrape.log')
        logging.debug("Generating: %s" % target_path)
        with open(target_path, 'w') as logfile:
            logfile.write('%s' % logbody)

    def list_projects(self, dic):
        """ Print all defined project. """
        for k, v in dic['projects'].items():
            logging.info(k)

    def set_toolchain(self, options):
        try:
            options.toolchain = self.TOOLCHAINS[options.tool]
        except KeyError:
            logging.error("The tool was find as supported: %s", options.tool)
            sys.exit(-1)

    def run(self, options):
        if not options.file:
            # create a list of all files in the dir that we're interested in
            self.scrape_dir()
            # print help menu
            # parser.print_help()
            sys.exit()

        logging.debug("Processing projects file.")
        project_file = open(options.file)
        config = yaml.load(project_file)

        if options.list:
            logging.info("Projects defined in the %s" % options.file)
            self.list_projects(config)
            sys.exit()

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

        project_file.close()
        return (projects, projects_paths)

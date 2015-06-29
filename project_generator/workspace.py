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

import yaml
import logging

from .project import Project
from .settings import ProjectSettings
from .tool import ToolsSupported
from .targets import Targets


class Workspace:

    """a collections of projects from a single projects.yaml file"""

    def __init__(self, projects_file='projects.yaml', project_root='.'):
        # load projects file

        with open(projects_file, 'rt') as f:
            self.projects_dict = yaml.load(f)

        self.settings = ProjectSettings()

        if 'settings' in self.projects_dict:
            self.settings.update(self.projects_dict['settings'])

        # so that we can test things independently of eachother
        self.projects = {}

        if 'projects' in self.projects_dict:
            for name,records in self.projects_dict['projects'].items():
                if "common" in records:
                    self.projects[name] = Project(name, records, self)
                else:
                    x = set([item if len(item)>1 else sublist for sublist in records for item in sublist])
                    self.projects[name] = Project(name, list(x), self)
        else:
            logging.debug("No projects found in the main record file.")
    def export_project(self, project_name, tool, copy):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Exporting Project %s" % project_name)

        self.projects[project_name].export(tool, copy)

    def export_projects(self, tool, copy):
        for name, project in self.projects.items():
            logging.debug("Exporting Project %s" % name)

            project.export(tool, copy)

    def build_projects(self, tool):
        for name, project in self.projects.items():
            logging.debug("Building Project %s" % name)

            project.build(tool)

    def flash_projects(self, tool):

        for name, project in self.projects.items():
            logging.debug("Flashing Project %s" % name)

            project.flash(tool)

    def build_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Building Project %s" % project_name)
        self.projects[project_name].build(tool)

    def flash_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Flashing Project %s" % project_name)
        self.projects[project_name].flash(tool)

    @staticmethod
    def pgen_list(type):
        if type == 'tools':
            print ("pgen supports the following tools:")
            print(yaml.dump(ToolsSupported().get_supported(), default_flow_style=False))
        elif type == 'targets':
            target = Targets(ProjectSettings().get_env_settings('definitions'))
            print ("pgen supports the following targets:")
            print(yaml.dump(target.targets, default_flow_style=False))

    def list(self, type, format='logging', out=True):
        output = []
        if type == 'projects':
            for project in self.projects:
                output.append(project)
                print (project)
        elif type == 'targets':
            for project in self.projects:
                print ("project: " + project + "\ntarget: " + str(self.projects_dict['projects'][project]['common']['target'][0]))
                output.append(self.projects_dict['projects'][project]['common']['target'][0])
        elif type == 'tools':
            for project in self.projects:
                tool = self.projects_dict['projects'][project]['tool_specific'].keys()[0]
                print ("project: " + project + "\ntool: " + tool)
                output.append(tool)

        if format == 'logging':
            for o in output:
                logging.info(o)
        elif format == 'yaml':
            projects = list(output)

            if out:
                print(yaml.dump(output, default_flow_style=False))
            else:
                return yaml.dump(output, default_flow_style=False)
        elif format == 'raw':
            return set(output)
        else:
            raise NotImplementedError("Output format not supported.")

    def clean_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        self.projects[project_name].clean(project_name, tool)

    def clean_projects(self, tool):
        for name, project in self.projects.items():
            logging.debug("Cleaning Project %s" % name)

            project.clean(tool)

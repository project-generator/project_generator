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

class Workspace:

    """a collections of projects from a single projects.yaml file"""

    def __init__(self, projects_file='projects.yaml', project_root='.'):
        # load projects file

        with open(projects_file, 'rt') as f:
            projects_dict = yaml.load(f)

        self.settings = ProjectSettings()

        if 'settings' in projects_dict:
            self.settings.update(projects_dict['settings'])

        # so that we can test things independently of eachother
        self.projects = {}
        
        if 'projects' in projects_dict:
            self.projects = {name: Project(name, records, self) for name, records in projects_dict['projects'].items()}
        else:
            logging.debug("No projects found in the main record file.")

    def export_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Exporting Project %s" % project_name)

        if tool is None:
            tool = self.settings.DEFAULT_TOOL

        self.projects[project_name].export(tool)

    def export_projects(self, tool):
        if tool is None:
            tool = self.settings.DEFAULT_TOOL
        
        for name, project in self.projects.items():
            logging.debug("Exporting Project %s" % name)

            project.export(tool)

    def build_projects(self, tool):
        if tool is None:
            tool = self.settings.DEFAULT_TOOL
        
        for name, project in self.projects.items():
            logging.debug("Building Project %s" % name)

            project.build(tool)

    def build_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Building Project %s" % project_name)

        if tool is None:
            tool = self.settings.DEFAULT_TOOL

        self.projects[project_name].build(tool)

    def list_projects(self, format='logging', out=True):
        if format == 'logging':
            for project in self.projects:
                logging.info(project)
        elif format == 'yaml':
            projects = list(self.projects)

            if out:
                print(yaml.dump(projects, default_flow_style=False))
            else:
                return yaml.dump(projects, default_flow_style=False)
        elif format == 'raw':
            return set(self.projects)
        else:
            raise NotImplementedError("Output format not supported.")

    def clean_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")

        self.projects[project_name].clean(tool)

    def clean_projects(self, tool):
        for name, project in self.projects.items():
            logging.debug("Cleaning Project %s" % name)

            project.clean(tool)

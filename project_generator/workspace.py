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

from .project import Project, ProjectWorkspace
from .settings import ProjectSettings
from .tool import ToolsSupported
from .targets import Targets
from .util import flatten, uniqify


class PgenWorkspace:

    """a collections of projects from a single projects.yaml file"""

    def __init__(self, projects_file='projects.yaml', project_root='.'):
        # load projects file

        with open(projects_file, 'rt') as f:
            self.projects_dict = yaml.load(f)

        self.settings = ProjectSettings()
        if 'settings' in self.projects_dict:
            self.settings.update(self.projects_dict['settings'])

        # so that we can test things independently of eachother
        self.workspaces = {}

        # We support grouping of projects or just a project for ProjectWorkspace
        #
        # [projects.yaml]
        #   projects:
        #       project_group_1:
        #           project_1:
        #               -a
        #               -b
        #               -c
        #           project_2:
        #               -d
        #               -e
        #               -f
        #       project_3:
        #           -g
        #           -h
        # extension - workspaces
        settings = {}
        if 'workspaces' in self.projects_dict:
            for work_name, sections in self.projects_dict['workspaces'].items():
                workspace_projects = []
                for project_name, proj_list in sections['projects'].items():
                    workspace_projects.append(Project(project_name, flatten(proj_list), self))
                if 'settings' in self.projects_dict['workspaces'][work_name]:
                    settings = self.projects_dict['workspaces'][work_name]['settings']
                self.workspaces[work_name] = ProjectWorkspace(work_name, workspace_projects, settings, self, False)
        else:
            logging.debug("No workspaces found in the main record file.")

        if 'projects' in self.projects_dict:
            for name, records in self.projects_dict['projects'].items():
                if type(records) is dict:
                    # workspace
                    projects = [Project(n, uniqify(flatten(r)), self) for n, r in records.items()]
                else:
                    # single project
                    projects = [Project(name, uniqify(flatten(records)), self)]

                self.workspaces[name] = ProjectWorkspace(name, projects, self, type(records) is not dict)
        else:
            logging.debug("No projects found in the main record file.")

    def export_project(self, project_name, tool, copy):
        if project_name not in self.workspaces:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Exporting Project %s" % project_name)
        self.workspaces[project_name].export(tool, copy)

    def export_projects(self, tool, copy):
        for name, project in self.workspace.items():
            logging.debug("Exporting Project %s" % name)

            project.export(tool, copy)

    def build_projects(self, tool):
        for name, project in self.workspace.items():
            logging.debug("Building Project %s" % name)

            project.build(tool)

    def flash_projects(self, tool):

        for name, project in self.workspace.items():
            logging.debug("Flashing Project %s" % name)

            project.flash(tool)

    def build_project(self, project_name, tool):
        if project_name not in self.workspace:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Building Project %s" % project_name)
        self.workspace[project_name].build(tool)

    def flash_project(self, project_name, tool):
        if project_name not in self.workspace:
            raise RuntimeError("Invalid Project Name")

        logging.debug("Flashing Project %s" % project_name)
        self.workspace[project_name].flash(tool)

    @staticmethod
    def pgen_list(type):
        if type == 'tools':
            print ("pgen supports the following tools:")
            return '\n'.join(ToolsSupported().get_supported())
        elif type == 'targets':
            target = Targets(ProjectSettings().get_env_settings('definitions'))
            print ("pgen supports the following targets:")
            return '\n'.join(target.targets)

    def list_projects(self, width = 1, use_unicode = True):
        # List the projects in a PgenWorkspace. If flat is true, don't display
        # as a tree.

        workspace_names = list(self.workspaces)
        lines = []

        unicode_chars = {
            'tl': u'\u250c',
            'bl': u'\u2514',
            'rt': u'\u251c',
            '-': u'\u2500',
            '|': u'\u2502',
            ' ': u' ',
            '.': u'\u2504'
        }

        ascii_chars = {
            'tl': '+',
            'bl': '+',
            'rt': '+',
            '-': '-',
            '|': '|',
            ' ': ' '
        }

        chars = unicode_chars if use_unicode else ascii_chars
        width = width if use_unicode else 0

        for i in range(len(workspace_names)):
            name = workspace_names[i]
            workspace = self.workspaces[name]
            line = u"" if unicode else ''

            if len(workspace_names) == 1:
                line += chars['.']
            elif i == 0:
                line += chars['tl']
            elif i == len(workspace_names) - 1:
                line += chars['bl']
            else:
                line += chars['rt']

            line += chars['-'] * width
            line += chars[' ']

            line += name
            lines.append(line)

            if not workspace.singular:
                # it's not a placeholder workspace for a single project
                for j in range(len(workspace.projects)):
                    project = workspace.projects[j]

                    line = u'' if unicode else ''

                    if i == len(workspace_names) - 1:
                        line += chars[' ']
                    else:
                        line += chars['|']

                    line += chars[' '] * (width + 1)

                    if j == len(workspace.projects) - 1:
                        line += chars['bl']
                    else:
                        line += chars['rt']

                    line += chars['-'] * width
                    line += chars[' ']

                    line += project.name

                    lines.append(line)

        return '\n'.join(lines)

    def list_targets(self):
        output = []
        for project in self.projects:
            output.append("project: " + project + "\ntarget: " + str(self.projects_dict['projects'][project]['common']['target'][0]))

        return '\n'.join(output)

    def list_tools(self):
        output = []

        for project in self.projects:
            tool = self.projects_dict['projects'][project]['tool_specific'].keys()[0]
            output.append("project: " + project + "\ntool: " + tool)

        return '\n'.join(output)

    def clean_project(self, project_name, tool):
        if project_name not in self.projects:
            raise RuntimeError("Invalid Project Name")
        logging.debug("Cleaning Project %s" % project_name)
        self.projects[project_name].clean(project_name, tool)

    def clean_projects(self, tool):
        for name, project in self.projects.items():
            self.clean_project(name,tool)

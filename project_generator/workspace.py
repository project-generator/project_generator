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
import logging

from .project import Project, ProjectWorkspace
from .settings import ProjectSettings
from .tools_supported import ToolsSupported
from .targets import Targets
from .util import flatten, uniqify, load_yaml_records


class PgenWorkspace:

    """a collections of projects from a single projects.yaml file"""

    def __init__(self, projects_file='projects.yaml', project_root='.'):
        # either it's file or a dictionary. If dictionary , proceed otherwise load yaml
        if type(projects_file) is not dict:
            try:
                with open(projects_file, 'rt') as f:
                    self.projects_dict = yaml.load(f)
            except IOError:
               raise IOError("The main pgen projects file %s doesn't exist." % projects_file)
        else:
            self.projects_dict = projects_file

        self.settings = ProjectSettings()
        if 'settings' in self.projects_dict:
            self.settings.update(self.projects_dict['settings'])

        # so that we can test things independently of eachother
        self.workspaces = {}
        self.projects = {}

        # We support grouping of projects which is a workspace
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

        if 'projects' in self.projects_dict:
            for name, records in self.projects_dict['projects'].items():
                if type(records) is dict:
                    # workspace
                    projects = [Project(n, load_yaml_records(uniqify(flatten(r))), self) for n, r in records.items()]
                    self.workspaces[name] = ProjectWorkspace(name, projects, self)
                else:
                    # single project
                    self.projects[name] = Project(name, load_yaml_records(uniqify(flatten(records))), self)
        else:
            logging.debug("No projects found in the main record file.")

    def _is_project(self, proj_name):
        return proj_name in [name for name, v in self.projects.items()]

    def _is_workspace(self, workspace_name):
        return workspace_name in [name for name, v in self.workspaces.items()]

    def export(self, name, tool, copy):
        """ Export a project or a workspace """
        if self._is_project(name):
            logging.debug("Exporting project: %s" % name)
            return self.projects[name].export(tool, copy)
        elif self._is_workspace(name):
            logging.debug("Exporting workspace: %s" % name)
            return self.workspaces[name].export(tool, copy)
        else:
            logging.warning("Invalid Project Name: %s" % name)
            return -1

    def export_all(self, tool, copy):
        # Export all, projects and workspaces
        result = 0
        for name, project in self.projects.items():
            logging.debug("Exporting project: %s" % name)
            export_result = project.export(tool, copy)
            if export_result == -1:
                result = -1

        for name, workspace in self.workspaces.items():
            logging.debug("Exporting workspace: %s" % name)
            export_result = workspace.export(tool, copy)
            if export_result == -1:
                result = -1
        return result

    def build(self, project_name, tool):
        if self._is_project(project_name):
            return self.projects[project_name].build(tool)
        elif self._is_workspace(project_name):
            return self.workspaces[project_name].build(tool)
        else:
            logging.warning("Invalid Project Name")
            return -1

        logging.debug("Building Project %s" % project_name)
        return self.projects[project_name].build(tool)

    def build_all(self, tool):
        result = 0
        for name, project in self.projects.items():
            logging.debug("Exporting project: %s" % name)
            build_result = project.build(tool)
            if build_result == -1:
                result = -1

        for name, workspace in self.workspaces.items():
            logging.debug("Exporting workspace: %s" % name)
            build_result = workspace.build(tool)
            if build_result == -1:
                result = -1
        return result

    @staticmethod
    def pgen_list(type):
        if type == 'tools':
            print ("pgen supports the following tools:")
            return '\n'.join(ToolsSupported().get_supported())
        elif type == 'targets':
            target = Targets(ProjectSettings().get_env_settings('definitions'))
            print ("pgen supports the following targets:")
            return '\n'.join(target.targets)
        elif type == 'projects':
            return '\n'.join('')

    def list_projects(self, width = 1, use_unicode = True):
        # List the projects in a PgenWorkspace. If flat is true, don't display
        # as a tree.

        # TODO: (matthewelse) tidy this up, along with other Workspace stuff

        names = list(self.workspaces) + [k for k, v in self.projects.items() if v.project['singular']]

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

        for i, name in enumerate(names):
            if name in self.workspaces:
                workspace = self.workspaces[name]
            else:
                workspace = self.projects[name]

            line = u"" if unicode else ''

            if len(names) == 1:
                line += chars['.']
            elif i == 0:
                line += chars['tl']
            elif i == len(names) - 1:
                line += chars['bl']
            else:
                line += chars['rt']

            line += chars['-'] * width
            line += chars[' ']

            line += name
            lines.append(line)

            if type(workspace) is ProjectWorkspace:
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

    def clean(self, name, tool):
        """ Export a project or a workspace """
        if self._is_project(name):
            logging.debug("Cleaning project: %s" % name)
            return self.projects[name].clean(tool)
        elif self._is_workspace(name):
            logging.debug("Cleaning workspace: %s" % name)
            return self.workspaces[name].clean(tool)
        else:
            logging.warning("Invalid Project Name: %s" % name)
            return -1

    def clean_all(self, tool):
        result = 0
        for name, project in self.projects.items():
            logging.debug("Cleaning project: %s" % name)
            clean_result = project.clean(tool)
            if clean_result == -1:
                result = -1

        for name, workspace in self.workspaces.items():
            logging.debug("Cleaning workspace: %s" % name)
            clean_result = workspace.clean(tool)
            if clean_result == -1:
                result = -1
        return result

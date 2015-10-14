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

from .settings import ProjectSettings
from .util import flatten, uniqify, load_yaml_records
from .project import *
from .targets import Targets

class Generator:
    def __init__(self, projects_file):
        if type(projects_file) is not dict:
            try:
                with open(projects_file, 'rt') as f:
                    self.projects_dict = yaml.load(f)
            except IOError:
               raise IOError("The main pgen projects file %s doesn't exist." % projects_file)
        else:
            self.projects_dict = projects_file
        self.workspaces = {}
        self.settings = ProjectSettings()

        if 'settings' in self.projects_dict:
            self.settings.update(self.projects_dict['settings'])

        # update Target definitions
        Targets().update_definitions(False, self.settings)

    def generate(self, name = ''):
        if 'projects' in self.projects_dict:
            if name != '':
                if name in self.projects_dict['projects'].keys():
                    records = self.projects_dict['projects'][name]
                    if type(records) is dict:
                        projects = [Project(n, load_yaml_records(uniqify(flatten(r))), self) for n, r in records.items()]
                        self.workspaces[name] = ProjectWorkspace(name, projects, self)
                        yield self.workspaces[name]
                    else:
                        yield Project(name, load_yaml_records(uniqify(flatten(records))), self)
                else:
                    raise RuntimeError("You specified an invalid project name.")
            else:
                for name, records in self.projects_dict['projects'].items():
                    if type(records) is dict:
                        # workspace
                        projects = [Project(n, load_yaml_records(uniqify(flatten(r))), self) for n, r in records.items()]
                        self.workspaces[name] = ProjectWorkspace(name, projects, self)
                        yield self.workspaces[name]
                    else:
                        yield Project(name, load_yaml_records(uniqify(flatten(records))), self)
        else:
            logging.debug("No projects found in the main record file.")

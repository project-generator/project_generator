# Copyright 2015 0xc0170
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
import logging

from .tool import build

class ProjectBuilder:

    def __init__(self, env_settings):
        self.project_path = "generated_projects" # default project path
        self.env_settings = env_settings

    def build_project_list(self, options, projects):
        projects_list = []
        for dirpath, dirnames, files in os.walk(self.project_path):
            for d in dirnames:
                for project_name in projects:
                    proj = options.tool + '_' + project_name
                    if proj in d:
                        projects_list.append(project_name)
                        break
        return projects_list

    def run(self, options, projects, projects_paths, root):
        #project_list = self.build_project_list(options, projects)
        logging.info("Building defined projects. Might take a while.")
        build(projects, projects_paths, options.tool, self.env_settings, root)

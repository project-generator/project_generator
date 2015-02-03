import os
import logging

from .tool import build

class ProjectBuilder:

    def __init__(self):
        self.project_path = "generated_projects"

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

    def run(self, options, projects, projects_paths):
        #project_list = self.build_project_list(options, projects)
        logging.info("Building all defined projects.")
        build(projects, projects_paths, options.tool)

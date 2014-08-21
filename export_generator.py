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
"""Just a template for subclassing"""
import uuid, shutil, os, logging, fnmatch
from os.path import join, dirname, isdir, split
from jinja2 import Template

class OldLibrariesException(Exception): pass

class Exporter():
    TEMPLATE_DIR = dirname(__file__) + '/templates'
    DOT_IN_RELATIVE_PATH = False

    def gen_file(self, template_file, data, target_file, ide):
        """ Fills data to the project template, using jinja2. """
        template_path = join(Exporter.TEMPLATE_DIR, template_file)
        template_text = open(template_path).read()
        template = Template(template_text)
        target_text = template.render(data)

        project_file_loc = 'generated_projects' + '\\'
        if not os.path.exists(project_file_loc):
            os.makedirs(project_file_loc)
        project_dir = project_file_loc + ide + '_' + data['name']
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        target_path = join(project_dir, target_file)
        logging.debug("Generating: %s" % target_path)
        open(target_path, "w").write(target_text)


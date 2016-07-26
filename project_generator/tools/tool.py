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
from collections import OrderedDict

from os.path import join, dirname, abspath, normpath
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment

from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools')


def get_tool_template():
    """ Internal project data

    a dict with the following keys is returned:
    source_paths - a list of source paths derived from s
    include_paths - a list of include paths derived from sources
    include_files - a dict of include files used in the copy function mapping
                    groups to the files with each group (a list)
    source_files_c - a dict of c source files mapping groups to a list of files
                     within the group
    source_files_cpp - a dict of c++ source files mapping groups to a list of
                       files within the group
    source_files_s - a dict of groups to lists of assembly source files within
                     each group
    source_files_obj - dict of groups to lists of object files within each group
    source_files_lib - a dict of libraries mapping a group to a list of
                       libraries
    singular - a Boolean value indicating whether this is a singular project or
               part of a workspace
    output_dir - a dict containing:
      path - directory that output files are generated into by the exported
             project, relative to the current directory
      rel_path - the relative path to the root
      rel_count - the number of steps to the root
    macros - a list of c pre-processor macros
    template - a filename of an external template file
    misc - a dict of miscellaneous tool options

    """

    internal_template = {
        'source_paths': [],
        'include_paths': [],
        'include_files': {},
        'source_files_c': {},
        'source_files_cpp': {},
        'source_files_s': {},
        'source_files_obj': {},
        'source_files_lib': {},
        'singular': True,
        'output_dir': {
            'path': '',
            'rel_path': '',
            'rel_count': '',
        },
        "macros": [],
        "template": None,
        "misc": {}
    }
    return internal_template


# Each new tool should at least support this Tool class methods
# and Exporter class. The build is optional as not every tool supports building
# via command line.

# Basic class to provide information about a tool like a name , toolchains
class Tool(object):
    """ Just a tool template for subclassing"""

    @staticmethod
    def get_toolnames():
        raise NotImplementedError

    @staticmethod
    def get_toolchain():
        raise NotImplementedError

# Builder class for building a project
class Builder:
    """ Just a builder template to be subclassed """

    def build_project(self):
        """ Should return 0 if built, otherwise return -1 """
        raise NotImplementedError

# Exporter class for exporting a project or a workspace
class Exporter(object):
    """Just an exporter template for subclassing"""

    TEMPLATE_DIR = abspath(join(dirname(__file__), '..', 'templates'))

    # Any tool which exports should implement these methods 3 methods
    def export_workspace(self):
        raise NotImplementedError

    def export_project(self):
        raise NotImplementedError

    def get_generated_project_files(self):
        raise NotImplementedError

    # Exporter supports currently 2 methods for exporting. Raw data, which can be
    # for example xml. Or jinja2 templates, not always possible to generate valid
    # xml/json/etc.. output, then jinja2 helps as it's just injects data to predefined
    # valid format. The easiest way is use raw, as we can template a project, take a valid
    # project, parse it and inject progen data into and generate a file which tool understands

    # jinja2 is quite a work for more advanced tools as there are many options and support all of
    # them requires lot of time. On the other hand, use a template file provided by a user (expecting
    # a valid template project file) is easier to implement and then we can support 100 percent of what
    # tool provides.

    def gen_file_raw(self, target_text, output, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        open(output, "w").write(target_text)
        return dirname(output), output

    def gen_file_jinja(self, template_file, data, output, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        """ Fills data to the project template, using jinja2. """
        env = Environment()
        env.loader = FileSystemLoader(self.TEMPLATE_DIR)
        # TODO: undefined=StrictUndefined - this needs fixes in templates
        template = env.get_template(template_file)
        target_text = template.render(data)

        open(output, "w").write(target_text)
        return dirname(output), output

    def fixup_executable(self, exe_path):
        return exe_path

    @staticmethod
    def is_supported_by_default(target):
        return False

    def _expand_data(self, old_data, new_data, group):
        """ data expansion - uvision needs filename and path separately. """
        for file in old_data:
            if file:
                extension = file.split(".")[-1].lower()
                if extension in self.file_types.keys():
                    new_data['groups'][group].append(self._expand_one_file(normpath(file),
                                                                           new_data, extension))
                else:
                    logger.debug("Filetype for file %s not recognized" % file)
        if hasattr(self, '_expand_sort_key'):
            new_data['groups'][group] = sorted(new_data['groups'][group],
                                               key=self._expand_sort_key)

    def _get_groups(self, data):
        """ Get all groups defined """
        groups = []
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    k = 'Sources'
                if k not in groups:
                    groups.append(k)
        for k, v in data['include_files'].items():
            if k == None:
                k = 'Includes'
            if k not in groups:
                groups.append(k)
        return groups

    def _iterate(self, data, expanded_data):
        """ _Iterate through all data, store the result expansion in extended dictionary """
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                if group in data[attribute].keys():
                    self._expand_data(data[attribute][group], expanded_data, group)
        for k, v in data['include_files'].items():
            if k == None:
                group = 'Includes'
            else:
                group = k
            self._expand_data(data['include_files'][group], expanded_data, group)

        # sort groups
        expanded_data['groups'] = OrderedDict(sorted(expanded_data['groups'].items(), key=lambda t: t[0]))

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

import copy
import logging

from collections import OrderedDict
# eclipse works with linux paths
from posixpath import normpath, join, basename

from .tool import Tool, Builder, Exporter
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.eclipse')

class EclipseGnuARM(Tool, Exporter, Builder):

    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1, 'h': 1}

    generated_project = {
        'path': '',
        'files': {
            'proj_file': '',
            'cproj': '',
            'makefile': '',
        }
    }

    def __init__(self, workspace, env_settings):
        self.definitions = 0
        self.exporter = MakefileGccArm(workspace, env_settings)
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['eclipse_make_gcc_arm', 'make_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def _expand_data(self, old_data, new_data, attribute, group):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for source in old_data[old_group]:
            if source:
                extension = source.split(".")[-1]
                if not extension in self.file_types.keys():
                    logger.debug("Filetype for file %s not recognized" % file)
                    continue
                # TODO: fix - workaround for windows, seems posixpath does not work
                source = source.replace('\\', '/')
                new_file = {"path": join('PARENT-%s-PROJECT_LOC' % new_data['output_dir']['rel_path'], normpath(source)), "name": basename(
                    source), "type": self.file_types[extension.lower()]}
                new_data['groups'][group].append(new_file)
        new_data['groups'][group] = sorted(new_data['groups'][group], key=lambda x: x['name'].lower())

#TODO: eliminate this duplicate in many tools. Same applies to _iterate
    def _get_groups(self, data):
        """ Get all groups defined. """
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
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                self._expand_data(data[attribute], expanded_data, attribute, group)
        for k, v in data['include_files'].items():
            if k == None:
                group = 'Includes'
            else:
                group = k
            self._expand_data(data['include_files'], expanded_data, attribute, group)

        # sort groups
        expanded_data['groups'] = OrderedDict(sorted(expanded_data['groups'].items(), key=lambda t: t[0]))

    def export_workspace(self):
        logger.debug("Current version of CoIDE does not support workspaces")

    def export_project(self):
        """ Processes groups and misc options specific for eclipse, and run generator """

        output = copy.deepcopy(self.generated_project)
        data_for_make = self.workspace.copy()

        self.exporter.process_data_for_makefile(data_for_make)
        output['path'], output['files']['makefile'] = self.gen_file_jinja('makefile_gcc.tmpl', data_for_make, 'Makefile', data_for_make['output_dir']['path'])

        expanded_dic = self.workspace.copy()
        expanded_dic['rel_path'] = data_for_make['output_dir']['rel_path']
        groups = self._get_groups(expanded_dic)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self._iterate(self.workspace, expanded_dic)

        # Project file
        project_path, output['files']['cproj'] = self.gen_file_jinja(
            'eclipse_makefile.cproject.tmpl', expanded_dic, '.cproject', data_for_make['output_dir']['path'])
        project_path, output['files']['proj_file'] = self.gen_file_jinja(
            'eclipse.project.tmpl', expanded_dic, '.project', data_for_make['output_dir']['path'])
        return output

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['proj_file'], self.workspace['files']['cproj'],
            self.workspace['files']['makefile']]}


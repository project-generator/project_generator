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

import copy

# eclipse works with linux paths
from posixpath import normpath, join, basename, relpath

from .exporter import Exporter
from .gccarm import MakefileGccArmExporter


class EclipseGnuARMExporter(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj']
    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1}

    def __init__(self):
        self.definitions = 0
        self.exporter = MakefileGccArmExporter()

    def expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for source in old_data[old_group]:
            if source:
                extension = source.split(".")[-1]
                # TODO: fix - workaround for windows, seems posixpath does not work
                source = source.replace('\\', '/')
                new_file = {"path": join('PARENT-%s-PROJECT_LOC' % new_data['rel_count'], normpath(source)), "name": basename(
                    source), "type": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                if dic:
                    for k, v in dic.items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k, v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group, rel_path)

    def generate(self, data, settings):
        """ Processes groups and misc options specific for eclipse, and run generator """
        data_for_make = data.copy()

        self.exporter.process_data_for_makefile(data_for_make, settings, "eclipse_makefile")
        project_path, makefile = self.gen_file('makefile_gcc.tmpl', data_for_make, 'Makefile', data_for_make['dest_path'])

        expanded_dic = data.copy()
        expanded_dic['rel_count'] = data_for_make['rel_count']
        groups = self.get_groups(expanded_dic)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, data_for_make['rel_path'])

        # Project file
        project_path, cproj = self.gen_file(
            'eclipse_makefile.cproject.tmpl', expanded_dic, '.cproject', data_for_make['dest_path'])
        project_path, projfile = self.gen_file(
            'eclipse.project.tmpl', expanded_dic, '.project', data_for_make['dest_path'])
        return project_path, [projfile, cproj, makefile]

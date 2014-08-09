"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from os.path import basename
from export_generator import Exporter

class GccArm(Exporter):
    NAME = 'GccArm'

    def __init__(self):
        self.data = []

    def list_files(self, data, attribute):
        c_list = []
        for groups in data['source_files_c']:
            try:
                for k,v in groups.items():
                    for file in v:
                        # name = basename(file)
                        c_list.append(file)
            except:
                continue
        data[attribute] = c_list

    def generate(self, data, ide):
        # Project file

        self.list_files(data, 'source_files_c')
        self.list_files(data, 'source_files_cpp')
        self.list_files(data, 'source_files_s')


        self.gen_file('gccarm_%s.tmpl' % data['mcu'], data, 'Makefile', ide)

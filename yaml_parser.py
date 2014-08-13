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
from compiler.ast import flatten

class YAML_parser():

    def __init__(self):
        self.data = {
            'name': '' ,                # project name
            'mcu' : '',                 # mcu
            'core' : '',                # core
            'linker_file': '',          # linker command file
            'include_paths': [],        # include paths
            'source_paths' : [],        # source paths
            'source_files_c': [],       # c source files
            'source_files_cpp': [],     # c++ source files
            'source_files_s': [],       # assembly source files
            'source_files_obj': [],     # object files
            'source_files_lib': [],     # libraries
            'macros': [],               # macros (defines)
            'misc' : [],                # tool specific settings, will be parsed separately
        }

    def process_files(self, source_list, group_name):
        """Process files accroding to the extension."""
        for source_file in source_list:
            extension = source_file.split(".")[-1]
            if extension == 'c':
                 self.data['source_files_c'][group_name].append(source_file)
            elif extension == 's':
                self.data['source_files_s'][group_name].append(source_file)
            elif extension == 'cpp':
                self.data['source_files_cpp'][group_name].append(source_file)

    def find_group_name(self, common_attributes):
        group_name = None
        for common_attribute in common_attributes:
            if common_attribute:
                try:
                    for k,v in common_attribute.items():
                        if k == 'group_name':
                            group_name = v
                except:
                    continue
        self.data['source_files_c'] = {}
        self.data['source_files_c'][group_name] = []
        self.data['source_files_cpp'] = {}
        self.data['source_files_cpp'][group_name] = []
        self.data['source_files_s'] = {}
        self.data['source_files_s'][group_name] = []
        return group_name

    def find_paths(self, common_attributes):
        include_paths = []
        source_paths = []
        for common_attribute in common_attributes:
            if common_attribute:
                try:
                    for k,v in common_attribute.items():
                        if k == 'source_paths':
                            source_paths = (v)
                        elif k == 'include_paths':
                            include_paths = (v)
                except:
                    continue
        self.data['source_paths'] = source_paths
        self.data['include_paths'] = include_paths

    def find_source_files(self, common_attributes, group_name):
        for common_attribute in common_attributes:
            if common_attribute:
                try:
                    for k,v in common_attribute.items():
                        if k == 'source_files':
                            self.process_files(v, group_name)
                except:
                    continue

    def find_macros(self, common_attributes):
        macros = []
        for common_attribute in common_attributes:
            if common_attribute:
                try:
                    for k,v in common_attribute.items():
                        if k == 'macros':
                            macros = v
                except:
                    continue
        self.data['macros'] = macros

    # returns updated data structure by virtual-folders
    def parse_yaml(self, dic, ide):
        # load all common attributes (paths, files, groups)
        common_attributes = find_all_values(dic, 'common')

        # prepare dic based on found groups in common
        group_name = self.find_group_name(common_attributes);
        self.find_paths(common_attributes)
        self.find_source_files(common_attributes, group_name)
        self.find_macros(common_attributes)

        #load all specific files
        specific_dic = {}
        specific_attributes = find_all_values(dic, 'tool_specific')
        for specific_attribute in specific_attributes:
            if specific_attribute:
                try:
                    for k,v in specific_attribute.items():
                        if k == ide:
                            specific_dic = v
                except:
                    continue

        for k,v in specific_dic.items():
            if "source_files" == k:
                # source files might have virtual dir
                self.process_files(v, group_name)
            elif "misc" == k:
                self.data[k] = v
            elif "include_paths" == k or "source_paths" == k:
                self.data[k].append(v)
            elif "macros" == k:
                self.data[k].append(v)
            else:
                self.data[k] = v

        # need to consider all object names (.o, .obj)
        self.data['source_files_obj'] = get_source_files_by_extension(dic, 'o')
        self.data['source_files_obj'].append(get_source_files_by_extension(dic, 'obj'))
        # need to consider all library names (.lib, .ar)
        self.data['source_files_lib'] = get_source_files_by_extension(dic, 'lib')
        self.data['source_files_lib'].append (get_source_files_by_extension(dic, 'ar'))
        self.data['source_files_lib'].append (get_source_files_by_extension(dic, 'a'))
        self.data['mcu'] = _finditem(dic, 'mcu')
        self.data['name'] = get_project_name(dic)
        self.data['core'] = _finditem(dic, 'core')
        return self.data

    def parse_list_yaml(self, project_list):
        for dic in project_list:
            name = _finditem(dic, 'name') #TODO fix naming
            if name:
                self.data['name'] = name[0]
            mcu = _finditem(dic, 'mcu') #TODO fix naming
            if mcu:
                self.data['mcu'] = mcu[0]
            include_paths = get_include_paths(dic)
            if include_paths:
                self.data['include_paths'].append(include_paths)
            source_paths = get_source_paths(dic)
            if source_paths:
                self.data['source_paths'].append(source_paths)
            linker_file = _finditem(dic, 'linker_file')
            if linker_file:
                if len(linker_file) != 1:
                    raise RuntimeError("Defined %s linker files. Only one allowed." % len(linker_file))
                self.data['linker_file'] = linker_file[0]
            source_c = find_all_values(dic, 'source_files_c')
            if source_c:
                self.data['source_files_c'].append(source_c)
            source_cpp = find_all_values(dic, 'source_files_cpp')
            if source_cpp:
                self.data['source_files_cpp'].append(source_cpp)
            source_s = find_all_values(dic, 'source_files_s')
            if source_s:
                self.data['source_files_s'].append(source_s)
            source_obj = find_all_values(dic, 'source_files_obj')
            if source_obj:
                self.data['source_files_obj'].append(source_obj)
            source_lib = find_all_values(dic, 'source_files_lib')
            if source_lib:
                self.data['source_files_lib'].append(source_lib)
            core = _finditem(dic, 'core')
            if core:
                self.data['core'] = core[0]

            macros = find_all_values(dic, 'macros')
            if macros:
                self.data['macros'].append(macros)
            misc = find_all_values(dic, 'misc')
            if misc:
                self.data['misc'].append(misc)

        self.data['tool_specific_options'] = flatten(self.data['misc'])
        self.data['macros'] = flatten(self.data['macros'])
        self.data['include_paths'] = flatten(self.data['include_paths'])
        self.data['source_paths'] = flatten(self.data['source_paths'])
        self.data['source_files_obj'] = flatten(self.data['source_files_obj'])
        self.data['source_files_lib'] = flatten(self.data['source_files_lib'])
        return self.data


def get_cc_flags(dic):
    return _finditem(dic, 'cc_flags')

def get_project_name(dic):
    return _finditem(dic, 'name')

def get_project_name_list(dic_list):
    for dic in dic_list:
        result = _finditem(dic, 'name')
        if result:
            return result
    return None

def get_macros(dic):
    return _finditem(dic, 'macros')

def get_include_paths(dic):
    paths_list = find_all_values(dic, 'include_paths')
    paths = flatten(paths_list)
    return paths

def get_source_paths(dic):
    paths_list = find_all_values(dic, 'source_paths')
    paths = flatten(paths_list)
    return paths

def get_source_files_by_extension(dic, extension):
    find_extension = 'source_files_' + extension
    source_list = find_all_values(dic, find_extension)
    source = flatten(source_list)
    return source

def find_all_values(obj, key):
    files = []
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = find_all_values(v, key)
            if item is not None:
                files.append(item)
    return files

def _finditem(obj, key):
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item

def get_project_files(dic, name):
    return flatten(find_all_values(dic, name))

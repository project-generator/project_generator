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

class YAML_parser():

    def __init__(self):
        self.data = {
            'name': '' ,                # project name
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
        """ Creates new dictionaries based on group_name """
        group_name = None
        try:
            for k,v in common_attributes.items():
                if k == 'group_name':
                    group_name = v[0]
        except KeyError:
            pass
        self.data['source_files_c'] = {}
        self.data['source_files_c'][group_name] = []
        self.data['source_files_cpp'] = {}
        self.data['source_files_cpp'][group_name] = []
        self.data['source_files_s'] = {}
        self.data['source_files_s'][group_name] = []
        return group_name

    def find_paths(self, common_attributes):
        """ Find defined include and source paths """
        include_paths = []
        source_paths = []
        try:
            for k,v in common_attributes.items():
                if k == 'source_paths':
                    source_paths = (v)
                elif k == 'include_paths':
                    include_paths = (v)
        except KeyError:
            pass
        self.data['source_paths'] = source_paths
        self.data['include_paths'] = include_paths

    def find_source_files(self, common_attributes, group_name):
        try:
            for k,v in common_attributes.items():
                if k == 'source_files':
                    self.process_files(v, group_name)
        except KeyError:
            pass

    def find_macros(self, common_attributes):
        macros = []
        try:
            for k,v in common_attributes.items():
                if k == 'macros':
                    macros = v
        except KeyError:
            pass
        self.data['macros'] = macros

    def parse_yaml(self, dic, ide):
        """ Parse single yaml file, find all data in records and return it. """
        # load all common attributes (paths, files, groups)
        common_attributes = _finditem(dic, 'common')

        # prepare dic based on found groups in common
        group_name = self.find_group_name(common_attributes);
        self.find_paths(common_attributes)
        self.find_source_files(common_attributes, group_name)
        self.find_macros(common_attributes)

        #load all specific files
        specific_dic = {}
        specific_attributes = _finditem(dic, 'tool_specific')
        if specific_attributes:
            try:
                for k,v in specific_attributes.items():
                    if k == ide:
                        specific_dic = v
            except KeyError:
                pass

        for k,v in specific_dic.items():
            if "source_files" == k:
                # source files might have virtual dir
                self.process_files(v, group_name)
            elif "misc" == k:
                self.data[k] = v
            elif "include_paths" == k or "source_paths" == k:
                self.data[k] += (v)
            elif "macros" == k:
                self.data[k] += (v)
            else:
                self.data[k] = v

        # need to consider all object names (.o, .obj)
        obj = get_source_files_by_extension(dic, 'o')
        if obj:
            self.data['source_files_obj'].append(obj)
        obj = get_source_files_by_extension(dic, 'obj')
        if obj:
            self.data['source_files_obj'].append(obj)

        # need to consider all library names (.lib, .ar)
        lib = get_source_files_by_extension(dic, 'lib')
        if lib:
            self.data['source_files_lib'].append(lib)
        lib = get_source_files_by_extension(dic, 'ar')
        if lib:
            self.data['source_files_lib'].append(lib)
        lib = get_source_files_by_extension(dic, 'a')
        if lib:
            self.data['source_files_lib'].append(lib)

        self.data['name'] = _finditem(dic, 'name')
        self.data['core'] = _finditem(dic, 'core')
        return self.data

    def parse_yaml_list(self, project_list):
        """ Process list of dictionaries from yaml files. """
        for dic in project_list:
            name = _finditem(dic, 'name') #TODO fix naming
            if name:
                self.data['name'] = name[0]
            mcu = _finditem(dic, 'mcu') #TODO fix naming
            if mcu:
                self.data['mcu'] = mcu[0]
            include_paths = _finditem(dic, 'include_paths')
            if include_paths:
                self.data['include_paths'] += (include_paths)
            source_paths = _finditem(dic, 'source_paths')
            if source_paths:
                self.data['source_paths'] += (source_paths)
            linker_file = _finditem(dic, 'linker_file')
            if linker_file:
                if len(linker_file) != 1:
                    raise RuntimeError("Defined %s linker files. Only one allowed." % len(linker_file))
                self.data['linker_file'] = linker_file[0]
            source_c = _finditem(dic, 'source_files_c')
            if source_c:
                self.data['source_files_c'].append(source_c)
            source_cpp = _finditem(dic, 'source_files_cpp')
            if source_cpp:
                self.data['source_files_cpp'].append(source_cpp)
            source_s = _finditem(dic, 'source_files_s')
            if source_s:
                self.data['source_files_s'].append(source_s)
            source_obj = _finditem(dic, 'source_files_obj')
            if source_obj:
                self.data['source_files_obj'].append(source_obj)
            source_lib = _finditem(dic, 'source_files_lib')
            if source_lib:
                self.data['source_files_lib'].append(source_lib)
            core = _finditem(dic, 'core')
            if core:
                self.data['core'] = core[0]

            macros = _finditem(dic, 'macros')
            if macros:
                self.data['macros'] += (macros)
            misc = _finditem(dic, 'misc')
            if misc:
                self.data['misc'].append(misc)

        return self.data

def get_source_files_by_extension(dic, extension):
    """ Returns list of source files based on defined extension. """
    find_extension = 'source_files_' + extension
    return _finditem(dic, find_extension)

def find_all_values(obj, key):
    files = []
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = find_all_values(v, key)
            if item:
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

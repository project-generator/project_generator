# Copyright 2014-2015 0xc0170
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
import yaml
import locale
import shutil
import string
import operator

from functools import reduce

FILES_EXTENSIONS = {
    'include_files': ['h', 'hpp', 'inc'],
    'source_files_s': ['s'],
    'source_files_c': ['c'],
    'source_files_cpp': ['cpp', 'cc'],
    'source_files_lib': ['lib', 'ar', 'a'],
    'source_files_obj': ['o', 'obj'],
    'linker_file': ['sct', 'ld', 'lin', 'icf'],
}

OUTPUT_TYPES = {
    'executable': 'exe',
    'exe': 'exe',
    'library': 'lib',
    'lib': 'lib',
}

FILE_MAP = {v:k for k,values in FILES_EXTENSIONS.items() for v in values}
SOURCE_KEYS = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_lib', 'source_files_obj']
VALID_EXTENSIONS = reduce(lambda x,y:x+y,[FILES_EXTENSIONS[key] for key in SOURCE_KEYS])

def rmtree_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def uniqify(_list):
    # see: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order/29898968#29898968
    return reduce(lambda r, v: v in r[1] and r or (r[0].append(v) or r[1].add(v)) or r, _list, ([], set()))[0]

def merge_recursive(*args):
    if all(isinstance(x, dict) for x in args):
        output = {}
        keys = reduce(operator.or_, [set(x) for x in args])

        for key in keys:
            # merge all of the ones that have them
            output[key] = merge_recursive(*[x[key] for x in args if key in x])

        return output
    else:
        return reduce(operator.add, args)

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def load_yaml_records(yaml_files):
    dictionaries = []
    for yaml_file in yaml_files:
        try:
            f = open(yaml_file, 'rt')
            dictionaries.append(yaml.load(f))
        except IOError:
           raise IOError("The file %s referenced in main yaml doesn't exist." % yaml_file)
    return dictionaries

class PartialFormatter(string.Formatter):
    def get_field(self, field_name, args, kwargs):
        try:
            val = super(PartialFormatter, self).get_field(field_name, args, kwargs)
        except (IndexError, KeyError, AttributeError):
            first, _ = field_name._formatter_field_name_split()
            val = '{' + field_name + '}', first
        return val

def fix_paths(project_data, rel_path, extensions):
    """ Fix paths for extension list """
    norm_func = lambda path : os.path.normpath(os.path.join(rel_path, path))
    for key in extensions:
        if type(project_data[key]) is dict:
            for k,v in project_data[key].items():
                project_data[key][k] = [norm_func(i) for i in v]
        elif type(project_data[key]) is list:
            project_data[key] = [norm_func(i) for i in project_data[key]]
        else:
            project_data[key] = norm_func(project_data[key])

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
import shutil
import locale

def rmtree_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def uniqify(l):
    # see: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order/29898968#29898968
    reduce(lambda r, v: v in r[1] and r or (r[0].append(v) or r[1].add(v)) or r, l, ([], set()))[0]

def flatten_list(l):
    all_items = [item if len(item) > 1 else sublist for sublist in l for item in sublist]
    return uniqify(all_items)

def unicode_available():
    return locale.getdefaultlocale()[1] == 'UTF-8'

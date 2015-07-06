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


def flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x

def unicode_available():
    return locale.getdefaultlocale()[1] == 'UTF-8'

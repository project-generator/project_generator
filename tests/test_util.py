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
from project_generator.util import *

def test_unicode_detection():
    try:
        print(u'\U0001F648')
    except UnicodeEncodeError:
        assert not unicode_available()
    else:
        assert unicode_available()

def test_flatten():
    l1 = [['aa', 'bb', ['cc', 'dd', 'ee'], ['ee', 'ff'], 'gg']]

    assert list(flatten(l1)) == ['aa', 'bb', 'cc', 'dd', 'ee', 'ee', 'ff', 'gg']
    assert uniqify(flatten(l1)) == ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg']

def test_uniqify():
    l1 = ['a', 'b', 'b', 'c', 'b', 'd', 'c', 'e', 'f', 'a']
    assert uniqify(l1) == ['a', 'b', 'c', 'd', 'e', 'f']

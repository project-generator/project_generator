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

from unittest import TestCase

from project_generator.commands.update import update

class TestProject(TestCase):

    """test things related to the Project class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update(self):
        # force update. This assumes that repository is alive and that travis has
        # internet connection
        update(True)

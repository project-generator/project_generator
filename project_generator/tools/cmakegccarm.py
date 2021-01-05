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

import os
import copy
import logging
import subprocess

from os.path import join, normpath, dirname, exists
from .tool import Tool, Exporter
from .cmake import CMake
from .gccarm import MakefileGccArm
from ..util import SOURCE_KEYS

logger = logging.getLogger('progen.tools.cmake_gcc_arm')

class CMakeGccArm(CMake):
    def __init__(self, workspace, env_settings):
        super(CMakeGccArm, self).__init__(workspace, env_settings)
        self.logging = logging
        self.workspace['preprocess_linker_file'] = True

    @staticmethod
    def get_toolnames():
        return ['cmake_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'gcc_arm'

    def get_template(self):
        return 'cmakelist_gccarm.tmpl'

    def get_workspace_template(self):
        return 'cmakelist_gccarm_workspace.tmpl'

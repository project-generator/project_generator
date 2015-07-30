# Copyright 2014-2015 0xc0170
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

from .tools.iar import IAREmbeddedWorkbench
from .tools.uvision import Uvision
from .tools.coide import Coide
from .tools.eclipse import EclipseGnuARM
from .tools.gccarm import MakefileGccArm
from .tools.sublimetext import SublimeTextMakeGccARM
from .tools.gdb import GDB
from .tools.gdb import ARMNoneEABIGDB

class ToolsSupported:
    """ Represents all tools available """

    # Tools dictionary
    # Each of this tool needs to support at least:
    # - get_toolchain (toolchain is a list of toolchains supported by tool)
    # - get_toolname (returns name string)
    # - export_project (basic functionality to be covered by a tool)
    TOOLS_DICT = {
        'iar_arm':              IAREmbeddedWorkbench,
        'uvision':              Uvision,
        'coide':                Coide,
        'make_gcc_arm':         MakefileGccArm,
        'eclipse_make_gcc_arm': EclipseGnuARM,
        'sublime_make_gcc_arm': SublimeTextMakeGccARM,
        'gdb':                  GDB,
        'arm_none_eabi_gdb':    ARMNoneEABIGDB,
    }

    TOOLCHAINS = list(set([v.get_toolchain() for k, v in TOOLS_DICT.items() if v.get_toolchain() is not None]))
    TOOLS = list(set([v for k, v in TOOLS_DICT.items() if v is not None]))

    def get_tool(self, tool):
        try:
            return self.TOOLS_DICT[tool]
        except KeyError:
            return None

    def get_toolnames(self, tool):
        try:
            return self.TOOLS_DICT[tool].get_toolnames()
        except KeyError:
            return None

    def get_toolchain(self, tool):
        try:
            return self.TOOLS_DICT[tool].get_toolchain()
        except KeyError:
            return None

    def get_supported(self):
        return self.TOOLS_DICT.keys()


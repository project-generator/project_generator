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
from .tools.uvision import Uvision, Uvision5
from .tools.coide import Coide
from .tools.eclipse import EclipseGnuARM
from .tools.gccarm import MakefileGccArm
from .tools.makearmcc import MakefileArmcc
from .tools.sublimetext import SublimeTextMakeGccARM
from .tools.gdb import GDB, ARMNoneEABIGDB, JLinkGDB
from .tools.cmake import CMakeGccArm
from .tools.visual_studio import VisualStudioMakeGCCARM, VisualStudioGDB

class ToolsSupported:
    """ Represents all tools available """

    # Default tools - aliases
    TOOLS_ALIAS = {
        'uvision':       'uvision4',
        'iar':           'iar_arm',
        'make_gcc':      'make_gcc_arm',
        'gcc_arm':       'make_gcc_arm',
        'eclipse':       'eclipse_make_gcc_arm',
        'sublime':       'sublime_make_gcc_arm',
        'sublime_text':  'sublime_make_gcc_arm',
        'visual_studio': 'visual_studio_make_gcc_arm',
        'cmake':         'cmake_gcc_arm',
     }

    # Tools dictionary
    # Each of this tool needs to support at least:
    # - get_toolchain (toolchain is a list of toolchains supported by tool)
    # - get_toolname (returns name string)
    # - export_project (basic functionality to be covered by a tool)
    TOOLS_DICT = {
        'iar_arm':              IAREmbeddedWorkbench,
        'uvision4':             Uvision,
        'uvision5':             Uvision5,
        'coide':                Coide,
        'make_gcc_arm':         MakefileGccArm,
        'make_armcc':           MakefileArmcc,
        'eclipse_make_gcc_arm': EclipseGnuARM,
        'sublime_make_gcc_arm': SublimeTextMakeGccARM,
        'gdb':                  GDB,
        'arm_none_eabi_gdb':    ARMNoneEABIGDB,
        'jlink_gdb':            JLinkGDB,
        'cmake_gcc_arm':        CMakeGccArm,
        'visual_studio_gdb':    VisualStudioGDB,
        'visual_studio_make_gcc_arm': VisualStudioMakeGCCARM,
    }

    TOOLCHAINS = list(set([v.get_toolchain() for k, v in TOOLS_DICT.items() if v.get_toolchain() is not None]))
    TOOLS = list(set([v for k, v in TOOLS_DICT.items() if v is not None]))

    def _get_tool_name(self, tool):
        if tool in self.TOOLS_ALIAS.keys():
            tool = self.TOOLS_ALIAS[tool]
        return tool

    def get_tool(self, tool):
        name = self._get_tool_name(tool)
        try:
            return self.TOOLS_DICT[name]
        except KeyError:
            return None

    def get_toolnames(self, tool):
        name = self._get_tool_name(tool)
        try:
            return self.TOOLS_DICT[name].get_toolnames()
        except KeyError:
            return None

    def get_toolchain(self, tool):
        name = self._get_tool_name(tool)
        try:
            return self.TOOLS_DICT[name].get_toolchain()
        except KeyError:
            return None

    def get_supported(self):
        return list(self.TOOLS_DICT.keys()) + list(self.TOOLS_ALIAS.keys())


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

from project_generator.tools_supported import ToolsSupported
from project_generator.tools.uvision import Uvision
from project_generator.tools.iar import IAREmbeddedWorkbench
from project_generator.tools.coide import Coide
from project_generator.tools.gccarm import MakefileGccArm
from project_generator.tools.makearmcc import MakefileArmcc
from project_generator.tools.eclipse import EclipseGnuARM
from project_generator.tools.sublimetext import SublimeTextMakeGccARM
from project_generator.tools.cmakegccarm import CMakeGccArm
from project_generator.tools.visual_studio import VisualStudioMakeGCCARM, VisualStudioGDB


class TestProject(TestCase):

    """test things related to the ToolsSupported class"""

    def setUp(self):
        self.tools = ToolsSupported()

    def tearDown(self):
        pass

    def test_tools(self):
        tool = self.tools.get_tool('uvision4')
        assert tool == Uvision
        tool = self.tools.get_tool('iar')
        assert tool == IAREmbeddedWorkbench
        tool = self.tools.get_tool('coide')
        assert tool == Coide
        tool = self.tools.get_tool('gcc_arm')
        assert tool == MakefileGccArm
        tool = self.tools.get_tool('make_armcc')
        assert tool == MakefileArmcc
        tool = self.tools.get_tool('eclipse_make_gcc_arm')
        assert tool == EclipseGnuARM
        tool = self.tools.get_tool('sublime_make_gcc_arm')
        assert tool == SublimeTextMakeGccARM
        tool = self.tools.get_tool('cmake_gcc_arm')
        assert tool == CMakeGccArm
        tool = self.tools.get_tool('visual_studio_make_gcc_arm')
        assert tool == VisualStudioMakeGCCARM

    def test_alias(self):
        tool = self.tools.get_tool('uvision')
        assert tool == Uvision
        tool = self.tools.get_tool('iar')
        assert tool == IAREmbeddedWorkbench
        tool = self.tools.get_tool('make_gcc')
        assert tool == MakefileGccArm
        tool = self.tools.get_tool('gcc_arm')
        assert tool == MakefileGccArm
        tool = self.tools.get_tool('sublime_text')
        assert tool == SublimeTextMakeGccARM
        tool = self.tools.get_tool('sublime')
        assert tool == SublimeTextMakeGccARM
        tool = self.tools.get_tool('visual_studio')
        assert tool == VisualStudioMakeGCCARM
        tool = self.tools.get_tool('eclipse')
        assert tool == EclipseGnuARM

    def test_toolnames(self):
        names = self.tools.get_toolnames('uvision')
        assert 'uvision' == names[0]
        toolchain = self.tools.get_toolchain('uvision')
        assert 'uvision' == toolchain

        names = self.tools.get_toolnames('uvision4')
        assert 'uvision' == names[0]
        toolchain = self.tools.get_toolchain('uvision4')
        assert 'uvision' == toolchain

        names = self.tools.get_toolnames('iar_arm')
        assert 'iar_arm' == names[0]
        toolchain = self.tools.get_toolchain('iar_arm')
        assert 'iar' == toolchain

        names = self.tools.get_toolnames('coide')
        assert 'coide' == names[0]
        toolchain = self.tools.get_toolchain('coide')
        assert 'gcc_arm' == toolchain

        names = self.tools.get_toolnames('make_gcc_arm')
        assert 'make_gcc_arm' == names[0]
        toolchain = self.tools.get_toolchain('make_gcc_arm')
        assert 'gcc_arm' == toolchain

        names = self.tools.get_toolnames('eclipse_make_gcc_arm')
        assert 'eclipse_make_gcc_arm' == names[0]
        toolchain = self.tools.get_toolchain('eclipse_make_gcc_arm')
        assert 'gcc_arm' == toolchain

        names = self.tools.get_toolnames('sublime_make_gcc_arm')
        assert 'sublime_make_gcc_arm' == names[0]
        toolchain = self.tools.get_toolchain('sublime_make_gcc_arm')
        assert 'gcc_arm' == toolchain

        names = self.tools.get_toolnames('cmake_gcc_arm')
        assert 'cmake_gcc_arm' == names[0]
        toolchain = self.tools.get_toolchain('cmake_gcc_arm')
        assert 'gcc_arm' == toolchain

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

from project_generator.project import Project, ProjectTemplate
from project_generator.settings import ProjectSettings

class TestProjectTemplate:

    def setup(self):
        # set common and tool specific options
        self.project_dic = {}
        self.project_dic['common'] = ProjectTemplate().get_project_template()
        self.project_dic['tool_specific'] = ProjectTemplate().get_project_template()

    def testDefaultCtor(self):
        assert self.project_dic['common']['name'] == 'Default'
        assert self.project_dic['common']['output_type'] == 'exe'
        assert self.project_dic['common']['debugger'] == None
        assert self.project_dic['common']['build_dir'] == 'build'

    def testProjectCommon(self):
        self.project_dic['common']['name'] = 'test_name'
        self.project_dic['common']['build_dir'] = 'test_build'
        self.project_dic['common']['debugger'] = 'test_debugger'
        self.project_dic['common']['export_dir'] = 'test_export'
        self.project_dic['common']['target'] = 'test_target'
        self.project_dic['common']['output_type'] = 'test_lib'
        self.project_dic['common']['tools_supported'] = ['test_tool']
        self.project_dic['common']['includes'] = ['test_export']
        self.project_dic['common']['linker_file'] = 'test_linker'
        self.project_dic['common']['macros'] = ['test_macro']
        self.project_dic['common']['misc'] = {'test_misc': 'test_value'}
        self.project_dic['common']['template'] = 'test_template'

        project = Project('test_name', [self.project_dic], ProjectSettings())

        assert project.project['common']['name'] == 'test_name'
        assert project.project['common']['build_dir'] == 'test_build'
        assert project.project['common']['debugger'] == 'test_debugger'
        assert project.project['common']['export_dir'] == 'test_export'
        assert project.project['common']['target'] == 'test_target'
        assert project.project['common']['output_type'] == 'test_lib'
        assert project.project['common']['tools_supported'][0] == 'test_tool'
        assert self.project_dic['common']['includes'][0] == 'test_export'
        assert self.project_dic['common']['linker_file'] == 'test_linker'
        assert self.project_dic['common']['macros'][0] == 'test_macro'
        assert self.project_dic['common']['misc']['test_misc'] == 'test_value'
        assert self.project_dic['common']['template'] == 'test_template'

    def testProjectToolSpecificNonvalid(self):
        project = Project('test_name', [self.project_dic], ProjectSettings())

        # non valid - no tool specified, tool specific should be empty array
        assert not project.project['tool_specific']

    def testProjectToolspecificValid(self):
        self.project_dic['tool_specific'] = {}
        self.project_dic['tool_specific']['uvision'] = {}
        self.project_dic['tool_specific']['uvision']['build_dir'] = 'test_build'
        self.project_dic['tool_specific']['uvision']['debugger'] = 'test_debugger'
        self.project_dic['tool_specific']['uvision']['export_dir'] = 'test_export'
        self.project_dic['tool_specific']['uvision']['target'] = 'test_target'
        self.project_dic['tool_specific']['uvision']['output_type'] = 'test_lib'
        self.project_dic['tool_specific']['uvision']['tools_supported'] = ['test_tool']
        self.project_dic['tool_specific']['uvision']['includes'] = ['test_export']
        self.project_dic['tool_specific']['uvision']['linker_file'] = 'test_linker'
        self.project_dic['tool_specific']['uvision']['macros'] = ['test_macro']
        self.project_dic['tool_specific']['uvision']['misc'] = {'test_misc': 'test_value'}
        self.project_dic['tool_specific']['uvision']['template'] = 'test_template'

        project = Project('test_name', [self.project_dic], ProjectSettings())

        # Tool specific should be same as common, we can override anything there
        assert project.project['tool_specific']['uvision']['name'] == 'test_name'
        assert project.project['tool_specific']['uvision']['build_dir'] == 'test_build'
        assert project.project['tool_specific']['uvision']['debugger'] == 'test_debugger'
        assert project.project['tool_specific']['uvision']['export_dir'] == 'test_export'
        assert project.project['tool_specific']['uvision']['target'] == 'test_target'
        assert project.project['tool_specific']['uvision']['output_type'] == 'test_lib'
        assert project.project['tool_specific']['uvision']['tools_supported'][0] == 'test_tool'
        assert self.project_dic['tool_specific']['uvision']['includes'][0] == 'test_export'
        assert self.project_dic['tool_specific']['uvision']['linker_file'] == 'test_linker'
        assert self.project_dic['tool_specific']['uvision']['macros'][0] == 'test_macro'
        assert self.project_dic['tool_specific']['uvision']['misc']['test_misc'] == 'test_value'
        assert self.project_dic['tool_specific']['uvision']['template'] == 'test_template'

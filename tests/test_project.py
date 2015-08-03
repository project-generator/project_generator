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
import shutil

import yaml
from unittest import TestCase

from project_generator.project import Project
from project_generator.generate import Generator

project_1_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['target1'],
        'core': ['core1'],
        'tools_supported': ['iar_arm', 'uvision', 'coide', 'unknown'],
        'output_type': ['exe'],
        'debugger': ['debugger_1'],
        'linker_file': ['test_workspace/linker.ld'],
    }
}

projects_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml']
    },
    'settings' : {
        'definitions_dir': ['./notpg/path/somewhere'],
        'export_dir': ['projects/{workspace}/{tool}_{target}/{project_name}']
    }
}

def test_output_directory_formatting():
    path, depth = Project._generate_output_dir('aaa/bbb/cccc/ddd/eee/ffff/ggg')

    assert depth == 7
    assert os.path.normpath(path) == os.path.normpath('../../../../../../../')

class TestProject(TestCase):

    """test things related to the Project class"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_yaml, default_flow_style=False))

        # now that Project and PgenWorkspace accepts dictionaries, we dont need to
        # create yaml files!
        self.project = next(Generator(projects_yaml).generate('project_1'))

        # create 3 files to test project
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header1.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/linker.ld'), 'wt') as f:
            pass

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('projects', ignore_errors=True)

    def test_project_yaml(self):
        # test using yaml files and compare basic data
        project = next(Generator('test_workspace/projects.yaml').generate('project_1'))
        assert self.project.name == project.name
        # fix this one, they should be equal
        #self.assertDictEqual(self.project.project, project.project)

    def test_name(self):
        assert self.project.name == 'project_1'

    def test_copy(self):
        # test copy method which shojld copy all files to generated project dir by default
        self.project._fill_export_dict('uvision')
        self.project._copy_sources_to_generated_destination()

    def test_set_output_dir_path(self):
        self.project._fill_export_dict('uvision')
        assert self.project.project['export']['output_dir']['path'] == os.path.join('projects', 'uvision_target1','project_1')

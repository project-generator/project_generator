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
from project_generator.settings import ProjectSettings
from project_generator.util import merge_recursive

project_1_yaml = {
    'common': {
        'sources': { 'sources_dict' : ['test_workspace/main.cpp']
        },
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2', None],
        'target': ['target1'],
        'core': ['core1'],
        'tools_supported': ['iar_arm', 'uvision', 'coide', 'unknown'],
        'output_type': ['exe'],
        'debugger': ['debugger_1'],
        'linker_file': ['test_workspace/linker.ld'],
    }
}

project_2_yaml = {
    'common': {
        'sources': { 
            'sources_dict' : ['test_workspace/file2.cpp'],
            'sources_dict2' : ['test_workspace/file3.cpp']
        },
        'includes':  {
            'include_dict' : ['test_workspace/header2.h'],
            'include_dict2' : ['test_workspace/header3.h']
        },
        'macros': ['MACRO2_1', 'MACRO2_2'],
    }
}

projects_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml', 'test_workspace/project_2.yaml']
    },
    'settings' : {
        'export_dir': ['projects/{tool}_{target}/{project_name}']
    }
}

def test_output_directory_formatting():
    path, depth = Project._generate_output_dir(ProjectSettings(),'aaa/bbb/cccc/ddd/eee/ffff/ggg')

    assert depth == 7
    assert os.path.normpath(path) == os.path.normpath('../../../../../../../')

class TestProjectYAML(TestCase):

    """test things related to the Project class"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        with open(os.path.join(os.getcwd(), 'test_workspace/project_2.yaml'), 'wt') as f:
            f.write(yaml.dump(project_2_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(projects_yaml, default_flow_style=False))

        # now that Project and PgenWorkspace accepts dictionaries, we dont need to
        # create yaml files!
        self.project = next(Generator(projects_yaml).generate('project_1'))

        # create 3 files to test project
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/file2.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/file3.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header1.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header2.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header3.h'), 'wt') as f:
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

    def test_project_attributes(self):
        self.project._fill_export_dict('uvision')
        assert set(self.project.project['export']['macros'] + [None]) & set(project_1_yaml['common']['macros'] + project_2_yaml['common']['macros']) 
        assert set(self.project.project['export']['include_files'].keys()) & set(['default'] + list(project_2_yaml['common']['includes'].keys()))

        # no c or asm files, empty dics
        assert self.project.project['export']['source_files_c'] == dict()
        assert self.project.project['export']['source_files_s'] == dict()
        # source groups should be equal
        assert self.project.project['export']['source_files_cpp'].keys() == merge_recursive(project_1_yaml['common']['sources'], project_2_yaml['common']['sources']).keys()

    def test_copy(self):
        # test copy method which should copy all files to generated project dir by default
        self.project._fill_export_dict('uvision', True)
        self.project._copy_sources_to_generated_destination()

    def test_set_output_dir_path(self):
        self.project._fill_export_dict('uvision')
        assert self.project.project['export']['output_dir']['path'] == os.path.join('projects', 'uvision_target1','project_1')

class TestProjectDict(TestCase):

    """test things related to the Project class, using python dicts"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')

        # create 3 files to test project
        with open(os.path.join(os.getcwd(), 'test_workspace/main.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/file2.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/file3.cpp'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header1.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header2.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/header3.h'), 'wt') as f:
            pass
        with open(os.path.join(os.getcwd(), 'test_workspace/linker.ld'), 'wt') as f:
            pass

        self.project = Project('project_1', [project_1_yaml, project_2_yaml], ProjectSettings())

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)

    def test_name(self):
        assert self.project.name == 'project_1'

    def test_project_attributes(self):
        self.project._fill_export_dict('uvision')
        assert set(self.project.project['export']['macros'] + [None]) & set(project_1_yaml['common']['macros'] + project_2_yaml['common']['macros']) 
        assert set(self.project.project['export']['include_files'].keys()) & set(['default'] + list(project_2_yaml['common']['includes'].keys()))

        # no c or asm files, empty dics
        assert self.project.project['export']['source_files_c'] == dict()
        assert self.project.project['export']['source_files_s'] == dict()
        # source groups should be equal
        assert self.project.project['export']['source_files_cpp'].keys() == merge_recursive(project_1_yaml['common']['sources'], project_2_yaml['common']['sources']).keys()

    def test_sources_groups(self):
        self.project._fill_export_dict('uvision')
        source_groups = []
        for dic in self.project.project['export']['sources']:
            for k, v in dic.items():
                source_groups.append(k)
        assert source_groups == list(project_1_yaml['common']['sources'].keys()) + list(project_2_yaml['common']['sources'].keys())

    def test_copy(self):
        # test copy method which should copy all files to generated project dir by default
        self.project._fill_export_dict('uvision', True)
        self.project._copy_sources_to_generated_destination()

    def test_set_output_dir_path(self):
        self.project._fill_export_dict('uvision')
        # we use default one in this class
        assert self.project.project['export']['output_dir']['path'] == os.path.join('generated_projects', 'uvision_project_1')

# Copyright 2014 0xc0170
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
from setuptools import setup, find_packages

setup(
    name='project_generator',
    version='0.4',
    description='Project generators for various embedded tools (IDE). IAR, uVision, Makefile and many more in the roadmap!',
    author='Martin Kojtal, Matthew Else',
    author_email='c0170@rocketmail.com, matthewelse1997@gmail.com',
    keywords="c cpp project generator embedded",
    url="https://github.com/0xc0170/project_generator",

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "project_generator=project_generator.export:main",
        ]
    },

    install_requires=[
        'pyyaml'
    ],
    include_package_data = True,
)

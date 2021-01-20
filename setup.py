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

import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

setup(
    name='project_generator',
    version='0.11.0',
    description='Project generators for various embedded tools (IDE). IAR, uVision, Makefile and many more in the roadmap!',
    author='Martin Kojtal',
    author_email='c0170@rocketmail.com',
    keywords="c cpp project generator embedded",
    url="https://github.com/project-generator/project_generator",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: C",
        "Topic :: Software Development"
    ],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyyaml>=5.1,<6.0',
        'Jinja2>2.0<3.0',
        'xmltodict',
        'project_generator_definitions>=0.2.2,<0.3.0',
        ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "project_generator=project_generator.__main__:main",
            "progen=project_generator.__main__:main",
        ]
    },
    include_package_data=True,
    zip_safe=True,
    options={
        'bdist_wheel': {
            'universal': True,
        },
    },
)

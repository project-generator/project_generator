# Project generator
[![Build Status](https://travis-ci.org/project-generator/project_generator.svg?branch=master)](https://travis-ci.org/project-generator/project_generator)

Source code is often times simple but building it is difficult when more than one person is involved.
Developers like what they like: IDE, compiler, debugger and really all we want is to produce an executable.
Sharing project files decoding XML in commit messages because someone was debugging and changed compile options before commiting distracts from doing what you want to do; develop software.

This project allows you to define a project in text using YAML files and generate IDE project files
based on the rules defined in records. No one should ever commit IDE specific project file to a repository again!

All open sourced - licensed under Apache v2.0 license.

### Current Status

The project is in alpha phase. Check issues for the ongoing tasks or todo tasks.

Project generator currently generaters projects for the following tools (IDE, Makefile, etc..):

 - uVision4 and uVision5
 - IAR
 - Makefile (GCC ARM)
 - Cmake (GCC ARM)
 - CoIDE (GCC ARM)
 - Eclipse (Makefile with GCC ARM)
 - Sublime (Makefile with GCC ARM)
 - Visual studio (Makefile with GCC ARM)

We appreciate any help and you are more than welcome to send a pull request or create a new issue in this repository.
The plan is to support as many IDE as possible , same applies for targets/MCU.

### How to use it

There are two options, how to use it. Either you download [pypi package](https://pypi.python.org/pypi/project_generator) or you can clone this repository to your project directory.

##### Using package
Once installed, test if project_generator is recognized:

```
progen --version
```

This should print the current installed version. You can use progen or project_generator as a command.

##### Using directly the repository
In case of using this repository directly, be aware, the project generator is using relative paths. To solve this, invoke run.py with arguments as you would if using the package. Something like: python run.py --version. This helps with debugging the package.

##### Getting started

An example how to use progen [here](https://github.com/project-generator/project_generator_mbed_examples).

###### Docs
To get familiar with it, read our wiki. Good start is [Getting started guide (wiki)](https://github.com/project-generator/project_generator/wiki/Getting_started). There are other sections which describe the each blocks of the project generator.

##### Add a new target/mcu

We use project generator definitions, which is a separate python module and contains mcu/target database plus parser to obtain those from tools projects, visit github page [here](https://github.com/project-generator/project_generator_definitions/).

Dependencies for Project generator
-------------------------
* Python 2.7
 * [pyYAML](https://github.com/yaml/pyyaml)
 * [Setuptools](https://pypi.python.org/pypi/distribute)
 * [Jinja2](https://pypi.python.org/pypi/Jinja2)
 * [xmltodict](https://pypi.python.org/pypi/xmltodict)
 * [project generator definitions](https://pypi.python.org/pypi/project_generator_definitions)

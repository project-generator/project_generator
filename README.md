# Project generator

Source code is often times simple but building it is difficult when more than one person is involved.
Developers like what they like: IDE, compiler, debugger and really all we want is to produce an executable.
Sharing project files decoding XML in commit messages because someone was debugging and changed compile options before commiting distracts from doing what you want to do; develop software.

This project allows you to define a project in text using YAML files and generate IDE project files
based on the rules defined in records. No one should ever commit IDE specific project file to a repository again!

All open sourced - licensed under Apache v2.0 license.

### Current Status

The project is in alpha phase. Check issues for the ongoing tasks or todo tasks.

Project generator currently generaters projects for the following IDE/toolchains:

 - uVision
 - Makefile (GCC ARM)
 - IAR

We appreciate any help and you are more than welcome to send a pull request or create a new issue in this repository. Want to see your IDE here? Create a new issue with a request.

### How to use it

In your project directory create a tools folder and clone this repo. There are examples in c0170 github, so check them out!

To get familiar with it, read our wiki. Good start is [Getting started guide (wiki)](https://github.com/0xc0170/project_generator/wiki/Getting_started)

Dependencies for Project generator
-------------------------
* Python 2.7
 * [pyYAML](https://github.com/yaml/pyyaml)
 * [Setuptools](https://pypi.python.org/pypi/distribute)
 * [Jinja2](https://pypi.python.org/pypi/Jinja2)

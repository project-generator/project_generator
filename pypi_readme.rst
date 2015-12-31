.. image:: https://travis-ci.org/project-generator/project_generator.svg

This project allows you to define a project in text using YAML files and generate IDE project files
based on the rules defined in records. No one should ever commit IDE specific project file to a repository again!

All open sourced - licensed under Apache v2.0 license.

Current Status
============

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

Getting started
============

An example how to use progen [here](https://github.com/project-generator/project_generator_mbed_examples).

To get familiar with it, read our wiki. Good start is [Getting started guide (wiki)](https://github.com/project-generator/project_generator/wiki/Getting_started). There are other sections which describe the each blocks of the project generator.

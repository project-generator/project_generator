Project generator
=========================
Source code is often times simple but building it is difficult when more than one person is involved.
Developers like what they like: IDE, compiler, debugger and really all we want is to produce an executable.
Sharing project files decoding XML in commit messages because someone was debugging and changed compile options
before commiting distracts from doing what you want to do; develop software.

Anyways, this project allows you to define a project in text using yaml files and then generate IDE project files
based on the rules defined in the project file. No one should ever commit a IDE specific project file to a repository again!

Current Status
-------------
Still adding options and moving things around so this is quite a bit unstable as radical changes can be added or
removed at any time as we come across gotchas.

[ToDo](https://docs.google.com/spreadsheets/d/1M413v3yVtD3YhSptgTLz715ctUT0Wa_--Df9jTVVDLQ/edit?usp=sharing)

Supported:
- uVision IDE project

How to use it
------------
In your project directory create a tools folder and clone this repo

<pre>
project/tools>git clone https://github.com/0xc0170/project_generator.git

+---project
    +---source
    +---tools
        +---exporters
</pre>

Notes
-----
**All scripts should be run from the projects tools directory**
<pre>
project/tools>python exporters/export.py -f exporters/records/projects.yaml
</pre>

Dependencies for exporters
-------------------------
* Python 2.7
 * [pyYAML](https://github.com/yaml/pyyaml)
 * [Setuptools](https://pypi.python.org/pypi/distribute)
 * [Jinja2](https://pypi.python.org/pypi/Jinja2)

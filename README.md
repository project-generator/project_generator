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

[ToDo (spreadsheet)](https://docs.google.com/spreadsheets/d/1M413v3yVtD3YhSptgTLz715ctUT0Wa_--Df9jTVVDLQ/edit?usp=sharing)

IDE currently supported:

 - uVision
 - GCC ARM (Makefile)

We appreciate any help and you are more than welcome to send a pull request or create a new issue in this repository.

How to use it
------------
In your project directory create a tools folder and clone this repo. There are examples in c0170 github, so check them out!

<pre>
project/tools>git clone https://github.com/0xc0170/project_generator.git

+---project
    +---source
    +---tools
        +---project_generator # this repository
        +---records           # records - project specific yaml files
</pre>

#### Command line options

<pre>
--file / -f  - project file
--project/-p - project (to generate only specific project. If not defined, it generates all projects withing a file).
--ide/-i     - ide (if not defined, uvision is set)
</pre>


Records
-----------

The Records are designated to describe a project in packages.

#### Project file
An example how a project file with only one project (k20dx128_bootloader) can look like. It consists of components.

<pre>
projects:
    k20dx128_bootloader:
        - tools/records/common/bootloader_usb.yaml
        - tools/records/common/rtos.yaml
        - tools/records/common/common_src.yaml
        - tools/records/common/drag_n_drop.yaml
        - tools/records/common/bootloader_common.yaml
        - tools/records/mcu/k20dx128/io_hal_k20dx128.yaml
        - tools/records/mcu/k20dx128/flash_write_k20dx128.yaml
        - tools/records/projects/bootloader/k20dx128_bootloader.yaml
</pre>

####  Component file

For more detailed syntax information of a component file, have a look at yaml parser script file (defines dictionaries and how data are processed from components).

<pre>
bootloader_k20:
    name:
        - k20dx128_bootloader
    mcu:
        - k20dx128
    core:
        - cortex-m4
    include_paths:
        - source/bootloader/hal/freescale/mk20dx128
        - source/common/cmsis_core/freescale/mk20dx128
        - source/common/rtos
    source_paths:
        - source/bootloader/hal/freescale/mk20dx128
        - source/common/cmsis_core/freescale/mk20dx128
        - source/common/rtos
    source_files:
        - source/common/cmsis_core/freescale/mk20dx128/system_MK20D5.c
        - source/common/rtos/HAL_CM3.c
        - source/bootloader/hal/freescale/mk20dx128/flash_erase_read_write.c
    macros:
        - TARGET_MK20DX
        - K20DX128
        - CPU_MK20DX128VFM5
        - __RTX
        - BOOTLOADER
    tool_specific:
        uvision:
            include_paths:
                - source/common/cmsis_core/freescale/mk20dx128/arm
            source_paths:
                - source/common/cmsis_core/freescale/mk20dx128/arm
            source_files:
                - source/common/cmsis_core/freescale/mk20dx128/arm/startup_MK20D5.s
            linker_file:
                - source/common/cmsis_core/freescale/mk20dx128/arm/MK20D5_0x0000.sct
            misc:
                c_settings:
                    - one_elf_per_function
                    - O3
                c_command_line:
                    - --debug
                    - --c99
                    - -g
</pre>

Notes
-----
**All scripts should be run from the projects tools directory**
<pre>
project/tools>python project_generator/export.py -f records/projects.yaml
</pre>

Dependencies for project_generator
-------------------------
* Python 2.7
 * [pyYAML](https://github.com/yaml/pyyaml)
 * [Setuptools](https://pypi.python.org/pypi/distribute)
 * [Jinja2](https://pypi.python.org/pypi/Jinja2)

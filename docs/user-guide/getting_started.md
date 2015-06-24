# Project Structure

Here's an example directory tree for a typical Project Generator project, which you can see [on Github](https://github.com/project-generator/project_generator_mbed_examples). 

**Throughout all of the yaml files in your project, always use relative paths specified from the root of your project.**

```
├── LICENSE
├── README.md
├── examples
│   └── blinky
│       └── main.cpp
├── mbed
├── projects.yaml
└── records
    ├── mbed
    │   ├── common.yaml
    │   ├── disco_f407vg_cmsis.yaml
    │   ├── disco_f407vg_target.yaml
    │   ├── frdm_k64f_target.yaml
    │   ├── freescale_ksdk.yaml
    │   ├── k20_cmsis.yaml
    │   ├── k20_target.yaml
    │   ├── k64f_cmsis.yaml
    │   ├── k64f_target.yaml
    │   ├── lpc1768_cmsis.yaml
    │   ├── lpc1768_target.yaml
    │   └── proj_set.yaml
    └── projects
        ├── disco_f407vg_blinky.yaml
        ├── frdm_k64f_blinky.yaml
        ├── k20_blinky.yaml
        └── lpc1768_blinky.yaml
```

## Projects File

The Projects YAML file (by default projects.yaml) defines one or more projects for a repository, as well as environment settings for toolchains. Each project consists of a list of files which each define a module, which together build the project. By default, Project Generator includes sane defaults, which can be changed to fit your project.

The following example specifies one project, called `my_project`, which contains one module, called `main`, as well as specifying settings which allow Project Generator to use the iar toolchain.

```yaml
projects:
    my_project:
        - main.yaml

settings:
    tool:
        iar:
            path:
                - path/to/iar
```

For more details about settings you can specify in projects.yaml, see the projects.yaml documentation **(TODO)**.

## Project Records

Project record files can be stored anywhere within project directory, however the most common place to put them is within a subdirectory called `records`. These specify attributes for a project or module, such as files and compiler options.

Since each project can have more than one record, you can create yaml files for different targets, which can be reused between projects.



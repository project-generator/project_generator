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

The Projects YAML file (by default projects.yaml) defines one or more projects for a repository, as well as toolchain environment settings. Each project consists of a list of record files, which together build the project. 

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

For more details about settings you can specify in projects.yaml, see the [projects.yaml documentation](/reference/projects).

### Advanced Use

Over time you may find that your projects.yaml files become cluttered, with many repeated record files. In order to simplify things, you can specifiy modules, which are groups of records which can be included by a project.

```yaml
modules:
	common: &common_module
		- records/common/common.yaml
		- records/common/other.yaml

projects:
	project_1:
		- *common_modules
		- records/project_1/a.yaml
		- records/project_1/b.yaml
```

## Project Records

Project record files can be stored anywhere within project directory, however the most common place to put them is within a subdirectory called `records`. These specify attributes for a project or module, such as files and compiler options.

Since each project can have more than one record, you can create yaml files for different targets, which can be reused between projects.



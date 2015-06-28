# projects.yaml Reference

## Projects

A YAML dictionary consisting of one or projects, which each contain a list of YAML files, specified from the root directory of the project.

## Modules

Modules allow you to specify a group of records which can easily be reused between projects.

## Settings

### Toolchain Paths

projects.yaml can be used to specify workspace-wide paths for toolchains. These can be specified as follows:

```yaml
settings:
    tool:
        iar:
            path: path/to/iar
        uvision:
            path: path/to/uvision
        gcc:
            path: path/to/gcc
```

If these toolchains are already in your PATH, Project Generator will try to access uVision by calling `UV4`, IAR by calling `IARBUILD` and ARM GCC by looking in `ARM_GCC_PATH`


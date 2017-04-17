# projects.yaml Reference

## Projects

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


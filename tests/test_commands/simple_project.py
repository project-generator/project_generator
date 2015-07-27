project_1_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['mbed-lpc1768'],
        'core': ['core1'],
        'tools_supported': ['iar_arm', 'uvision', 'coide', 'unknown'],
        'output_type': ['exe'],
        'debugger': ['j-link'],
        'linker_file': ['test_workspace/linker.ld'],
    }
}

project_2_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['mbed-lpc1768'],
        'core': ['core2'],
        'tools_supported': ['iar_arm', 'uvision', 'coide', 'unknown'],
        'output_type': ['exe'],
        'debugger': ['j-link'],
        'linker_file': ['test_workspace/linker.ld'],
    }
}

projects_yaml = {
    'projects': {
        'project_workspace': {
            'project_1': ['test_workspace/project_1.yaml'],
        },
        'project_2': ['test_workspace/project_2.yaml'],
    
    }
}

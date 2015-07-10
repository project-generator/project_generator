project_1_yaml = {
    'common': {
        'sources': ['sources/main.cpp'],
        'includes': ['includes/header1.h'],
        'target': ['mbed-lpc1768'],
        'linker_file': ['linker_script'],
    }
}

projects_1_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml']
    },
}

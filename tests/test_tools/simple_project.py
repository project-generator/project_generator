project_1_yaml = {
    'common': {
        'sources': ['sources/main.cpp'],
        'includes': ['includes/header1.h'],
        'target': ['mbed-lpc1768'],
        'linker_file': ['linker_script'],
    },
    'tool_specific': {
        'iar': {
            'macros': ['IAR_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test'],
                'asm_flags': ['asm_flag_test'],
                'cxx_flags': ['cxx_flag_test'],
                'ld_flags': ['ld_flag_test'],
            }
        },
        'uvision': {
            'macros': ['UVISION_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test'],
                'asm_flags': ['asm_flag_test'],
                'cxx_flags': ['cxx_flag_test'],
                'ld_flags': ['ld_flag_test'],
            }
        },
        'coide': {
            'macros': ['COIDE_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test'],
                'asm_flags': ['asm_flag_test'],
                'cxx_flags': ['cxx_flag_test'],
                'ld_flags': ['ld_flag_test'],
            }
        },
        'gcc_arm': {
            'macros': ['GCC_ARM_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test'],
                'asm_flags': ['asm_flag_test'],
                'cxx_flags': ['cxx_flag_test'],
                'ld_flags': ['ld_flag_test'],
            }
        }
    }
}

projects_1_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml']
    },
}

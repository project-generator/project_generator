project_1_yaml = {
    'common': {
        'sources': {'sources': ['sources/main.cpp']},
        'includes': {'includes': ['includes/header1.h']},
        'target': ['mbed-lpc1768'],
        'linker_file': ['linker_script'],
        'debugger': ['j-link'],
        'macros': ['macro_test','macro_test2'],
    },
    'tool_specific': {
        'iar': {
            'macros': ['IAR_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test', 'c_flag_test2'],
                'asm_flags': ['asm_flag_test', 'asm_flag_test2'],
                'cxx_flags': ['cxx_flag_test', 'cxx_flag_test2'],
                'ld_flags': ['ld_flag_test', 'ld_flag_test2'],
            },
        },
        'uvision': {
            'macros': ['UVISION_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test', 'c_flag_test2'],
                'asm_flags': ['asm_flag_test', 'asm_flag_test2'],
                'cxx_flags': ['cxx_flag_test', 'cxx_flag_test'],
                'ld_flags': ['ld_flag_test', 'ld_flag_test'],
            }
        },
        'coide': {
            'macros': ['COIDE_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test', 'c_flag_test2'],
                'asm_flags': ['asm_flag_test', 'asm_flag_test2'],
                'cxx_flags': ['cxx_flag_test', 'cxx_flag_test2'],
                'ld_flags': ['ld_flag_test', 'ld_flag_test2'],
            }
        },
        'gcc_arm': {
            'macros': ['GCC_ARM_TEST_MACRO'],
            'misc': {
                'c_flags': ['c_flag_test', 'c_flag_test2'],
                'asm_flags': ['asm_flag_test', 'asm_flag_test2'],
                'cxx_flags': ['cxx_flag_test', 'cxx_flag_test2'],
                'ld_flags': ['ld_flag_test', 'ld_flag_test2'],
                'common_flags': ['common_flag_test', 'common_flag_test2'],
                'standard_libraries': ['standard_libraries_test'],
            },
        }
    }
}

project_2_yaml = {
    'common': {
        'sources': ['sources/main.cpp'],
        'includes': ['includes/header1.h'],
        'target': ['mbed-lpc1768'],
        'debugger': ['j-link'],
        'macros': ['macro_test','macro_test2'],
    },
    'tool_specific': {
        'coide': {
            'template': [ 'template_test'],
            'linker_file': ['linker_script'],
        },
        'iar': {
            'template': [ 'template_test'],
            'linker_file': ['linker_script'],
        },
        'uvision': {
            'template': [ 'template_test'],
            'linker_file': ['linker_script'],
        }
    }
}

projects_1_yaml = {
    'projects': {
        'project_1' : ['test_workspace/project_1.yaml'],
        'project_2' : ['test_workspace/project_2.yaml']
    },
}


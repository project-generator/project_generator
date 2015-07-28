#!/usr/bin/env python
# Copyright 2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import copy

from .tool import Tool, Builder, Exporter

class gdb_definitions():

    SUPPORTED_MCUS = {
        'K64F': {
        }
    }


class GDB(Tool, Exporter, Builder):
    def __init__(self, workspace, env_settings):
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['gdb']

    @staticmethod
    def get_toolchain():
        return None

    def export_project(self):
        # for native debugging, no command files are necessary
        return None, []

    def supports_target(self, target):
        # !!! TODO: should be yes for native targets
        return False

    @staticmethod
    def is_supported_by_default(target):
        # does not require additional information
        return True


class ARMNoneEABIGDB(GDB):
    SUPPORTED = gdb_definitions.SUPPORTED_MCUS

    generated_project = {
        'path': '',
        'files': {
            'startupfile': '',
        }
    }

    def __init__(self, workspace, env_settings):
        super(ARMNoneEABIGDB, self).__init__(workspace, env_settings)

    @staticmethod
    def get_toolnames():
        return ['gdb']

    @staticmethod
    def get_toolchain():
        return None

    def export_project(self):
        generated_projects = copy.deepcopy(self.generated_project)
        expanded_dic = self.workspace.copy()
        
        # !!! TODO: store and read settings from gdb_definitions
        expanded_dic['gdb_server_port'] = 3333

        project_path, startupfile = self.gen_file_jinja(
            'gdb.tmpl', expanded_dic, '%s.gdbstartup' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        generated_projects['path'] = project_path
        generated_projects['files']['startupfile'] = startupfile
        return generated_projects

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['startupfile']]}


    def supports_target(self, target):
        return target in self.SUPPORTED

    @staticmethod
    def is_supported_by_default(target):
        # does not require additional information
        return True

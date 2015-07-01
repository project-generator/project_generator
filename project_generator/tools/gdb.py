#!/usr/bin/env python
# Copyright 2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from .exporter import Exporter

class gdb_definitions():

    SUPPORTED_MCUS = {
        'K64F': {
        }
    }


class GDB(Exporter):
    def export_project(self, data, env_settings):
        # for native debugging, no command files are necessary
        return None, []

    def supports_target(self, target):
        # !!! TODO: should be yes for native targets
        return False

    def is_supported_by_default(self, target):
        # does not require additional information
        return True


class ARMNoneEABIGDB(GDB):
    SUPPORTED = gdb_definitions.SUPPORTED_MCUS

    def export_project(self, data, env_settings):
        expanded_dic = data.copy()
        
        # !!! TODO: store and read settings from gdb_definitions
        expanded_dic['gdb_server_port'] = 3333

        project_path, startupfile = self.gen_file_jinja(
            'gdb.tmpl', expanded_dic, '%s.gdbstartup' % data['name'], expanded_dic['output_dir']['path'])
        return project_path, [startupfile]

    def supports_target(self, target):
        return target in self.SUPPORTED

    def is_supported_by_default(self, target):
        # does not require additional information
        return True

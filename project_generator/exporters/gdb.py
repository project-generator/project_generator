#!/usr/bin/env python
# Copyright 2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from . import gdb_definitions
from .exporter import Exporter

class GDBExporter(Exporter):
    def generate(self, data, env_settings):
        # for native debugging, no command files are necessary
        return None, []

    def supports_target(self, target):
        # !!! TODO: should be yes for native targets
        return False


class ARMNoneEABIGDBExporter(GDBExporter):
    SUPPORTED = gdb_definitions.SUPPORTED_MCUS

    def generate(self, data, env_settings):
        expanded_dic = data.copy()
        
        # !!! TODO: store and read settings from gdb_definitions 
        expanded_dic['gdb_server_port'] = 3333

        project_path, startupfile = self.gen_file(
            'gdb.tmpl', expanded_dic, '%s.gdbstartup' % data['name'], "gdb", data['project_dir']['path'], data['project_dir']['name']
        )
        return project_path, [startupfile]

    def supports_target(self, target):
        return target in self.SUPPORTED


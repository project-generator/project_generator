# Copyright 2014 0xc0170
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import logging
import xmltodict

from os import getcwd
from os.path import join, normpath
from .exporter import Exporter
from ..targets import Targets
from ..tools.iar import IAREmbeddedWorkbench

class IAREmbeddedWorkbenchARMExporter(Exporter, IAREmbeddedWorkbench):

    def __init__(self):
        IAREmbeddedWorkbench.__init__(self)

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for IAR, and run generator """
        expanded_dic = data.copy()

        # TODO 0xc0170: fix misc , its a list with a dictionary
        if 'misc' in expanded_dic and bool(expanded_dic['misc'][0]):
            print ("Using deprecated misc options for iar. Please use template project files.")

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        # generic tool template specified or project
        if expanded_dic['template']:
            # TODO 0xc0170: template list !
            project_file = join(getcwd(), expanded_dic['template'][0])
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        elif 'iar' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), env_settings.templates['iar'][0])
            ewp_dic = xmltodict.parse(file(project_file), dict_constructor=dict)
        else:
            ewp_dic = self.definitions.ewp_file

        # TODO 0xc0170: add ewd file parsing and support
        ewd_dic = self.definitions.ewd_file
        eww_dic = self.definitions.eww_file

        # replace all None with empty strings ''
        self._clean_xmldict_ewp(ewp_dic)
        #self._clean_xmldict_ewd(ewd_dic)

        # set ARM toolchain and project name\
        self._ewp_set_toolchain(ewp_dic, 'ARM')
        self._ewp_set_name(ewp_dic, expanded_dic['name'])

        # set eww
        self._eww_set_path(eww_dic, expanded_dic['name'])

        # set common things we have for IAR
        self._ewp_general_set(ewp_dic, expanded_dic)
        self._ewp_iccarm_set(ewp_dic, expanded_dic)
        self._ewp_aarm_set(ewp_dic, expanded_dic)
        self._ewp_ilink_set(ewp_dic, expanded_dic)
        self._ewp_files_set(ewp_dic, expanded_dic)

        # set target only if defined, otherwise use from template/default one
        if expanded_dic['target']:
            # get target definition (target + mcu)
            target = Targets(env_settings.get_env_settings('definitions'))
            if not target.is_supported(expanded_dic['target'].lower(), 'iar'):
                raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
            mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'iar')
            if not mcu_def_dic:
                 raise RuntimeError(
                    "Mcu definitions were not found for %s. Please add them to https://github.com/project-generator/project_generator_definitions" % expanded_dic['target'].lower())
            self.normalize_mcu_def(mcu_def_dic)
            logging.debug("Mcu definitions: %s" % mcu_def_dic)
            self._ewp_set_target(ewp_dic, mcu_def_dic)

        # overwrite debugger only if defined in the project file, otherwise use either default or from template
        if expanded_dic['debugger']:
            try:
                debugger = self.definitions.debuggers[expanded_dic['debugger']]
                self._ewd_set_debugger(ewd_dic, ewp_dic, debugger)
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        ewp_xml = xmltodict.unparse(ewp_dic, pretty=True)
        project_path, ewp = self.gen_file_raw(ewp_xml, '%s.ewp' % expanded_dic['name'], expanded_dic['output_dir']['path'])

        eww_xml = xmltodict.unparse(eww_dic, pretty=True)
        project_path, eww = self.gen_file_raw(eww_xml, '%s.eww' % expanded_dic['name'], expanded_dic['output_dir']['path'])

        ewd_xml = xmltodict.unparse(ewd_dic, pretty=True)
        project_path, ewd = self.gen_file_raw(ewd_xml, '%s.ewd' % expanded_dic['name'], expanded_dic['output_dir']['path'])
        return project_path, [ewp, eww, ewd]

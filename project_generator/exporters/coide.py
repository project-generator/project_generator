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

from os.path import basename, join, relpath, normpath
from os import getcwd
import xmltodict

from .exporter import Exporter
from .coide_definitions import CoIDEdefinitions
from ..targets import Targets

class CoideExporter(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s',
                        'source_files_cpp', 'source_files_obj', 'source_files_lib']
    file_types = {'cpp': 1, 'c': 1, 's': 1, 'obj': 1, 'lib': 1}

    def __init__(self):
        self.definitions = CoIDEdefinitions()

    def expand_data(self, old_data, new_data, attribute, group, rel_path):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                extension = file.split(".")[-1]
                new_file = {'@path': rel_path + normpath(file), '@name': basename(
                    file), '@type': str(self.file_types[extension])}
                new_data['groups'][group].append(new_file)

    def get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                if dic:
                    for k, v in dic.items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k, v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group, rel_path)

    def normalize_mcu_def(self, mcu_def):
        for k,v in mcu_def['Device'].items():
            mcu_def['Device'][k] = v[0]
        for k,v in mcu_def['DebugOption'].items():
            mcu_def['DebugOption'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IROM1'].items():
            mcu_def['MemoryAreas']['IROM1'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IROM2'].items():
            mcu_def['MemoryAreas']['IROM2'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IRAM1'].items():
            mcu_def['MemoryAreas']['IRAM1'][k] = v[0]
        for k,v in mcu_def['MemoryAreas']['IRAM2'].items():
            mcu_def['MemoryAreas']['IRAM2'][k] = v[0]

    def fix_paths(self, data, rel_path):
        data['includes'] = [join(rel_path, normpath(path)) for path in data['includes']]

        for k in data['source_files_lib'][0].keys():
            data['source_files_lib'][0][k] = [join(rel_path,normpath(path)) for path in data['source_files_lib'][0][k]]

        for k in data['source_files_obj'][0].keys():
            data['source_files_obj'][0][k] = [join(rel_path,normpath(path)) for path in data['source_files_obj'][0][k]]
        if data['linker_file']:
            data['linker_file'] = join(rel_path, normpath(data['linker_file']))

    def _coide_option_dictionarize(self, option, key, coide_settings):
        dictionarized = {}
        for option in coide_settings[option]:
            dictionarized[option[key]] = {}
            dictionarized[option[key]].update(option)
        return dictionarized

    def _coproj_set_files(self, coproj_dic, project_dic):
        coproj_dic['Project']['Files'] = {}
        coproj_dic['Project']['Files']['File'] = []
        for group,files in project_dic['groups'].items():
            # TODO 0xc0170: this might not be needed
            # coproj_dic['Project']['Files']['File'].append({u'@name': group, u'@path': '', u'@type' : '2' })
            for file in files:
                if group:
                    file['@name'] = group + '/' + file['@name']
                coproj_dic['Project']['Files']['File'].append(file)

    def _coproj_set_macros(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'] = []
        for macro in project_dic['macros']:
            coproj_dic['Project']['Target']['BuildOption']['Compile']['DefinedSymbols']['Define'].append({'@name': macro})

    def _coproj_set_includepaths(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Compile']['Includepaths']['Includepath'] = []
        for include in project_dic['includes']:
            coproj_dic['Project']['Target']['BuildOption']['Compile']['Includepaths']['Includepath'].append({'@path': include})

    def _coproj_set_linker(self, coproj_dic, project_dic):
        coproj_dic['Project']['Target']['BuildOption']['Link']['LocateLinkFile']['@path'] = project_dic['linker_file']

    def generate(self, data, env_settings):
        """ Processes groups and misc options specific for CoIDE, and run generator """
        expanded_dic = data.copy()

        # TODO 0xc0170: fix misc , its a list with a dictionary
        if 'misc' in expanded_dic and bool(expanded_dic['misc'][0]):
            print "Using deprecated misc options for coide. Please use template project files."

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic, expanded_dic['output_dir']['rel_path'])
        self.fix_paths(expanded_dic, expanded_dic['output_dir']['rel_path'])

        # generic tool template specified or project
        if expanded_dic['template']:
            project_file = join(getcwd(), expanded_dic['template'][0])
            coproj_dic = xmltodict.parse(file(project_file))
        elif 'coide' in env_settings.templates.keys():
            # template overrides what is set in the yaml files
            # TODO 0xc0170: extension check/expansion
            project_file = join(getcwd(), env_settings.templates['coide'][0])
            coproj_dic = xmltodict.parse(file(project_file))
        else:
            # setting values from the yaml files
            coproj_dic = self.definitions.coproj_file

        # set name and target
        coproj_dic['Project']['@name'] = expanded_dic['name']
        coproj_dic['Project']['Target']['@name'] = expanded_dic['name']
        # library/exe
        coproj_dic['Project']['Target']['BuildOption']['Output']['Option'][0]['@value'] = 0 if expanded_dic['output_type'] == 'exe' else 1

        # Fill in pgen data to the coproj_dic
        self._coproj_set_files(coproj_dic, expanded_dic)
        self._coproj_set_macros(coproj_dic, expanded_dic)
        self._coproj_set_includepaths(coproj_dic, expanded_dic)
        self._coproj_set_linker(coproj_dic, expanded_dic)

        target = Targets(env_settings.get_env_settings('definitions'))
        if not target.is_supported(expanded_dic['target'].lower(), 'coide'):
            raise RuntimeError("Target %s is not supported." % expanded_dic['target'].lower())
        mcu_def_dic = target.get_tool_def(expanded_dic['target'].lower(), 'coide')
        if not mcu_def_dic:
             raise RuntimeError(
                "Mcu definitions were not found for %s. Please add them to https://github.com/0xc0170/project_generator_definitions"
                % expanded_dic['target'].lower())
        self.normalize_mcu_def(mcu_def_dic)
        logging.debug("Mcu definitions: %s" % mcu_def_dic)
        # correct attributes from definition, as yaml does not allowe multiple keys (=dict), we need to
        # do this magic.
        for k,v in mcu_def_dic['Device'].items():
            del mcu_def_dic['Device'][k]
            mcu_def_dic['Device']['@' + k] = str(v)
        memory_areas = []
        for k,v in mcu_def_dic['MemoryAreas'].items():
             for k,att in v.items():
                 del v[k]
                 v['@' + k] = str(att)
             memory_areas.append(v)

        coproj_dic['Project']['Target']['Device'].update(mcu_def_dic['Device'])
        # TODO 0xc0170: fix debug options
        # coproj_dic['Project']['Target']['DebugOption'].update(mcu_def_dic['DebugOption'])
        coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'] = memory_areas

        # get debugger definitions
        if expanded_dic['debugger']:
            try:
                # find debugger definitions in the list of options
                index = 0
                for option in coproj_dic['Project']['Target']['DebugOption']['Option']:
                    for k,v in option.items():
                        if option['@name'] == 'org.coocox.codebugger.gdbjtag.core.adapter':
                            found = index
                index = index + 1

                coproj_dic['Project']['Target']['DebugOption']['Option'][found]['@value'] = self.definitions.debuggers[expanded_dic['debugger']]['Target']['DebugOption']['org.coocox.codebugger.gdbjtag.core.adapter']
            except KeyError:
                raise RuntimeError("Debugger %s is not supported" % expanded_dic['debugger'])

        # Project file
        # somehow this xml is not compatible with coide, coide v2.0 changing few things, lets use jinja
        # for now, more testing to get xml output right. Jinja template follows the xml dictionary,which is
        # what we want anyway.
        # coproj_xml = xmltodict.unparse(coproj_dic, pretty=True)
        project_path, projfile = self.gen_file_jinja(
            'coide.coproj.tmpl', coproj_dic, '%s.coproj' % data['name'], expanded_dic['output_dir']['path'])
        return project_path, [projfile]

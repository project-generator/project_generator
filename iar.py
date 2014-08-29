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
from export_generator import Exporter
from iar_mcu_definitions import get_mcu_definition

class IAR(Exporter):
    source_files_dic = ['source_files_c', 'source_files_s', 'source_files_cpp', 'source_files_obj', 'source_files_lib']
    core_dic = {
        "cortex-m0" : 34,
        "cortex-m0+" : 35,
        "cortex-m3" : 38,
        "cortex-m4" : 39,
        "cortex-m4f" : 40,
    }

    iar_settings = {
        'Variant' : {
            'state' : 0,
        },
        'GEndianMode' : {
            'state' : 0,
        },
        'Input variant' : {
            'version' : 0,
            'state' : 0,
        },
        'Output variant' : {
            'state' : 0,
        },
        'GOutputBinary' : {
            'state' : 0,
        },
        'FPU' : {
            'version' : 2,
            'state' : 0,
        },
        'GRuntimeLibSelect' : {
            'version' : 0,
            'state' : 0,
        },
        'GRuntimeLibSelectSlave' : {
            'version' : 0,
            'state' : 0,
        },
        'GeneralEnableMisra' : {
            'state' : 0,
        },
        'GeneralMisraVerbose' : {
            'state' : 0,
        },
        'OGChipSelectEditMenu' : {
            'state' : 0,
        },
        'GenLowLevelInterface' : {
            'state' : 0,
        },
        'GEndianModeBE' : {
            'state' : 0,
        },
        'OGBufferedTerminalOutput' : {
            'state' : 0,
        },
        'GenStdoutInterface' : {
            'state' : 0,
        },
        'GeneralMisraVer' : {
            'state' : 0,
        },
        'GFPUCoreSlave' : {
            'state' : 0,
        },
        'GBECoreSlave' : {
            'state' : 0,
        },
        'OGUseCmsis' : {
            'state' : 0,
        },
        'OGUseCmsisDspLib' : {
            'state' : 0,
        },
        'CCPreprocFile' : {
            'state' : 0,
        },
        'CCPreprocComments' : {
            'state' : 0,
        },
        'CCPreprocLine' : {
            'state' : 0,
        },
        'CCListCFile' : {
            'state' : 0,
        },
        'CCListCMnemonics' : {
            'state' : 0,
        },
        'CCListCMessages' : {
            'state' : 0,
        },
        'CCListAssFile' : {
            'state' : 0,
        },
        'CCListAssSource' : {
            'state' : 0,
        },
        'CCEnableRemarks' : {
            'state' : [],
        },
        'CCDiagRemark' : {
            'state' : 0,
        },
        'CCDiagWarning' : {
            'state' : 0,
        },
        'CCDiagError' : {
            'state' : 0,
        },
        'CCObjPrefix' : {
            'state' : 0,
        },
        'CCAllowList' : {
            'version' : 1,
            'state' : 1111111,
        },
        'CCDebugInfo' : {
            'state' : 1,
        },
        'IEndianMode' : {
            'state' : 1,
        },
        'IProcessor' : {
            'state' : 1,
        },
        'IExtraOptionsCheck' : {
            'state' : 0,
        },
        'IExtraOptions' : {
            'state' : 0,
        },
        'CCLangConformance' : {
            'state' : 0,
        },
        'CCSignedPlainChar' : {
            'state' : 1,
        },
        'CCRequirePrototypes' : {
            'state' : 0,
        },
        'CCMultibyteSupport' : {
            'state' : 0,
        },
        'CCDiagWarnAreErr' : {
            'state' : 0,
        },
        'IFpuProcessor' : {
            'state' : 0,
        },
        'OutputFile' : {
            'state' : '',
        },
        'CCLibConfigHeader' : {
            'state' : 0,
        },
        'PreInclude' : {
            'state' : 0,
        },
        'CompilerMisraOverride' : {
            'state' : 0,
        },
        'CCStdIncCheck' : {
            'state' : 0,
        },
        'CCCodeSection' : {
            'state' : '.text',
        },
        'IInterwork2' : {
            'state' : 0,
        },
        'IProcessorMode2' : {
            'state' : 0,
        },
        'IInterwork2' : {
            'state' : 0,
        },
        'CCOptStrategy' : {
            'version' : 0,
            'state' : 0,
        },
        'CCOptLevelSlave' : {
            'state' : 0,
        },
        'CompilerMisraRules98' : {
            'version' : 0,
            'state' : 0,
        },
        'CompilerMisraRules04' : {
            'version': 0,
            'state' : 0,
        },
        'CCPosIndRopi' : {
            'state' : 0,
        },
        'IccLang' : {
            'state' : 0,
        },
        'CCPosIndRwpi' : {
            'state' : 0,
        },
        'IccCDialect' : {
            'state' : 1,
        },
        'IccAllowVLA' : {
            'state' : 0,
        },
        'IccCppDialect' : {
            'state' : 0,
        },
        'IccExceptions' : {
            'state' : 0,
        },
        'IccRTTI' : {
            'state' : 0,
        },
        'IccStaticDestr' : {
            'state' : 1,
        },
        'IccCppInlineSemantics' : {
            'state' : 0,
        },
        'IccCmsis' : {
            'state' : 1,
        },
        'IccFloatSemantics' : {
            'state' : 0,
        },
        'AObjPrefix' : {
            'state' : 0,
        },
        'AEndian' : {
            'state' : 0,
        },
        'ACaseSensitivity' : {
            'state' : 0,
        },
        'MacroChars' : {
            'state' : 0,
        },
        'AWarnEnable' : {
            'state' : 0,
        },
        'AWarnWhat' : {
            'state' : 0,
        },
        'AWarnOne' : {
            'state' : 0,
        },
        'AWarnRange1' : {
            'state' : 0,
        },
        'AWarnRange2' : {
            'state' : 0,
        },
        'ADebug' : {
            'state' : 0,
        },
        'AltRegisterNames' : {
            'state' : 0,
        },
        'ADefines' : {
            'state' : 0,
        },
        'AList' : {
            'state' : 0,
        },
        'AListHeader' : {
            'state' : 0,
        },
        'AListing' : {
            'state' : 0,
        },
        'Includes' : {
            'state' : 0,
        },
        'MacDefs' : {
            'state' : 0,
        },
        'MacExps' : {
            'state' : 0,
        },
        'MacExec' : {
            'state' : 0,
        },
        'OnlyAssed' : {
            'state' : 0,
        },
        'MultiLine' : {
            'state' : 0,
        },
        'PageLengthCheck' : {
            'state' : 0,
        },
        'PageLength' : {
            'state' : 0,
        },
        'TabSpacing' : {
            'state' : 0,
        },
        'AXRefDefines' : {
            'state' : 0,
        },
        'AXRefInternal' : {
            'state' : 0,
        },
        'AXRefDual' : {
            'state' : 0,
        },
        'AProcessor' : {
            'state' : 0,
        },
        'AFpuProcessor' : {
            'state' : 0,
        },
        'AOutputFile' : {
            'state' : 0,
        },
        'AMultibyteSupport' : {
            'state' : 0,
        },
        'ALimitErrorsCheck' : {
            'state' : 0,
        },
        'ALimitErrorsEdit' : {
            'state' : 0,
        },
        'AIgnoreStdInclude' : {
            'state' : 0,
        },
        'AUserIncludes' : {
            'state' : 0,
        },
        'AExtraOptionsCheckV2' : {
            'state' : 0,
        },
        'AExtraOptionsV2' : {
            'state' : 0,
        },
        'OOCOutputFormat' : {
            'state' : 0,
        },
        'OCOutputOverride' : {
            'state' : 0,
        },
        'OOCCommandLineProducer' : {
            'state' : 0,
        },
        'OOCObjCopyEnable' : {
            'state' : 1,
        },
    }

    def expand_data(self, old_data, new_data, attribute, group):
        """ Groups expansion for Sources. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for file in old_data[old_group]:
            if file:
                new_data['groups'][group].append(file)

    def iterate(self, data, expanded_data):
        """ Iterate through all data, store the result expansion in extended dictionary. """
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        group = 'Sources'
                    else:
                        group = k
                    self.expand_data(dic, expanded_data, attribute, group)

    def get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in self.source_files_dic:
            for dic in data[attribute]:
                for k,v in dic.items():
                    if k == None:
                        k = 'Sources'
                    if k not in groups:
                        groups.append(k)
        return groups

    def find_target_core(self, data):
        """ Sets Target core. """
        for k,v in self.core_dic.items():
            if k == data['core']:
                return v
        return core_dic['cortex-m0'] #def cortex-m0 if not defined otherwise

    def parse_specific_options(self, data):
        """ Parse all IAR specific setttings. """
        data['iar_settings'].update(self.iar_settings) # set specific options to default values
        for dic in data['misc']:
            #for k,v in dic.items():
            self.set_specific_settings(dic, data)

    def set_specific_settings(self, value_list, data):
        for k,v in value_list.items():
            if v[0] == 'enable':
                v[0] = 1
            elif v[0] == 'disable':
                v[0] = 0
            data['iar_settings'][k]['state'] = v[0]

    def generate(self, data, ide):
        """ Processes groups and misc options specific for IAR, and run generator """
        expanded_dic = data.copy()

        groups = self.get_groups(data)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self.iterate(data, expanded_dic)
        # expanded_dic['target_core'] = self.find_target_core(expanded_dic)
        expanded_dic['iar_settings'] = {}
        self.parse_specific_options(expanded_dic)
        expanded_dic['iar_settings'].update(get_mcu_definition(expanded_dic['mcu']))

        self.gen_file('iar.ewp.tmpl' , expanded_dic, '%s.ewp' % data['name'], ide)
        self.gen_file('iar.eww.tmpl' , expanded_dic, '%s.eww' % data['name'], ide)


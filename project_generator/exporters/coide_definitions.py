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
from collections import OrderedDict

class CoIDEdefinitions():

    coproj_file = OrderedDict([(u'Project', OrderedDict([(u'@version', u'2G - 1.7.5'), (u'@name', u''), (u'Target', OrderedDict([(u'@name', u''), (u'@isCurrent', u'1'), (u'Device', OrderedDict([(u'@manufacturerId', u'7'), (u'@manufacturerName', u'NXP'), (u'@chipId', u'165'), (u'@chipName', u'LPC1768'), (u'@boardId', u''), (u'@boardName', u'')])), (u'BuildOption', OrderedDict([(u'Compile', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OptimizationLevel'), (u'@value', u'4')]), OrderedDict([(u'@name', u'UseFPU'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditCompiler'), (u'@value', u'-fno-common;-fmessage-length=0;-Wall;-fno-strict-aliasing;-fno-rtti;-fno-exceptions;-ffunction-sections;-fdata-sections;-std=gnu++98;')])]), (u'Includepaths', OrderedDict([(u'Includepath', OrderedDict([(u'@path', u'')]))])), (u'DefinedSymbols', OrderedDict([(u'Define', OrderedDict([(u'@name', u'')]))]))])), (u'Link', OrderedDict([(u'@useDefault', u'0'), (u'Option', [OrderedDict([(u'@name', u'DiscardUnusedSection'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinkder'), (u'@value', u'1')]), OrderedDict([(u'@name', u'UseMemoryLayout'), (u'@value', u'0')]), OrderedDict([(u'@name', u'LTO'), (u'@value', u'')]), OrderedDict([(u'@name', u'IsNewStartupCode'), (u'@value', u'')]), OrderedDict([(u'@name', u'Library'), (u'@value', u'Use nano C Library')]), OrderedDict([(u'@name', u'nostartfiles'), (u'@value', u'0')]), OrderedDict([(u'@name', u'UserEditLinker'), (u'@value', u'')]), OrderedDict([(u'@name', u'Printf'), (u'@value', u'1')]), OrderedDict([(u'@name', u'Scanf'), (u'@value', u'1')])]), (u'LinkedLibraries', OrderedDict([(u'Libset', [OrderedDict([(u'@dir', u''), (u'@libs', u'stdc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'supc++')]), OrderedDict([(u'@dir', u''), (u'@libs', u'm')]), OrderedDict([(u'@dir', u''), (u'@libs', u'gcc')]), OrderedDict([(u'@dir', u''), (u'@libs', u'c')]), OrderedDict([(u'@dir', u''), (u'@libs', u'nosys')])])])), (u'MemoryAreas', OrderedDict([(u'@debugInFlashNotRAM', u'1'), (u'Memory', [OrderedDict([(u'@name', u'IROM1'), (u'@type', u'ReadOnly'), (u'@size', u'524288'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM1'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'268435456')]), OrderedDict([(u'@name', u'IROM2'), (u'@type', u'ReadOnly'), (u'@size', u'0'), (u'@startValue', u'0')]), OrderedDict([(u'@name', u'IRAM2'), (u'@type', u'ReadWrite'), (u'@size', u'32768'), (u'@startValue', u'537378816')])])])), (u'LocateLinkFile', OrderedDict([(u'@path', u''), (u'@type', u'0')]))])), (u'Output', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'OutputFileType'), (u'@value', u'0')]), OrderedDict([(u'@name', u'Path'), (u'@value', u'./')]), OrderedDict([(u'@name', u'Name'), (u'@value', u'')]), OrderedDict([(u'@name', u'HEX'), (u'@value', u'1')]), OrderedDict([(u'@name', u'BIN'), (u'@value', u'1')])])])), (u'User', OrderedDict([(u'UserRun', [OrderedDict([(u'@name', u'Run#1'), (u'@type', u'Before'), (u'@checked', u'0'), (u'@value', u'')]), OrderedDict([(u'@name', u'Run#1'), (u'@type', u'After'), (u'@checked', u'0'), (u'@value', u'')])])]))])), (u'DebugOption', OrderedDict([(u'Option', [OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.adapter'), (u'@value', u'J-Link')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.debugMode'), (u'@value', u'SWD')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.clockDiv'), (u'@value', u'1M')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.corerunToMain'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkgdbserver'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.userDefineGDBScript'), (u'@value', u'')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.targetEndianess'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.jlinkResetMode'), (u'@value', u'Type 0: Normal')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.resetMode'), (u'@value', u'SYSRESETREQ')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifSemihost'), (u'@value', u'0')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ifCacheRom'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.ipAddress'), (u'@value', u'127.0.0.1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.portNumber'), (u'@value', u'2009')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.autoDownload'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.verify'), (u'@value', u'1')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.downloadFuction'), (u'@value', u'Erase Effected')]), OrderedDict([(u'@name', u'org.coocox.codebugger.gdbjtag.core.defaultAlgorithm'), (u'@value', u'')])])])), (u'ExcludeFile', None)])), (u'Components', OrderedDict([(u'@path', u'./')])), (u'Files', None)]))])

    debuggers = {
        'cmsis-dap' : {
            'Target': {
                'DebugOption' : {
                    'org.coocox.codebugger.gdbjtag.core.adapter' : 'CMSIS-DAP',
                }
            }
        },
        'j-link' : {
            'Target': {
                'DebugOption' : {
                    'org.coocox.codebugger.gdbjtag.core.adapter' : 'J-Link',
                }
            }
        },
    }

# Copyright 2015 0xc0170
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

import os
import yaml
import logging
import bisect

from .project import FILES_EXTENSIONS

def _determine_tool(linker_ext):
        if "sct" in linker_ext or "lin" in linker_ext:
            return "uvision"
        elif "ld" in linker_ext:
            return "make_gcc_arm"
        elif "icf" in linker_ext:
            return "iar_arm"


def _scan(section, root, directory, extensions, list_files):
        if section == "sources":
            data_dict = {}
        else:
            data_dict = []
        for dirpath, dirnames, files in os.walk(directory):
            for filename in files:
                ext = filename.split('.')[-1]
                relpath = os.path.relpath(dirpath, root)
                if ext in extensions:
                    if section == "sources":
                        p = relpath
                        if list_files:
                            p = os.path.join(p,filename)
                        dir = directory.split(os.path.sep)[-1] if dirpath == directory else dirpath.replace(directory,'').split(os.path.sep)[1]
                        if dir in data_dict and relpath not in data_dict[dir]:
                            bisect.insort(data_dict[dir], p)
                        else:
                            data_dict[dir] = [(p)]
                    elif section == 'includes':
                        dirs = relpath.split(os.path.sep)
                        for i in range(1, len(dirs)+1):
                            data_dict.append(os.path.sep.join(dirs[:i]))
                    else:
                        data_dict.append(os.path.join(relpath, filename))
        if section == "sources":
            return data_dict
        l = list(set(data_dict))
        l.sort()
        return l

def _generate_file(filename,root,directory,data):
        logging.debug('Generating yaml file')
        overwrite = False
        if os.path.isfile(os.path.join(directory, filename)):
            print("Project file " +filename+  " already exists")
            while True:
                answer = raw_input('Should I overwrite it? (Y/n)')
                try:
                    overwrite = answer.lower() in ('y', 'yes')
                    if not overwrite:
                        logging.critical('Unable to save project file')
                        return -1
                    break
                except ValueError:
                    continue
        if overwrite:
            with open(os.path.join(root, filename), 'r+') as f:
                f.write(yaml.dump(data, default_flow_style=False))
        else:
            with open(os.path.join(root, filename), 'w+') as f:
                f.write(yaml.dump(data, default_flow_style=False))
        p = os.popen('attrib +h ' + filename)
        p.close()


def create_yaml(root, directory, project_name, board, files):
        common_section = {
            'linker_file': FILES_EXTENSIONS['linker_file'],
            'sources': FILES_EXTENSIONS['source_files_c'] + FILES_EXTENSIONS['source_files_cpp'] +
                        FILES_EXTENSIONS['source_files_s'] + FILES_EXTENSIONS['source_files_obj'],
            'includes': FILES_EXTENSIONS['includes'],
            'target': [],
        }
        projects_yaml = {
            'projects': {
                project_name: ['project.yaml']
            }
        }

        project_yaml = {
            'common': {},
            'tool_specific': {}
        }

        for section in common_section:
            if len(common_section[section]) > 0:
                project_yaml['common'][section] = _scan(section, root, directory,common_section[section], files)

        project_yaml['common']['target'] = [board]
        tool = _determine_tool(str(project_yaml['common']['linker_file']).split('.')[-1])
        project_yaml['tool_specific'] = {
            tool: {
                'linker_file': project_yaml['common']['linker_file']
            }
        }
        _generate_file("projects.yaml", root, directory, projects_yaml)
        _generate_file("project.yaml", root, directory, project_yaml)
        return 0




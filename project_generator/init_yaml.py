import os
import yaml
from .project import FILES_EXTENSIONS
import logging

def _determine_tool(linker_ext):
        if "sct" in linker_ext or "lin" in linker_ext:
            return "uvision"
        elif "ld" in linker_ext:
            return "make_gcc_arm"
        elif "icf" in linker_ext:
            return "iar_arm"


def _scan(section, root, directory, extensions, is_path):
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
                        dir = directory.split(os.path.sep)[-1] if dirpath == directory else dirpath.replace(directory,'').split(os.path.sep)[1]
                        if dir in data_dict:
                            data_dict[dir].append(os.path.join(relpath, filename))
                        else:
                            data_dict[dir] = [(os.path.join(relpath, filename))]
                    elif section == 'includes':
                        dirs = relpath.split(os.path.sep)
                        for i in range(1, len(dirs)+1):
                            data_dict.append(os.path.sep.join(dirs[:i]))
                    else:
                        data_dict.append(relpath if is_path else os.path.join(relpath, filename))
        if section == "sources":
            return data_dict
        return list(set(data_dict))

def _generate_file(filename,root,directory,data):
        logging.debug('Generating yaml file')
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
        with open(os.path.join(root, filename), 'wt') as f:
            f.write(yaml.dump(data, default_flow_style=False))


def create_yaml(root, directory, project_name, board, list_sources):
        common_section = {
            'linker_file': [False, FILES_EXTENSIONS['linker_file']],
            'sources': [False, FILES_EXTENSIONS['source_files_c'] + FILES_EXTENSIONS['source_files_cpp'] +
                        FILES_EXTENSIONS['source_files_s'] + FILES_EXTENSIONS['source_files_obj'] +
                        FILES_EXTENSIONS['source_files_lib']],
            'includes': [True, FILES_EXTENSIONS['includes']],
            'target': [False, []],
        }
        projects = {
            'projects': {
                project_name: ['project.yaml']
            }
        }

        data = {
            'common': {},
            'tool_specific': {}
        }

        for section in common_section:
            if len(common_section[section][1]) > 0:
                data['common'][section] = _scan(section, root, directory,common_section[section][1],common_section[section][0])

        data['common']['target'] = []
        data['common']['target'].append(board)
        tool = _determine_tool(str(data['common']['linker_file']).split('.')[-1])
        data['tool_specific'] = {
            tool: {
                'linker_file': data['common']['linker_file']
            }
        }
        _generate_file("projects.yaml", root, directory, projects)
        _generate_file("project.yaml", root, directory, data)




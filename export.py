from optparse import OptionParser
import yaml
import logging
import os
from yaml_parser import get_project_files, get_ide, YAML_parser
import sys
from os.path import basename
from ide import export

# TODO:
# GCC support

def run_generator(dic, project, ide):
    project_list = []
    yaml_files = get_project_files(dic, project) # TODO fix list inside list
    if yaml_files:
        for yaml_file in yaml_files:
            try:
                file = open(yaml_file)
            except IOError:
                raise RuntimeError("Cannot open a file: %s" % yaml_file)
            else:
                loaded_yaml = yaml.load(file)
                yaml_parser = YAML_parser()
                project_list.append(yaml_parser.parse_yaml(loaded_yaml, ide))
                file.close()
        yaml_parser_final = YAML_parser()
        process_data = yaml_parser_final.parse_list_yaml(project_list)
    else:
        raise RuntimeError("Project record is empty")

    logging.info("Generating project: %s" % project)
    #ide = get_ide(process_data)
    export(process_data, ide)

def process_all_projects(dic, ide):
    projects = []
    yaml_files = []
    for k,v in dic['projects'].items():
        projects.append(k);

    for project in projects:
        run_generator(dic, project, ide)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Parse Options
    parser = OptionParser()
    parser.add_option("-f", "--file", help="YAML projects file")
    parser.add_option("-p", "--project", help="Project to be generated")
    parser.add_option("-i", "--ide", help="Create project files for toolchain (uvision by default)")

    (options, args) = parser.parse_args()

    if not options.file:
        parser.print_help()
        sys.exit()

    if not options.ide:
        options.ide = "uvision"

    # always run from the root directory
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(script_dir)
    os.chdir('../')

    print "Processing projects file."
    project_file = open(options.file)
    config = yaml.load(project_file)

    if options.project:
        run_generator(config, options.project, options.ide) # one project
    else:
        process_all_projects(config, options.ide) # all projects within project.yaml

    project_file.close()

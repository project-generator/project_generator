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
from optparse import OptionParser
import yaml
import logging
import os
from yaml_parser import get_project_files, YAML_parser
from os.path import join
import sys
from os.path import basename
from ide import export

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

def scrape_dir():
    exts = ['s', 'c', 'cpp', 'h', 'inc', 'sct', 'ld']
    found = {x: [] for x in exts} # lists of found files
    ignore = '.'
    for dirpath, dirnames, files in os.walk(os.getcwd()):
        # Remove directories in ignore
        # directory names must match exactly!
        for idir in ignore:
            if idir in dirnames:
                dirnames.remove(idir)
        # Loop through the file names for the current step
        for name in files:
            # Split the name by '.' & get the last element
            ext = name.lower().rsplit('.', 1)[-1]
            # Save the full name if ext matches
            if ext in exts:
                relpath = dirpath.replace(os.getcwd(), "")
                found[ext].append(os.path.join(relpath, name))
    # The body of our log file
    logbody = ''
    # loop thru results
    for search in found:
        # Concatenate the result from the found dict
        logbody += "<< Results with the extension '%s' >>" % search
        logbody += '\n\n%s\n\n' % '\n'.join(found[search])
    # Write results to the logfile
    source_list_path = os.getcwd() + '\\tools\\exporters\\records\\'
    if not os.path.exists(source_list_path):
        os.makedirs(source_list_path)
    target_path = join(source_list_path, 'scrape.log')
    logging.debug("Generating: %s" % target_path)
    with open(target_path, 'w') as logfile:
        logfile.write('%s' % logbody)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Should be launched from root/tools but all scripts are referenced to root
    root = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    os.chdir(root)
    logging.debug('This should be the project root: %s', os.getcwd())

    # Parse Options
    parser = OptionParser()
    parser.add_option("-f", "--file", help="YAML projects file")
    parser.add_option("-p", "--project", help="Project to be generated")
    parser.add_option("-i", "--ide", help="Create project files for toolchain (uvision by default)")

    (options, args) = parser.parse_args()

    if not options.file:
        # create a list of all files in the dir that we're interested in
        scrape_dir()
        # print help menu
        parser.print_help()
        sys.exit()

    if not options.ide:
        options.ide = "uvision"

    # always run from the root directory
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    # os.chdir(script_dir)
    # os.chdir('../')

    print "Processing projects file."
    project_file = open('tools//' + options.file)
    config = yaml.load(project_file)

    if options.project:
        run_generator(config, options.project, options.ide) # one project
    else:
        process_all_projects(config, options.ide) # all projects within project.yaml

    project_file.close()

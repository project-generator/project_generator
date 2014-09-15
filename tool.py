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
from uvision import UvisionExporter, UvisionBuilder
from gccarm import GccArmExporter, GccArmBuilder
from iar import IARExporter, IARBuilder

EXPORTERS = {
    'uvision': UvisionExporter,
    'gcc_arm': GccArmExporter,
    'iar' : IARExporter,
}

BUILDERS = {
    'uvision': UvisionBuilder,
    'gcc_arm': GccArmBuilder,
    'iar' : IARBuilder,
}

def export(data, tool):
    """ Invokes tool generator. """
    if tool not in EXPORTERS:
        raise RuntimeError("Exporter does not support defined tool.")

    Exporter = EXPORTERS[tool]
    exporter = Exporter()
    exporter.generate(data)

def build(project_path, project_list, tool):
    """ Invokes builder for specificed tool. """
    if tool not in BUILDERS:
        raise RuntimeError("Builder does not support defined tool.")

    Builder = BUILDERS[tool]
    builder = Builder()
    builder.build(project_path, project_list)

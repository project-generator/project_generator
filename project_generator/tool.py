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

# exporters
from .exporters.iar import IARExporter
from .exporters.coide import CoideExporter
from .exporters.gccarm import MakefileGccArmExporter
from .exporters.uvision import UvisionExporter
from .exporters.eclipse import EclipseGnuARMExporter

# builders
from .builders.iar import IARBuilder
from .builders.gccarm import MakefileGccArmBuilder
from .builders.uvision import UvisionBuilder

EXPORTERS = {
    'uvision': UvisionExporter,
    'make_gcc_arm': MakefileGccArmExporter,
    'iar': IARExporter,
    'coide': CoideExporter,
    'eclipse_make_gcc_arm': EclipseGnuARMExporter,
}

BUILDERS = {
    'uvision': UvisionBuilder,
    'make_gcc_arm': MakefileGccArmBuilder,
    'iar': IARBuilder,
}


def export(data, tool, settings):
    """ Invokes tool generator. """
    if tool not in EXPORTERS:
        raise RuntimeError("Exporter does not support defined tool.")

    Exporter = EXPORTERS[tool]
    exporter = Exporter()
    project_path = exporter.generate(data, settings)
    return project_path


def build(projects, project_path, tool, settings, root):
    """ Invokes builder for specificed tool. """
    if tool not in BUILDERS:
        raise RuntimeError("Builder does not support defined tool.")

    Builder = BUILDERS[tool]
    builder = Builder()
    builder.build(projects, project_path, settings, root)

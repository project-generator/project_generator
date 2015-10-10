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

import yaml

from os.path import join
from os import getcwd

# This helps to create a new target. As target consists of mcu, this function
# parses the provided proj_file and creates a valid yaml file, which can be pushed
# to pgen definitions.
def mcu_create(ToolParser, mcu_name, proj_file, tool):
    data = ToolParser(None, None).get_mcu_definition(proj_file)
    data['mcu']['name'] = [mcu_name]
    # we got target, now damp it to root using target.yaml file
    # we can make it better, and ask for definitions repo clone, and add it
    # there, at least to MCU folder
    with open(join(getcwd(), mcu_name + '.yaml'), 'wt') as f:
        f.write(yaml.safe_dump(data, default_flow_style=False, width=200))
    return 0

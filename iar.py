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

class IAR(Exporter):

    def generate(self, data, ide):
        self.gen_file('iar.ewp.tmpl' , data, '%s.ewp' % data['name'])
        self.gen_file('iar.eww.tmpl' , data, '%s.eww' % data['name'])


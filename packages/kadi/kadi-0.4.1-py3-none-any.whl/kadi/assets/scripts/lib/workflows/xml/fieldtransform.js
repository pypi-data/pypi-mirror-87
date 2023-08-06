/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

/* eslint-disable max-len */
export default {
  'program_name': 'fieldtransform',
  'version': '2.5.1 (Release date: 07.12.2018)',
  'description': 'Fieldtransform applys a function to each cell of a field and stores it. The datatype will be determined by the output file extension.',
  'parameters': [
    {
      'param_name': 'arg0',
      'description': 'ScalarData file to process.',
      'required': true,
      'type': 'filein',
    },
    {
      'param_name': 'arg1',
      'description': 'The file which will be created containing f(x)=y',
      'required': true,
      'type': 'fileout',
    },
    {
      'param_name': 'expression',
      'char': 'e',
      'description': 'Expression to calculate, the field coordinate is given by x,y,z and the value itself by the parameter value',
      'required': true,
      'type': 'string',
    },
    {
      'param_name': 'frames',
      'char': 'F',
      'description': 'Working frames',
      'type': 'frame',
    },
    {
      'param_name': 'sort',
      'char': 's',
      'description': 'Sort working frames (ascending)',
      'type': 'flag',
      'relations': '!Fe',
      'default': false,
    },
    {
      'param_name': 'force',
      'char': 'f',
      'description': 'Force replacement of existing files',
      'type': 'flag',
      'default': false,
    },
    {
      'param_name': 'verbose',
      'char': 'v',
      'description': 'Enable the output (stderr) of some (helpful) log messages with log-level <i>, a higher level <i> will create more messages.',
      'type': 'long',
      'default': 1,
    },
    {
      'param_name': 'help',
      'char': 'h',
      'description': 'Print help',
      'type': 'flag',
    },
  ],
};
/* eslint-enable max-len */

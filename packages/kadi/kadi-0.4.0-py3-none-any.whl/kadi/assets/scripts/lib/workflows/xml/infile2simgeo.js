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
  'program_name': 'infile2simgeo',
  'version': '2.5.1 (Release date: 07.12.2018)',
  'description': 'infile2simgeo takes .infile files as input and creates the corresponding .simgeo file.',
  'parameters': [
    {
      'param_name': 'arg0',
      'description': 'The input Infile for SimGeo creation',
      'required': true,
      'type': 'filein',
    },
    {
      'param_name': 'arg1',
      'description': 'The output SimGeo file',
      'required': true,
      'type': 'fileout',
    },
    {
      'param_name': 'dimension',
      'char': 'D',
      'description': 'Generate boundary layers for D dimensional simgeo',
      'type': 'long',
      'interval': '[1,3]',
      'default': 3,
    },
    {
      'param_name': 'force',
      'char': 'f',
      'description': 'Force replacement of existing files',
      'type': 'flag',
      'default': false,
    },
    {
      'param_name': 'noprint',
      'char': 'p',
      'description': 'Do not print the read values',
      'type': 'flag',
      'default': true,
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

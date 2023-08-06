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
  'program_name': 'volume',
  'version': '2.5.1 (Release date: 07.12.2018)',
  'istested': '0',
  'description': 'Calculates the volume of a phase or a grain of that phase.',
  'example': 'e.g.: volume input.phi_alpha.p3s -F 3,5,7,10-15 -c[20,2,300]&#10;this will calculate volume of the grain at coordinate[x=20, y=2, z=300] of the frames 3, 5, 7, 10, 11, 12, 13, 14, 15&#10;e.g.: volume input.p3simgeo -a alpha,beta,gamma&#10;this will calculate the volume for the phases alpha, beta and gamma in the whole simulation domain&#10;e.g.: volume input.phiindex.p3s -o parameter.infile -k nuclei&#10;calculates the volume of all phases in the infile key \'nuclei=(1,0,0,0,0,1)\'&#10;1 determines phases for the volume calculation',
  'parameters': [
    {
      'param_name': 'arg0',
      'description': 'Input datafile',
      'required': true,
      'type': 'filein',
    },
    {
      'param_name': 'coordinate',
      'char': 'c',
      'description': 'Set a coordinate of a point at which volume calculation will begin. Note: pay attention to third phases. Use threshold to limit flooding.',
      'type': 'vector_long',
      'default': '[-1,-1,-1]',
    },
    {
      'param_name': 'periodic',
      'char': 'p',
      'description': 'Let the floodfill algorithm work periodically, to do this give the dimension(s),&#10;e.g.: -p xyz, -p xz, -p x',
      'type': 'periodic',
    },
    {
      'param_name': 'threshold',
      'char': 't',
      'description': 'Threshold, when using coordinates of a grain, specifies the minimum value of the phase-field to be added to the calculated volume.',
      'type': 'real',
      'relations': '!a',
      'interval': '[0.0,#]',
      'default': 0.000000,
    },
    {
      'param_name': 'phases',
      'char': 'a',
      'description': 'Phases to determine the fraction',
      'type': 'tokenlist',
      'relations': '!c!t',
      'separator': ',',
    },
    {
      'param_name': 'invert',
      'char': 'I',
      'description': 'Invert the selection of phases',
      'type': 'flag',
      'relations': 'a',
      'default': false,
    },
    {
      'param_name': 'infile',
      'char': 'i',
      'description': 'The file with a key to determine the phases to be calculated.',
      'type': 'filein',
      'relations': '!ak',
    },
    {
      'param_name': 'infilekey',
      'char': 'k',
      'description': 'Key which contains the phases to calculate the volume. key=(N vector)',
      'type': 'filein',
      'relations': 'i',
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
      'relations': 'F',
      'default': false,
    },
    {
      'param_name': 'plotter',
      'char': 'P',
      'description': 'Generate plot of the table',
      'type': 'plot',
      'default': 'filename=pace3D_graphic_2020-02-04_12:14:52;tfsize=24;lt=linespoints;lfsize=14',
    },
    {
      'param_name': 'verbose',
      'char': 'v',
      'description': 'enable the output (stderr) of some (helpful) log messages with log-level &lt;i&gt;, a higher level &lt;i&gt; will create more messages.',
      'type': 'long',
      'default': 1,
    },
    {
      'param_name': 'help',
      'char': 'h',
      'description': 'print help',
      'type': 'flag',
    },
  ],
};
/* eslint-enable max-len */

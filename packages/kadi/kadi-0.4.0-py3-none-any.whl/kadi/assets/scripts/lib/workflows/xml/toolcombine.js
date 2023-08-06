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
  'program_name': 'toolcombine',
  'version': '2.5.1 (Release date: 07.12.2018)',
  'description': 'Generate a diagram out of a simulation series. It analyses the simulation data and shows the result of the whole series in one plot.',
  'parameters': [
    {
      'param_name': 'tool',
      'char': 't',
      'description': 'Name of tool for execution',
      'required': true,
      'type': 'string',
    },
    {
      'param_name': 'inputfiles',
      'char': 'i',
      'description': 'The input files of the simulation to process',
      'required': true,
      'type': 'tokenlist',
      'separator': ',',
    },
    {
      'param_name': 'outputfiles',
      'char': 'o',
      'description': 'The output files of the simulation to process',
      'type': 'tokenlist',
      'separator': ',',
    },
    {
      'param_name': 'xticslabel',
      'char': 'l',
      'description': 'Seriennamen (Labels for xtics)',
      'type': 'tokenlist',
      'separator': ',',
    },
    {
      'param_name': 'dimname',
      'char': 'd',
      'description': 'Name of 3th dimension',
      'type': 'string',
      'default': '3th_Dim',
    },
    {
      'param_name': 'additional',
      'char': 'a',
      'description': 'Fuer zusaetzliche Bedingungen an das aufzurufende Tool. Man kann eine Bedinung fuer alle Simulationen eingeben, z.B. -a&quot;(-t 200 -f)&quot; oder fuer jede Input-Datei unterschiedliche Bedingungen anwenden: ein Beispiel fuer 4 Input-Dateien -a;(-t 250 -f)#(-t 200 -d 22)#(-t 20 -f)#(-t 200 -f)#(-t 2);',
      'type': 'string',
    },
    {
      'param_name': 'mode',
      'char': 'm',
      'description': 'mode for execution: 1 - all simulations in one graph; 2 - Cut through all results at the position &quot;section&quot; 3 - 3D-diagram of all simulations; 4 - combination of mode 1 and 2',
      'required': true,
      'type': 'long',
      'interval': '[1,4]',
      'default': 0,
    },
    {
      'param_name': 'section',
      'char': 's',
      'description': 'x-Wert, wo der Schnitt gemacht wird',
      'type': 'real',
      'default': 0.000000,
    },
    {
      'param_name': 'accuracy',
      'char': 'g',
      'description': 'accuracy of the results in mode 2:&#10;0 - integer, 1 - floating point',
      'type': 'long',
      'interval': '[0,1]',
      'default': 1,
    },
    {
      'param_name': 'plotter',
      'char': 'P',
      'description': 'settings of the plotter',
      'required': true,
      'type': 'plot',
      'default': 'filename=pace3D_graphic_2020-05-19_13:43:35;tfsize=24;lt=linespoints;lfsize=14',
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

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
  'program_name': 'scalardata2image',
  'version': '2.5.1 (Release date: 07.12.2018)',
  'description': 'This program will create an image of a ScalarData-file.',
  'example': 'e.g.: scalardata2image input.phiindex.p3s -F 1,4,10;create an image for frames 1,4,10 with name input.phiindex.p3s_frame01.bmp, input.phiindex.p3s_frame04.bmp and input.phiindex.p3s_frame10.bmp.',
  'parameters': [
    {
      'param_name': 'arg0',
      'description': 'The scalardata file',
      'required': true,
      'type': 'filein',
    },
    {
      'param_name': 'imagebasename',
      'char': 'i',
      'description': 'Basename for each image (Default is filename of scalardatafile)',
      'type': 'string',
    },
    {
      'param_name': 'boundaryoff',
      'char': 'b',
      'description': 'Do not process boundary. Does only work if no boundingbox is given.',
      'type': 'flag',
      'relations': '!B',
      'default': false,
    },
    {
      'param_name': 'boundingbox',
      'char': 'B',
      'description': 'Set boundingbox [left,bottom],[right,top]. ',
      'type': 'bbox2D',
      'relations': '!b',
      'default': '[-1,-1],[-1,-1]',
    },
    {
      'param_name': 'plane',
      'char': 'p',
      'description': 'Plane for the image.',
      'type': 'string',
      'default': 'xy',
    },
    {
      'param_name': 'scalefactor',
      'char': 's',
      'description': 'scaling factor',
      'type': 'real',
      'interval': '(0.0,#]',
      'default': 1.000000,
    },
    {
      'param_name': 'layer',
      'char': 'l',
      'description': 'layer used for the image',
      'type': 'long',
      'default': 0,
    },
    {
      'param_name': 'threshold',
      'char': 't',
      'description': 'draw boundary, e.g -t 10.0',
      'type': 'real',
      'interval': '(0.0,#]',
      'default': Infinity,
    },
    {
      'param_name': 'colormap',
      'char': 'c',
      'description': 'Colormap file.',
      'type': 'string',
      'relations': '!C',
    },
    {
      'param_name': 'colormode',
      'char': 'C',
      'description': 'Color mode string: BRY, BRG, ContrastlessBRY, OVB, BYR, BYb, BGR, grey.',
      'type': 'string',
      'relations': '!c',
      'default': 'BRY',
    },
    {
      'param_name': 'invert',
      'char': 'I',
      'description': 'Invert colors',
      'type': 'flag',
      'relations': '!c',
      'default': false,
    },
    {
      'param_name': 'min',
      'char': 'm',
      'description': 'minimum value',
      'type': 'real',
      'relations': 'M',
      'default': 340282346638528859811704183484516925440.000000,
    },
    {
      'param_name': 'max',
      'char': 'M',
      'description': 'maximum value',
      'type': 'real',
      'relations': 'm',
      'default': 340282346638528859811704183484516925440.000000,
    },
    {
      'param_name': 'frames',
      'char': 'F',
      'description': 'Give frames to process, default is all frames',
      'type': 'frame',
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

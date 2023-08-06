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
  'program_name': 'ImageJMacro',
  'version': '1.0',
  'description': 'A program to start an ImageJ macro with variables.',
  'example': 'ImageJMacro --variables "var1=0, var2=1" example.ijm',
  'parameters': [
    {
      'param_name': 'macro',
      'char': 'm',
      'description': 'path to the macro file (.ijm)',
      'required': true,
    },
    {
      'param_name': 'variables',
      'char': 'v',
      'description': 'Define variables which will be inserted into the macro. Separate multiple variables by comma. Overwrites variables specified by --varfile. Example: --variables "myint=1,myString=abc" ',
    },
    {
      'param_name': 'varfile',
      'char': 'f',
      'description': 'Load a list of variables from a file',
    },
    {
      'param_name': 'virtual-framebuffer',
      'char': 'x',
      'description': 'Use a virtual framebuffer to hide windows which would be opened by imagej.',
      'type': 'flag',
      'default': true,
    },
  ],
};
/* eslint-enable max-len */

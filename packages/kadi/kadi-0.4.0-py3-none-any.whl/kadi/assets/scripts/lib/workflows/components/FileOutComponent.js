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

import Rete from 'rete';
import Node from 'scripts/lib/workflows/Node.vue';
import CheckboxControl from 'scripts/lib/workflows/controls/CheckboxControl';
import TextControl from 'scripts/lib/workflows/controls/TextControl';

export default class FileOutComponent extends Rete.Component {
  constructor(strSocket, flagSocket, depSocket, anyTypeSocket) {
    super('File Output');
    this.componentType = 'InputOutput';
    this.model_name = 'FileOutput';
    this.data.component = Node;
    this.strSocket = strSocket;
    this.flagSocket = flagSocket;
    this.depSocket = depSocket;
    this.anyTypeSocket = anyTypeSocket;
  }

  builder(node) {
    const inp1 = new Rete.Input('path', 'File path', this.strSocket);
    const inp2 = new Rete.Input('outputFilePath', 'Output file path', this.strSocket);
    const inp3 = new Rete.Input('createShortcut', 'shortcut', this.flagSocket);
    const outdep = new Rete.Output('OutDep', 'Dependents', this.depSocket);
    const inpdep = new Rete.Input('InpDep', 'Dependencies', this.depSocket);
    const stdinp = new Rete.Input('stdinput', 'stdin', this.anyTypeSocket);
    const stdout = new Rete.Output('stdoutput', 'stdout', this.anyTypeSocket);

    inp1.addControl(new TextControl(this.editor, 'path'));
    inp2.addControl(new TextControl(this.editor, 'outputFilePath'));
    inp3.addControl(new CheckboxControl(this.editor, 'createShortcut'));

    node.componentType = this.componentType;
    node.model_name = this.model_name;

    inp1.param = '';
    inp2.param = '';
    inp3.param = '';
    inpdep.param = '';
    stdinp.param = '';

    return node
      .addInput(inpdep)
      .addInput(inp1)
      .addInput(inp2)
      .addInput(inp3)
      .addInput(stdinp)
      .addOutput(outdep)
      .addOutput(stdout);
  }

  worker(node, inputs) {
    for (const control of ['path', 'outputFilePath', 'createShortcut']) {
      if (inputs[control].length > 0) {
        node.data[control] = inputs[control][0];
        this.editor.nodes
          .find((n) => n.id === node.id).inputs.get(control).control
          .setValue(inputs[control][0]);
      }
    }
  }
}

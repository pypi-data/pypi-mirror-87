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
import TextControl from 'scripts/lib/workflows/controls/TextControl';

export default class FileInComponent extends Rete.Component {
  constructor(strSocket, depSocket, anyTypeSocket) {
    super('File Input');
    this.componentType = 'InputOutput';
    this.model_name = 'FileInput';
    this.data.component = Node;
    this.strSocket = strSocket;
    this.depSocket = depSocket;
    this.anyTypeSocket = anyTypeSocket;
  }

  builder(node) {
    const inp1 = new Rete.Input('path', 'File path', this.strSocket);
    const outdep = new Rete.Output('OutDep', 'Dependencies', this.depSocket);
    const inpdep = new Rete.Input('InpDep', 'Dependents', this.depSocket);
    const stdout = new Rete.Output('stdoutput', 'stdout', this.anyTypeSocket);

    node.componentType = this.componentType;
    node.model_name = this.model_name;

    inp1.addControl(new TextControl(this.editor, 'path'));

    inp1.param = '';
    inpdep.param = '';

    return node
      .addInput(inpdep)
      .addInput(inp1)
      .addOutput(outdep)
      .addOutput(stdout);
  }

  worker(node, inputs) {
    if (inputs.path.length > 0) {
      node.data.path = inputs.path[0];
      this.editor.nodes
        .find((n) => n.id === node.id).inputs.get('path').control
        .setValue(inputs.path[0]);
    }
  }
}

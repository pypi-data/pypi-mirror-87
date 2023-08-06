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

export default class UserInputFileComponent extends Rete.Component {
  constructor(strSocket, depSocket) {
    super('UserInput: File');
    this.componentType = 'PromptNode';
    this.model_name = 'UserInputFile';
    this.data.component = Node;
    this.strSocket = strSocket;
    this.depSocket = depSocket;
  }

  builder(node) {
    const inp1 = new Rete.Input('prompt_text', 'Prompt', this.strSocket);
    const inpdep = new Rete.Input('InpDep', 'Dependencies', this.depSocket);
    const outdep = new Rete.Output('OutDep', 'Dependents', this.depSocket);
    const out1 = new Rete.Output('value', 'value', this.strSocket);

    inp1.addControl(new TextControl(this.editor, 'prompt_text'));

    node.componentType = this.componentType;
    node.model_name = this.model_name;

    inp1.param = '';
    inpdep.param = '';

    return node
      .addInput(inpdep)
      .addInput(inp1)
      .addOutput(outdep)
      .addOutput(out1);
  }

  worker(node, inputs) {
    if (inputs.prompt_text.length > 0) {
      node.data.prompt_text = inputs.prompt_text[0];
      this.editor.nodes
        .find((n) => n.id === node.id).inputs.get('prompt_text').control
        .setValue(inputs.prompt_text[0]);
    }
  }
}

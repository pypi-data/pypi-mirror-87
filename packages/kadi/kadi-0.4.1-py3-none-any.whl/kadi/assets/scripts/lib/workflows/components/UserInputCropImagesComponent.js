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

export default class UserInputCropImagesComponent extends Rete.Component {
  constructor(strSocket, depSocket) {
    super('UserInput: Crop Images');
    this.componentType = 'PromptNode';
    this.model_name = 'UserInputCropImages';
    this.data.component = Node;
    this.strSocket = strSocket;
    this.depSocket = depSocket;
  }

  builder(node) {
    const inp1 = new Rete.Input('prompt_text', 'Prompt', this.strSocket);
    const inp2 = new Rete.Input('image_path', 'Image path', this.strSocket);
    const inpdep = new Rete.Input('InpDep', 'Dependencies', this.depSocket);
    const outdep = new Rete.Output('OutDep', 'Dependents', this.depSocket);
    const out1 = new Rete.Output('cropinfo', 'Crop info', this.strSocket);

    node.componentType = this.componentType;
    node.model_name = this.model_name;

    inp1.addControl(new TextControl(this.editor, 'prompt_text'));
    inp2.addControl(new TextControl(this.editor, 'image_path'));

    inp1.param = '';
    inp2.param = '';
    inpdep.param = '';

    return node
      .addInput(inpdep)
      .addInput(inp1)
      .addInput(inp2)
      .addOutput(outdep)
      .addOutput(out1);
  }

  worker(node, inputs) {
    for (const control of ['prompt_text', 'image_path']) {
      if (inputs[control].length > 0) {
        node.data[control] = inputs[control][0];
        this.editor.nodes
          .find((n) => n.id === node.id).inputs.get(control).control
          .setValue(inputs[control][0]);
      }
    }
  }
}

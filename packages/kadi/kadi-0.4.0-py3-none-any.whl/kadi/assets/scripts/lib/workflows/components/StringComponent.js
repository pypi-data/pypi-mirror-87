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
import TextControl from 'scripts/lib/workflows/controls/TextControl';
import Node from 'scripts/lib/workflows/Node.vue';

export default class StringComponent extends Rete.Component {
  constructor(socket) {
    super('String');
    this.componentType = 'SourceNode';
    this.socket = socket;
    this.data.component = Node;
  }

  builder(node) {
    const output = new Rete.Output('str', 'String', this.socket);
    node.componentType = this.componentType;
    node.nodeDescription = 'Source data type String';

    return node.addControl(new TextControl(this.editor, 'str')).addOutput(output);
  }

  // eslint-disable-next-line class-methods-use-this
  worker(node, inputs, outputs) {
    outputs.str = node.data.str;
  }
}

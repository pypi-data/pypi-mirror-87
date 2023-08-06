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
import CheckboxControl from 'scripts/lib/workflows/controls/CheckboxControl';
import TextControl from 'scripts/lib/workflows/controls/TextControl';
import IntControl from 'scripts/lib/workflows/controls/IntControl';
import FloatControl from 'scripts/lib/workflows/controls/FloatControl';
import Node from 'scripts/lib/workflows/Node.vue';
import {Parameter, Relation} from 'scripts/lib/workflows/relations';

export default class CustomComponent extends Rete.Component {
  constructor(tool, numSocket, strSocket, flagSocket, depSocket, anyTypeSocket) {
    super(tool.program_name.toString());
    this.componentType = 'ToolNode';
    this.tool = tool;
    this.version = tool.version;
    this.numSocket = numSocket;
    this.strSocket = strSocket;
    this.flagSocket = flagSocket;
    this.depSocket = depSocket;
    this.anyTypeSocket = anyTypeSocket;
    this.data.component = Node;
    this.showParam = false;
    this.Parameters = [];
    this.Relations = [];
    for (let i = 0; i < this.tool.parameters.length; i++) {
      this.Parameters.push(new Parameter(this.tool.parameters[i]));
    }
    // Relations between parameters
    for (let i = 0; i < this.tool.parameters.length; i++) {
      if (this.Parameters[i].relations) {
        let k = 0; // Index to go through all the chars in relations
        let rel = 1; // Parameter for the type of relation
        do {
          let p2 = null;
          if (this.Parameters[i].relations[k] === '!') {
            rel = 0; // Incompatible
          } else {
            for (let j = 0; j < this.tool.parameters.length; j++) {
              if (j !== i && this.Parameters[j].char === this.Parameters[i].relations[k]) {
                p2 = this.Parameters[j];
              }
            }
            this.Relations.push(new Relation(this.Parameters[i], p2, rel));
            rel = 1; // Required
          }
          k++;
        }
        while (k < this.Parameters[i].relations.length); // It counts the number of characters
      }
    }
  }

  builder(node) {
    const stdout = new Rete.Output('stdoutput', 'stdout', this.anyTypeSocket);
    const outdep = new Rete.Output('OutDep', 'Dependents', this.depSocket);
    const inpdep = new Rete.Input('InpDep', 'Dependencies', this.depSocket);
    const stdinp = new Rete.Input('stdinput', 'stdin', this.anyTypeSocket);

    node.nodeDescription = this.tool.description;
    node.componentType = this.componentType;
    node.version = this.version;
    node.relations = this.Relations;

    node.addInput(inpdep);
    inpdep.param = '';

    for (let i = 0; i < this.tool.parameters.length; i++) {
      if (this.Parameters[i].type === 'long') {
        const inpNum = new Rete.Input(`input${i}`, `int: ${this.Parameters[i].name}`, this.numSocket);
        inpNum.param = this.Parameters[i];
        inpNum.param.portId = `input${i}`;
        inpNum.addControl(new IntControl(this.editor, `input${i}`, this.Parameters[i].defaultVal));
        node.addInput(inpNum);
      } else if (this.Parameters[i].type === 'real') {
        const inpFloat = new Rete.Input(`input${i}`, `float: ${this.Parameters[i].name}`, this.numSocket);
        inpFloat.param = this.Parameters[i];
        inpFloat.param.portId = `input${i}`;
        inpFloat.addControl(new FloatControl(this.editor, `input${i}`, this.Parameters[i].defaultVal));
        node.addInput(inpFloat);
      } else if (this.Parameters[i].type === 'flag') {
        const inpBool = new Rete.Input(`input${i}`, `bool: ${this.Parameters[i].name}`, this.flagSocket);
        inpBool.param = this.Parameters[i];
        inpBool.param.portId = `input${i}`;
        inpBool.addControl(new CheckboxControl(this.editor, `input${i}`, this.Parameters[i].defaultVal));
        node.addInput(inpBool);
      } else {
        const inpStr = new Rete.Input(`input${i}`, `str: ${this.Parameters[i].name}`, this.strSocket);
        inpStr.param = this.Parameters[i];
        inpStr.param.portId = `input${i}`;
        inpStr.addControl(new TextControl(this.editor, `input${i}`, this.Parameters[i].defaultVal));
        node.addInput(inpStr);
      }
    }
    node.addInput(stdinp);
    stdinp.param = '';

    return node
      .addOutput(outdep)
      .addOutput(stdout);
  }

  // eslint-disable-next-line no-unused-vars
  worker(node, inputs, outputs) {
    const iterator = this.editor.nodes.find((n) => n.id === node.id).inputs.keys();
    // Moving data between controls that are connected to each other
    iterator.next(); // The first element is always Dependencies that has no control or data
    for (let i = 0; i < this.tool.parameters.length; i++) {
      const oldPortIn = this.editor.nodes.find((n) => n.id === node.id).inputs.get(iterator.next().value);
      const inputKey = `input${i}`;
      oldPortIn.param.value = node.data[inputKey];
      if (inputs[inputKey].length > 0) {
        node.data[inputKey] = inputs[inputKey][0];
        oldPortIn.control.setValue(inputs[inputKey][0]);
      }
    }
  }
}

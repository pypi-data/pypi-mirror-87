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
import {v4 as uuidv4} from 'uuid';

export default class WorkflowEditor extends Rete.NodeEditor {
  fromJSONrete(data) {
    return super.fromJSON(data);
  }

  toJSONrete() {
    return super.toJSON();
  }

  /** Convert our own workflow representation into one that Rete can use. */
  fromJSON(data) {
    const convertedData = {
      id: data.id || this.id, // Use the default ID as fallback.
      nodes: {},
    };
    const uuidArray = [];
    // Include all nodes.
    for (let index = 0; index < data.nodes.length; index++) {
      const currentNode = {
        id: index,
        data: {},
        inputs: {},
        outputs: {},
        position: [data.nodes[index].position.x, data.nodes[index].position.y],
        name: data.nodes[index].model.name === 'ToolNode' ? data.nodes[index].model.tool.name
          : data.nodes[index].model.name,
      };
      uuidArray.push(data.nodes[index].id);
      // The node type can currently only be derived using the node's name.
      const nodeName = data.nodes[index].model.name;

      if (nodeName === 'UserInputText') {
        currentNode.name = 'UserInput: Text';
        currentNode.inputs = {
          InpDep: {connections: []},
          prompt_text: {connections: []},
          default_value: {connections: []},
        };
        currentNode.outputs = {
          OutDep: {connections: []},
          value: {connections: []},
        };
      } else if (nodeName === 'UserInputCropImages') {
        currentNode.name = 'UserInput: Crop Images';
        currentNode.inputs = {
          InpDep: {connections: []},
          prompt_text: {connections: []},
          image_path: {connections: []},
        };
        currentNode.outputs = {
          OutDep: {connections: []},
          cropinfo: {connections: []},
        };
      } else if (nodeName === 'UserInputFile') {
        currentNode.name = 'UserInput: File';
        currentNode.inputs = {
          InpDep: {connections: []},
          prompt_text: {connections: []},
        };
        currentNode.outputs = {
          OutDep: {connections: []},
          value: {connections: []},
        };
      } else if (nodeName === 'String') {
        currentNode.name = 'String';
        currentNode.inputs = {};
        currentNode.outputs = {
          str: {connections: []},
        };

        currentNode.data = {
          str: data.nodes[index].model.value,
        };
      } else if (nodeName === 'Float') {
        currentNode.name = 'Float';
        currentNode.inputs = {};
        currentNode.outputs = {
          float: {connections: []},
        };

        currentNode.data = {
          float: data.nodes[index].model.value,
        };
      } else if (nodeName === 'Integer') {
        currentNode.name = 'Integer';
        currentNode.inputs = {};
        currentNode.outputs = {
          num: {connections: []},
        };

        currentNode.data = {
          num: data.nodes[index].model.value,
        };
      } else if (nodeName === 'Boolean' || nodeName === 'Bool') {
        currentNode.name = 'Bool';
        currentNode.inputs = {};
        currentNode.outputs = {
          flag: {connections: []},
        };

        currentNode.data = {
          flag: data.nodes[index].model.value,
        };
      } else if (nodeName === 'FileOutput') {
        currentNode.name = 'File Output';
        currentNode.inputs = {
          InpDep: {connections: []},
          path: {connections: []},
          outputFilePath: {connections: []},
          createShortcut: {connections: []},
          stdinput: {connections: []},
        };
        currentNode.outputs = {
          OutDep: {connections: []},
          stdoutput: {connections: []},
        };
      } else if (nodeName === 'FileInput') {
        currentNode.name = 'File Input';
        currentNode.inputs = {
          InpDep: {connections: []},
          path: {connections: []},
        };
        currentNode.outputs = {
          OutDep: {connections: []},
          stdoutput: {connections: []},
        };
      } else if (nodeName === 'ToolNode') {
        currentNode.inputs.InpDep = {connections: []};
        currentNode.outputs.OutDep = {connections: []};

        // Iterate through the ports and add the corresponding inputs and outputs.
        let inputs = 0;
        let outputs = 0;
        for (let portIndex = 0; portIndex < data.nodes[index].model.tool.ports.length; portIndex++) {
          const currentPort = data.nodes[index].model.tool.ports[portIndex];

          if (currentPort.port_direction === 'in'
              && currentPort.name !== 'stdin'
              && currentPort.name !== 'Dependencies') {
            currentNode.inputs[`input${inputs}`] = {
              connections: [],
            };

            if (currentPort.type === 'flag') {
              currentNode.data[`input${inputs}`] = currentPort.value;
            }
            if (currentPort.required || currentPort.default_value !== currentPort.value) {
              currentNode.data[`input${inputs}`] = currentPort.value;
            }

            inputs++;
          } else if (currentPort.port_direction === 'out'
                     && currentPort.name !== 'stdout'
                     && currentPort.name !== 'Dependents') {
            currentNode.outputs[`output${outputs}`] = {
              connections: [],
            };

            if (currentPort.required || currentPort.default_value !== currentPort.value) {
              currentNode.data[`output${outputs}`] = currentPort.value;
            }

            outputs++;
          }
        }
        currentNode.inputs.stdinput = {connections: []};
        currentNode.outputs.stdoutput = {connections: []};
      }

      // All data needs to be added to the node.
      if (nodeName !== 'ToolNode') {
        for (const prop in data.nodes[index].model) {
          if (prop !== 'name' && prop !== 'stdinput' && prop !== 'value' && data.nodes[index].model[prop] !== '') {
            currentNode.data[prop] = data.nodes[index].model[prop];
          }
        }
      }

      convertedData.nodes[index] = currentNode;
    }

    // Include all connections.
    for (let index = 0; index < data.connections.length; index++) {
      const currentConnection = data.connections[index];
      const inId = uuidArray.findIndex((element) => element === currentConnection.in_id); // ID of the input node.
      const inIndex = currentConnection.in_index; // Index of the used port.
      const outId = uuidArray.findIndex((element) => element === currentConnection.out_id); // ID of the output node.
      const outIndex = currentConnection.out_index; // Index of the used port.
      // At this point the input and output nodes used in the connection are known.
      const inputName = Object.keys(convertedData.nodes[inId].inputs)[inIndex];
      const outputName = Object.keys(convertedData.nodes[outId].outputs)[outIndex];
      const nodeInput = {
        node: outId,
        output: outputName,
        data: {},
      };
      convertedData.nodes[inId].inputs[inputName].connections.push(nodeInput);

      const nodeOutput = {
        node: inId,
        input: inputName,
        data: {},
      };
      convertedData.nodes[outId].outputs[outputName].connections.push(nodeOutput);
    }

    return super.fromJSON(convertedData);
  }

  /** Convert the Rete representation into our own workflow representation. */
  toJSON() {
    const transformedData = {
      id: this.id,
      connections: [],
      nodes: [],
    };

    for (let i = 0; i < this.nodes.length; i++) {
      const oldNode = this.nodes[i];
      const newNode = {
        id: '',
        model: {},
      };
      if (!oldNode.uuid) {
        newNode.id = `{${uuidv4().toString()}}`;
        oldNode.uuid = newNode.id;
      } else {
        newNode.id = oldNode.uuid;
      }

      if (oldNode.componentType === 'SourceNode') {
        if (oldNode.name === 'Number') {
          newNode.model.name = 'Float';
        } else if (oldNode.name === 'Bool') {
          newNode.model.name = 'Boolean';
        } else {
          newNode.model.name = oldNode.name;
        }
        newNode.model.value = oldNode.data.str || oldNode.data.float || oldNode.data.num || oldNode.data.flag;
      } else if (oldNode.componentType === 'ToolNode') {
        newNode.model.name = oldNode.componentType;
        newNode.model.tool = {
          name: oldNode.name,
          description: oldNode.description,
          path: oldNode.name, // Including an actual path probably does not make sense here.
          version: oldNode.version,
          ports: [],
        };

        // Input ports.
        let iterator = oldNode.inputs.keys();
        for (let j = 0; j < oldNode.inputs.size; j++) {
          const oldPortIn = oldNode.inputs.get(iterator.next().value);
          const newPort = {
            name: oldPortIn.param === '' ? oldPortIn.name : oldPortIn.param.name,
            shortName: oldPortIn.param.char || '',
            description: oldPortIn.param.description,
            port_direction: 'in',
            port_index: j,
            position: j,
            required: oldPortIn.param.required || false,
            default_value: oldPortIn.param.defaultVal || null,
          };

          newPort.value = oldNode.data[oldPortIn.key] || newPort.default_value;

          if (newPort.name === 'Dependencies') {
            newPort.type = 'dependency';
          } else if (newPort.name === 'stdin') {
            newPort.type = 'pipe';
          } else {
            newPort.type = oldPortIn.param.type;
          }

          newNode.model.tool.ports.push(newPort);
        }

        // Output ports.
        iterator = oldNode.outputs.keys();
        for (let j = 0; j < oldNode.outputs.size; j++) {
          const oldPortOut = oldNode.outputs.get(iterator.next().value);
          const newPort = {
            name: oldPortOut.name,
            shortName: '',
            port_direction: 'out',
            port_index: j,
            position: j,
            required: false,
            value: null,
          };

          if (newPort.name === 'Dependents') {
            newPort.type = 'dependency';
          } else if (newPort.name === 'stdout') {
            newPort.type = 'pipe';
          } else {
            newPort.type = '';
          }

          newNode.model.tool.ports.push(newPort);
        }
      } else if (oldNode.componentType === 'PromptNode' || oldNode.componentType === 'InputOutput') {
        newNode.model.name = oldNode.model_name;

        const iterator = oldNode.inputs.keys();
        iterator.next(); // Dependencies are not saved.
        for (let j = 1; j < oldNode.inputs.size; j++) {
          const inp = oldNode.inputs.get(iterator.next().value).key;
          newNode.model[inp] = oldNode.data[inp] || '';
        }
      }

      newNode.position = {
        x: oldNode.position[0],
        y: oldNode.position[1],
      };
      transformedData.nodes.push(newNode);

      // Connections.
      const iterator = oldNode.outputs.keys();
      for (let outputIndex = 0; outputIndex < oldNode.outputs.size; outputIndex++) {
        const oldPortOut = oldNode.outputs.get(iterator.next().value);

        for (let connectionIndex = 0; connectionIndex < oldPortOut.connections.length; connectionIndex++) {
          const oldConnection = oldPortOut.connections[connectionIndex];
          const connectionKeys = [...oldConnection.input.node.inputs.keys()];

          if (!oldConnection.input.node.uuid) {
            oldConnection.input.node.uuid = `{${uuidv4().toString()}}`;
          }
          const newConnection = {
            in_id: oldConnection.input.node.uuid,
            in_key: oldConnection.input.key,
            out_id: oldNode.uuid,
            out_key: oldPortOut.key,
            out_index: outputIndex,
          };
          newConnection.in_index = connectionKeys.findIndex((element) => element === newConnection.in_key);
          transformedData.connections.push(newConnection);
        }
      }
    }
    return transformedData;
  }
}

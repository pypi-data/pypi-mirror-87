<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="node" :class="[selected(), node.name] | kebab">
    <div class="title" :title="node.nodeDescription || ''">{{ node.name }}</div>
    <div class="content">
      <!-- Inputs-->
      <div class="inputs" v-for="input in inputs()" :key="input.title" style="text-align: left">
        <div class="column" v-if="node.controls.size > 0 || node.inputs.size > 0">
          <socket v-socket:input="input" type="input" :socket="input.socket" :used="input.connections.length > 0">
          </socket>
          <div class="input-title" v-if="input.param.required" :title="input.param.description || 'none'">
            {{ input.name + "*" }}
          </div>
          <div class="input-title" v-else :title="input.param.description">{{ input.name }}</div>
        </div>
        <div class="column">
          <div class="input-control" v-show="input.showControl()" v-control="input.control"></div>
        </div>
        <div class="column">
          <button class="btn btn-link text-white" @click="restoreDefault(input)">
            <div>
              <i class="fas fa-undo"
                 v-if="input.param.defaultVal && (String(input.param.value) !== input.param.defaultVal)"
                 title="Restore default value">
              </i>
            </div>
          </button>
        </div>
        <div class="column align-bottom">
          <div class="fas fa-exclamation-triangle"
               v-if="input.param.relations && input.param.paramDependenceError"
               :title="input.param.message">
          </div>
        </div>
      </div>
      <!-- Controls-->
      <div class="control" v-for="control in controls()" :key="control.key" v-control="control"></div>
      <!-- Outputs-->
      <div class="column">
        <div class="outputs" v-for="output in outputs()" :key="output.key" style="text-align: right">
          <div class="output-title" style="margin-left:-30px">{{ output.name }}</div>
          <socket v-socket:output="output" type="output" :socket="output.socket" :used="output.connections.length > 0">
          </socket>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueRenderPlugin from 'rete-vue-render-plugin';
import Socket from './Socket.vue';

export default {
  data() {
    return {
    };
  },
  mixins: [VueRenderPlugin.mixin],
  components: {
    Socket,
  },
  methods: {
    restoreDefault(restoreParam) {
      const keysArray = [...this.node.inputs.keys()];
      const correspIndex = keysArray.findIndex((element) => element === restoreParam.key);
      const currparam = this.node.inputs.get(keysArray[correspIndex]);
      if (currparam) {
        currparam.control.setValue(currparam.param.defaultVal);
      }
    },
  },
  updated() {
    this.$nextTick(function() {
      this.editor.view.updateConnections({node: this.node});
    });
  },
  mounted() {
    // Error message
    // Remove error if the connection is removed
    this.editor.on('connectionremoved', (connection) => {
      if (connection.input.param) {
        connection.input.param.paramDependenceError = false;
      }
    });
    this.editor.on('process connectioncreated connectionremoved', (connection) => {
      if (this.node.relations) {
        for (let i = 0; i < this.node.relations.length; i++) {
          const portL = this.node.relations[i].paramLeft.portId;
          // Check if the parameter that might cause an error is empty
          if (this.node.data[portL]) {
            const portR = this.node.relations[i].paramRight.portId;
            // Check type of relation
            if (this.node.relations[i].relation === 1) {
              // Required
              if (this.node.data[portR]
                 || (Object.keys(connection).length === 3
                 && connection.input.param.name === this.node.relations[i].paramRight.name)) {
                this.node.relations[i].paramLeft.paramDependenceError = false;
              } else {
                this.node.relations[i].paramLeft.paramDependenceError = true;
                this.node.relations[i].paramLeft.message = this.node.relations[i].message;
              }
            } else {
              // Incompatible
              if (this.node.data[portR]
                 || (Object.keys(connection).length === 3
                 && connection.input.param.name === this.node.relations[i].paramRight.name)) {
                this.node.relations[i].paramLeft.paramDependenceError = true;
                this.node.relations[i].paramLeft.message = this.node.relations[i].message;
                break;
              } else {
                this.node.relations[i].paramLeft.paramDependenceError = false;
              }
            }
          } else {
            this.node.relations[i].paramLeft.paramDependenceError = false;
          }
        }
      }
      this.node.update();
    });
  },
};
</script>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.node {
  color: white;
  background: #2c3e50;
  border: 2px solid white;
  border-radius: 10px;
  cursor: pointer;
  min-width: 180px;
  height: auto;
  padding-bottom: 6px;
  box-sizing: border-box;
  position: relative;
  user-select: none;

  &:hover {
    background: #3a5169;
  }

  &.selected {
    background: #4f6e8f;
  }

  .title {
    font-size: 18px;
    font-weight: bold;
    padding-bottom: 8px;
    padding-left: 15px;
    padding-top: 8px;
  }

  .output {
    text-align: right;
  }

  .input {
    text-align: left;
  }

  .input-title,.output-title {
    vertical-align: middle;
    display: inline-block;
    font-size: 14px;
    width: 120px;
    margin: $socket-margin;
    margin-left: 0px;
    line-height: $socket-size;
  }

  .input-control {
    z-index: 1;
    width: calc(100% - #{$socket-size + 2 * $socket-margin});
    vertical-align: middle;
    display: inline-block;
  }

  .control {
    padding: $socket-margin $socket-size / 2 + $socket-margin;
  }

  .content {
    display: table;
    width: 100%;

    .column {
      display: table-cell;
      white-space: nowrap;

      &:not(:last-child) {
        padding-right: 20px;
      }
    }
  }
}
</style>

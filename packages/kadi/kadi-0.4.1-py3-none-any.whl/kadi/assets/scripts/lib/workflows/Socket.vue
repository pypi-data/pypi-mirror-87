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
  <div class="socket" :class="[type, socket.name, used ? 'used' : ''] | kebab" :title="socket.name"></div>
</template>

<script>
import VueRenderPlugin from 'rete-vue-render-plugin';

export default {
  extends: VueRenderPlugin.Socket,
  props: {
    used: Boolean,
  },
};
</script>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

$socket-color: #2c3e50;

.socket {
  display: inline-block;
  cursor: pointer;
  border: 2px solid $socket-color;
  border-radius: $socket-size / 2.0;
  width: $socket-size;
  height: $socket-size;
  margin: $socket-margin;
  vertical-align: middle;
  background: white;
  position: relative;
  z-index: 2;
  box-sizing: border-box;

  &.used {
    background: $socket-color;
    border: 2px solid white;
  }

  &:hover {
    border-width: 4px;
  }

  &.multiple {
    border-color: yellow;
  }

  &.output {
    margin-right: - $socket-size / 2;
  }

  &.input {
    margin-left: - $socket-size / 2;
  }
}

.socket.num {
  background:rgb(250, 98, 93);
}

.socket.any {
  background:rgb(253, 237, 87);
}

.socket.bool {
  background:rgb(188, 105, 255);
}

.socket.str {
  background:rgb(146, 212, 250);
}

.socket.dep {
  background:rgb(49, 214, 34);
}

</style>

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
  <input :readonly="readonly" v-model.number="value" @pointerdown.stop>
</template>

<script>
export default {
  props: {
    readonly: Boolean,
    emitter: Object,
    ikey: String,
    getData: Function,
    putData: Function,
    defaultValue: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      value: 0,
    };
  },
  methods: {
    update() {
      if (this.ikey) {
        this.putData(this.ikey, this.value);
      }
      this.emitter.trigger('process');
    },
  },
  watch: {
    value() {
      if (isNaN(this.value)) {
        this.value = this.defaultValue;
      }
      this.update();
    },
  },
  mounted() {
    this.value = this.getData(this.ikey) || this.defaultValue;
  },
};
</script>

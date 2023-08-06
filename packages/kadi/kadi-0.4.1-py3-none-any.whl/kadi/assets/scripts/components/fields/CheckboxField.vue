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
  <div class="mb-3">
    <div class="form-check form-check-inline">
      <input type="checkbox"
             :id="field.id"
             :name="field.name"
             :disabled="disabled"
             :class="classes"
             v-model="input">
      <label class="form-check-label" :for="field.id">{{ field.label }}</label>
    </div>
    <br>
  </div>
</template>

<script>
export default {
  data() {
    return {
      input: this.field.data,
    };
  },
  props: {
    field: Object,
    disabled: {
      type: Boolean,
      default: false,
    },
    classes: {
      type: String,
      default: 'form-check-input',
    },
  },
  watch: {
    input() {
      this.$emit('change', this.input);
    },
  },
};
</script>

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
  <div>
    <!-- eslint-disable max-len -->
    <!-- Using the index as key should be fine in this case. -->
    <pre><div v-for="(line, index) in lines" :key="index" class="line"><span class="text-muted">{{ lineNum(index) }}</span>  {{ `${line}\n` }}</div></pre>
    <!-- eslint-enable max-len -->
    <small class="text-muted" v-if="encoding">{{ i18n.t('misc.detectedEncoding') }} {{ encoding }}</small>
  </div>
</template>

<style scoped>
.line:hover {
  background-color: #d9d9d9;
  white-space: pre-wrap;
}
</style>

<script>
export default {
  data() {
    return {
      lines: [],
      numDigits: 1,
    };
  },
  props: {
    text: String,
    encoding: {
      type: String,
      default: null,
    },
    showLineNumbers: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    lineNum(index) {
      return `${' '.repeat(this.lines.length.toString().length - (index + 1).toString().length)}${index + 1}`;
    },
  },
  mounted() {
    this.lines = this.text.split('\n');
  },
};
</script>

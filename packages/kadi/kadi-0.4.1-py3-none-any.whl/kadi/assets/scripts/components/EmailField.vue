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
  <!-- Prevent newlines from getting rendered as space. -->
  <a ref="mailto" href="mailto:admin@localhost.localdomain"><!--
 --><strong v-if="title">{{ title }}</strong><!--
 --><strong v-if="!title">{{ name }}<i class="fas fa-at"></i>{{ domain }}</strong><!--
--></a>
</template>

<script>
export default {
  props: {
    name: String,
    domain: String,
    title: {
      type: String,
      default: '',
    },
  },
  mounted() {
    this.$refs.mailto.setAttribute('href', `mailto:${this.name}@${this.domain}`);
  },
};
</script>

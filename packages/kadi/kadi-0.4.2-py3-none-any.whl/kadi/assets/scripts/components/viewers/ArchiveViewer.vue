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
  <ul>
    <li v-for="entry in entries_" :key="entry.id">
      <div v-if="!entry.is_dir">
        <div class="d-flex justify-content-between">
          <div>
            <i class="fas fa-file"></i> {{ entry.name }}
          </div>
          <small>{{ entry.size | filesizeFormat }}</small>
        </div>
      </div>
      <div v-if="entry.is_dir">
        <collapse-item :id="entry.id" show-icon-class="fas fa-folder" hide-icon-class="fas fa-folder-open">
          <strong>{{ entry.name }}</strong>
        </collapse-item>
        <archive-viewer class="collapse show" :id="entry.id" :entries="entry.files"></archive-viewer>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  data() {
    return {
      entries_: [],
    };
  },
  props: {
    entries: Array,
  },
  mounted() {
    this.entries.forEach((entry) => {
      entry.id = kadi.utils.randomAlnum();
      this.entries_.push(entry);
    });
  },
};
</script>

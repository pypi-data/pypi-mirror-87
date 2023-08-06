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
    <div v-for="(extra, index) in extras"
         :key="extra.id"
         class="px-1"
         :class="{'hover-extra': extra === hoverExtra}"
         @mouseover.stop="hoverExtra = extra"
         @mouseout="hoverExtra = null">
      <span v-if="isNestedType(extra)" class="mr-2">
        <collapse-item :id="extra.id" show-icon-class="fas fa-plus-square" hide-icon-class="fas fa-minus-square">
          <span></span>
        </collapse-item>
      </span>
      <button type="button" class="btn btn-link text-primary pl-0 py-1" @click="$emit('focus-extra', extra)">
        <strong>
          <span v-if="extra.key.value.trim() && nestedType !== 'list'">{{ extra.key.value }}</span>
          <span v-else>({{ index + 1 }})</span>
        </strong>
        <span class="text-muted ml-2">
          <small>({{ extra.type.value | prettyTypeName | capitalize }})</small>
        </span>
      </button>
      <div v-if="isNestedType(extra)">
        <div :id="extra.id" class="border-dotted pl-5 ml-1 collapse show">
          <extra-tree-view :extras="extra.value.value"
                           :nested-type="extra.type.value"
                           @focus-extra="$emit('focus-extra', $event)">
          </extra-tree-view>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-dotted {
  border-left: 1px dotted #2c3e50;
}

.hover-extra {
  background-color: #dee6ed;
}
</style>

<script>
export default {
  data() {
    return {
      hoverExtra: null,
    };
  },
  props: {
    extras: Array,
    nestedType: {
      type: String,
      default: null,
    },
  },
  methods: {
    isNestedType(extra) {
      return ['dict', 'list'].includes(extra.type.value);
    },
  },
};
</script>

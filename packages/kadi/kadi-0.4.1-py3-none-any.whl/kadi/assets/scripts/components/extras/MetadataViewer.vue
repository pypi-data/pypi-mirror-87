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
    <div v-if="!nestedType">
      <div class="d-flex justify-content-between mb-2">
        <div>
          <slot></slot>
        </div>
        <div v-if="hasNestedType">
          <div class="btn-group">
            <button type="button"
                    class="btn btn-link text-muted py-0 pl-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, true)">
              <i class="fas fa-minus-square"></i> Collapse all
            </button>
            <button type="button"
                    class="btn btn-link text-muted py-0 pr-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, false)">
              <i class="fas fa-plus-square"></i> Expand all
            </button>
          </div>
        </div>
      </div>
    </div>
    <ul class="list-group mb-2">
      <li v-for="(extra, index) in extras_"
          :key="extra.id"
          class="list-group-item py-1 pl-3 pr-0"
          :class="{'bg-nested': depth % 2 == 1}"
          style="margin-right: -1px;">
        <div v-if="isNestedType(extra)">
          <div class="row align-items-center" :class="{'mb-1': extra.value.length > 0 && !extra.isCollapsed}">
            <div class="col-md-5">
              <collapse-item :id="extra.id"
                             :is-collapsed="extra.isCollapsed"
                             show-icon-class=""
                             hide-icon-class=""
                             @collapse="extra.isCollapsed = $event">
                <strong>{{ extra.key || `(${index + 1})` }}</strong>
              </collapse-item>
            </div>
            <div class="col-md-6">
              <collapse-item :id="extra.id"
                             :is-collapsed="extra.isCollapsed"
                             show-icon-class=""
                             hide-icon-class=""
                             @collapse="extra.isCollapsed = $event"
                             v-if="extra.isCollapsed && extra.value.length > 0">
                <strong>{...}</strong>
              </collapse-item>
            </div>
            <div class="col-md-1 text-muted d-md-flex justify-content-end">
              <small class="mr-3">{{ extra.type | prettyTypeName | capitalize }}</small>
            </div>
          </div>
          <div v-if="extra.value.length > 0">
            <div :id="extra.id" class="collapse show">
              <metadata-viewer :extras="extra.value" :nested-type="extra.type" :depth="depth + 1"></metadata-viewer>
            </div>
          </div>
        </div>
        <div v-if="!isNestedType(extra)">
          <div class="row align-items-center">
            <div class="col-md-5">{{ extra.key || `(${index + 1})` }}</div>
            <div class="col-md-6">
              <span v-if="extra.value !== null">
                <span v-if="extra.type === 'date'">
                  <local-timestamp :timestamp="extra.value"></local-timestamp>
                </span>
                <span v-else>{{ extra.value }}</span>
              </span>
              <span v-if="extra.value === null">
                <em>null</em>
              </span>
              <span class="text-muted">{{ extra.unit }}</span>
            </div>
            <div class="col-md-1 text-muted d-md-flex justify-content-end">
              <small class="mr-3">{{ extra.type | prettyTypeName | capitalize }}</small>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.bg-nested {
  background-color: #f2f2f2;
}
</style>

<script>
export default {
  data() {
    return {
      extras_: this.extras,
      isCollapsing: false,
    };
  },
  props: {
    extras: Array,
    nestedType: {
      type: String,
      default: null,
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  methods: {
    visitExtras(extras, callback) {
      extras.forEach((extra) => {
        callback(extra);
        if (this.isNestedType(extra)) {
          this.visitExtras(extra.value, callback);
        }
      });
    },
    collapseExtras(extras, collapse) {
      this.isCollapsing = true;
      this.visitExtras(extras, (extra) => extra.isCollapsed = collapse);
      // Take the collapse cooldown into account.
      setTimeout(() => this.isCollapsing = false, 400);
    },
    isNestedType(extra) {
      return ['dict', 'list'].includes(extra.type);
    },
  },
  computed: {
    hasNestedType() {
      for (const extra of this.extras_) {
        if (this.isNestedType(extra)) {
          return true;
        }
      }
      return false;
    },
  },
  created() {
    this.visitExtras(this.extras_, (extra) => {
      extra.id = kadi.utils.randomAlnum();
      this.$set(extra, 'isCollapsed', false);
    });
  },
};
</script>

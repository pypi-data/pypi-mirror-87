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

<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="form-group mb-4">
    <div class="form-row" :class="{'drag-extra': extra.isDragging}">
      <div class="col-xl-4 mb-1 mb-xl-0" :class="{'mr-3 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">Key</span>
          </div>
          <input name="extra_key"
                 class="form-control"
                 v-model="keyModel"
                 :class="{'has-error': extra.key.errors.length > 0 && !extra.isDragging,
                          'font-weight-bold': isNestedType}"
                 :readonly="nestedType === 'list'"
                 :tabindex="nestedType === 'list' ? -1 : 0"
                 @change="$emit('save-checkpoint')"
                 ref="key">
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.key.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <div class="mb-1 mb-xl-0"
           :class="{'col-xl-3': showUnit, 'col-xl-5': !showUnit, 'mr-3 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">Value</span>
          </div>
          <input name="extra_value"
                 class="form-control"
                 v-model="valueModel"
                 :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                 :readonly="isNestedType"
                 :tabindex="isNestedType ? -1 : 0"
                 v-if="!['bool', 'date'].includes(extra.type.value)"
                 @change="$emit('save-checkpoint')">
          <select name="extra_value"
                  class="custom-select"
                  v-model="extra.value.value"
                  :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                  v-if="extra.type.value === 'bool'"
                  @change="$emit('save-checkpoint')">
            <option value=""></option>
            <option value="true">true</option>
            <option value="false">false</option>
          </select>
          <input type="hidden" name="extra_value" :value="extra.value.value" v-if="extra.type.value === 'date'">
          <date-time-picker :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                            :initial-value="extra.value.value"
                            @input="changeDate"
                            v-if="extra.type.value === 'date'">
          </date-time-picker>
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.value.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <div class="col-xl-2 mb-1 mb-xl-0" :class="{'mr-3 mr-xl-0': nestedType}" v-show="showUnit">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">Unit</span>
          </div>
          <input name="extra_unit"
                 class="form-control"
                 v-model="unitModel"
                 :class="{'has-error': extra.unit.errors.length > 0 && !extra.isDragging}"
                 @change="$emit('save-checkpoint')">
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.unit.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <div class="col-xl-3" :class="{'mr-3 mr-xl-0': nestedType}">
        <div class="form-row">
          <div class="col-xl-9 mb-1 mb-xl-0">
            <select name="extra_type"
                    class="custom-select custom-select-sm"
                    tabindex="-1"
                    v-model="extra.type.value"
                    :class="{'has-error': extra.type.errors.length > 0 && !extra.isDragging}"
                    @change="changeType">
              <option value="str">String</option>
              <option value="int">Integer</option>
              <option value="float">Float</option>
              <option value="bool">Boolean</option>
              <option value="date">Date</option>
              <option value="dict">Dictionary</option>
              <option value="list">List</option>
            </select>
            <div v-show="!extra.isDragging">
              <div class="invalid-feedback" v-for="error in extra.type.errors" :key="error">{{ error }}</div>
            </div>
          </div>
          <div class="col-xl-3">
            <div class="d-none d-xl-block pr-2">
              <button type="button"
                      class="btn btn-sm btn-light btn-block"
                      tabindex="-1"
                      :title="toggleCopy ? 'Copy' : 'Remove'"
                      @click="toggleCopy ? $emit('copy-extra') : $emit('remove-extra')">
                <i class="fas fa-times" v-if="!toggleCopy"></i>
                <i class="fas fa-copy" v-else></i>
                <span class="d-xl-none pl-1">
                  <span v-if="!toggleCopy">Remove</span>
                  <span v-else>Copy</span>
                </span>
              </button>
            </div>
            <div class="btn-group w-100 d-xl-none">
              <button type="button"
                      class="btn btn-sm btn-light"
                      tabindex="-1"
                      title="Remove"
                      @click="$emit('remove-extra')">
                <i class="fas fa-times pr-1"></i> Remove
              </button>
              <button type="button"
                      class="btn btn-sm btn-light"
                      tabindex="-1"
                      title="Copy"
                      @click="$emit('copy-extra')">
                <i class="fas fa-copy pr-1"></i> Copy
              </button>
            </div>
          </div>
        </div>
      </div>
      <input name="extra_depth" type="hidden" :value="depth">
    </div>
    <div class="card mt-1 pl-3 py-2"
         :class="{'bg-nested': depth % 2 == 0}"
         style="margin-right: -1px;"
         v-if="isNestedType"
         v-show="!extra.isDragging">
      <extra-metadata :extras="extra.value.value"
                      :toggle-copy="toggleCopy"
                      :nested-type="extra.type.value"
                      :depth="depth + 1"
                      @save-checkpoint="$emit('save-checkpoint')">
      </extra-metadata>
    </div>
  </div>
</template>

<style scoped>
.bg-nested {
  background-color: #f2f2f2;
}

.drag-extra {
  background-color: #dee6ed;
  border-radius: 0.5rem;
  padding: 0.5rem 0 0.5rem 0.5rem;
}

.sort-handle {
  cursor: pointer;
}
</style>

<!-- eslint-disable vue/no-mutating-props -->
<script>
export default {
  data() {
    return {
      prevType: null,
    };
  },
  props: {
    extra: Object,
    index: Number,
    toggleCopy: {
      type: Boolean,
      default: false,
    },
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
    changeType() {
      const specialInputTypes = ['bool', 'date'];
      if ((!this.isNestedType && ['dict', 'list'].includes(this.prevType))
          || specialInputTypes.includes(this.extra.type.value)
          || specialInputTypes.includes(this.prevType)) {
        this.extra.value.value = '';
      }

      if (this.isNestedType && !['dict', 'list'].includes(this.prevType)) {
        this.$emit('init-nested-value');
      }

      this.prevType = this.extra.type.value;
      this.$emit('save-checkpoint');
    },
    changeDate(value) {
      this.extra.value.value = value;
      this.$emit('save-checkpoint');
    },
  },
  computed: {
    keyModel: {
      get() {
        return this.nestedType === 'list' ? `(${this.index + 1})` : this.extra.key.value;
      },
      set(value) {
        this.extra.key.value = value;
      },
    },
    valueModel: {
      get() {
        return this.isNestedType ? '' : this.extra.value.value;
      },
      set(value) {
        this.extra.value.value = value;
      },
    },
    unitModel: {
      get() {
        return ['int', 'float'].includes(this.extra.type.value) ? this.extra.unit.value : '';
      },
      set(value) {
        this.extra.unit.value = value;
      },
    },
    showUnit() {
      return ['int', 'float'].includes(this.extra.type.value);
    },
    isNestedType() {
      return ['dict', 'list'].includes(this.extra.type.value);
    },
  },
  watch: {
    'extra.key.value'() {
      this.extra.key.errors = [];
    },
    'extra.value.value'() {
      this.extra.value.errors = [];
    },
    'extra.unit.value'() {
      this.extra.unit.errors = [];
    },
    'extra.type.value'() {
      this.extra.type.errors = [];
      this.prevType = this.extra.type.value;
    },
  },
  mounted() {
    this.extra.input = this.$refs.key;
    this.prevType = this.extra.type.value;
  },
};
</script>

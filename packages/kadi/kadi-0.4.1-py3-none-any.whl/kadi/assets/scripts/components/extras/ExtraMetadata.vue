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
    <div :class="{'mt-2': nestedType && extras.length > 0}">
      <vue-draggable :list="extras"
                     :group="{name: 'extras'}"
                     :force-fallback="true"
                     :empty-insert-threshold="35"
                     scroll-sensitivity="100"
                     scroll-speed="15"
                     handle=".sort-handle"
                     @start="startDrag"
                     @end="endDrag">
        <div v-for="(extra, index) in extras" :key="`${extra.id}`">
          <extra-field :extra="extra"
                       :index="index"
                       :toggle-copy="toggleCopy"
                       :nested-type="nestedType"
                       :depth="depth"
                       @remove-extra="removeExtra(extra)"
                       @copy-extra="copyExtra(extra)"
                       @init-nested-value="initNestedValue(extra)"
                       @save-checkpoint="$emit('save-checkpoint')">
          </extra-field>
        </div>
      </vue-draggable>
    </div>
    <div class="row align-items-center">
      <div class="col-xl-3">
        <button type="button"
                class="btn btn-link text-muted p-0"
                tabindex="-1"
                title="Add entry (Ctrl+I)"
                @click="addExtra(null)">
          <i class="fas fa-plus mr-1"></i> Add entry
        </button>
      </div>
      <div class="col-xl-9">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<!-- eslint-disable vue/no-mutating-props -->
<script>
import VueDraggable from 'vuedraggable';

export default {
  components: {
    VueDraggable,
  },
  props: {
    extras: Array,
    toggleCopy: Boolean,
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
    getExtraFormdata(extra = null) {
      const extraFormdata = {
        id: kadi.utils.randomAlnum(), // Unique key for v-for, so there are no issues when reordering extras.
        isDragging: false, // To change an extra's appearance while dragging it.
        key: {value: '', errors: []},
        value: {value: '', errors: []},
        unit: {value: '', errors: []},
        type: {value: 'str', errors: []},
      };

      // Always deep copy the extra.
      if (extra) {
        // Assume the extra is formatted as formdata if the key is an object.
        const isFormdata = typeof extra.key === 'object';
        if (isFormdata) {
          extraFormdata.key.errors = extra.key.errors;
          extraFormdata.value.errors = extra.value.errors;
          extraFormdata.unit.errors = extra.unit.errors;
          extraFormdata.type.errors = extra.type.errors;
        }

        /* All potential missing or nullable values have to be set to empty strings so all fields get initialized
           correctly. */
        extraFormdata.key.value = isFormdata ? extra.key.value : (extra.key ? extra.key : '');
        extraFormdata.unit.value = isFormdata ? extra.unit.value : (extra.unit ? extra.unit : '');
        extraFormdata.type.value = isFormdata ? extra.type.value : extra.type;
        const value = isFormdata ? extra.value.value : (extra.value !== null ? extra.value : '');

        if (['dict', 'list'].includes(extraFormdata.type.value)) {
          extraFormdata.value.value = [];
          value.forEach((extra) => extraFormdata.value.value.push(this.getExtraFormdata(extra)));
        } else {
          extraFormdata.value.value = value;
        }
      }

      return extraFormdata;
    },
    addExtra(extra, createCheckpoint = true) {
      const newExtra = this.getExtraFormdata(extra);
      this.extras.push(newExtra);
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
      return newExtra;
    },
    addExtras(extras, createCheckpoint = true) {
      extras.forEach((extra) => this.addExtra(extra, false));
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtra(extra, createCheckpoint = true) {
      kadi.utils.removeFromList(this.extras, extra);
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtras(createCheckpoint = true) {
      // Yes, this actually works and does not modify the prop directly.
      this.extras.length = 0;
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    copyExtra(extra) {
      const index = this.extras.indexOf(extra);
      const copy = this.getExtraFormdata(extra);
      this.extras.splice(index, 0, copy);
      this.$emit('save-checkpoint');
    },
    focusExtra(extra) {
      extra.input.focus();
      kadi.utils.scrollIntoView(extra.input);
    },
    initNestedValue(extra) {
      extra.value.value = [this.getExtraFormdata()];
    },
    keydownHandler(e) {
      // Keycodes: 73 = I
      if (e.ctrlKey && e.keyCode === 73) {
        e.preventDefault();
        e.stopPropagation();
        const newExtra = this.addExtra(null);
        this.$nextTick(() => this.focusExtra(newExtra));
      }
    },
    startDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = true;
    },
    endDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = false;

      if (e.from !== e.to) {
        extra.key.errors = [];
        this.$emit('save-checkpoint');
      } else if (e.oldIndex !== e.newIndex) {
        this.$emit('save-checkpoint');
      }
    },
  },
  mounted() {
    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>

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
  <base-field :field="field">
    <template #default="props">
      <select :id="field.id"
              :name="field.name"
              :required="field.validation.required"
              :disabled="disabled"
              :class="[{'has-error': props.hasError}, enableSearch ? 'select2-hidden-accessible' : classes]"
              v-model="input"
              ref="select">
        <option v-for="choice in field.choices" :key="choice[0]" :value="choice[0]">{{ choice[1] }}</option>
      </select>
    </template>
  </base-field>
</template>

<script>
export default {
  data() {
    return {
      input: null,
      initialValueSet: false,
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
      default: 'form-control custom-select',
    },
    enableSearch: {
      type: Boolean,
      default: false,
    },
    searchPlaceholder: {
      type: String,
      default: '',
    },
    searchContainerClasses: {
      type: String,
      default: '',
    },
    searchDropdownParent: {
      type: String,
      default: null,
    },
  },
  watch: {
    input() {
      // Ignore the change event triggered by the initial value.
      if (this.initialValueSet) {
        this.$emit('select', this.input);
        this.$el.dispatchEvent(new Event('change', {bubbles: true}));
      } else {
        this.initialValueSet = true;
      }
    },
  },
  mounted() {
    if (this.enableSearch) {
      const select = $(this.$refs.select).select2({
        containerCssClass: this.searchContainerClasses,
        placeholder: this.searchPlaceholder,
        dropdownParent: this.searchDropdownParent ? $(this.searchDropdownParent) : null,
        allowClear: true,
        language: {
          removeAllItems() {
            return 'Clear selection';
          },
        },
      });

      select.on('select2:select', (e) => this.input = e.params.data.id);
    }

    for (const choice of this.field.choices) {
      if (choice[0] === this.field.data) {
        this.input = this.field.data;
        return;
      }
    }

    this.input = this.field.choices[0][0];
  },
  beforeDestroy() {
    $(this.$refs.select).select2('destroy');
  },
};
</script>

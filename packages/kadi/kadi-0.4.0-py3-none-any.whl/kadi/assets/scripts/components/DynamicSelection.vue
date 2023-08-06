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
  <select :multiple="multiple" ref="select"></select>
</template>

<script>
export default {
  props: {
    endpoint: String,
    multiple: {
      type: Boolean,
      default: false,
    },
    requestParams: {
      type: Object,
      default: () => ({}),
    },
    containerClasses: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
    tags: {
      type: Boolean,
      default: false,
    },
    maxInputLength: {
      type: Number,
      default: null,
    },
    dropdownParent: {
      type: String,
      default: null,
    },
    initialValues: {
      type: Array,
      default: () => [],
    },
    resetOnSelect: {
      type: Boolean,
      default: false,
    },
  },
  mounted() {
    const select = $(this.$refs.select).select2({
      containerCssClass: this.containerClasses,
      placeholder: this.placeholder,
      tags: this.tags,
      maximumInputLength: this.maxInputLength,
      dropdownParent: this.dropdownParent ? $(this.dropdownParent) : null,
      allowClear: !this.multiple,
      templateResult: (data) => {
        if (!data.id || !data.body) {
          return data.text;
        }
        return $(data.body);
      },
      ajax: {
        url: this.endpoint,
        delay: 100,
        data: (params) => {
          return {
            page: params.page || 1,
            term: params.term,
            ...this.requestParams,
          };
        },
      },
      language: {
        removeAllItems() {
          return i18n.t('misc.clearSelection');
        },
      },
    });

    this.initialValues.forEach((option) => {
      select.append(new Option(option[1], option[0], true, true)).trigger('change');
    });

    select.on('select2:select', (e) => {
      this.$emit('select', e.params.data);
      if (this.resetOnSelect) {
        select.val(null).trigger('change');
      }
    });

    select.on('select2:unselect', (e) => {
      this.$emit('unselect', e.params.data);
    });
  },
  beforeDestroy() {
    $(this.$refs.select).select2('destroy');
  },
};
</script>

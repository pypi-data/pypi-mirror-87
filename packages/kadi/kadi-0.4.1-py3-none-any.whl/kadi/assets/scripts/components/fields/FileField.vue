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
    <label class="form-control-label" :for="field.id">{{ field.label }}</label>
    <div class="form-group" :class="{'required': field.validation.required}">
      <div class="input-group">
        <div class="custom-file">
          <input type="file"
                 class="custom-file-input"
                 :id="field.id"
                 :name="field.name"
                 :required="field.validation.required"
                 :accept="mimetypes"
                 :disabled="disabled"
                 @change="previewFile"
                 ref="files">
          <label class="custom-file-label" :class="{'has-error': field.errors.length > 0 || errorMessage}">
            {{ message }}
          </label>
        </div>
      </div>
      <div v-for="error in field.errors" :key="error" class="invalid-feedback">{{ error }}</div>
      <div class="invalid-feedback">{{ errorMessage }}</div>
      <small class="form-text text-muted" v-if="field.errors.length === 0 && !errorMessage">{{ description }}</small>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      defaultMessage: 'No file selected',
      message: '',
      errorMessage: null,
    };
  },
  props: {
    field: Object,
    mimetypes: Array,
    maxSize: Number,
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    clearFiles() {
      this.message = this.defaultMessage;
      this.$refs.files.value = '';
    },
    previewFile(e) {
      const file = e.target.files[0];
      this.message = file.name;

      if (this.maxSize > 0) {
        if (file.size > this.maxSize) {
          this.errorMessage = 'File exceeds the maximum size.';
          this.clearFiles();
        } else {
          this.errorMessage = null;
        }
      }
    },
  },
  computed: {
    description() {
      return `Maximum permitted file size: ${kadi.utils.filesizeFormat(this.maxSize)}`;
    },
  },
  watch: {
    disabled() {
      if (this.disabled) {
        this.clearFiles();
        this.errorMessage = null;
      }
    },
  },
  mounted() {
    this.message = this.defaultMessage;
  },
};
</script>

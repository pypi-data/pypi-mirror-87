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
  <button class="btn" @click="copy" ref="trigger">
    <slot>
      <i class="fas fa-copy"></i>
    </slot>
  </button>
</template>

<script>
export default {
  props: {
    content: String,
  },
  methods: {
    copy() {
      // Courtesy of https://stackoverflow.com/a/33928558
      if (window.clipboardData && window.clipboardData.setData) {
        window.clipboardData.setData('Text', this.content);
      } else if (document.queryCommandSupported && document.queryCommandSupported('copy')) {
        const textarea = document.createElement('textarea');
        textarea.textContent = this.content;
        textarea.style.position = 'fixed';
        document.body.appendChild(textarea);
        textarea.select();

        try {
          document.execCommand('copy');
        } catch (error) {
          console.warn('Cannot copy to clipboard.', error);
        } finally {
          document.body.removeChild(textarea);
        }
      }
    },
  },
  mounted() {
    $(this.$refs.trigger).tooltip({title: i18n.t('misc.copyToClipboard')});
  },
  beforeDestroy() {
    $(this.$refs.trigger).tooltip('dispose');
  },
};
</script>

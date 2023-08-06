/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

new Vue({
  el: '#vm',
  data: {
    requestInProgress: false,
  },
  methods: {
    downloadFiles() {
      this.requestInProgress = true;
      axios.post(kadi.js_resources.download_files_endpoint)
        .then(() => kadi.getNotifications())
        .catch((error) => {
          if (error.request.status === 429) {
            // Use the error message from the backend.
            kadi.alert(error.response.data.description, {type: 'info'});
          } else {
            kadi.alert(i18n.t('error.packageFiles'), {xhr: error.request});
          }
        })
        .finally(() => this.requestInProgress = false);
    },
    templateFromExtras(extras) {
      const extraTemplate = [];

      for (const extra of extras) {
        const extraTemplateEntry = {type: extra.type};

        if (extra.key) {
          extraTemplateEntry.key = extra.key;
        }
        if (extra.unit) {
          extraTemplateEntry.unit = extra.unit;
        }
        if (['dict', 'list'].includes(extra.type)) {
          extraTemplateEntry.value = this.templateFromExtras(extra.value);
        }

        extraTemplate.push(extraTemplateEntry);
      }

      return extraTemplate;
    },
    exportExtras() {
      this.requestInProgress = true;
      const extras = this.templateFromExtras(kadi.js_resources.extras);
      const title = kadi.js_resources.title;
      const identifier = kadi.js_resources.identifier;

      axios.post(kadi.js_resources.new_template_endpoint, {title, identifier, type: 'extras', data: extras})
        .then(() => kadi.alert(i18n.t('success.createTemplateIdentifier', {identifier}), {type: 'success'}))
        .catch((error) => {
          // Assume the duplicate identifier is the problem in this case.
          if (error.request.status === 400) {
            kadi.alert(i18n.t('error.createTemplateDuplicateIdentifier'));
          } else {
            kadi.alert(i18n.t('error.createTemplate'), {xhr: error.request});
          }
        })
        .finally(() => this.requestInProgress = false);
    },
    deleteFile(file) {
      if (!confirm(i18n.t('warning.deleteIdentifier', {identifier: file.name}))) {
        return;
      }

      this.$set(file, 'disabled', true);

      axios.delete(file._actions.delete)
        .then(() => {
          this.$refs.filesPagination.update();
          this.$refs.fileRevisionsPagination.update();
          kadi.alert(i18n.t('success.deleteFile'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert(i18n.t('error.deleteFile'), {xhr: error.request});
          file.disabled = false;
        });
    },
  },
});

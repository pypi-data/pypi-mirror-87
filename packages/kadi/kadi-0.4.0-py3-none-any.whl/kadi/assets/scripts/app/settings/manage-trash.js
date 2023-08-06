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
  methods: {
    restoreResource(resource) {
      if (!confirm(i18n.t('warning.restoreResourceTitle', {title: resource.title}))) {
        return;
      }

      this.$set(resource, 'disabled', true);

      axios.post(resource._links.restore)
        .then(() => {
          this.$refs.pagination.update();
          kadi.alert(i18n.t('success.restoreResource'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert(i18n.t('error.restoreResource'), {xhr: error.request});
          resource.disabled = false;
        });
    },
    purgeResource(resource) {
      if (!confirm(i18n.t('warning.purgeResourceTitle', {title: resource.title}))) {
        return;
      }

      this.$set(resource, 'disabled', true);

      axios.post(resource._links.purge)
        .then(() => {
          this.$refs.pagination.update();
          kadi.alert(i18n.t('success.deleteResource'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert(i18n.t('error.deleteResource'), {xhr: error.request});
          resource.disabled = false;
        });
    },
  },
});

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
    token: kadi.js_resources.token,
    scopes: {},
    scopesCollapsed: true,
  },
  methods: {
    removeToken(token) {
      if (!confirm(i18n.t('warning.removeIdentifier', {identifier: token.name}))) {
        return;
      }

      this.$set(token, 'disabled', true);

      axios.delete(token._actions.remove)
        .then(() => {
          this.$refs.pagination.update();
          kadi.alert(i18n.t('success.removeToken'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert(i18n.t('error.removeToken'), {xhr: error.request});
          token.disabled = false;
        });
    },
    checkAllScopes(model, e) {
      for (const action in this.scopes[model]) {
        this.scopes[model][action].checked = e.target.checked;
      }
    },
    allScopesChecked(model) {
      for (const action in this.scopes[model]) {
        if (!this.scopes[model][action].checked) {
          return false;
        }
      }
      return true;
    },
  },
  mounted() {
    const accessTokenScopes = kadi.js_resources.access_token_scopes;
    const currentScopes = kadi.js_resources.current_scopes;
    const scopes = {};

    for (const model in accessTokenScopes) {
      scopes[model] = {};

      accessTokenScopes[model].forEach((action) => {
        let checked = false;
        if (currentScopes.includes(`${model}.${action}`)) {
          checked = true;
          this.scopesCollapsed = false;
        }
        scopes[model][action] = {checked};
      });
    }
    this.scopes = scopes;
  },
});

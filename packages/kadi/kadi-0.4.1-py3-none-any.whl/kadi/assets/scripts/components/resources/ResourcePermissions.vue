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
  <dynamic-pagination :endpoint="endpoint" :placeholder="placeholder" :per-page="perPage" ref="pagination">
    <template #default="paginationProps">
      <div class="row">
        <div class="col-lg-4">
          <p>
            <strong>{{ title }}</strong>
            <span class="badge badge-pill badge-light text-muted border border-muted">{{ paginationProps.total }}</span>
          </p>
        </div>
        <div class="col-lg-8">
          <slot></slot>
        </div>
      </div>
      <ul class="list-group">
        <li class="list-group-item py-1"
            v-for="subject in paginationProps.items"
            :key="subject.user ? subject.user.id : subject.group.id">
          <div class="row align-items-center">
            <div class="col-md-7" v-if="subject.user">
              <identity-popover :user="subject.user"></identity-popover>
              <br>
              <small>@{{ subject.user.identity.username }}</small>
            </div>
            <div class="col-md-7" v-if="subject.group">
              <a :is="subject.group._links ? 'a' : 'div'"
                 :href="subject.group._links ? subject.group._links.view : ''"
                 :class="{'text-muted': !subject.group._links}">
                <basic-resource-info :resource="subject.group"></basic-resource-info>
              </a>
            </div>
            <div class="col-md-4">
              <select class="custom-select custom-select-sm role-select"
                      v-model="subject.role.name"
                      :disabled="subject.disabled"
                      @change="changeRole(subject)">
                <option v-for="role in roles" :key="role.name" :value="role.name">{{ role.name | capitalize }}</option>
              </select>
            </div>
            <div class="col-md-1 d-md-flex justify-content-end">
              <button type="button"
                      class="btn btn-sm btn-light"
                      :disabled="subject.disabled"
                      @click="removeRole(subject)">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>
    </template>
  </dynamic-pagination>
</template>

<script>
export default {
  props: {
    title: String,
    placeholder: String,
    endpoint: String,
    roles: Array,
    perPage: {
      type: Number,
      default: 5,
    },
  },
  methods: {
    changeRole(subject) {
      this.$set(subject, 'disabled', true);

      axios.patch(subject._actions.change_role || subject._actions.change_member, {name: subject.role.name})
        .catch((error) => kadi.alert('Error changing role.', {xhr: error.request}))
        .finally(() => subject.disabled = false);
    },
    removeRole(subject) {
      const title = subject.user ? subject.user.identity.displayname : subject.group.title;
      if (!confirm(`Are you sure you want to remove '${title}'?`)) {
        return;
      }

      this.$set(subject, 'disabled', true);

      axios.delete(subject._actions.remove_role || subject._actions.remove_member)
        .then(() => {
          this.$refs.pagination.update();
          kadi.alert('Role removed successfully.', {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert('Error removing role.', {xhr: error.request});
          subject.disabled = false;
        });
    },
  },
};
</script>

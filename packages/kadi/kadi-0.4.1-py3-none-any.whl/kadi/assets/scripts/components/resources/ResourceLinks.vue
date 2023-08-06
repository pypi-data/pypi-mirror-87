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
    <template #default="props">
      <div class="row">
        <div class="col-lg-4">
          <p>
            <strong>{{ title }}</strong>
            <span class="badge badge-pill badge-light text-muted border border-muted">{{ props.total }}</span>
          </p>
        </div>
        <div class="col-lg-8">
          <slot></slot>
        </div>
      </div>
      <ul class="list-group">
        <li class="list-group-item py-1" v-for="resource in props.items" :key="resource.id">
          <div class="d-sm-flex justify-content-between align-items-center">
            <a :href="resource._links.view">
              <basic-resource-info :resource="resource"></basic-resource-info>
            </a>
            <button type="button"
                    class="btn btn-sm btn-light"
                    :disabled="resource.disabled"
                    @click="removeLink(resource)">
              <i class="fas fa-trash"></i>
            </button>
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
    perPage: {
      type: Number,
      default: 5,
    },
  },
  methods: {
    removeLink(resource) {
      if (!confirm(`Are you sure you want to remove '${resource.title}'?`)) {
        return;
      }

      this.$set(resource, 'disabled', true);

      axios.delete(resource._actions.remove_link)
        .then(() => {
          this.$refs.pagination.update();
          kadi.alert('Link removed successfully.', {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert('Error removing link.', {xhr: error.request});
          resource.disabled = false;
        });
    },
  },
};
</script>

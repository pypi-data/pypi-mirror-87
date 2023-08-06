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
    <slot :items="items" :total="total" :total-unfiltered="totalUnfiltered"></slot>
    <em class="text-muted" v-if="initialized && total === 0">{{ placeholder }}</em>
    <i class="fas fa-circle-notch fa-spin" v-if="!initialized"></i>
    <div class="row align-items-end" :class="{'mt-4': total > perPage || (enableFilter && initialized)}">
      <div class="col-sm-8 mb-2 mb-sm-0" v-show="total > perPage">
        <pagination-control :total="total" :per-page="perPage" @update-page="updatePage" ref="pagination">
          <i class="fas fa-circle-notch fa-spin ml-4 align-self-center" v-if="loading"></i>
        </pagination-control>
      </div>
      <div class="col-sm-4" v-if="enableFilter && initialized">
        <div class="input-group input-group-sm">
          <input :id="filterId" class="form-control" :placeholder="filterPlaceholder" v-model="filter">
          <clear-button :input-id="filterId" :input="filter" :small="true" @clear-input="filter = ''"></clear-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      total: 0,
      totalUnfiltered: null,
      page: 1,
      filter: '',
      filterId: kadi.utils.randomAlnum(),
      endpoint_: this.endpoint,
      initialized: false,
      loading: false,
      timeoutHandle: null,
    };
  },
  props: {
    endpoint: String,
    args: {
      type: Object,
      default: () => ({_internal: true}),
    },
    placeholder: {
      type: String,
      default: 'No data.',
    },
    perPage: {
      type: Number,
      default: 10,
    },
    enableFilter: {
      type: Boolean,
      default: false,
    },
    filterPlaceholder: {
      type: String,
      default: 'Filter',
    },
    filterParam: {
      type: String,
      default: '?filter',
    },
  },
  watch: {
    endpoint() {
      this.endpoint_ = this.endpoint;
      this.$refs.pagination.updatePage(1, true);
    },
    filter() {
      if (this.enableFilter) {
        this.endpoint_ = `${this.endpoint}${this.filterParam}=${this.filter}`;
        this.$refs.pagination.updatePage(1, true);
      }
    },
  },
  methods: {
    updatePage(page) {
      this.page = page;
      this.updateData();
    },
    updateData() {
      this.loading = true;

      if (this.timeoutHandle !== null) {
        clearTimeout(this.timeoutHandle);
      }

      this.timeoutHandle = setTimeout(() => {
        axios.get(this.endpoint_, {params: {page: this.page, per_page: this.perPage, ...this.args}})
          .then((response) => {
            this.initialized = true;
            this.items = response.data.items;
            this.total = response.data._pagination.total_items;

            if (!this.filter) {
              this.totalUnfiltered = this.total;
            }
          })
          .catch((error) => kadi.alert('Error loading data.', {xhr: error.request, scrollTo: false}))
          .finally(() => this.loading = false);
      }, 500);
    },
    // Convenience function for forcing an update from outside.
    update() {
      this.updateData();
    },
  },
  mounted() {
    this.updateData();
  },
};
</script>

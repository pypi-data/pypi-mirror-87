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
  <div class="input-group input-group-sm" v-if="totalPages > 1">
    <div class="input-group-prepend">
      <button type="button" class="btn btn-light" @click="page = 1" :disabled="page === 1">
        <i class="fas fa-angle-double-left"></i>
      </button>
    </div>
    <div class="input-group-prepend">
      <button type="button" class="btn btn-light" @click="page--" :disabled="page === 1">
        <i class="fas fa-angle-left"></i>
      </button>
    </div>
    <div class="input-group-prepend">
      <span class="input-group-text bg-light text-primary">Page</span>
    </div>
    <input class="num-control" :autocomplete="autocomplete" v-model.number="page">
    <div class="input-group-append">
      <span class="input-group-text bg-light text-primary">of {{ totalPages }}</span>
    </div>
    <div class="input-group-append">
      <button type="button" class="btn btn-light" @click="page++" :disabled="page === totalPages">
        <i class="fas fa-angle-right"></i>
      </button>
    </div>
    <div class="input-group-append">
      <button type="button" class="btn btn-light" @click="page = totalPages" :disabled="page === totalPages">
        <i class="fas fa-angle-double-right"></i>
      </button>
    </div>
    <slot></slot>
  </div>
</template>

<style scoped>
.num-control {
  text-align: center;
  width: 50px;
  border: 1px solid #dfdfdf;
  background-color: #ffffff;
}
</style>

<script>
export default {
  data() {
    return {
      page: 1,
      prevPage: 1,
      autocomplete: 'on',
    };
  },
  props: {
    total: Number,
    perPage: Number,
  },
  methods: {
    updatePage(page, forceUpdate = false) {
      this.page = page;
      if (this.page !== this.prevPage || forceUpdate) {
        this.prevPage = this.page;
        this.$emit('update-page', this.page);
      }
    },
  },
  computed: {
    totalPages() {
      let totalPages = Math.ceil(this.total / this.perPage);

      if (totalPages <= 1) {
        totalPages = 1;
        this.updatePage(totalPages);
      } else if (this.page > totalPages) {
        this.updatePage(totalPages);
      }

      return totalPages;
    },
  },
  watch: {
    page() {
      let page = this.page;

      if (page < 1 || isNaN(page)) {
        page = 1;
      } else if (page > this.totalPages) {
        page = this.totalPages;
      }

      this.updatePage(Math.round(page));
    },
  },
  mounted() {
    // Workaround related to the problem of form fields not being repopulated correctly using the back button on Chrome.
    // This component in particular leads to Chrome putting the pagination input value in some other available input
    // field, and even overwriting any value there. Doesn't seem to happen with other components so far. Obviously, this
    // still does not fix the core issue in Chrome.
    const userAgent = window.navigator.userAgent.toLowerCase();
    if ((/chrome\/\d+/).test(userAgent)) {
      this.autocomplete = 'off';
    }
  },
};
</script>

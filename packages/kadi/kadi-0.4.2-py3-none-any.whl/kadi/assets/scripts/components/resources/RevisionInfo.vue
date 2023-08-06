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
    <div v-if="initialized">
      <div class="row">
        <span class="col-md-2">User</span>
        <div :class="{'col-md-8': revision._links.view_object, 'col-md-10': !revision._links.view_object}">
          <identity-popover :user="revision.revision.user"></identity-popover>
        </div>
        <div class="col-md-2 d-md-flex justify-content-end" v-if="revision._links.view_object">
          <a class="btn btn-sm btn-light" :href="revision._links.view_object">View object</a>
        </div>
      </div>
      <div class="row mt-2">
        <span class="col-md-2">Object ID</span>
        <span class="col-md-10">{{ revision.object_id }}</span>
      </div>
      <div class="row mt-2">
        <span class="col-md-2">Timestamp</span>
        <div class="col-md-10">
          <local-timestamp :timestamp="revision.revision.timestamp"></local-timestamp>
          <br>
          <small class="text-muted">
            (<from-now :timestamp="revision.revision.timestamp"></from-now>)
          </small>
        </div>
      </div>
      <hr>
      <div v-for="(value, prop) in revision.data" :key="prop">
        <!-- First line, containing the prop and either the unchanged value or the potential previous value. -->
        <div class="row">
          <span class="col-md-2">
            <strong>{{ prop | capitalize }}</strong>
          </span>
          <!-- Unchanged value. -->
          <div class="col-md-10" v-if="!revision.diff[prop]">
            <pre class="d-inline wrap" v-if="value !== null">{{ value }}</pre>
            <pre class="d-inline" v-else><em>null</em></pre>
          </div>
          <!-- Potential previous value. -->
          <div class="col-md-10 diff-delete" v-if="revision.diff[prop]">
            <pre class="crossed d-inline wrap"
                 v-if="revision.diff[prop]['prev'] !== null">{{ revision.diff[prop]['prev'] }}</pre>
            <pre class="crossed text-muted d-inline" v-else><em>null</em></pre>
          </div>
        </div>
        <!-- Second line, containing the potential new value. -->
        <div class="row" v-if="revision.diff[prop]">
          <span class="col-md-2">&nbsp;</span>
          <!-- Potential new value. -->
          <div class="col-md-10 diff-add">
            <pre class="d-inline wrap" v-if="revision.diff[prop]['new'] !== null">{{ revision.diff[prop]['new'] }}</pre>
            <pre class="text-muted d-inline" v-else><em>null</em></pre>
          </div>
        </div>
        <br>
      </div>
    </div>
    <i class="fas fa-circle-notch fa-spin" v-if="!initialized"></i>
  </div>
</template>

<style scoped>
.diff-add {
  background-color: #ecfdf0;
}

.diff-delete {
  background-color: #fbe9eb;
}

.wrap {
  white-space: pre-wrap;
}
</style>

<script>
export default {
  data() {
    return {
      revision: null,
      initialized: false,
    };
  },
  props: {
    endpoint: String,
  },
  mounted() {
    axios.get(this.endpoint)
      .then((response) => {
        this.revision = response.data;
        this.initialized = true;
      })
      .catch((error) => kadi.alert('Error loading revision.', {xhr: error.request}));
  },
};
</script>

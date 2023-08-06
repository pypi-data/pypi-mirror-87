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
  <span>
    <small>
      <i class="fas mr-1"
         :class="{'fa-lock': resource.visibility === 'private', 'fa-lock-open': resource.visibility === 'public'}">
      </i>
    </small>
    <strong>{{ resource.title }}</strong>
    <span class="badge badge-primary font-weight-normal ml-lg-2"
          style="vertical-align: middle; margin-top: -0.4em;"
          v-if="resource.type">
      {{ resource.type }}
    </span>
    <br>
    <small>@{{ resource.identifier }}</small>
    <span v-if="enableDescription">
      <br>
      <small class="text-muted" v-if="resource.plain_description">
        {{ resource.plain_description | truncate(150) }}
      </small>
      <small class="text-muted" v-else>
        <em>No description.</em>
      </small>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    resource: Object,
    enableDescription: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

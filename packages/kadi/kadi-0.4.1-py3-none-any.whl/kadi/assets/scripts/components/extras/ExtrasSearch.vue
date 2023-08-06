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
    <div v-for="(query, index) in queries_" :key="query.id">
      <div class="form-row mb-4 mb-xl-2">
        <div class="col-xl-1 mb-1 mb-xl-0">
          <select class="custom-select custom-select-sm" v-model="query.link" v-if="index > 0">
            <option v-for="(title, value) in selectors.links" :key="value" :value="value">{{ title }}</option>
          </select>
        </div>
        <div class="col-xl-3 mb-1 mb-xl-0">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">Key</span>
            </div>
            <input class="form-control" v-model="query.key">
          </div>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">Type</span>
            </div>
            <select class="custom-select custom-select-sm" v-model="query.type">
              <option value=""></option>
              <option v-for="(title, value) in selectors.types" :key="value" :value="value">{{ title }}</option>
            </select>
          </div>
        </div>
        <div class="col-xl-1 mb-1 mb-xl-0" v-if="['numeric', 'date'].includes(query.type)">
          <select class="custom-select custom-select-sm" v-model="query.range" v-if="query.type === 'date'">
            <option v-for="(title, value) in selectors.dateRanges" :key="value" :value="value">{{ title }}</option>
          </select>
          <select class="custom-select custom-select-sm" v-model="query.range" v-if="query.type === 'numeric'">
            <option v-for="(title, value) in selectors.numRanges" :key="value" :value="value">{{ title }}</option>
          </select>
        </div>
        <div class="col-xl-4 mb-1 mb-xl-0" v-if="query.type === 'date'">
          <div class="input-group input-group-sm">
            <date-time-picker key="dateMin"
                              placeholder="Start date"
                              :initial-value="query.date.min"
                              @input="query.date.min = $event"
                              v-if="['gt', 'bt'].includes(query.range)">
            </date-time-picker>
            <date-time-picker key="dateMax"
                              placeholder="End date"
                              :initial-value="query.date.max"
                              @input="query.date.max = $event"
                              v-if="['lt', 'bt'].includes(query.range)">
            </date-time-picker>
          </div>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0" v-if="query.type === 'numeric'">
          <div class="input-group input-group-sm">
            <input class="form-control"
                   key="numMin"
                   placeholder="Minimum"
                   v-model="query.numeric.min"
                   v-if="['gt', 'bt'].includes(query.range)">
            <input class="form-control"
                   key="numMax"
                   placeholder="Maximum"
                   v-model="query.numeric.max"
                   v-if="['lt', 'bt'].includes(query.range)">
          </div>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0" v-if="query.type === 'numeric'">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">Unit</span>
            </div>
            <input class="form-control" key="numUnit" v-model="query.numeric.unit">
          </div>
        </div>
        <div class="col-xl-5 mb-1 mb-xl-0" v-if="['bool', 'str'].includes(query.type)">
          <div class="input-group input-group-sm" v-if="query.type === 'bool'">
            <div class="input-group-prepend">
              <span class="input-group-text">Value</span>
            </div>
            <select class="custom-select" v-model="query.bool">
              <option value=""></option>
              <option v-for="(title, value) in selectors.boolValues" :key="value" :value="value">{{ title }}</option>
            </select>
          </div>
          <div class="input-group input-group-sm" v-if="query.type === 'str'">
            <div class="input-group-prepend">
              <span class="input-group-text">Value</span>
            </div>
            <input class="form-control" v-model="query.str">
          </div>
        </div>
        <div class="btn-group btn-group-sm col-xl-1">
          <button type="button" class="btn btn-light" title="Add search field after" @click="addQuery(null, index)">
            <i class="fas fa-plus"></i>
          </button>
          <button type="button" class="btn btn-light" title="Remove search field" @click="removeQuery(index)">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
    <input type="hidden" name="extras" :value="serializedQuery" :disabled="!isEnabled">
    <div class="form-row my-4">
      <div class="col-md-10 mb-4 mb-md-0">
        <button type="button" class="btn btn-link text-muted p-0" @click="addQuery">
          <i class="fas fa-plus mr-1"></i> Add search field
        </button>
      </div>
      <div class="col-md-2">
        <button class="btn btn-block btn-light" type="submit">
          <i class="fas fa-search"></i> Search
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      queries_: [],
      serializedQuery: '[]',
      selectors: {
        types: {str: 'Text', bool: 'Boolean', date: 'Date', numeric: 'Numeric'},
        links: {and: 'AND', or: 'OR'},
        dateRanges: {gt: 'Later', lt: 'Before', bt: 'Between'},
        numRanges: {gt: 'Greater', lt: 'Less', bt: 'Between'},
        boolValues: {true: 'true', false: 'false'},
      },
    };
  },
  props: {
    queries: Array,
    isEnabled: Boolean,
  },
  methods: {
    addQuery(query = null, index = null) {
      const newQuery = {
        id: kadi.utils.randomAlnum(),
        key: '',
        str: '',
        type: '',
        bool: '',
        link: 'and',
        date: {min: '', max: ''},
        numeric: {min: '', max: '', unit: ''},
        range: 'gt',
      };

      if (query) {
        newQuery.key = query.key || '';
        newQuery.str = query.str || '';

        if (Object.keys(this.selectors.types).includes(query.type)) {
          newQuery.type = query.type;
        }

        if (Object.keys(this.selectors.boolValues).includes(query.bool) || [true, false].includes(query.bool)) {
          newQuery.bool = query.bool.toString();
        }

        if (Object.keys(this.selectors.links).includes(query.link)) {
          newQuery.link = query.link;
        }

        if (query.date) {
          newQuery.date.min = query.date.min || '';
          newQuery.date.max = query.date.max || '';

          if (newQuery.date.min && newQuery.date.max) {
            newQuery.range = 'bt';
          } else if (newQuery.date.max) {
            newQuery.range = 'lt';
          }
        }

        if (query.numeric) {
          newQuery.numeric.min = query.numeric.min || '';
          newQuery.numeric.max = query.numeric.max || '';
          newQuery.numeric.unit = query.numeric.unit || '';

          if (newQuery.numeric.min && newQuery.numeric.max) {
            newQuery.range = 'bt';
          } else if (newQuery.numeric.max) {
            newQuery.range = 'lt';
          }
        }
      }

      if (index !== null) {
        this.queries_.splice(index + 1, 0, newQuery);
      } else {
        this.queries_.push(newQuery);
      }
    },
    removeQuery(index) {
      this.queries_.splice(index, 1);
    },
  },
  watch: {
    queries_: {
      handler() {
        const results = [];
        for (const query of this.queries_) {
          const result = {
            type: query.type,
            link: query.link,
            key: query.key,
          };

          if (['date', 'numeric'].includes(query.type)) {
            if (Object.keys(query[query.type]).some((element) => query[query.type][element])) {
              result[query.type] = query[query.type];

              // Ignore the max value in this case.
              if (query.range === 'gt') {
                result[query.type].max = '';
              }

              // Ignore the min value in this case.
              if (query.range === 'lt') {
                result[query.type].min = '';
              }
            }
          } else {
            result[query.type] = query[query.type];
          }

          // A query needs at least a type or key in order to be included in the serialization.
          if (result.type || result.key) {
            results.push(result);
          }
        }

        this.serializedQuery = JSON.stringify(results);
      },
      deep: true,
    },
  },
  mounted() {
    if (this.queries.length > 0) {
      this.queries.forEach((query) => this.addQuery(query));
    } else {
      this.addQuery();
    }
  },
};
</script>

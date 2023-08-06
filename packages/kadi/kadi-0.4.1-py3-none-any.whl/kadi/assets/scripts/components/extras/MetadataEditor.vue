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
  <div class="mb-4" tabindex="-1" ref="editor">
    <div class="row mb-2">
      <div class="col-lg-4">
        <collapse-item :id="id">{{ label }}</collapse-item>
        <popover-toggle toggle-class="btn btn-sm btn-link text-primary">
          <template #toggle>
            <i class="fas fa-question-circle"></i>
          </template>
          <template #content>
            <p>
              An entry's position can be changed by dragging an add-on of any input (e.g. the grey 'Key' label).
              Additionally, the following keyboard shortcuts are supported as long as the editor is in focus:
            </p>
            <dl class="row mb-0">
              <dt class="col-3"><strong>Ctrl+B</strong></dt>
              <dd class="col-9">Toggle the copy/remove button.</dd>
              <dt class="col-3"><strong>Ctrl+E</strong></dt>
              <dd class="col-9">Toggle the tree/editor view.</dd>
              <dt class="col-3"><strong>Ctrl+I</strong></dt>
              <dd class="col-9">Add a new entry in the same layer as the current input.</dd>
              <dt class="col-3"><strong>Ctrl+Y</strong></dt>
              <dd class="col-9">Redo the previous step (up to 10 steps are recorded).</dd>
              <dt class="col-3"><strong>Ctrl+Z</strong></dt>
              <dd class="col-9">Undo the last step (up to 10 steps are recorded).</dd>
            </dl>
          </template>
        </popover-toggle>
      </div>
      <div class="col-lg-8 d-lg-flex justify-content-end">
        <div class="btn-group btn-group-sm">
          <button type="button"
                  class="btn btn-link text-muted"
                  title="Undo (Ctrl+Z)"
                  tabindex="-1"
                  :disabled="!undoable"
                  @click="undo">
            <i class="fas fa-undo"></i> Undo
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  title="Redo (Ctrl+Y)"
                  tabindex="-1"
                  :disabled="!redoable"
                  @click="redo">
            <i class="fas fa-redo"></i> Redo
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  title="Toggle copy/remove button (Ctrl+B)"
                  tabindex="-1"
                  @click="toggleCopy = !toggleCopy">
            <span v-if="toggleCopy">
              <i class="fas fa-times"></i> Remove
            </span>
            <span v-else>
              <i class="fas fa-copy"></i> Copy
            </span>
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  title="Reset editor"
                  tabindex="-1"
                  @click="resetEditor">
            <i class="fas fa-sync-alt"></i> Reset
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  title="Toggle view (Ctrl+E)"
                  tabindex="-1"
                  @click="showTree = !showTree">
            <span v-if="showTree">
              <i class="fas fa-edit"></i> Editor view
            </span>
            <span v-else>
              <i class="fas fa-list"></i> Tree view
            </span>
          </button>
        </div>
      </div>
    </div>
    <div :id="id" class="collapse show">
      <div v-show="!showTree">
        <extra-metadata :extras="extras" :toggle-copy="toggleCopy" @save-checkpoint="saveCheckpoint" ref="extras">
          <div class="form-row align-items-center" v-if="templateEndpoint">
            <div class="offset-xl-7 col-xl-5 mt-2 mt-xl-0">
              <dynamic-selection placeholder="Select a metadata template"
                                 container-classes="select2-single-sm"
                                 :endpoint="templateEndpoint"
                                 :reset-on-select="true"
                                 @select="loadTemplate">
              </dynamic-selection>
            </div>
          </div>
        </extra-metadata>
      </div>
      <div class="card" v-show="showTree">
        <div class="card-body text-break py-3 px-3">
          <extra-tree-view :extras="extras" @focus-extra="focusExtra"></extra-tree-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import undoRedoMixin from 'scripts/lib/mixins/undo-redo-mixin';

export default {
  mixins: [undoRedoMixin],
  data() {
    return {
      extras: [],
      toggleCopy: false,
      showTree: false,
      numInitialFields: 3,
    };
  },
  props: {
    id: {
      type: String,
      default: 'metadata-editor',
    },
    label: {
      type: String,
      default: 'Extra metadata',
    },
    templateEndpoint: {
      type: String,
      default: null,
    },
  },
  methods: {
    focusExtra(extra) {
      this.showTree = false;
      this.$nextTick(() => this.$refs.extras.focusExtra(extra));
    },
    extraIsEmpty(extra) {
      if (extra.key.value === '' && extra.value.value === '' && extra.unit.value === '') {
        return true;
      }
      return false;
    },
    initializeFields() {
      for (let i = 0; i < this.numInitialFields; i++) {
        this.$refs.extras.addExtra(null, false);
      }
    },
    initializeEditor(extras = null) {
      this.$refs.extras.removeExtras(false);
      if (extras) {
        this.$refs.extras.addExtras(extras, false);
      } else {
        this.initializeFields();
      }
      this.resetCheckpoints();
      this.saveCheckpoint();
    },
    resetEditor() {
      const reset = () => {
        this.$refs.extras.removeExtras(false);
        this.initializeFields();
        this.saveCheckpoint();
      };

      // Only reset the editor if it is not in initial state already.
      if (this.extras.length === this.numInitialFields) {
        for (const extra of this.extras) {
          if (!this.extraIsEmpty(extra)) {
            reset();
            return;
          }
        }
      } else {
        reset();
      }
    },
    loadTemplate(data) {
      axios.get(data.endpoint)
        .then((response) => {
          this.extras.slice().forEach((extra) => {
            // Remove completely empty extras.
            if (this.extraIsEmpty(extra)) {
              this.$refs.extras.removeExtra(extra, false);
            }
          });

          this.$refs.extras.addExtras(response.data.data);
        })
        .catch((error) => kadi.alert('Error loading template.', {xhr: error.request}));
    },
    keydownHandler(e) {
      // Keycodes: 66 = B, 69 = E, 89 = Y, 90 = Z
      if (e.ctrlKey) {
        if (e.keyCode === 66) {
          e.preventDefault();
          this.toggleCopy = !this.toggleCopy;
        } else if (e.keyCode === 69) {
          e.preventDefault();
          this.showTree = !this.showTree;
          this.$refs.editor.focus();
        } else if (e.keyCode === 89) {
          e.preventDefault();
          this.redo();
          this.$refs.editor.focus();
        } else if (e.keyCode === 90) {
          e.preventDefault();
          this.undo();
          this.$refs.editor.focus();
        }
      }
    },
    getCheckpointData() {
      const checkpointData = [];
      this.extras.forEach((extra) => checkpointData.push(this.$refs.extras.getExtraFormdata(extra)));
      return checkpointData;
    },
    restoreCheckpointData(data) {
      this.$refs.extras.removeExtras(false);
      this.$refs.extras.addExtras(data, false);
    },
    /* eslint-disable no-unused-vars */
    verifyCheckpointData(currentData, newData) {
      // Dispatch a native change event every time a checkpoint is created.
      this.$el.dispatchEvent(new Event('change', {bubbles: true}));
      return true;
    },
    /* eslint-enable no-unused-vars */
  },
  mounted() {
    this.initializeEditor();
    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>

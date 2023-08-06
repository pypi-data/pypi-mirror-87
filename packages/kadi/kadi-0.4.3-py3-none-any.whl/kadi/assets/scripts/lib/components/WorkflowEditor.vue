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
  <div class="card" ref="container">
    <div class="card-header" v-if="editable">
      <div class="row" v-if="!loadingWorkflow">
        <div class="col-xl-5">
          <div v-if="currentWorkflow">
            <tooltip-item title="Unsaved changes." v-if="unsavedChanges">
              <i class="fas fa-exclamation-triangle"></i>
            </tooltip-item>
            {{ currentWorkflow.name }}
            <br>
            <small class="text-muted">
              {{ i18n.t('misc.createdAt') }}
              <local-timestamp :timestamp="currentWorkflow.created_at"></local-timestamp>
            </small>
            <br>
            <small class="text-muted">
              {{ i18n.t('misc.lastModifiedAt') }}
              <local-timestamp :timestamp="currentWorkflow.last_modified"></local-timestamp>
            </small>
          </div>
          <div v-else>
            {{ name }}
            <br>
            <small class="text-muted">(Unsaved)</small>
          </div>
        </div>
        <div class="col-xl-7">
          <input class="form-control form-control-sm text-primary mb-2" v-model="name" @input="unsavedChanges = true">
          <div class="btn-group btn-group-sm d-flex">
            <button class="btn btn-sm btn-light"
                    :disabled="requestInProgress"
                    @click="newWorkflow">
              <i class="fas fa-plus-square"></i> New
            </button>
            <button class="btn btn-sm btn-light"
                    :disabled="requestInProgress"
                    @click="loadingWorkflow = true"
                    v-if="selectWorkflowsEndpoint">
              <i class="fas fa-file"></i> Load
            </button>
            <button class="btn btn-sm btn-light"
                    :disabled="requestInProgress"
                    @click="saveWorkflow(false)"
                    v-if="newWorkflowEndpoint">
              <i class="fas fa-save"></i> Save
            </button>
            <button class="btn btn-sm btn-light"
                    :disabled="requestInProgress || !currentWorkflow"
                    @click="saveWorkflow(true)"
                    v-if="newWorkflowEndpoint">
              <i class="fas fa-save"></i> Save as copy
            </button>
            <button class="btn btn-sm btn-light"
                    :disabled="requestInProgress || !currentWorkflow"
                    @click="deleteWorkflow">
              <i class="fas fa-trash"></i> Delete
            </button>
          </div>
        </div>
      </div>
      <div v-if="loadingWorkflow">
        <div class="row">
          <div class="col-sm-2">
            <button class="btn btn-sm btn-light" @click="loadingWorkflow = false">
              <i class="fas fa-chevron-left"></i> Back
            </button>
          </div>
          <div class="col-sm-10">
            <dynamic-selection placeholder="Select a workflow"
                               container-classes="select2-single-sm"
                               :endpoint="selectWorkflowsEndpoint"
                               :reset-on-select="true"
                               @select="loadWorkflow($event.endpoint)">
            </dynamic-selection>
          </div>
        </div>
      </div>
    </div>
    <div style="height: 75vh;" ref="editorContainer">
      <div class="position-absolute" style="right: 0; z-index: 1;" ref="editorToolbar">
        <button class="btn btn-link text-muted"
                title="Reset view"
                :disabled="requestInProgress"
                @click="resetView">
          <i class="fas fa-eye"></i>
        </button>
        <button class="btn btn-link text-muted"
                title="Toggle fullscreen"
                :disabled="requestInProgress"
                @click="toggleFullscreen">
          <i class="fas fa-expand"></i>
        </button>
        <button class="btn btn-link text-muted"
                title="Download"
                :disabled="requestInProgress"
                @click="downloadWorkflow"
                v-if="currentWorkflow && !unsavedChanges">
          <i class="fas fa-download"></i>
        </button>
        <a :href="currentWorkflow._links.download" class="d-none" v-if="currentWorkflow" ref="download"></a>
      </div>
      <div ref="editor"></div>
    </div>
  </div>
</template>

<script>
import 'regenerator-runtime';
import Rete from 'rete';
import AreaPlugin from 'rete-area-plugin';
import ConnectionPlugin from 'rete-connection-plugin';
import ConnectionMasteryPlugin from 'rete-connection-mastery-plugin';
import ContextMenuPlugin from 'rete-context-menu-plugin';
import VueRenderPlugin from 'rete-vue-render-plugin';

import WorkflowEditor from 'scripts/lib/workflows/core';
import Menu from 'scripts/lib/workflows/Menu.vue';

import IntComponent from 'scripts/lib/workflows/components/IntComponent';
import FloatComponent from 'scripts/lib/workflows/components/FloatComponent';
import StringComponent from 'scripts/lib/workflows/components/StringComponent';
import BoolComponent from 'scripts/lib/workflows/components/BoolComponent';
import FileOutComponent from 'scripts/lib/workflows/components/FileOutComponent';
import FileInComponent from 'scripts/lib/workflows/components/FileInComponent';
import UserInputTextComponent from 'scripts/lib/workflows/components/UserInputTextComponent';
import UserInputFileComponent from 'scripts/lib/workflows/components/UserInputFileComponent';
import UserInputCropImagesComponent from 'scripts/lib/workflows/components/UserInputCropImagesComponent';
import CustomComponent from 'scripts/lib/workflows/components/CustomComponent';

import scalardata2image from 'scripts/lib/workflows/xml/scalardata2image';
import fieldtransformData from 'scripts/lib/workflows/xml/fieldtransform';
import volumeData from 'scripts/lib/workflows/xml/volume';
import infile2simgeoData from 'scripts/lib/workflows/xml/infile2simgeo';
import toolcombineData from 'scripts/lib/workflows/xml/toolcombine';
import StartReportData from 'scripts/lib/workflows/xml/StartReport';
import TextReportData from 'scripts/lib/workflows/xml/TextReport';
import EndReportData from 'scripts/lib/workflows/xml/EndReport';
import ImageJMacroData from 'scripts/lib/workflows/xml/ImageJMacro';
import mkdirData from 'scripts/lib/workflows/xml/systemMkdir';

import 'styles/workflows/workflow-editor.scss';

export default {
  data() {
    return {
      name: '',
      editor: null,
      engine: null,
      area: null,
      currentWorkflow: null,
      loadingWorkflow: false,
      requestInProgress: false,
      unsavedChanges: false,
    };
  },
  props: {
    version: {
      type: String,
      default: 'kadi@0.1.0',
    },
    newWorkflowEndpoint: {
      type: String,
      default: null,
    },
    selectWorkflowsEndpoint: {
      type: String,
      default: null,
    },
    initialWorkflowEndpoint: {
      type: String,
      default: null,
    },
    editable: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    confirmDiscard() {
      if (this.unsavedChanges && !confirm('Are you sure you want to discard all current changes?')) {
        return false;
      }

      return true;
    },

    resetEditor() {
      this.editor.silent = true;
      this.editor.clear();
      this.editor.silent = false;

      this.currentWorkflow = null;
      this.unsavedChanges = false;
      this.name = 'Untitled workflow';
    },

    updateCurrentWorkflow(workflow) {
      this.currentWorkflow = workflow;
      this.unsavedChanges = false;
      this.name = workflow.name;
    },

    newWorkflow() {
      if (!this.confirmDiscard()) {
        return;
      }

      this.resetEditor();
    },

    saveWorkflow(asCopy) {
      let method = null;
      let endpoint = null;
      let msg = '';

      if (this.currentWorkflow !== null && !asCopy) {
        method = axios.patch;
        endpoint = this.currentWorkflow._actions.edit;
        msg = 'Workflow updated successfully.';
      } else {
        method = axios.post;
        endpoint = this.newWorkflowEndpoint;
        msg = 'Workflow saved successfully.';
      }

      this.requestInProgress = true;

      method(endpoint, {name: this.name, data: this.editor.toJSON()})
        .then((response) => {
          this.updateCurrentWorkflow(response.data);
          kadi.alert(msg, {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          if (error.request.status === 400) {
            kadi.alert('Invalid name or workflow data.');
          } else {
            kadi.alert('Error saving workflow.', {xhr: error.request});
          }
        })
        .finally(() => this.requestInProgress = false);
    },

    loadWorkflow(endpoint) {
      if (!this.confirmDiscard()) {
        return;
      }

      this.loadingWorkflow = false;

      axios.get(endpoint)
        .then((response) => {
          this.editor.fromJSON(response.data.data)
            .then((success) => {
              if (!success) {
                kadi.alert('Could not fully reconstruct workflow.', {type: 'warning'});
              }
            })
            .catch((error) => {
              console.error(error);
              kadi.alert('Error parsing workflow data.');
            })
            .finally(() => {
              this.resetView();
              this.updateCurrentWorkflow(response.data);
            });
        })
        .catch((error) => kadi.alert('Error loading workflow.', {xhr: error.request}));
    },

    deleteWorkflow() {
      const msg = `Are you sure you want to delete '${this.currentWorkflow.name}'?`;
      if (!confirm(msg)) {
        return;
      }

      this.requestInProgress = true;

      axios.delete(this.currentWorkflow._actions.remove)
        .then(() => {
          this.resetEditor();
          kadi.alert('Workflow deleted successfully.', {type: 'success'});
        })
        .catch((error) => kadi.alert('Error deleting workflow.', {xhr: error.request}))
        .finally(() => this.requestInProgress = false);
    },

    resetView() {
      this.area.zoomAt(this.editor);
    },

    toggleFullscreen() {
      if (document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen) {
        document.exitFullscreen();
        this.$refs.container.style.borderRadius = '0.25rem';
        this.$refs.editorContainer.style.height = '75vh';
      } else {
        this.$refs.container.requestFullscreen();
        this.$refs.container.style.borderRadius = '0';
        this.$refs.editorContainer.style.height = '100vh';
      }
    },

    downloadWorkflow() {
      this.$refs.download.click();
    },
  },
  computed: {
    toolbarBtnClass() {
      return 'btn btn-sm btn-light text-primary';
    },
  },
  mounted() {
    // Disable some events if the editor is not editable.
    if (!this.editable) {
      let handler = (e) => {
        if (!Array.from(this.$refs.editorToolbar.getElementsByTagName('*')).includes(e.target)) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('click', handler, {capture: true});

      handler = (e) => {
        if (e.target !== this.$refs.editor) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('pointerdown', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('pointerup', handler, {capture: true});

      handler = (e) => {
        e.preventDefault();
        e.stopPropagation();
      };
      this.$refs.editorContainer.addEventListener('dblclick', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('contextmenu', handler, {capture: true});
    }

    // Initialize the editor and its plugins.
    this.editor = new WorkflowEditor(this.version, this.$refs.editor);
    this.engine = new Rete.Engine(this.version);
    this.area = AreaPlugin;

    this.editor.use(AreaPlugin);
    this.editor.use(ConnectionPlugin);
    this.editor.use(VueRenderPlugin);
    this.editor.use(ConnectionMasteryPlugin);
    this.editor.use(ContextMenuPlugin, {
      vueComponent: Menu,
      searchBar: false,
      delay: 10,
      items: {
        'Debug': {
          /* eslint-disable no-console */
          'Dump JSONflow': () => console.log(this.editor.toJSON()),
          'Dump JSONrete': () => console.log(this.editor.toJSONrete()),
          /* eslint-enable no-console */
        },
      },
      allocate(component) {
        if (component.componentType === 'ToolNode') {
          return ['Tool'];
        } else if (component.componentType === 'InputOutput') {
          return ['Input/Output'];
        } else if (component.componentType === 'PromptNode') {
          return ['Prompt'];
        }
        return ['Source'];
      },
      rename(component) {
        return component.name;
      },
    });

    // Register all components and sockets.
    const numSocket = new Rete.Socket('num');
    const strSocket = new Rete.Socket('str');
    const flagSocket = new Rete.Socket('bool');
    const depSocket = new Rete.Socket('dep');

    const anyTypeSocket = new Rete.Socket('any');
    anyTypeSocket.combineWith(numSocket);
    anyTypeSocket.combineWith(strSocket);
    anyTypeSocket.combineWith(flagSocket);

    const intComponent = new IntComponent(numSocket);
    const floatComponent = new FloatComponent(numSocket);
    const strComponent = new StringComponent(strSocket);
    const boolComponent = new BoolComponent(flagSocket);
    const fileOutComponent = new FileOutComponent(strSocket, flagSocket, depSocket, anyTypeSocket);
    const fileInComponent = new FileInComponent(strSocket, depSocket, anyTypeSocket);
    const userInputTextComponent = new UserInputTextComponent(strSocket, depSocket);
    const userInputFileComponent = new UserInputFileComponent(strSocket, depSocket);
    const userInputCropImagesComponent = new UserInputCropImagesComponent(strSocket, depSocket);

    const customComponentSockets = [numSocket, strSocket, flagSocket, depSocket, anyTypeSocket];
    const customComponent = new CustomComponent(scalardata2image, ...customComponentSockets);
    const fieldtransform = new CustomComponent(fieldtransformData, ...customComponentSockets);
    const volume = new CustomComponent(volumeData, ...customComponentSockets);
    const infile2simgeo = new CustomComponent(infile2simgeoData, ...customComponentSockets);
    const toolcombine = new CustomComponent(toolcombineData, ...customComponentSockets);
    const StartReport = new CustomComponent(StartReportData, ...customComponentSockets);
    const TextReport = new CustomComponent(TextReportData, ...customComponentSockets);
    const EndReport = new CustomComponent(EndReportData, ...customComponentSockets);
    const ImageJMacro = new CustomComponent(ImageJMacroData, ...customComponentSockets);
    const mkdir = new CustomComponent(mkdirData, ...customComponentSockets);

    [
      intComponent,
      floatComponent,
      strComponent,
      boolComponent,
      fileOutComponent,
      fileInComponent,
      userInputTextComponent,
      userInputFileComponent,
      userInputCropImagesComponent,
      customComponent,
      fieldtransform,
      volume,
      infile2simgeo,
      toolcombine,
      StartReport,
      TextReport,
      EndReport,
      ImageJMacro,
      mkdir,
    ].forEach((c) => {
      this.editor.register(c);
      this.engine.register(c);
    });

    this.editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async() => {
      // This flag is set when calling fromJSON, in which case we can ignore the events.
      if (this.editor.silent) {
        return;
      }

      await this.engine.abort();
      await this.engine.process(this.editor.toJSONrete());
    });

    // TODO: Needs another event when changing controls (could propably be done easiest in a custom node).
    this.editor.on('nodecreated noderemoved connectioncreated connectionremoved nodetranslated', () => {
      this.unsavedChanges = true;
    });

    this.editor.on('click', () => {
      this.editor.selected.clear();
      this.editor.nodes.map((n) => n.update());
    });

    this.editor.on('zoom', ({source}) => {
      return source !== 'dblclick';
    });

    // Finalize initialization.
    this.editor.view.resize();
    this.resetEditor();

    // In case the fullscreen is exited using the escape key.
    window.addEventListener('fullscreenchange', () => {
      const isFullscreen = document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
      if (!isFullscreen) {
        this.$refs.container.style.borderRadius = '0.25rem';
        this.$refs.editorContainer.style.height = '75vh';
      }

      // We use a timeout and hope the container has the correct size once it is over.
      setTimeout(() => this.resetView(), 250);
    });

    /* eslint-disable consistent-return */
    window.addEventListener('beforeunload', (e) => {
      if (this.unsavedChanges) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
    });
    /* eslint-enable consistent-return */

    if (this.initialWorkflowEndpoint) {
      this.loadWorkflow(this.initialWorkflowEndpoint);
    }
  },
};
</script>

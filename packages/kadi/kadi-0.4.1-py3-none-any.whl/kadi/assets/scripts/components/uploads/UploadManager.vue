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
    <upload-dropzone @add-file="addFile"></upload-dropzone>
    <input class="input" type="file" @change="inputChange" ref="input">
    <div class="card bg-light py-2 px-4 mt-4 mb-3" v-if="uploads.length > 0">
      <div class="form-row align-items-center">
        <div class="col-xl-8">
          {{ `${completedUploadsCount}/${uploads.length} ${i18n.t('uploads.completed', {count: uploads.length})}` }}
          <i class="fas fa-xs fa-check ml-2" v-if="completedUploadsCount === uploads.length"></i>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <small class="text-muted">{{ totalUploadSize | filesizeFormat }}</small>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <div class="btn-group btn-group-sm">
            <button class="btn btn-primary"
                    :title="i18n.t('uploads.resumeAll')"
                    :disabled="!resumable"
                    @click="resumeUploads(null)">
              <i class="fas fa-play"></i>
            </button>
            <button class="btn btn-primary"
                    :title="i18n.t('uploads.pauseAll')"
                    :disabled="!pausable"
                    @click="pauseUploads(false)">
              <i class="fas fa-pause"></i>
            </button>
            <button class="btn btn-primary"
                    :title="i18n.t('uploads.cancelAll')"
                    :disabled="!cancelable"
                    @click="cancelUploads(false)">
              <i class="fas fa-ban"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card"
         :class="{'mb-3': index < uploads.length - 1}"
         v-for="(upload, index) in paginatedUploads"
         :key="upload.id">
      <div class="card-body py-2">
        <div class="form-row align-items-center" :class="{'mb-2': upload.state !== 'completed'}">
          <div class="col-xl-5">
            <strong v-if="upload.chunkCount">
              <a :href="upload.viewFileEndpoint" v-if="upload.viewFileEndpoint">{{ upload.name }}</a>
              <span v-else>{{ upload.name }}</span>
            </strong>
            <span class="text-muted" v-else>{{ upload.name }}</span>
          </div>
          <div class="col-xl-3">{{ upload.mimetype }}</div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <small class="text-muted">{{ upload.size | filesizeFormat }}</small>
          </div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <span class="badge badge-primary">{{ stateNames[upload.state] }}</span>
          </div>
        </div>
        <div class="form-row align-items-center" v-if="upload.state !== 'completed'">
          <div class="col-xl-10 py-1">
            <div class="progress border border-muted" style="height: 17px;">
              <div class="progress-bar" :style="{width: Math.floor(upload.progress) + '%'}">
                {{ Math.floor(upload.progress) }}%
              </div>
            </div>
          </div>
          <div class="col-xl-2 mt-2 mt-xl-0 d-xl-flex justify-content-end">
            <i class="fas fa-circle-notch fa-spin" v-if="upload.state === 'processing'"></i>
            <div class="btn-group btn-group-sm">
              <button class="btn btn-light"
                      :title="i18n.t('uploads.pause')"
                      @click="pauseUploads(false, upload)"
                      v-if="['pending', 'uploading'].includes(upload.state)">
                <i class="fas fa-pause"></i>
              </button>
              <button class="btn btn-light"
                      :title="i18n.t('uploads.resume')"
                      @click="resumeUploads(upload)"
                      v-if="upload.state === 'paused'">
                <i class="fas fa-play" v-if="isResumable(upload)"></i>
                <i class="fas fa-folder-open" v-else></i>
              </button>
              <button class="btn btn-light"
                      :title="i18n.t('uploads.cancel')"
                      @click="cancelUploads(false, upload)"
                      v-if="['pending', 'paused', 'uploading'].includes(upload.state)">
                <i class="fas fa-ban"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white py-1" v-if="upload.replacedFile !== null || upload.createdAt !== null">
        <div class="d-flex justify-content-between">
          <div>
            <div v-if="upload.replacedFile !== null">
              <span class="text-muted">{{ i18n.t('uploads.replaces') }}</span>
              <a class="text-muted" :href="upload.replacedFile._links.view">
                <strong>{{ upload.replacedFile.name }}</strong>
              </a>
            </div>
          </div>
          <div>
            <small class="text-muted" v-if="upload.createdAt !== null">
              {{ i18n.t('misc.createdAt') }} <local-timestamp :timestamp="upload.createdAt"></local-timestamp>
            </small>
          </div>
        </div>
      </div>
    </div>
    <pagination-control :total="uploads.length" :per-page="perPage" @update-page="page = $event"></pagination-control>
  </div>
</template>

<style scoped>
.input {
  position: absolute;
  visibility: hidden;
}
</style>

<script>
export default {
  data() {
    return {
      uploads: [],
      uploadQueue: [],
      addedFileTimeoutHandle: null,
      resumedUpload: null,
      page: 1,
      stateNames: {
        paused: i18n.t('uploads.statePaused'),
        pending: i18n.t('uploads.statePending'),
        uploading: i18n.t('uploads.stateUploading'),
        processing: i18n.t('uploads.stateProcessing'),
        completed: i18n.t('uploads.stateCompleted'),
      },
    };
  },
  props: {
    newUploadEndpoint: String,
    getUploadsEndpoint: String,
    perPage: {
      type: Number,
      default: 5,
    },
  },
  watch: {
    uploadQueue() {
      if (this.addedFileTimeoutHandle !== null) {
        clearTimeout(this.addedFileTimeoutHandle);
      }

      this.addedFileTimeoutHandle = setTimeout(() => this.uploadNextFile(), 100);
    },
  },
  methods: {
    addFile(file) {
      const upload = {
        id: kadi.utils.randomAlnum(), // For use in v-for before the upload has an actual ID.
        name: file.name,
        size: file.size,
        state: 'pending',
        chunks: [],
        file,
        progress: 0,
        source: null,
        mimetype: null,
        chunkSize: null,
        chunkCount: null,
        replacedFile: null,
        createdAt: null,
        uploadChunkEndpoint: null,
        finishUploadEndpoint: null,
        deleteUploadEndpoint: null,
        getStatusEndpoint: null,
        viewFileEndpoint: null,
      };

      this.uploadQueue.push(upload);
      this.uploads.push(upload);
    },

    inputChange(e) {
      const file = e.target.files[0];
      if (file.size !== this.resumedUpload.size) {
        if (!confirm(i18n.t('warning.uploadSizeDiffers'))) {
          return;
        }
      }

      this.resumedUpload.file = file;
      this.resumedUpload.state = 'pending';
      this.uploadQueue.push(this.resumedUpload);
    },

    async uploadNextFile() {
      if (this.uploadQueue.length > 0 && !this.uploadInProgress) {
        const upload = this.uploadQueue[0];
        upload.state = 'uploading';

        // Check if the upload was already initiated. We could check any property that will be set from the backend.
        if (!upload.chunkCount) {
          const _errorInitiatingUpload = (error) => {
            // Some quota was exceeded.
            if (error.request.status === 413) {
              // Use the error message from the backend.
              kadi.alert(error.response.data.description, {type: 'warning'});
            } else {
              kadi.alert(i18n.t('error.initiateUpload'), {xhr: error.request});
            }
            this.cancelUploads(true, upload);
          };

          try {
            await this.initiateUpload(upload);
          } catch (error) {
            // A file with that name already exists in the current record.
            if (error.request.status === 409) {
              if (!confirm(i18n.t('warning.replaceUpload', {filename: upload.name}))) {
                this.cancelUploads(true, upload);
                return;
              }

              try {
                await this.initiateUpload(upload, error.response.data.file._actions.edit_data);
                // eslint-disable-next-line require-atomic-updates
                upload.replacedFile = error.response.data.file;
              } catch (error) {
                _errorInitiatingUpload(error);
                return;
              }
            } else {
              _errorInitiatingUpload(error);
              return;
            }
          }
        }

        /* Loop until all chunks have been uploaded successfully. We upload each chunk sequentially, as parallel chunk
           uploads are probably not faster at the moment. */
        while (true) {
          // The upload state was modified from outside.
          if (upload.state !== 'uploading') {
            return;
          }

          // Find the next chunk index to upload.
          let chunkIndex = null;
          for (let index = 0; index < upload.chunkCount; index++) {
            const found = upload.chunks.find((chunk) => chunk.index === index && chunk.state === 'active');
            if (!found) {
              chunkIndex = index;
              break;
            }
          }

          // No index for the next chunk could be found, so we are done uploading.
          if (chunkIndex === null) {
            break;
          }

          const start = chunkIndex * upload.chunkSize;
          const end = Math.min(start + upload.chunkSize, upload.size);
          const blob = upload.file.slice(start, end);

          let timeout = 0;
          while (true) {
            // The upload state was modified from outside.
            if (upload.state !== 'uploading') {
              return;
            }

            try {
              /* eslint-disable no-await-in-loop */
              await this.uploadChunk(upload, blob, chunkIndex);
              break;
            } catch (error) {
              // Check if the request was cancelled from outside.
              if (axios.isCancel(error)) {
                return;
              }

              // There is no point in retrying when some quota was exceeded.
              if (error.request.status === 413) {
                // Use the error message from the backend.
                kadi.alert(error.response.data.description, {type: 'warning'});
                this.pauseUploads(false, upload);
                return;
              }

              timeout += 5000;
              kadi.alert(i18n.t('error.uploadChunk', {timeout: timeout / 1000}), {xhr: error.request, timeout});
              await kadi.utils.sleep(timeout);
              /* eslint-enable no-await-in-loop */
            }
          }
        }

        // eslint-disable-next-line require-atomic-updates
        upload.state = 'processing';

        try {
          await this.finishUpload(upload);
        } catch (error) {
          if (error.request.status === 413) {
            // Use the error message from the backend.
            kadi.alert(error.response.data.description, {type: 'warning'});
          } else {
            kadi.alert(i18n.t('error.finishUpload'), {xhr: error.request});
          }
          this.pauseUploads(true, upload);
          return;
        }

        this.finalizeUpload(upload);

        this.uploadQueue.shift();
      }
    },

    initiateUpload(upload, endpoint = null) {
      let _endpoint = endpoint;
      let requestFunc = null;
      let data = null;

      if (!_endpoint) {
        _endpoint = this.newUploadEndpoint;
        requestFunc = axios.post;
        data = {name: upload.name, size: upload.size};
      } else {
        requestFunc = axios.put;
        data = {size: upload.size};
      }

      return requestFunc(_endpoint, data)
        .then((response) => {
          const data = response.data;
          upload.id = data.id;
          upload.mimetype = data.mimetype;
          upload.chunkSize = data._meta.chunk_size;
          upload.chunkCount = data.chunk_count;
          upload.createdAt = data.created_at;
          upload.uploadChunkEndpoint = data._actions.upload_chunk;
          upload.finishUploadEndpoint = data._actions.finish_upload;
          upload.deleteUploadEndpoint = data._actions.delete;
          upload.getStatusEndpoint = data._links.status;
        });
    },

    uploadChunk(upload, blob, index) {
      // The chunk and its metadata is uploaded using multipart/form-data encoding.
      const chunkFormData = new FormData();
      chunkFormData.append('blob', blob);
      chunkFormData.append('index', index);
      chunkFormData.append('size', blob.size);

      // The cancel token allows us to cancel an ongoing request.
      const source = axios.CancelToken.source();
      upload.source = source;

      const config = {
        onUploadProgress: (e) => {
          // Stop the progress from jumping around when pausing the upload.
          upload.progress = Math.max(this.getUploadProgress(upload, Math.min(e.loaded, blob.size)), upload.progress);
        },
        cancelToken: source.token,
      };

      return axios.put(upload.uploadChunkEndpoint, chunkFormData, config)
        .then((response) => {
          upload.chunks = response.data.chunks;
          upload.progress = this.getUploadProgress(upload);
        })
        .finally(() => upload.source = null);
    },

    finishUpload(upload) {
      return axios.post(upload.finishUploadEndpoint);
    },

    finalizeUpload(upload) {
      /* Try to update the status periodically using a randomized timeout to distribute load a bit in case of many
         files. */
      let timeout = Math.floor(Math.random() * 5000);

      const _updateStatus = () => {
        if (timeout < 30000) {
          timeout += 2000;
        }

        axios.get(upload.getStatusEndpoint, {params: {_internal: true}})
          .then((response) => {
            const data = response.data;
            if (data.state === 'processing') {
              setTimeout(_updateStatus, timeout);
            } else if (data.state === 'inactive') {
              // Check the status of the upload processing task.
              if (data._meta.file) {
                upload.state = 'completed';
                upload.viewFileEndpoint = data._meta.file._links.view;
              } else if (data._meta.error) {
                kadi.alert(data._meta.error);
                this.cancelUploads(true, upload);
              } else {
                setTimeout(_updateStatus, timeout);
              }
            }
          })
          .catch((error) => kadi.alert(i18n.t('error.updateStatus'), {xhr: error.request}));
      };

      setTimeout(_updateStatus, timeout);
    },

    cancelUploads(force, upload = null) {
      const _removeUpload = (upload) => {
        kadi.utils.removeFromList(this.uploadQueue, upload);
        kadi.utils.removeFromList(this.uploads, upload);
      };

      let uploads = [];
      let message = '';

      if (upload === null) {
        uploads = this.uploads.slice();
        message = i18n.t('warning.cancelUploads');
      } else {
        uploads.push(upload);
        message = i18n.t('warning.cancelUpload', {filename: upload.name});
      }

      if (!force && !confirm(message)) {
        return;
      }

      for (const _upload of uploads) {
        // If the upload is already processing or completed we just ignore the cancel request.
        if (!force && ['processing', 'completed'].includes(_upload.state)) {
          continue;
        }

        // Cancel the current chunk upload if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        // If the upload was already initiated, try to delete it.
        if (_upload.deleteUploadEndpoint) {
          axios.delete(_upload.deleteUploadEndpoint)
            .then(() => _removeUpload(_upload))
            .catch((error) => {
              if (error.request.status !== 404) {
                kadi.alert(i18n.t('error.removeUpload'), {xhr: error.request});
              } else {
                _removeUpload(_upload);
              }
            });
        } else {
          _removeUpload(_upload);
        }
      }
    },

    pauseUploads(force, upload = null) {
      let uploads = [];
      if (upload === null) {
        uploads = this.uploads.slice();
      } else {
        uploads.push(upload);
      }

      for (const _upload of uploads) {
        // If the upload is already processing or completed we just ignore the pause request.
        if (!force && ['processing', 'completed'].includes(_upload.state)) {
          continue;
        }

        _upload.state = 'paused';

        // Cancel the current chunk upload if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        kadi.utils.removeFromList(this.uploadQueue, _upload);
      }
    },

    resumeUploads(upload = null) {
      if (upload !== null) {
        if (this.isResumable(upload)) {
          // The upload was started in the current session or has no missing chunks.
          upload.state = 'pending';
          this.uploadQueue.push(upload);
        } else {
          // The upload was started in a previous session and is still missing chunks.
          this.resumedUpload = upload;
          this.$refs.input.click();
        }
      } else {
        // We only take the first case mentioned above into account for bulk resuming.
        for (const _upload of this.uploads.slice()) {
          if (this.isResumable(_upload)) {
            _upload.state = 'pending';
            this.uploadQueue.push(_upload);
          }
        }
      }
    },

    getTotalChunkSize(upload) {
      // eslint-disable-next-line no-param-reassign
      return upload.chunks.reduce((acc, chunk) => (chunk.state === 'active' ? acc += chunk.size : acc), 0);
    },

    getUploadProgress(upload, additionalSize = 0) {
      // Special case for files with a size of 0.
      if (upload.size === 0) {
        return (upload.chunks.length > 0 && upload.chunks[0].state === 'active') ? 100 : 0;
      }
      return ((this.getTotalChunkSize(upload) + additionalSize) / upload.size) * 100;
    },

    isResumable(upload) {
      // Special case for files with a size of 0.
      if (upload.size === 0) {
        return upload.state === 'paused'
          && (upload.file !== null || (upload.chunks.length > 0 && upload.chunks[0].state === 'active'));
      }
      return upload.state === 'paused' && (upload.file !== null || this.getTotalChunkSize(upload) === upload.size);
    },
  },
  computed: {
    paginatedUploads() {
      return kadi.utils.paginateList(this.uploads, this.page, this.perPage);
    },
    totalUploadSize() {
      /* eslint-disable no-param-reassign */
      return this.uploads.reduce((acc, upload) => acc += upload.size, 0);
    },
    completedUploadsCount() {
      return this.uploads.reduce((acc, upload) => (upload.state === 'completed' ? acc += 1 : acc), 0);
      /* eslint-enable no-param-reassign */
    },
    uploadInProgress() {
      return this.uploads.slice().some((upload) => upload.state === 'uploading');
    },
    pausable() {
      return this.uploads.slice().some((upload) => ['pending', 'uploading'].includes(upload.state));
    },
    resumable() {
      return this.uploads.slice().some((upload) => this.isResumable(upload));
    },
    cancelable() {
      return this.uploads.slice().some((upload) => ['pending', 'uploading', 'paused'].includes(upload.state));
    },
  },
  mounted() {
    axios.get(this.getUploadsEndpoint)
      .then((response) => {
        response.data.items.forEach((upload) => {
          upload.replacedFile = upload.file;
          upload.file = null;
          upload.progress = this.getUploadProgress(upload);
          upload.source = null;
          upload.chunkSize = response.data._meta.chunk_size;
          upload.chunkCount = upload.chunk_count;
          upload.createdAt = upload.created_at;
          upload.uploadChunkEndpoint = upload._actions.upload_chunk;
          upload.finishUploadEndpoint = upload._actions.finish_upload;
          upload.deleteUploadEndpoint = upload._actions.delete;
          upload.getStatusEndpoint = upload._links.status;
          upload.uploadviewFileEndpoint = null;

          if (upload.state === 'active') {
            upload.state = 'paused';
          } else if (upload.state === 'processing') {
            this.finalizeUpload(upload);
          }

          this.uploads.push(upload);
        });
      });
  },
};
</script>

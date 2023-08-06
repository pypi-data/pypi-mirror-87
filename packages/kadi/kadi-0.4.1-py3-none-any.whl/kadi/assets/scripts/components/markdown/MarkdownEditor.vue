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
    <div class="card toolbar">
      <div class="card-body px-0 py-0">
        <span v-for="button in toolbar" :key="button.title">
          <span class="separator" v-if="button === '|'"></span>
          <button type="button"
                  :class="toolbarBtnClasses"
                  :title="button.title"
                  :disabled="previewActive"
                  @click="handleToolbarButton(button.handler)"
                  v-else>
            <i :class="button.icon"></i>
          </button>
        </span>
        <span class="separator"></span>
        <button type="button"
                title="Preview (Ctrl+P)"
                :class="toolbarBtnClasses"
                @click="previewActive = !previewActive">
          <i class="fas fa-eye"></i>
        </button>
        <span class="separator"></span>
        <button type="button" title="Undo (Ctrl+Z)" :class="toolbarBtnClasses" :disabled="!undoable" @click="undo">
          <i class="fas fa-undo"></i>
        </button>
        <button type="button" title="Redo (Ctrl+Y)" :class="toolbarBtnClasses" :disabled="!redoable" @click="redo">
          <i class="fas fa-redo"></i>
        </button>
      </div>
    </div>
    <div v-show="!previewActive">
      <textarea class="form-control editor"
                :id="id"
                :name="name"
                :required="required"
                :rows="rows"
                v-model="input"
                @keydown.tab="handleTab"
                @keydown.tab.prevent
                @keydown.enter="handleEnter"
                @keydown.enter.prevent
                ref="editor">
      </textarea>
    </div>
    <div v-show="previewActive">
      <div class="card preview" tabindex="-1" ref="preview">
        <div class="card-body pb-0">
          <markdown-preview :input="input"></markdown-preview>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.editor {
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  box-shadow: none;
  font-family: monospace, monospace;
  font-size: 10pt;
  position: relative;
}

.preview {
  border-color: #ced4da;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
}

.separator {
  border-right: 1px solid #dfdfdf;
  margin-left: 7px;
  margin-right: 11px;
  padding-bottom: 3px;
  padding-top: 3px;
}

.toolbar {
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0px;
  border-color: #ced4da;
  margin-bottom: -1px;
}

.toolbar-btn {
  margin-left: -5px;
  margin-right: -5px;
  width: 45px;
}
</style>

<script>
import undoRedoMixin from 'scripts/lib/mixins/undo-redo-mixin';

export default {
  mixins: [undoRedoMixin],
  data() {
    return {
      input: this.initialValue,
      tabSize: 4,
      previewActive: false,
      checkpointTimeoutHandle: null,
      undoStackDepth: 25,
      toolbar: [
        {
          icon: 'fas fa-bold',
          title: 'Bold (Ctrl+B)',
          handler: this.toggleBold,
          shortcut: 66,
        },
        {
          icon: 'fas fa-italic',
          title: 'Italic (Ctrl+I)',
          handler: this.toggleItalic,
          shortcut: 73,
        },
        {
          icon: 'fas fa-strikethrough',
          title: 'Strikethrough (Ctrl+S)',
          handler: this.toggleStrikethrough,
          shortcut: 83,
        },
        {
          icon: 'fas fa-superscript',
          title: 'Superscript (Ctrl+1)',
          handler: this.toggleSuperscript,
          shortcut: 49,
        },
        {
          icon: 'fas fa-subscript',
          title: 'Subscript (Ctrl+2)',
          handler: this.toggleSubscript,
          shortcut: 50,
        },
        {
          icon: 'fas fa-code',
          title: 'Code (Ctrl+D)',
          handler: this.toggleCode,
          shortcut: 68,
        },
        '|',
        {
          icon: 'fas fa-heading',
          title: 'Heading (Ctrl+H)',
          handler: this.toggleHeading,
          shortcut: 72,
        },
        {
          icon: 'fas fa-list-ul',
          title: 'Unordered List (Ctrl+U)',
          handler: this.toggleUnorderedList,
          shortcut: 85,
        },
        {
          icon: 'fas fa-list-ol',
          title: 'Ordered List (Ctrl+O)',
          handler: this.toggleOrderedList,
          shortcut: 79,
        },
        '|',
        {
          icon: 'fas fa-link',
          title: 'Link',
          handler: this.insertLink,
        },
        {
          icon: 'fas fa-image',
          title: 'Image',
          handler: this.insertImage,
        },
        {
          icon: 'fas fa-table',
          title: 'Table',
          handler: this.insertTable,
        },
        {
          icon: 'fas fa-minus',
          title: 'Horizontal Rule',
          handler: this.insertHorizontalRule,
        },
      ],
    };
  },
  props: {
    id: {
      type: String,
      default: 'markdown-editor',
    },
    name: {
      type: String,
      default: 'markdown-editor',
    },
    required: {
      type: Boolean,
      default: false,
    },
    initialValue: {
      type: String,
      default: '',
    },
    rows: {
      type: Number,
      default: 8,
    },
  },
  methods: {
    selectText(selectionStart, selectionEnd = null) {
      this.$nextTick(() => {
        const editor = this.$refs.editor;
        editor.focus();
        editor.selectionStart = Math.max(selectionStart, 0);
        editor.selectionEnd = selectionEnd || selectionStart;
      });
    },

    getSelectedRows() {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;

      let firstRowStart = selectionStart;
      let prevChar = this.input[firstRowStart - 1];
      while (firstRowStart > 0 && prevChar !== '\n') {
        firstRowStart--;
        prevChar = this.input[firstRowStart - 1];
      }

      let lastRowEnd = selectionEnd;
      let currentChar = this.input[lastRowEnd];
      while (lastRowEnd < this.input.length && currentChar !== '\n') {
        lastRowEnd++;
        currentChar = this.input[lastRowEnd];
      }

      const currentText = this.input.substring(firstRowStart, lastRowEnd);
      const rows = currentText.split('\n');

      const selectedRows = {
        start: firstRowStart,
        end: lastRowEnd,
        rows: [],
      };

      for (let i = 0; i < rows.length; i++) {
        let row = rows[i];
        if (i < (rows.length - 1)) {
          row += '\n';
        }
        selectedRows.rows.push(row);
      }

      return selectedRows;
    },

    handleTab(e) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();
      const spaces = ' '.repeat(this.tabSize);

      const getAmountToRemove = (text) => {
        const match = text.match(/^( +)([\s\S]*)/);
        let toRemove = 0;
        if (match) {
          toRemove = Math.min(match[1].length, this.tabSize);
        }

        return toRemove;
      };

      if (selectedRows.rows.length === 1) {
        // Insert a normal tab at the current selection.
        if (!e.shiftKey) {
          this.input = this.input.substring(0, selectionStart) + spaces + this.input.substring(selectionEnd);
          this.selectText(selectionStart + spaces.length);
        // Unindent the current line.
        } else {
          const toRemove = getAmountToRemove(selectedRows.rows[0]);
          this.input = this.input.substring(0, selectedRows.start)
                     + this.input.substring(selectedRows.start + toRemove);
          this.selectText(Math.max(selectionStart - toRemove, selectedRows.start));
        }
      } else {
        const endText = this.input.substring(selectedRows.end);
        this.input = this.input.substring(0, selectedRows.start);

        // Indent all selected lines.
        if (!e.shiftKey) {
          for (const row of selectedRows.rows) {
            this.input += spaces + row;
          }

          this.input += endText;
          this.selectText(selectionStart + spaces.length, selectionEnd + (selectedRows.rows.length * spaces.length));
        // Unindent all selected lines.
        } else {
          let toRemoveFirst = 0;
          let toRemoveTotal = 0;

          for (let i = 0; i < selectedRows.rows.length; i++) {
            const toRemove = getAmountToRemove(selectedRows.rows[i]);
            if (i === 0) {
              toRemoveFirst = toRemove;
            }

            this.input += selectedRows.rows[i].substring(toRemove);
            toRemoveTotal += toRemove;
          }

          this.input += endText;
          this.selectText(Math.max(selectionStart - toRemoveFirst, selectedRows.start), selectionEnd - toRemoveTotal);
        }
      }
    },

    handleEnter() {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();

      let insertText = '\n';
      // Handle unordered and ordered lists.
      const match = selectedRows.rows[0].match(/^( *)(\* |[0-9]+\. )([\s\S]*)/);
      if (match) {
        if (match[2].includes('*')) {
          insertText += `${match[1]}* `;
        } else {
          insertText += `${match[1]}${parseInt(match[2], 10) + 1}. `;
        }
      // Handle spaces at the beginning.
      } else {
        const match = selectedRows.rows[0].match(/^( +)([\s\S]*)/);
        if (match) {
          insertText += match[1];
        }
      }

      this.input = this.input.substring(0, selectionStart) + insertText + this.input.substring(selectionEnd);
      this.selectText(selectionStart + insertText.length);
    },

    toggleBlock(startChars, endChars) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      let removeBlock = false;
      let newSelectionStart = selectionStart + startChars.length;
      let newSelectionEnd = selectionEnd + endChars.length;

      if (selectionStart >= startChars.length && selectionEnd <= this.input.length - endChars.length) {
        const textBlock = this.input.substring(selectionStart - startChars.length, selectionEnd + endChars.length);

        let regexStart = '';
        let regexEnd = '';
        for (const char of startChars) {
          regexStart += `\\${char}`;
        }
        for (const char of endChars) {
          regexEnd += `\\${char}`;
        }
        const regex = new RegExp(`^${regexStart}[\\s\\S]*${regexEnd}$`);

        if (regex.test(textBlock)) {
          this.input = this.input.substring(0, selectionStart - startChars.length)
                     + this.input.substring(selectionStart, selectionEnd)
                     + this.input.substring(selectionEnd + endChars.length, this.input.length);
          removeBlock = true;
          newSelectionStart = selectionStart - startChars.length;
          newSelectionEnd = selectionEnd - endChars.length;
        }
      }

      if (!removeBlock) {
        this.input = this.input.substring(0, selectionStart)
                   + startChars
                   + this.input.substring(selectionStart, selectionEnd)
                   + endChars
                   + this.input.substring(selectionEnd, this.input.length);
      }

      this.selectText(newSelectionStart, newSelectionEnd);
    },

    togglePrefix(toggleFunction) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();
      const endText = this.input.substring(selectedRows.end);

      this.input = this.input.substring(0, selectedRows.start);

      const newSelections = toggleFunction(selectedRows, selectionStart, selectionEnd);

      this.input += endText;

      this.selectText(Math.max(newSelections.start, selectedRows.start), newSelections.end);
    },

    insertText(text) {
      const selectionEnd = this.$refs.editor.selectionEnd;
      this.input = this.input.substring(0, selectionEnd) + text + this.input.substring(selectionEnd);
      this.selectText(selectionEnd + text.length);
    },

    handleToolbarButton(handler) {
      this.forceSaveCheckpoint();
      handler();
      this.saveCheckpoint();
    },

    toggleBold() {
      this.toggleBlock('**', '**');
    },

    toggleItalic() {
      this.toggleBlock('*', '*');
    },

    toggleSuperscript() {
      this.toggleBlock('^', '^');
    },

    toggleSubscript() {
      this.toggleBlock('~', '~');
    },

    toggleStrikethrough() {
      this.toggleBlock('~~', '~~');
    },

    toggleCode() {
      const selectedRows = this.getSelectedRows();
      if (selectedRows.rows.length === 1) {
        this.toggleBlock('`', '`');
      } else {
        this.toggleBlock('```\n', '\n```');
      }
    },

    toggleHeading() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          if ((/^#{1,5} [\s\S]*/).test(selectedRows.rows[i])) {
            this.input += `#${selectedRows.rows[i]}`;
            end += 1;
            if (i === 0) {
              start += 1;
            }
          } else if ((/^#{6} [\s\S]*/).test(selectedRows.rows[i])) {
            this.input += selectedRows.rows[i].substring(7);
            end -= 7;
            if (i === 0) {
              start -= 7;
            }
          } else {
            this.input += `# ${selectedRows.rows[i]}`;
            end += 2;
            if (i === 0) {
              start += 2;
            }
          }
        }

        return {start, end};
      });
    },

    toggleUnorderedList() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          const match = selectedRows.rows[i].match(/^( *)(\* )([\s\S]*)/);
          if (match) {
            this.input += match[1] + match[3];
            end -= 2;
            if (i === 0) {
              start -= 2;
            }
          } else {
            const match = selectedRows.rows[i].match(/^( *)([\s\S]*)/);
            if (match[2] === '') {
              this.input += `* ${match[1]}`;
            } else {
              this.input += `${match[1]}* ${match[2]}`;
            }
            end += 2;
            if (i === 0) {
              start += 2;
            }
          }
        }

        return {start, end};
      });
    },

    toggleOrderedList() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          const match = selectedRows.rows[i].match(/^( *)([0-9]+\. )([\s\S]*)/);
          if (match) {
            this.input += match[1] + match[3];
            end -= match[2].length;
            if (i === 0) {
              start -= match[2].length;
            }
          } else {
            const match = selectedRows.rows[i].match(/^( *)([\s\S]*)/);
            const index = `${i + 1}. `;
            this.input += match[1] + index + match[2];
            end += index.length;
            if (i === 0) {
              start += index.length;
            }
          }
        }

        return {start, end};
      });
    },

    insertLink() {
      const link = '[Link text](https:// "Title")';
      this.insertText(link);
    },

    insertImage() {
      const image = '![Alt text](https:// "Title")';
      this.insertText(image);
    },

    insertTable() {
      const table = '\n\n| Column 1 | Column 2 | Column 3 |\n'
                  + '| -------- | -------- | -------- |\n'
                  + '| Text     | Text     | Text     |\n\n';
      this.insertText(table);
    },

    insertHorizontalRule() {
      const rule = '\n\n---\n\n';
      this.insertText(rule);
    },

    forceSaveCheckpoint() {
      if (this.checkpointTimeoutHandle !== null) {
        clearTimeout(this.checkpointTimeoutHandle);
        this.saveCheckpoint();
      }
    },

    verifyCheckpointData(currentData, newData) {
      return currentData.input !== newData.input;
    },

    getCheckpointData() {
      return {
        input: this.input,
        selectionStart: this.$refs.editor.selectionStart,
        selectionEnd: this.$refs.editor.selectionEnd,
      };
    },

    restoreCheckpointData(data) {
      this.input = data.input;
      this.selectText(data.selectionStart, data.selectionEnd);
    },

    undo() {
      // Custom undo function to correctly handle the timeout.
      if (this.undoable) {
        this.forceSaveCheckpoint();
        this.undoStackIndex--;
        this.restoreCheckpointData(this.undoStack[this.undoStackIndex]);
      }
    },

    keydownHandler(e) {
      if (e.ctrlKey) {
        for (const button of this.toolbar) {
          if (button.shortcut === e.keyCode) {
            e.preventDefault();

            if (!this.previewActive) {
              button.handler();
            }
            return;
          }
        }

        // Keycodes: 80 = P, 89 = Y, 90 = Z
        if (e.keyCode === 80) {
          e.preventDefault();
          this.previewActive = !this.previewActive;

          this.$nextTick(() => {
            if (!this.previewActive) {
              this.$refs.editor.focus();
            } else {
              this.$refs.preview.focus();
            }
          });
        } else if (e.keyCode === 89) {
          e.preventDefault();
          this.redo();
        } else if (e.keyCode === 90) {
          e.preventDefault();
          this.undo();
        }
      }
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-primary toolbar-btn my-1';
    },
  },
  watch: {
    input() {
      this.$emit('input', this.input);

      if (this.checkpointTimeoutHandle !== null) {
        clearTimeout(this.checkpointTimeoutHandle);
      }

      this.checkpointTimeoutHandle = setTimeout(() => {
        this.saveCheckpoint();
      }, 500);
    },
  },
  mounted() {
    this.saveCheckpoint();
    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>

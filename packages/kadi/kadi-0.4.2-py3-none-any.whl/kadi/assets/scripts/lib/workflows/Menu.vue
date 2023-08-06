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

<script>
import {Menu} from 'rete-context-menu-plugin';
import Item from './Item.vue';

export default {
  extends: Menu,
  components: {Item},
};
</script>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.context-menu {
  left: 0;
  top: 0;
  position: fixed;
  padding: 10px;
  width: $context-menu-width;
  margin-top: -20px;
  margin-left: -$context-menu-width / 2;

  .search {
    @extend .item
  }
}
</style>

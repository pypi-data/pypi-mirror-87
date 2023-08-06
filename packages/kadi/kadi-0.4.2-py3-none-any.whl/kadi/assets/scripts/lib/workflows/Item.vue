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
import {Item} from 'rete-context-menu-plugin';

export default {
  extends: Item,
  name: 'Item',
};
</script>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.item {
  @extend .item;

  &.hasSubitems:after {
    content: '►';
    position: absolute;
    opacity: 0.6;
    right: 5px;
    top: 5px;
  }

  .subitems {
    position: absolute;
    top: 0;
    left: 100%;
    width: 120px;

    .subitem {
      @extend .item;
    }
  }
}
</style>

/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

export class Parameter {
  constructor(par, portId = '') {
    this.name = par.param_name || '';
    this.char = par.char || ''; // Short name
    this.description = par.description || '';
    this.required = par.required || false;
    this.type = par.type || 'string';
    this.relations = par.relations || '';
    this.defaultVal = (typeof par.default !== 'undefined') ? par.default : null;
    this.paramDependenceError = false; // Default. When the node is created (no connections = no errors)
    // This.separator = par.separator || null;
    this.portId = portId;
    this.value = this.defaultVal;
  }
}

// The direction of the relation is paramLeft => paramRight
export class Relation {
  constructor(paramLeft, paramRight, rel) {
    this.paramLeft = paramLeft;
    this.paramRight = paramRight;
    this.relation = rel;
    this.message = '';

    if (rel) {
      this.message = `Requires parameter "${this.paramRight.name}".`;
    } else {
      this.message = `Incompatible with parameter "${this.paramRight.name}".`;
    }
  }
}

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

import axios from 'axios';
import i18next from 'i18next';
import jQuery from 'jquery';
import qs from 'qs';
import Vue from 'vue';
import 'bootstrap';
import 'select2/dist/js/select2.full.js';

import translations from 'translations/translations';
import utils from 'scripts/lib/utils';
import 'styles/main.scss';

// Globally accessible objects.
window.kadi = kadi;
window.kadi.utils = utils;

window.axios = axios;
window.i18n = i18next;
window.$ = window.jQuery = jQuery;
window.Vue = Vue;

// Global axios settings.
axios.defaults.headers.common['X-CSRF-TOKEN'] = kadi.js_resources.csrf_token;
axios.defaults.paramsSerializer = (params) => qs.stringify(params, {arrayFormat: 'repeat'});

// Global i18n settings.
i18next.init({
  lng: kadi.js_resources.locale,
  resources: translations,
  whitelist: Object.keys(translations),
});

// Global jQuery AJAX settings.
$.ajaxSetup({
  headers: {'X-CSRF-TOKEN': kadi.js_resources.csrf_token},
  traditional: true,
});

// Global Vue settings.
Vue.options.delimiters = ['{$', '$}']; // For using Vue and Jinja in the same template.

Vue.prototype.$ = Vue.prototype.jQuery = jQuery;
Vue.prototype.kadi = kadi;
Vue.prototype.i18n = i18next;

// Global Vue filters.
Vue.filter('capitalize', kadi.utils.capitalize);
Vue.filter('filesizeFormat', kadi.utils.filesizeFormat);
Vue.filter('prettyTypeName', kadi.utils.prettyTypeName);
Vue.filter('timestamp', kadi.utils.timestamp);
Vue.filter('truncate', kadi.utils.truncate);

// All Vue components inside the 'components' directory are registered globally.
const requireComponent = require.context('./components', true, /\.vue$/);

requireComponent.keys().forEach((fileName) => {
  const componentConfig = requireComponent(fileName);
  const componentName = fileName.split('/').pop().replace(/\.\w+$/, '');
  Vue.component(componentName, componentConfig.default);
});

// Global Bootstrap settings.
const whiteList = $.fn.popover.Constructor.Default.whiteList;
whiteList.button = [];
whiteList.dd = [];
whiteList.dl = [];
whiteList.dt = [];
whiteList.table = [];
whiteList.tbody = [];
whiteList.td = [];
whiteList.th = [];
whiteList.thead = [];
whiteList.tr = [];

// Global Select2 settings.
$.fn.select2.defaults.set('theme', 'bootstrap4');

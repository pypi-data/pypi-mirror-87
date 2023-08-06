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

import moment from 'moment';

export default {
  /** Wrap a value inside a list if the given value is not a list already. */
  asList(list) {
    let _list = list;
    if (!Array.isArray(_list)) {
      _list = [_list];
    }
    return _list;
  },

  /** Capitalize a string. */
  capitalize(string) {
    if (string.length === 0) {
      return string;
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
  },

  /** Scroll an element into the view using a specific alignment relative to it. */
  scrollIntoView(element, alignment = 'center') {
    if (alignment === 'top') {
      element.scrollIntoView(true);
      // Take the potentially fixed navigation header into account.
      const viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      if (viewportWidth >= 768) {
        window.scrollBy(0, -66);
      }
    } else if (alignment === 'bottom') {
      element.scrollIntoView(false);
    } else {
      element.scrollIntoView(false);
      const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
      const viewPortPercentage = element.getBoundingClientRect().top / viewportHeight;
      window.scrollBy(0, (viewPortPercentage - 0.5) * viewportHeight);
    }
  },

  /** Wrapper of the window confirm function for inline usage. */
  confirm(text, callback, ...args) {
    if (confirm(text)) {
      callback(...args);
    }
  },

  /**
   * Get a human readable file size from a given amount of bytes.
   * Works the same as Jinja's 'filesizeformat' filter.
   */
  filesizeFormat(bytes, binary = false) {
    const base = binary ? 1024 : 1000;
    const prefixes = [
      binary ? 'KiB' : 'kB',
      binary ? 'MiB' : 'MB',
      binary ? 'GiB' : 'GB',
      binary ? 'TiB' : 'TB',
      binary ? 'PiB' : 'PB',
    ];

    if (bytes === 1) {
      return '1 Byte';
    } else if (bytes < base) {
      return `${bytes} Bytes`;
    }

    let unit = 0;
    for (let i = 0; i < prefixes.length; i++) {
      unit = base ** (i + 2);
      if (bytes < unit) {
        return `${Number(base * bytes / unit).toFixed(1)} ${prefixes[i]}`;
      }
    }
    return `${Number(base * bytes / unit).toFixed(1)} ${prefixes[prefixes.length - 1]}`;
  },

  /** Get a nested property of an object given a string specifying the property separated by dots. */
  getProp(object, property) {
    const props = property.split('.');
    let result = object;

    for (const prop of props) {
      result = result[prop];
    }
    return result;
  },

  /** Insert a string at a given position inside another string. */
  insertString(string, index, toInsert) {
    if (index > 0) {
      return `${string.slice(0, index)}${toInsert}${string.slice(index)}`;
    }
    return toInsert + string;
  },

  /** Paginate a list given a page and the amount of items per page. */
  paginateList(list, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return list.slice(start, end);
  },

  /** Return a pretty type name based on a Python-like type string. */
  prettyTypeName(type) {
    switch (type) {
    case 'str': return 'string';
    case 'int': return 'integer';
    case 'bool': return 'boolean';
    case 'dict': return 'dictionary';
    default: return type;
    }
  },

  /** Generate a random alphanumeric string with a given length. */
  randomAlnum(length = 16) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  },

  /** Remove all occurences of a given item from a list. */
  removeFromList(list, item) {
    let index = list.indexOf(item);
    while (index >= 0) {
      list.splice(index, 1);
      index = list.indexOf(item);
    }
  },

  /** Sleep for the given amount of milliseconds. */
  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  },

  /** Build a UTC timestamp from a given valid date string. */
  timestamp(datestring) {
    return moment.utc(datestring).format('YYYYMMDDHHmmss');
  },

  /** Truncate a string by a given length. */
  truncate(string, length) {
    const originalLength = string.length;
    let _string = string.substring(0, length);

    if (originalLength > length) {
      _string += '...';
    }
    return _string;
  },
};

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

import Visibility from 'visibilityjs';

import BaseNavSearch from 'scripts/lib/components/BaseNavSearch.vue';
import NotificationAlert from 'scripts/lib/components/NotificationAlert.vue';
import NotificationToast from 'scripts/lib/components/NotificationToast.vue';

// Stop the logo animation once the site loaded and the current animation iteration finished.
const stopAnimation = () => [].forEach.call(document.querySelectorAll('.kadi-logo'), (el) => {
  el.style.animation = 'none';
});

[].forEach.call(document.querySelectorAll('.kadi-logo'), (el) => {
  el.addEventListener('animationiteration', stopAnimation);
  el.addEventListener('webkitAnimationIteration', stopAnimation);
});

// Scroll required inputs to a more sensible location, also taking different layouts into account.
document.addEventListener('invalid', (e) => kadi.utils.scrollIntoView(e.target), true);

// To handle global, short lived alerts.
const alertsVm = new Vue({
  el: '#notification-alerts',
  components: {
    NotificationAlert,
  },
  data: {
    alerts: [],
  },
  methods: {
    alert(message, options) {
      let _message = message;
      const settings = {
        xhr: null,
        type: 'danger',
        timeout: 5000,
        scrollTo: true,
        ...options,
      };

      if (settings.xhr !== null) {
        if (settings.xhr.status !== 0) {
          _message = `${message} (${settings.xhr.status})`;
        } else {
          return;
        }
      }

      this.alerts.push({
        id: kadi.utils.randomAlnum(),
        message: _message,
        type: settings.type,
        timeout: settings.timeout,
      });

      if (settings.scrollTo) {
        kadi.utils.scrollIntoView(this.$el, 'bottom');
      }
    },
  },
});

kadi.alert = alertsVm.alert;

if (kadi.js_resources.user_active) {
  // Base navigation bar quick search.
  new Vue({
    el: '#base-nav-search',
    components: {
      BaseNavSearch,
    },
  });

  // To handle global, persistent notifications.
  const toastsVm = new Vue({
    el: '#notification-toasts',
    components: {
      NotificationToast,
    },
    data: {
      notifications: [],
      title: null,
    },
    methods: {
      getNotifications(scrollTo = true) {
        axios.get(kadi.js_resources.notifications_endpoint)
          .then((response) => {
            this.notifications = response.data;

            const numNotifications = this.notifications.length;
            if (scrollTo && numNotifications > 0) {
              this.$nextTick(() => kadi.utils.scrollIntoView(this.$el, 'bottom'));
            }

            if (numNotifications > 0) {
              document.title = `(${numNotifications}) ${this.title}`;
            } else {
              document.title = this.title;
            }
          });
      },
    },
    mounted() {
      this.title = document.title;

      Visibility.every(5000, () => {
        this.getNotifications(false);
      });
      this.getNotifications(false);
    },
  });

  kadi.getNotifications = toastsVm.getNotifications;
}

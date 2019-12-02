import Vue from 'vue';
import Vuelidate from 'vuelidate';
import VueMoment from 'vue-moment';
import lang from 'quasar/lang/zh-hans.js';
import '@quasar/extras/material-icons/material-icons.css';
import '@quasar/extras/mdi-v3/mdi-v3.css';
import 'animate.css';
import Quasar from 'quasar';

import App from './App.vue';
import router from './router';
import './registerServiceWorker';
import './styles/quasar.styl';
import store from './views/.storee';

Vue.use(Quasar, {
  config: {},
  lang: lang
});
Vue.use(Vuelidate);
Vue.use(VueMoment);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');

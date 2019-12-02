<template>
  <Authorized
    :authority="basicRoute.meta.authority"
    :noMatch="basicRoute.meta.noMatch"
  >
    <q-layout view="hHh LpR lfr">
      <q-header>
        <GlobalHeader class="bg-primary text-white" />
      </q-header>

      <q-page-container class="page-container">
        <q-page>
          <Authorized
            :authority="$route.meta.authority"
            :noMatch="$route.meta.noMatch"
          >
            <router-view />
          </Authorized>
        </q-page>
      </q-page-container>

      <q-footer class="bg-transparent">
        <Footer />
      </q-footer>
    </q-layout>
  </Authorized>
</template>

<script>
import { mapGetters } from 'vuex';
import { openURL } from 'quasar';
import Footer from './Footer';
import GlobalHeader from '@/components/GlobalHeader';
import Authorized from '@/components/Authorized';
import store from '@/views/.storee';

export default {
  name: 'BlankLayout',
  components: { GlobalHeader, Footer, Authorized },
  data() {
    return {
      orgs: []
    };
  },
  computed: {
    ...mapGetters('authorized', {
      checkPermissions: 'checkPermissions'
    }),
    basicRoute() {
      return this.$route.matched[0];
    }
  },
  methods: {
    openURL
  },
  async created() {},
  async beforeRouteEnter(to, from, next) {
    await store.dispatch('authorized/fetch');
    await store.dispatch('user/fetchCurrent');
    store.commit('authorized/reloadAuthorized');
    next();
  },
  async mounted() {}
};
</script>

<style lang="stylus" scoped>

.page-container
  background: $layout-bgColor;

.org
  min-width: 200px;
  font-size: 13px;
</style>

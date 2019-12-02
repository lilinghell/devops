<template>
  <Authorized
    :authority="basicRoute.meta.authority"
    :noMatch="basicRoute.meta.noMatch"
  >
    <q-layout view="hHh LpR lfr">
      <q-header>
        <Header />
      </q-header>

      <q-drawer
        :width="256"
        :value="isOpen"
        :mini="isMini"
        content-class="menu"
        no-swipe-open
      >
        <SiderMenu
          :menuData="getMenu(basicRoute.name, $route.params)"
          :check="checkPermissions"
          :mini="isMini"
        />
      </q-drawer>

      <q-page-container class="page-container">
        <q-page>
          <Authorized :authority="$route.meta.authority">
            <router-view :key="$route.fullPath" />
            <template v-slot:exception>
              <Exception403 />
            </template>
          </Authorized>
        </q-page>
      </q-page-container>

      <q-footer
        class="bg-transparent"
        :class="$route.meta.footerHidden ? 'hidden' : ''"
      >
        <Footer />
      </q-footer>
    </q-layout>

    <!-- project add modal -->
    <Modal v-model="projectAddModalOpened" title="新建项目">
      <ProjectAdd :onProjectAdd="toggleProjectAddModal" />
    </Modal>
  </Authorized>
</template>

<script>
import { mapGetters } from 'vuex';
import { openURL } from 'quasar';
import Header from './Header';
import Footer from './Footer';
import SiderMenu from '@/components/SiderMenu';
import Authorized from '@/components/Authorized';
import Modal from '@/components/Modal';
import Exception403 from '@/views/app/Exception/403.vue';
import ProjectAdd from '@/views/project/Add.vue';
import store from '@/views/.storee';

export default {
  name: 'BasicLayout',
  components: {
    Header,
    Footer,
    SiderMenu,
    Authorized,
    Exception403,
    ProjectAdd,
    Modal
  },
  data() {
    return {
      projectAddModalOpened: false,
      isMini: false
    };
  },
  computed: {
    ...mapGetters('menu', ['getMenu']),
    ...mapGetters('authorized', {
      checkPermissions: 'checkPermissions'
    }),
    basicRoute() {
      return this.$route.matched[0];
    },
    isOpen() {
      return !this.$route.meta.siderHidden;
    }
  },
  methods: {
    openURL,
    toggleLeftDrawer() {
      this.isMini = !this.isMini;
    },
    toggleProjectAddModal() {
      this.projectAddModalOpened = !this.projectAddModalOpened;
    }
  },
  async created() {
    this.$root.$on('toggleLeftDrawer', this.toggleLeftDrawer);
    this.$root.$on('toggleProjectAddModal', this.toggleProjectAddModal);
    this.isMini = !!this.$route.meta.mini;

    this.$store.dispatch('menu/initMenu', null, { root: true });
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch('authorized/fetch');
    await store.dispatch('user/fetchCurrent');
    store.commit('authorized/reloadAuthorized');

    next();
  },
  beforeRouteLeave(to, from, next) {
    this.isMini = !!to.meta.mini;
    next();
  },
  async mounted() {}
};
</script>

<style lang="stylus" scoped>

.page-container
  background: $layout-bgColor;
</style>

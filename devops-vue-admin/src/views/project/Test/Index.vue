<template>
  <q-page class="column">
    <PageHeader />
    <div class="col relative-position">
      <div class="absolute-full overflow-hidden row">
        <div class="sub-menu">
          <q-list>
            <q-item class="menu-header">
              <q-item-section side>
                <q-icon color="white" :name="subMenu.icon" />
              </q-item-section>
              <q-item-section>
                <h6>{{ project.name }}</h6>
              </q-item-section>
            </q-item>
            <q-separator class="separator" />
            <q-item
              v-for="menu in subMenu.children"
              :key="menu.name"
              :to="menu.path"
            >
              <q-item-section>{{ menu.name }}</q-item-section>
            </q-item>
          </q-list>
        </div>
        <router-view class="content" />
      </div>
    </div>
  </q-page>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
  import PageHeader from '@/components/PageHeader';
  import { createProjectModel } from '../model';

  export default {
    name: 'Index',
    components: { PageHeader },
    data() {
      return {};
    },
    computed: {
      ...mapState('project', ['currentProjects']),
      ...mapGetters('menu', ['getMenu']),
      project() {
        return this.currentProjects[0] || createProjectModel();
      },
      subMenu() {
        let menuData = this.getMenu(
          this.$route.matched[0].name,
          this.$route.params
        );
        return menuData.find(menu => menu.name === '测试');
      }
    },
    methods: {},
    created() {},
    mounted() {}
  };
</script>

<style lang="stylus" scoped>
.container
  margin: -24px -24px 0;
  display: flex;
  height: 100%;
.sub-menu
  padding: 16px 0 16px 16px;
  width: 240px;
  height: 100%;
  overflow-y: scroll;
  color: white;
  background: $primary;
  .menu-header
    h6
      font-weight: 600
      margin: 12px;
      margin-left: 0;
  a
    color: white;
    border-radius: 4px 0 0 4px;
    min-height: 40px;
    &:hover
      background: $teal-6;
    &.q-router-link--active
      background: $layout-bgColor;
      color: $primary;
.content
  flex: 1;
  margin: 24px;
  height: calc(100% - 48px);
  overflow-y: scroll;
.separator
  height: 2px;
  margin-bottom: 8px;
  width: calc(100% - 16px);
</style>

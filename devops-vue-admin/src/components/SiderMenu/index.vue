<template>
  <div class="menu">
    <q-list>
      <q-item class="siderMenu-header">
        <q-item-section>
          <router-link to="/">
            <!--<img alt="f'(dev)" src="../../assets/logo.gif">-->
            <h1>Devops</h1>
          </router-link>
        </q-item-section>
        <q-item-section side>
          <q-btn
            color="white"
            flat
            dense
            round
            @click="$root.$emit('toggleLeftDrawer')"
            icon="menu"
          />
        </q-item-section>
      </q-item>
      <template v-for="menu in flatMenu">
        <q-item
          :key="menu.name"
          v-if="!menu.children || (menu.meta && menu.meta.behave === 'link')"
          :to="menu.path"
        >
          <q-item-section side>
            <q-icon :name="menu.icon" />
          </q-item-section>
          <q-item-section>{{ menu.name }}</q-item-section>
          <q-tooltip
            content-class="bg-grey-10"
            transition-show="fade"
            transition-hide="fade"
            anchor="center right"
            self="center left"
            :offset="[-8, 0]"
            v-if="mini"
            >{{ menu.name }}
          </q-tooltip>
        </q-item>
        <q-expansion-item
          :key="menu.name"
          :icon="menu.icon"
          :label="menu.name"
          :default-opened="menu.opened"
          :header-class="menu.opened ? 'opened' : ''"
          group="menu"
          class="siderMenu-expansion"
          dense-toggle
          v-else
        >
          <template v-for="subMenu in menu.children">
            <q-item
              :key="subMenu.name"
              v-if="!subMenu.children"
              :to="subMenu.path"
              :inset-level="0.7"
              >{{ subMenu.name }}</q-item
            >
            <q-expansion-item
              :label="subMenu.name"
              :key="subMenu.name"
              :default-opened="subMenu.opened"
              :header-class="subMenu.opened ? 'opened' : ''"
              :header-inset-level="0.7"
              dense-toggle
              v-else
            >
              <q-item
                v-for="menu3 in subMenu.children"
                :key="menu3.name"
                :to="menu3.path"
                :inset-level="1.4"
              >
                {{ menu3.name }}
              </q-item>
            </q-expansion-item>
          </template>
        </q-expansion-item>
      </template>
    </q-list>
  </div>
</template>

<script>
export default {
  name: 'SiderMenu',
  components: {},
  props: {
    menuData: Array,
    check: Function,
    mini: Boolean
  },
  data() {
    return {};
  },
  computed: {
    flatMenu() {
      return this.getSubMenu(this.menuData);
    }
  },
  methods: {
    getSubMenu(menu, parent) {
      const { fullPath } = this.$route;
      return menu
        .filter(item => !!item.path)
        .filter(item => !(item.meta && item.meta.hideInMenu))
        .filter(item => this.check(item.authority))
        .map(item => {
          const result = {
            ...item
          };
          if (fullPath.startsWith(item.path) && item.path !== '/') {
            result.opened = true;
            if (parent) {
              parent.opened = true;
            }
          }
          if (result.children) {
            // Reduce memory usage
            result.children = this.getSubMenu(result.children, result);
          }
          return result;
        });
    }
  },
  created() {},
  mounted() {}
};
</script>

<style lang="stylus">

$menu-bgColor = $blue-grey-10
$header-bgColor = $blue-grey-10 + #020202
$sub-menu-bgColor = $blue-grey-10 - #111
$menu-bgColor-active = $primary

.menu
  background-color: $menu-bgColor
  color: rgba(255, 255, 255, 0.85)
  .siderMenu-header
    background: $header-bgColor
    margin-bottom: 8px
    height: 53px
    h1
      display: inline-block
      vertical-align: middle
      color: white
      font-size: 20px
      line-height: 20px
      font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif
      font-weight: 600
      text-decoration: none
      margin: 0 0 0 12px;
    img
      height: 20px
      vertical-align: middle
  .siderMenu-expansion
    .opened
      color: white
      .q-item__section--side
        color: inherit
    .q-expansion-item__content
      background: $sub-menu-bgColor
  .q-item
    min-height: 40px;
    .q-item__section--side
      color: inherit;
    &:hover
      color: white
      .q-item__section--side
        color: inherit
    &.q-router-link--active
      color: white
      background $menu-bgColor-active
      font-weight: $text-weights.medium
    &:hover
      .q-focus-helper
        opacity: 0 !important
    .q-item__section--avatar
      min-width: 38px
</style>

<template>
  <q-toolbar class="toolbar">
    <slot name="left" />
    <q-space />
    <slot name="right" />
    <q-btn stretch flat class="text-weight-regular">
      <q-avatar size="24px">
        <q-img :src="currentUser.avatar_url" />
      </q-avatar>
      <span class="q-ml-sm">{{ currentUser.name }}</span>
      <q-menu>
        <q-list dense class="account-list">
          <q-item clickable v-ripple v-close-popup to="/account/center">
            <q-item-section side>
              <q-icon name="account_circle" />
            </q-item-section>
            <q-item-section>
              <q-item-label>个人中心</q-item-label>
            </q-item-section>
          </q-item>
          <q-item clickable v-ripple v-close-popup to="/account/settings/base">
            <q-item-section side>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>
              <q-item-label>个人设置</q-item-label>
            </q-item-section>
          </q-item>
          <q-separator class="q-my-sm" />
          <q-item clickable v-ripple v-close-popup @click.native="handleLogout">
            <q-item-section side>
              <q-icon name="exit_to_app" />
            </q-item-section>
            <q-item-section>
              <q-item-label>退出登陆</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
    <slot name="append" />
  </q-toolbar>
</template>

<script>
import { mapState } from 'vuex';
export default {
  name: 'GlobalHeader',
  components: {},
  data() {
    return {};
  },
  computed: {
    ...mapState('user', {
      currentUser: 'currentUser'
    })
  },
  methods: {
    async handleLogout() {
      await this.$store.dispatch('login/logout');
    }
  },
  created() {},
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.toolbar
  background: #eff5f5
  color: $grey-10;
.account-list
  width: 150px;
  padding: 8px 0;
  /*.q-item
    &:hover
      background: $teal-1;*/
</style>

<template>
  <q-btn flat round icon="notifications_none" @click="onVisibleChange">
    <q-badge color="red" floating>{{ currentUser.notifyCount }}</q-badge>
    <q-menu>
      <q-list class="notice-list" padding>
        <q-item clickable v-ripple v-for="item in notices" :key="item.id">
          <q-item-section avatar>
            <q-avatar icon="folder" color="primary" text-color="white" />
          </q-item-section>
          <q-item-section>
            <q-item-label lines="2">{{ item.title }}</q-item-label>
            <q-item-label caption>{{ item.datetime }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-icon name="info" color="amber" />
          </q-item-section>
        </q-item>
        <q-separator spaced inset="item" />
        <q-item-label header>很关键</q-item-label>
        <q-item clickable v-ripple>
          <q-item-section avatar>
            <q-avatar icon="assignment" color="secondary" text-color="white" />
          </q-item-section>
          <q-item-section>
            <q-item-label lines="2">Vacation</q-item-label>
            <q-item-label caption>February 22, 2016</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-icon name="info" color="amber" />
          </q-item-section>
        </q-item>
        <q-separator spaced />
        <q-item>
          <q-btn
            flat
            icon="delete_outline"
            color="negative"
            size="sm"
            class="full-width"
            :label="`清空通知(${currentUser.notifyCount})`"
            @click="onClear('notification')"
          />
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
import { mapState } from 'vuex';
export default {
  name: 'NoticeIcon',
  props: {
    onClear: Function,
    onPopupVisibleChange: Function
  },
  data() {
    return {
      showing: false
    };
  },
  computed: {
    ...mapState('user', {
      currentUser: 'currentUser'
    }),
    ...mapState('global', {
      notices: 'notices'
    })
  },
  methods: {
    onVisibleChange() {
      this.showing = !this.showing;
      this.onPopupVisibleChange(this.showing);
    }
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.notice-list
  max-width: 336px;
</style>

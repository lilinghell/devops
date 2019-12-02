<template>
  <GlobalHeader class="text-grey-10">
    <template v-slot:left>
      <q-btn
        stretch
        flat
        label="Dashboard"
        to="/dashboard"
        no-caps
        class="text-weight-regular"
      />
      <q-btn stretch flat label="项目" class="text-weight-regular">
        <q-menu>
          <q-list class="project-list" separator>
            <q-item class="bg-primary">
              <q-item-section>
                <q-input
                  v-model="filter"
                  autofocus
                  type="text"
                  dense
                  bg-color="white"
                  outlined
                >
                  <template v-slot:append>
                    <q-icon name="search" color="primary" />
                  </template>
                </q-input>
              </q-item-section>
            </q-item>
            <q-item v-for="project in projects" :key="project.id" v-close-popup>
              <q-item-section>
                <q-item-label>{{ project.name }}</q-item-label>
                <q-item-label caption lines="1">{{
                  project.description
                }}</q-item-label>
                <q-item-label caption class="row q-gutter-x-xs">
                  <router-link :to="`/project/${project.id}`" class="link"
                    >issue</router-link
                  >
                  <router-link :to="`/project/${project.id}`" class="link"
                    >流水线</router-link
                  >
                  <router-link :to="`/project/${project.id}/app`" class="link"
                    >应用</router-link
                  >
                  <router-link :to="`/project/${project.id}`" class="link"
                    >统计</router-link
                  >
                  <router-link
                    :to="`/project/${project.id}/setting`"
                    class="link"
                    >设置</router-link
                  >
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label caption>{{ project.created_at }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
      <q-btn
        stretch
        flat
        label="流水线"
        to="/dashboard"
        class="text-weight-regular"
      />
      <q-btn
        stretch
        flat
        label="资源"
        to="/dashboard"
        class="text-weight-regular"
      />
      <q-btn
        stretch
        flat
        label="Wiki"
        to="/dashboard"
        no-caps
        class="text-weight-regular"
      />
    </template>
    <template v-slot:right>
      <div class="text-grey-8 text-weight-regular">
        <q-btn flat round icon="add">
          <q-menu>
            <q-list dense padding class="add-list">
              <q-item
                clickable
                v-ripple
                v-close-popup
                @click="$root.$emit('toggleProjectAddModal')"
              >
                <q-item-section>
                  <q-item-label>新建项目</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-ripple v-close-popup>
                <q-item-section>
                  <q-item-label>新建ISSUE</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn flat round icon="search" />
        <NoticeIcon
          :onClear="handleNoticeClear"
          :onPopupVisibleChange="handleNoticeVisibleChange"
        />
      </div>
    </template>
    <template v-slot:append>
      <q-separator vertical class="q-my-md" />
      <q-btn
        flat
        icon="domain"
        to="/admin"
        stretch
        color="grey-8"
        class="text-weight-regular"
      />
    </template>
  </GlobalHeader>
</template>

<script>
import GlobalHeader from '@/components/GlobalHeader';
import NoticeIcon from '@/components/NoticeIcon';
import { successNotify } from '@/utils/utils';
import { mapState, mapActions } from 'vuex';

export default {
  name: 'Header',
  components: { GlobalHeader, NoticeIcon },
  data() {
    return {
      orgs: [],
      filter: ''
    };
  },
  computed: {
    ...mapState('global', {
      notices: 'notices'
    }),
    ...mapState('project', ['currentProjects']),
    projects() {
      return this.currentProjects.filter(
        project =>
          project.name.toLowerCase().indexOf(this.filter.toLowerCase()) > -1
      );
    }
  },
  methods: {
    ...mapActions('global', ['fetchNotices', 'clearNotices']),
    ...mapActions('project', {
      queryProject: 'fetchCurrent'
    }),
    handleNoticeVisibleChange(visible) {
      if (visible) {
        this.fetchNotices();
      }
    },
    handleNoticeClear(type) {
      successNotify(`清空了 ${type}`);
      this.clearNotices(type);
    }
  },
  async created() {
    await this.queryProject();
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.project-list
  width: 300px;
.add-list
  width: 150px;
  .q-item
    &:hover
      background: $teal-1;
</style>

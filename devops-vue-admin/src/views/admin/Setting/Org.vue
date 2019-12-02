<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page class="flex-center">
        <q-form class="container" ref="orgForm" @submit="handleUpdateOrg">
          <q-card-section class="text-center">
            <q-avatar
              size="88px"
              @mouseover="isUploadIconVisible = true"
              @mouseout="isUploadIconVisible = false"
              class="relative-position"
            >
              <q-img
                :src="require('@/assets/logo.png')"
                class="absolute-center"
              />
              <transition
                enter-active-class="animated fadeIn"
                leave-active-class="animated fadeOut"
              >
                <q-icon
                  name="edit"
                  v-show="isUploadIconVisible"
                  class="avatar-upload"
                />
              </transition>
            </q-avatar>
          </q-card-section>
          <q-card-section class="row q-my-lg">
            <div class="col-9">
              <Field label="企业名称" :label-col="4" align="right">
                <q-input
                  outlined
                  v-model="org.name"
                  type="text"
                  autofocus
                  dense
                  :rules="[() => !org.name.$error || '请输入企业名称']"
                />
              </Field>
              <Field label="企业描述" :label-col="4" align="right">
                <q-input
                  outlined
                  v-model="org.description"
                  type="textarea"
                  dense
                />
              </Field>
            </div>
          </q-card-section>
          <q-card-actions align="center">
            <q-btn
              color="primary"
              type="submit"
              :loading="loading['org/update']"
              class="btn-fixed-width"
              >提交</q-btn
            >
          </q-card-actions>
        </q-form>
      </Page>
    </Loading>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import Page from '@/components/Page';
import { successNotify } from '@/utils/utils';

export default {
  name: 'Profile',
  components: { PageHeaderWrapper, Loading, Field, Page },
  data() {
    return {
      globalLoading: true,
      members: [],
      org: {},
      isUploadIconVisible: false
    };
  },
  watch: {
    memberOptions(val) {
      this.members = val.slice(0);
    }
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('org', {
      memberOptions: 'members'
    }),
    ...mapState('user', {
      currentUser: 'currentUser'
    })
  },
  methods: {
    ...mapActions('org', ['update']),
    ...mapActions('org', {
      queryMember: 'fetchMember',
      updateCurrentOrg: 'updateCurrentOrg'
    }),
    async handleUpdateOrg() {
      await this.updateCurrentOrg(this.org);
      successNotify('修改成功');
    },
    async memberFilter(val, update, abort) {
      update(() => {
        this.members = this.memberOptions.filter(
          user => user.name.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    }
  },
  async created() {
    this.org = this.currentUser.org;

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.container
  margin: 24px auto;
  width: 100%;
  max-width: 820px;
.btn-fixed-width
  width: 100px;
.avatar-upload
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  z-index: 10;
  background: rgba(255, 255, 255, 0.6);
  border: 2px dashed $primary;
  border-radius: inherit;
  color: $primary;
  cursor: pointer;
</style>

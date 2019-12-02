<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page class="bg-transparent">
        <q-splitter v-model="splitterModel" disable class="container">
          <template v-slot:before>
            <q-tabs v-model="tab" vertical class="text-primary">
              <q-tab name="profile" icon="domain" label="企业信息" />
              <q-tab
                name="member"
                icon="mdi-set mdi-account-multiple-outline"
                label="企业用户"
              />
            </q-tabs>
          </template>

          <template v-slot:after>
            <q-tab-panels
              v-model="tab"
              animated
              transition-prev="jump-up"
              transition-next="jump-up"
            >
              <q-tab-panel name="profile">
                <q-form ref="orgForm" @submit="handleUpdateOrg">
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
                          v-model="$v.org.name.$model"
                          type="text"
                          autofocus
                          dense
                          :rules="[
                            () => !$v.org.name.$error || '请输入企业名称'
                          ]"
                        />
                      </Field>
                      <Field label="企业管理员" :label-col="4" align="right">
                        <q-select
                          outlined
                          use-chips
                          use-input
                          multiple
                          input-debounce="0"
                          v-model="$v.org.admins.$model"
                          :options="members"
                          dense
                          emit-value
                          map-options
                          :rules="[
                            () => !$v.org.admins.$error || '请选择企业管理员'
                          ]"
                          @filter="memberFilter"
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
              </q-tab-panel>
              <q-tab-panel name="member">
                <q-table
                  :data="members"
                  :columns="columns"
                  :filter="filter"
                  row-key="id"
                  :pagination.sync="pagination"
                  flat
                >
                  <template v-slot:top-left>
                    <q-input v-model="filter" dense class="table-head-input">
                      <template v-slot:append>
                        <q-icon name="search" color="primary" />
                      </template>
                    </q-input>
                  </template>

                  <template v-slot:top-right>
                    <q-btn
                      color="primary"
                      unelevated
                      class="table-head-btn"
                      @click="handleAddModalOpen"
                    >
                      新增用户<q-icon name="add" class="q-ml-sm" />
                    </q-btn>
                  </template>

                  <template v-slot:body-cell-operation="props">
                    <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
                      <router-link :to="`/org/${props.row.id}`" class="link"
                        >管理</router-link
                      >
                      <a @click="handleRemoveMember(props.row)" class="link"
                        >删除</a
                      >
                    </q-td>
                  </template>
                </q-table>
              </q-tab-panel>
            </q-tab-panels>
          </template>
        </q-splitter>
      </Page>
    </Loading>

    <q-dialog
      v-model="addModalOpened"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div class="modal-content-sm">
        <q-toolbar class="bg-primary text-white">
          <q-btn flat v-close-popup round dense icon="arrow_back" />
          <q-toolbar-title>新增用户</q-toolbar-title>
        </q-toolbar>
        <q-form ref="memberForm" @submit="handleAdd">
          <q-stepper v-model="step" vertical color="primary" header-nav>
            <q-step
              :name="1"
              title="请输入邮件地址"
              icon="email"
              :done="step > 1"
            >
              <q-input
                label="邮件"
                v-model="$v.addMemberModel.email.$model"
                type="email"
                autofocus
                :rules="[
                  () => !$v.addMemberModel.email.$error || '请输入邮件地址'
                ]"
                @keydown.stop.prevent.enter="handleVerifyEmail"
              >
                <template v-slot:before>
                  <q-icon name="email" />
                </template>
                <template v-slot:append>
                  <q-btn
                    flat
                    round
                    icon="send"
                    color="primary"
                    @click="handleVerifyEmail"
                    :disabled="$v.addMemberModel.email.$invalid"
                  />
                </template>
              </q-input>
            </q-step>

            <q-step
              :name="2"
              title="请填写基本信息"
              icon="create_new_folder"
              :done="step > 2"
              :header-nav="false"
            >
              <q-input
                label="名称"
                v-model="$v.addMemberModel.username.$model"
                type="text"
                dense
                autofocus
                :rules="[
                  () => !$v.addMemberModel.username.$error || '请输入名称'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="account_box" class="q-mr-sm" />
                </template>
              </q-input>
              <q-input
                label="密码"
                v-model="$v.addMemberModel.password.$model"
                type="password"
                dense
                :rules="[
                  () => !$v.addMemberModel.password.$error || '请输入密码'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="lock" class="q-mr-sm" />
                </template>
              </q-input>
              <q-input
                label="确认密码"
                v-model="$v.addMemberModel.password2.$model"
                type="password"
                dense
                :rules="[
                  () => !$v.addMemberModel.password2.$error || '请输入确认密码'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="lock" class="q-mr-sm" />
                </template>
              </q-input>
              <q-select
                label="角色"
                v-model="$v.addMemberModel.type.$model"
                :options="types"
                dense
                :rules="[() => !$v.addMemberModel.type.$error || '请选择角色']"
              >
                <template v-slot:before>
                  <q-icon name="business" class="q-mr-sm" />
                </template>
              </q-select>
              <q-stepper-navigation align="right">
                <q-btn unelevated type="submit" color="primary" label="提交" />
                <q-btn
                  flat
                  @click="step = 1"
                  color="primary"
                  label="上一步"
                  class="q-ml-sm"
                />
              </q-stepper-navigation>
            </q-step>
          </q-stepper>
        </q-form>
      </div>
    </q-dialog>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required, email } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import Page from '@/components/Page';
import {
  resolveResponseError,
  successNotify,
  errorNotify,
  formatSelectDisplay
} from '@/utils/utils';
import { createUserModel, vars } from '@/views/model';
import { set, get } from '@/views/setting';
const paginationKey = 'org/profile/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

import { query } from '@/services/org';
import { query as queryUser } from '@/services/user';

export default {
  name: 'Profile',
  components: { PageHeaderWrapper, Loading, Field, Page },
  data() {
    return {
      globalLoading: true,
      tab: 'profile',
      splitterModel: 10,
      members: [],
      org: {},
      isUploadIconVisible: false,

      columns: [
        {
          name: 'name',
          label: '员工姓名',
          align: 'left',
          field: 'name',
          style: 'width: 20%'
        },
        {
          name: 'email',
          label: 'email',
          align: 'center',
          field: 'email',
          style: 'width: 20%'
        },
        {
          name: 'date_expired',
          label: '到期时间',
          align: 'center',
          field: 'date_expired',
          style: 'width: 20%'
        },
        {
          name: 'role',
          label: '角色',
          align: 'center',
          field: row => formatSelectDisplay(this.userRoles, row.authority),
          style: 'width: 20%'
        },
        {
          name: 'operation',
          label: '操作',
          align: 'right',
          field: row => row,
          style: 'width: 20%'
        }
      ],
      pagination: getPagination(),
      filter: '',

      addModalOpened: false,
      addMemberModel: createUserModel(),
      types: vars.types,
      userRoles: vars.userRoles,

      step: 1
    };
  },
  validations: {
    org: {
      name: { required },
      admins: { required }
    },
    addMemberModel: {
      email: { required, email },
      password: { required },
      password2: { required },
      username: { required },
      type: { required }
    }
  },
  watch: {
    pagination(val) {
      setPagination({
        rowsPerPage: val.rowsPerPage
      });
    },
    memberOptions(val) {
      this.members = val.slice(0);
    }
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('org', {
      memberOptions: 'members'
    })
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('org', {
      update: 'update',
      addMember: 'addMember',
      queryMember: 'fetchMember',
      removeMember: 'removeMember'
    }),
    async memberFilter(val, update, abort) {
      update(() => {
        this.members = this.memberOptions.filter(
          user => user.name.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    async handleUpdateOrg() {
      await this.update(this.org);
      successNotify('修改成功');
    },
    async handleUpdateMember() {
      await this.update(this.org);
    },
    handleAddModalOpen() {
      this.step = 1;
      this.addMemberModel = createUserModel();
      this.$v.addMemberModel.$reset();
      this.addModalOpened = true;
    },
    async handleAdd() {
      this.$v.addMemberModel.$touch();
      this.$refs.memberForm.validate();
      if (this.$v.addMemberModel.$invalid) {
        return;
      }
      await this.addMember({
        orgId: this.org.id,
        ...this.addMemberModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    async handleRemoveMember(user) {
      await this.removeMember({
        orgId: this.org.id,
        id: user.id
      });
      successNotify('删除成功');
    },
    // TODO async rules
    async handleVerifyEmail() {
      if (this.$v.addMemberModel.email.$invalid) {
        return;
      }
      // email exist check
      const users = await resolveResponseError(() =>
        queryUser('', {
          email: this.addMemberModel.email
        })
      );
      this.step = 2;
      if (users.length === 0) {
        this.step = 2;
      } else {
        errorNotify('该邮件地址已注册');
      }
    }
  },
  async created() {
    const id = this.$route.params.id;
    this.org = await resolveResponseError(() => query(id));
    await this.queryMember({ orgId: id });

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.container
  flex: 1;
  background: white;
  margin: 0 auto;
  width: 100%;
  max-width: 820px;
  height: 100%;
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

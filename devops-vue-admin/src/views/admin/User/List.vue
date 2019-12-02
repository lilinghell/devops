<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page>
        <q-table
          :data="users"
          :columns="columns"
          :filter="filter"
          row-key="id"
          :pagination.sync="pagination"
          flat
          class="q-ma-md"
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
              <router-link to="" class="link">管理</router-link>
              <a @click="handleRemoveModalOpened(props.row)" class="link"
                >删除</a
              >
            </q-td>
          </template>
        </q-table>
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
        <q-form ref="userForm" @submit="handleAdd">
          <q-stepper v-model="step" vertical color="primary" header-nav>
            <q-step
              :name="1"
              title="请输入邮件地址"
              icon="email"
              :done="step > 1"
            >
              <q-input
                label="邮件"
                v-model="$v.addUserModel.email.$model"
                type="email"
                autofocus
                :rules="[
                  () => !$v.addUserModel.email.$error || '请输入邮件地址'
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
                    :disabled="$v.addUserModel.email.$invalid"
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
                v-model="$v.addUserModel.username.$model"
                type="text"
                dense
                autofocus
                :rules="[
                  () => !$v.addUserModel.username.$error || '请输入名称'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="account_box" class="q-mr-sm" />
                </template>
              </q-input>
              <q-input
                label="密码"
                v-model="$v.addUserModel.password.$model"
                type="password"
                dense
                :rules="[
                  () => !$v.addUserModel.password.$error || '请输入密码'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="lock" class="q-mr-sm" />
                </template>
              </q-input>
              <q-input
                label="确认密码"
                v-model="$v.addUserModel.password2.$model"
                type="password"
                dense
                :rules="[
                  () => !$v.addUserModel.password2.$error || '请输入确认密码'
                ]"
              >
                <template v-slot:before>
                  <q-icon name="lock" class="q-mr-sm" />
                </template>
              </q-input>
              <q-select
                label="角色"
                v-model="$v.addUserModel.type.$model"
                :options="types"
                dense
                :rules="[() => !$v.addUserModel.type.$error || '请选择角色']"
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

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除用户</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除用户{{ this.user.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveUser"
          />
          <q-btn flat label="取消" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required, email } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Page from '@/components/Page';
import {
  resolveResponseError,
  successNotify,
  errorNotify,
  formatSelectDisplay
} from '@/utils/utils';
import { query as queryUser } from '@/services/user';
import { createUserModel, vars } from '@/views/model';
import { set, get } from '@/views/setting';
const paginationKey = 'user/list/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'List',
  components: { PageHeaderWrapper, Loading, Page },
  data() {
    return {
      globalLoading: true,
      users: [],
      org: {},

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
      addUserModel: createUserModel(),
      types: vars.types,
      userRoles: vars.userRoles,
      step: 1,

      removeModalOpened: false,
      user: ''
    };
  },
  validations: {
    addUserModel: {
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
    userOptions(val) {
      this.users = val.slice(0);
    }
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('user', {
      userOptions: 'list'
    })
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('org', {
      update: 'update'
    }),
    ...mapActions('user', {
      addUser: 'add',
      queryUser: 'fetch',
      removeUser: 'remove'
    }),
    async handleUpdateUser() {
      await this.update(this.org);
    },
    handleAddModalOpen() {
      this.step = 1;
      this.addUserModel = createUserModel();
      this.$v.addUserModel.$reset();
      this.addModalOpened = true;
    },
    async handleAdd() {
      this.$v.addUserModel.$touch();
      this.$refs.userForm.validate();
      if (this.$v.addUserModel.$invalid) {
        return;
      }
      await this.addUser(
        Object.assign({}, this.addUserModel, {
          orgId: this.org.id
        })
      );
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    handleRemoveModalOpened(user) {
      this.removeModalOpened = true;
      this.user = user;
    },
    async handleRemoveUser() {
      await this.removeUser(this.user);
      this.removeModalOpened = false;
      successNotify('删除成功');
    },
    // TODO async rules
    async handleVerifyEmail() {
      if (this.$v.addUserModel.email.$invalid) {
        return;
      }
      // email exist check
      const users = await resolveResponseError(() =>
        queryUser('', {
          email: this.addUserModel.email
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
    await this.queryUser();

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
</style>

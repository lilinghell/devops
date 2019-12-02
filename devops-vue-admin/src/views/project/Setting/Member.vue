<template>
  <div class="bg-white q-pa-md">
    <q-table
      :data="members"
      :columns="columns"
      row-key="id"
      :pagination.sync="pagination"
      flat
      class="overflow-hidden"
    >
      <template v-slot:top-right>
        <q-btn
          color="primary"
          unelevated
          class="table-head-btn"
          @click="handleAddModalOpen"
        >
          新增成员<q-icon name="add" class="q-ml-sm" />
        </q-btn>
      </template>
      <template v-slot:body-cell-operation="props">
        <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
          <a @click="handleRemoveModalOpened(props.row)" class="link">删除</a>
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除成员</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除成员{{ this.member.user.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveMember"
          />
          <q-btn flat label="取消" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="addModalOpened">
      <q-card class="modal-content-xs">
        <q-toolbar class="bg-primary text-white">
          <q-btn flat v-close-popup round dense icon="arrow_back" />
          <q-toolbar-title>新增成员</q-toolbar-title>
        </q-toolbar>
        <q-form @submit="handleAddMember" ref="form">
          <q-card-section>
            <q-select
              label="成员"
              use-input
              transition-show="jump-down"
              transition-hide="jump-down"
              v-model="$v.addModel.user.$model"
              dense
              :options="users"
              @filter="userFilter"
              hide-selected
              fill-input
              :rules="[() => !$v.addModel.user.$error || '请选择成员']"
            >
              <template v-slot:no-option>
                <q-item dense>
                  <q-item-section side>
                    <q-icon name="warning" size="16px" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="text-grey-7">
                      没有可用数据
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </template>
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps" v-on="scope.itemEvents">
                  <q-item-section side>
                    <q-avatar size="24px">
                      <q-img :src="scope.opt.avatar_url" />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ scope.opt.name }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
            <q-select
              label="角色"
              v-model="$v.addModel.access_level.$model"
              dense
              :options="access_levels"
              :rules="[() => !$v.addModel.access_level.$error || '请选择角色']"
            />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              color="primary"
              unelevated
              type="submit"
              label="提交"
              :loading="loading['project/addModule']"
            />
            <q-btn color="primary" flat label="取消" v-close-popup />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import { successNotify, formatSelectDisplay } from '@/utils/utils';
import { createMemberModel } from '@/views/model';
import { set, get } from '@/views/setting';
import { vars } from '../model';
const paginationKey = 'setting/member/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'Member',
  components: {},
  data() {
    return {
      globalLoading: true,

      columns: [
        {
          name: 'name',
          label: '员工姓名',
          align: 'left',
          field: row => row.user.name,
          style: 'width: 30%'
        },
        {
          name: 'email',
          label: '邮件地址',
          align: 'center',
          field: row => row.user.email,
          style: 'width: 30%'
        },
        {
          name: 'phone',
          label: '电话',
          align: 'center',
          field: row => row.user.phone,
          style: 'width: 20%'
        },
        {
          name: 'access_level',
          label: '角色',
          align: 'center',
          field: row =>
            formatSelectDisplay(this.access_levels, row.access_level),
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
      term: '',

      addMemberModalOpened: false,
      userTerm: '',
      users: [],
      addModel: createMemberModel(),
      member: createMemberModel(),
      removeModalOpened: false,

      access_levels: vars.access_levels,
      addModalOpened: false
    };
  },
  validations: {
    addModel: {
      user: {
        name: { required }
      },
      access_level: { required }
    }
  },
  watch: {
    pagination(val) {
      setPagination({
        rowsPerPage: val.rowsPerPage
      });
    }
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('project', {
      members: 'members'
    }),
    ...mapState('user', {
      userOptions: 'list'
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('project', {
      addMember: 'addMember',
      removeMember: 'removeMember',
      queryMember: 'fetchMember'
    }),
    ...mapActions('user', {
      queryUser: 'fetch'
    }),

    userFilter(val, update, abort) {
      if (val === '') {
        return abort();
      }
      update(() => {
        this.users = this.userOptions.filter(
          user => user.name.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    handleRemoveModalOpened(member) {
      this.removeModalOpened = true;
      this.member = member;
    },
    async handleRemoveMember() {
      await this.removeMember({
        projectId: this.projectId,
        ...this.member
      });
      this.removeModalOpened = false;
      successNotify('删除成功');
    },
    async handleAddMember() {
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      await this.addMember({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    handleAddModalOpen() {
      this.addModel = createMemberModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    }
  },
  async created() {
    await this.queryMember({
      projectId: this.projectId
    });
    await this.queryUser();

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped></style>

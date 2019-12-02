<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page full-height>
        <q-splitter :value="30" disable class="full-height">
          <template v-slot:before>
            <div class="column full-height">
              <q-input
                v-model="term"
                dense
                outlined
                class="q-ma-md"
                placeholder="团队查询"
              >
                <template v-slot:after>
                  <q-btn
                    class="btn-add"
                    color="primary"
                    icon="mdi-set mdi-account-multiple-plus-outline"
                    unelevated
                    @click="handleAddTeamModalOpen"
                  />
                </template>
              </q-input>
              <q-list class="col scroll">
                <q-item
                  clickable
                  v-ripple
                  v-for="team in teamFilter()"
                  :key="team.id"
                  :active="team.active"
                  active-class="bg-teal-1"
                  @click="handleSelectTeam(team)"
                >
                  <q-item-section avatar>
                    <q-avatar
                      color="grey-7"
                      text-color="white"
                      icon="mdi-set mdi-account-group"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ team.name }}</q-item-label>
                    <q-item-label caption
                      >{{ team.owner.name }}
                      {{ team.owner.email }}</q-item-label
                    >
                  </q-item-section>
                  <q-item-section side>
                    <q-icon name="keyboard_arrow_right" color="grey-7" />
                  </q-item-section>
                </q-item>
              </q-list>
              <transition
                enter-active-class="animated slideInDown"
                leave-active-class="animated slideOutUp"
              >
                <q-card
                  v-show="addTeamModalOpened"
                  square
                  class="team-add-wrapper"
                >
                  <q-form ref="teamForm" @submit="handleAddTeam">
                    <q-card-section>
                      <div class="text-h6 text-white">新增团队</div>
                    </q-card-section>
                    <q-card-section>
                      <q-input
                        v-if="addTeamModalOpened"
                        label="名称"
                        v-model="$v.addTeamModel.name.$model"
                        type="text"
                        autofocus
                        dense
                        bg-color="white"
                        outlined
                        :rules="[
                          () => !$v.addTeamModel.name.$error || '请输入名称'
                        ]"
                      >
                      </q-input>
                    </q-card-section>
                    <q-card-section>
                      <q-select
                        label="负责人"
                        v-model="$v.addTeamModel.owner.$model"
                        :options="userOptions"
                        dense
                        bg-color="white"
                        outlined
                        :rules="[
                          () => !$v.addTeamModel.owner.$error || '请选择负责人'
                        ]"
                      >
                      </q-select>
                    </q-card-section>
                    <q-card-actions align="right">
                      <q-btn
                        color="white"
                        text-color="primary"
                        type="submit"
                        label="提交"
                        unelevated
                        :loading="loading['team/add']"
                      />
                      <q-btn
                        color="white"
                        flat
                        label="取消"
                        @click="addTeamModalOpened = false"
                      />
                    </q-card-actions>
                  </q-form>
                </q-card>
              </transition>
            </div>
          </template>
          <template v-slot:after>
            <q-table
              :data="members"
              :columns="columns"
              row-key="id"
              :pagination.sync="pagination"
              flat
              class="q-ma-md overflow-hidden"
            >
              <template v-slot:top-right>
                <transition-group
                  tag="div"
                  class="row justify-end"
                  enter-active-class="animated slideInLeft"
                  leave-active-class="animated slideOutRight absolute"
                >
                  <q-btn
                    icon="mdi-set mdi-account-plus-outline"
                    flat
                    round
                    color="primary"
                    unelevated
                    :disabled="!teams.some(team => team.active)"
                    @click="addMemberModalOpened = !addMemberModalOpened"
                    key="btn"
                  />
                  <q-select
                    class="fixed-head-input"
                    v-show="addMemberModalOpened"
                    key="input"
                    use-input
                    hide-dropdown-icon
                    transition-show="jump-down"
                    transition-hide="jump-down"
                    v-model="addMemberModel"
                    dense
                    :options="users"
                    @filter="userFilter"
                    @input="handleAddMember"
                    @blur="addMemberModalOpened = false"
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
                </transition-group>
              </template>
              <template v-slot:body-cell-operation="props">
                <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
                  <a @click="handleRemoveMember(props.row)" class="link"
                    >删除</a
                  >
                </q-td>
              </template>
            </q-table>
          </template>
        </q-splitter>
      </Page>
    </Loading>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Page from '@/components/Page';
import { successNotify, formatSelectDisplay } from '@/utils/utils';
import { createTeamModel, vars } from '@/views/model';
import { set, get } from '@/views/setting';
const paginationKey = 'user/team/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'Team',
  components: { PageHeaderWrapper, Loading, Page },
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
          name: 'team_role',
          label: '角色',
          align: 'center',
          field: row => formatSelectDisplay(this.teamRoles, row.access_level),
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

      addTeamModalOpened: false,
      addTeamModel: createTeamModel(),
      ...vars,

      addMemberModalOpened: false,
      userTerm: '',
      users: [],
      addMemberModel: '',
      team: ''
    };
  },
  validations: {
    addTeamModel: {
      name: { required },
      owner: { required }
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
    ...mapState('team', {
      teams: 'list',
      members: 'members'
    }),
    ...mapState('user', {
      userOptions: 'list'
    })
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('team', {
      addTeam: 'add',
      removeTeam: 'remove',
      updateTeam: 'update',
      queryTeam: 'fetch',
      addMember: 'addMember',
      removeMember: 'removeMember',
      updateMember: 'updateMember',
      queryMember: 'fetchMember'
    }),
    ...mapActions('user', {
      queryUser: 'fetch'
    }),
    ...mapMutations('team', ['saveMember']),

    teamFilter() {
      return this.teams.filter(
        team => team.name.toLowerCase().indexOf(this.term.toLowerCase()) > -1
      );
    },
    async handleSelectTeam(team) {
      this.teams.forEach(team => (team.active = false));
      team.active = true;
      this.team = team;

      await this.queryMember({ teamId: team.id });
    },
    async handleUpdateTeam() {
      await this.update(this.team);
    },
    handleAddTeamModalOpen() {
      this.addTeamModel = createTeamModel();
      this.$v.addTeamModel.$reset();
      this.addTeamModalOpened = true;
    },
    async handleAddTeam() {
      this.$v.addTeamModel.$touch();
      this.$refs.teamForm.validate();
      if (this.$v.addTeamModel.$invalid) {
        return;
      }
      await this.addTeam(this.addTeamModel);
      successNotify('新增成功');
      this.addTeamModalOpened = false;
    },
    handleRemoveTeam(id) {
      console.log(id);
    },
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
    async handleUpdateMember() {
      await this.update(this.team);
    },
    async handleRemoveMember(id) {
      await this.removeMember({
        teamId: this.team.id,
        id: id.id
      });
      successNotify('删除成功');
    },
    async handleAddMember(user) {
      this.addMemberModel = '';
      await this.addMember({
        teamId: this.team.id,
        user: user.id,
        ...user
      });
    }
  },
  async created() {
    await this.queryTeam();
    await this.queryUser();

    this.globalLoading = false;
  },
  mounted() {},
  destroyed() {
    this.saveMember([]);
  }
};
</script>

<style lang="stylus" scoped>
.team-add-wrapper
  background: $primary;
  position: absolute;
  z-index: 10;
  top: 0;
  left: 0;
  right: 0;
.btn-add
  width: 40px;
</style>

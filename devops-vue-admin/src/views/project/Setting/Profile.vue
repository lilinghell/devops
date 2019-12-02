<template>
  <div class="bg-white q-pa-md row flex-center">
    <div class="col-4">
      <Loading :visible="globalLoading">
        <q-form ref="form" @submit="handleUpdate">
          <Field stack-label label="名称">
            <q-input
              outlined
              v-model="$v.updateModel.name.$model"
              type="text"
              autofocus
              dense
              :rules="[() => !$v.updateModel.name.$error || '请输入项目名称']"
              placeholder="输入项目名称"
            />
          </Field>
          <Field stack-label label="归属团队">
            <q-select
              outlined
              use-input
              :display-value="
                formatSelectDisplay(teams, $v.updateModel.team.$model.id)
              "
              v-model="$v.updateModel.team.$model"
              dense
              :options="teams"
              @filter="teamFilter"
              :rules="[() => !$v.updateModel.team.$error || '请选择归属团队']"
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
            </q-select>
          </Field>
          <Field stack-label label="转让管理员">
            <q-select
              outlined
              use-input
              :display-value="
                formatSelectDisplay(users, $v.updateModel.owner.$model.id)
              "
              v-model="$v.updateModel.owner.$model"
              :options="users"
              dense
              @filter="userFilter"
              :rules="[() => !$v.updateModel.owner.$error || '请选择管理员']"
            >
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
            </q-select>
          </Field>
          <Field label="公开性" contracted>
            <q-option-group
              v-model="updateModel.visit_level"
              :options="visit_levels"
              color="primary"
              inline
            />
          </Field>
          <div class="text-right q-mt-lg">
            <q-btn
              type="submit"
              unelevated
              color="primary"
              label="修改"
              :loading="loading['project/update']"
            />
          </div>
        </q-form>
      </Loading>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import {
  resolveResponseError,
  successNotify,
  formatSelectDisplay
} from '@/utils/utils';
import { createProjectModel, vars } from '../model';
import { query as queryProject } from '@/services/project';

export default {
  name: 'Profile',
  components: { Loading, Field },
  data() {
    return {
      globalLoading: true,
      updateModel: createProjectModel(),
      visit_levels: vars.visit_levels,
      teams: [],
      members: []
    };
  },
  validations: {
    updateModel: {
      name: {
        required
      },
      team: {
        required
      },
      visit_level: {
        required
      },
      owner: {
        required
      }
    }
  },
  watch: {},
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('team', {
      teamOptions: 'list'
    }),
    ...mapState('project', {
      memberOptions: 'members'
    }),
    users() {
      return this.members.map(member => member.user);
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('team', {
      queryTeam: 'fetch'
    }),
    ...mapActions('project', {
      update: 'update',
      queryMember: 'fetchMember'
    }),
    teamFilter(val, update, abort) {
      update(() => {
        this.teams = this.teamOptions.filter(
          team => team.label.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    userFilter(val, update, abort) {
      update(() => {
        this.members = this.memberOptions.filter(
          member =>
            member.user.label.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    async handleUpdate() {
      this.$v.updateModel.$touch();
      this.$refs.form.validate();
      if (this.$v.updateModel.$invalid) {
        return;
      }
      await this.update(this.updateModel);
      successNotify('修改成功');
    }
  },
  async created() {
    const id = this.$route.params.projectId;
    this.updateModel = await resolveResponseError(() => queryProject(id));
    await this.queryTeam();
    this.teams = this.teamOptions.slice(0);
    await this.queryMember({
      projectId: id
    });
    this.members = this.memberOptions.slice(0);
    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped></style>

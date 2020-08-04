<template>
  <PageHeaderWrapper>
    <template v-slot:header>
      <q-card-section class="q-pl-none q-pt-none row items-start">
        <div class="col-8">
          <div class="text-h5 text-title">
            {{ app.name }}
            <q-badge class="q-ml-sm">{{ app.type }}</q-badge>
          </div>
          <div class="text-subtitle1 text-grey-7">{{ app.owner }}</div>
          <div class="text-subtitle2 text-grey-7">{{ app.description }}</div>
        </div>
        <q-space/>
        <q-btn-group unelevated>
          <q-btn outline color="primary" label="处理"/>
          <q-btn outline color="primary" label="处理"/>
          <q-btn outline color="primary" label="处理"/>
        </q-btn-group>
      </q-card-section>
      <q-card-section>
        <DescriptionList :col="1">
          <Description label="代码仓库">{{ app.repo.scm_url }}</Description>
        </DescriptionList>
      </q-card-section>
      <q-tabs
        align="left"
        v-model="tab"
        class="text-grey-7"
        active-color="primary"
        indicator-color="primary"
      >
        <q-tab name="_a" label="服务定义"/>
        <q-tab name="_b" label="SCM信息"/>
        <q-tab name="_c" label="流水线"/>
        <q-tab name="_d" label="任务"/>
      </q-tabs>
    </template>

    <Loading :visible="globalLoading">
      <q-tab-panels v-model="tab">
        <q-tab-panel name="_a">
          <div class="text-h6">服务定义</div>
        </q-tab-panel>
        <q-tab-panel name="_b" class="column panel">
          <div class="col row q-col-gutter-x-md">
            <div class="col-8">
              <q-table
                :data="branches"
                :columns="columns"
                row-key="id"
                flat
                square
                class="q-pa-md"
                :pagination="{ rowsPerPage: 0 }"
                hide-bottom
              >
                <template v-slot:body-cell-operation="props">
                  <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
                    <a :href="props.row.web_url" target="_blank" class="link"
                    >管理</a
                    >
                  </q-td>
                </template>
              </q-table>
            </div>
            <div class="col-4">
              <q-card flat>
                <q-form ref="SCMForm" @submit="handleUpdateSCM">
                  <q-toolbar class="bg-primary text-white">
                    <q-space/>
                    <q-btn
                      flat
                      size="12px"
                      round
                      icon="edit"
                      @click="editable = true"
                      v-show="!editable"
                    />
                    <template v-if="editable">
                      <q-btn
                        type="submit"
                        flat
                        size="12px"
                        round
                        icon="done"
                        :loading="loading['app/updateRepo']"
                      />
                      <q-btn
                        flat
                        size="12px"
                        round
                        icon="clear"
                        @click="handleResetSCM"
                      />
                    </template>
                  </q-toolbar>
                  <q-card-section class="q-gutter-y-sm">
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">SCM类型</span>
                      </template>
                      <q-select
                        filled
                        v-model="$v.updateSCMModel.type.$model"
                        :options="scmTypes"
                        :error="$v.updateSCMModel.type.$error"
                        dense
                        hint=""
                        bg-color="white"
                        hide-dropdown-icon
                        :disable="!editable"
                        hide-bottom-space
                      />
                    </Field>
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">代码仓库</span>
                      </template>
                      <q-input
                        filled
                        square
                        v-model="$v.updateSCMModel.scm_url.$model"
                        type="text"
                        bg-color="white"
                        dense
                        :error="$v.updateSCMModel.scm_url.$error"
                        hide-bottom-space
                        :disable="!editable"
                      />
                    </Field>
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">认证类型</span>
                      </template>
                      <q-select
                        filled
                        v-model="$v.updateSCMModel.auth_type.$model"
                        :options="authTypes"
                        :error="$v.updateSCMModel.auth_type.$error"
                        dense
                        hint=""
                        bg-color="white"
                        hide-dropdown-icon
                        :disable="!editable"
                        hide-bottom-space
                      />
                    </Field>
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">token</span>
                      </template>
                      <q-input
                        filled
                        square
                        v-model="$v.updateSCMModel.auth_token.$model"
                        type="text"
                        bg-color="white"
                        dense
                        :error="$v.updateSCMModel.auth_token.$error"
                        hide-bottom-space
                        :disable="!editable"
                      />
                    </Field>
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">主分支</span>
                      </template>
                      <q-input
                        filled
                        square
                        v-model="$v.updateSCMModel.branch.$model"
                        type="text"
                        bg-color="white"
                        dense
                        :error="$v.updateSCMModel.branch.$error"
                        hide-bottom-space
                        :disable="!editable"
                      >
                      </q-input>
                    </Field>
                  </q-card-section>
                </q-form>
              </q-card>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="_c">
          <div class="text-h6">流水线</div>
        </q-tab-panel>
        <q-tab-panel name="_d">
          <div class="text-h6">任务</div>
        </q-tab-panel>
      </q-tab-panels>
    </Loading>
  </PageHeaderWrapper>
</template>

<script>
import {mapState, mapActions} from 'vuex';
import {required} from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import DescriptionList from '@/components/DescriptionList';
import Description from '@/components/DescriptionList/Description';
import {queryApp} from '@/services/project';
import {resolveResponseError, successNotify} from '@/utils/utils';
import {createAppModel, createRepoModel, vars} from '../model';

export default {
  name: 'Profile',
  components: {
    PageHeaderWrapper,
    Loading,
    Field,
    DescriptionList, Description
  },
  data() {
    return {
      globalLoading: true,
      app: createAppModel(),
      tab: '_a',
      columns: [
        {
          name: 'name',
          label: '分支名',
          align: 'left',
          field: 'name',
          style: 'width: 50%'
        },
        {
          name: 'operation',
          label: '操作',
          align: 'right',
          field: row => row,
          style: 'width: 50%'
        }
      ],
      editable: false,
      updateSCMModel: createRepoModel(),
      ...vars
    };
  },
  validations: {
    updateSCMModel: {
      type: {required},
      scm_url: {required},
      auth_type: {required},
      auth_token: {required},
      branch: {required}
    }
  },
  watch: {},
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('app', {
      branches: 'branches'
    }),
    projectId() {
      return this.$route.params.projectId;
    },
    appId() {
      return this.$route.params.appId;
    }
  },
  methods: {
    ...mapActions('app', {
      queryBranch: 'fetchBranch',
      updateRepo: 'updateRepo'
    }),
    async handleUpdateSCM() {
      this.$v.updateSCMModel.$touch();
      this.$refs.SCMForm.validate();
      if (this.$v.updateSCMModel.$invalid) {
        return;
      }
      await this.updateRepo({
        projectId: this.projectId,
        appId: this.appId,
        ...this.updateSCMModel
      });
      Object.assign(this.app.repo, this.updateSCMModel);

      this.editable = false;
      successNotify('修改成功');
    },
    handleResetSCM() {
      this.editable = false;
      this.updateSCMModel = {
        ...(this.app.repo || createRepoModel())
      };
    }
  },
  async created() {
    this.app = await resolveResponseError(() =>
      queryApp(this.projectId, this.appId)
    );
    this.handleResetSCM();

    try {
      await this.queryBranch({
        projectId: this.projectId,
        appId: this.appId
      });
    } catch (e) {
      console.log(e);
    }

    this.globalLoading = false;
  },
  mounted() {
  }
};
</script>

<style lang="stylus" scoped>
.field
  font-weight: $text-weights.medium;
  color: $blue-grey-6;

.panel
  background: $layout-bgColor;
</style>

<template>
  <PageHeaderWrapper>
    <template v-slot:header>
      <q-card-section class="q-pl-none q-pt-none row items-start">
        <div class="col-8">
          <div class="text-h5 text-title">
            {{ feature.title }}
            <q-badge
              class="q-ml-xs"
              v-for="label in feature.labels"
              :key="label.color"
              align="middle"
              :style="`background: ${label.color}`"
              >{{ label.title }}</q-badge
            >
          </div>
          <div class="text-subtitle1 text-grey-7">{{ feature.owner.name }}</div>
          <div class="text-subtitle2 text-grey-7">
            {{ feature.description }}
          </div>
        </div>
        <q-space />
        <q-btn-group unelevated>
          <q-btn outline color="primary" label="处理" />
          <q-btn outline color="primary" label="处理" />
          <q-btn outline color="primary" label="处理" />
        </q-btn-group>
      </q-card-section>
      <q-card-section class="row">
        <div class="col-8 q-col-gutter-y-sm">
          <DescriptionList :col="2">
            <Description label="关联应用">
              <div class="q-gutter-x-sm">
                <span v-for="app in feature.apps" :key="app.name">{{
                  app.name
                }}</span>
              </div>
            </Description>
            <Description label="创建者">{{
              feature.created_by.name
            }}</Description>
            <Description label="处理人">{{ feature.owner.name }}</Description>
            <Description label="开始日期">{{ feature.start_date }}</Description>
            <Description label="结束日期">{{ feature.end_date }}</Description>
            <Description label="优先级">{{
              formatSelectDisplay(priorities, feature.priority)
            }}</Description>
            <Description label="重要程度">{{
              formatSelectDisplay(important, feature.important)
            }}</Description>
            <Description label="模块">{{ feature.module.name }}</Description>
            <Description label="附件">
              <div class="q-gutter-x-sm">
                <a
                  v-for="attachment in feature.attachments"
                  :key="attachment.id"
                  :src="attachment.file"
                  class="link"
                  >{{ attachment.filename }}</a
                >
              </div>
            </Description>
          </DescriptionList>
        </div>
        <q-space />
        <!--<div class="q-mr-lg">
          <div class="label">总任务数</div>
          <div class="value">20</div>
        </div>
        <div>
          <div class="label">已完成</div>
          <div class="value">12</div>
        </div>-->
      </q-card-section>
      <q-tabs
        align="left"
        v-model="tab"
        class="text-grey-7"
        active-color="primary"
        indicator-color="primary"
      >
        <q-tab name="_a" label="需求任务" />
        <q-tab name="_b" label="需求分支" />
        <q-tab name="_c" label="操作历史" />
      </q-tabs>
    </template>

    <Loading :visible="globalLoading">
      <q-tab-panels v-model="tab">
        <q-tab-panel name="_a">
          <div class="text-h6">需求任务</div>
        </q-tab-panel>
        <q-tab-panel name="_b" class="q-pa-none">
          <Page>
            <q-splitter :value="30" disable class="col">
              <template v-slot:before>
                <q-list>
                  <q-item
                    clickable
                    v-ripple
                    v-for="branch in branches"
                    :key="branch.id"
                    :active="branch.active"
                    active-class="bg-teal-1"
                    @click="handleSelectBranch(branch)"
                  >
                    <q-item-section avatar>
                      <q-avatar
                        color="grey-7"
                        text-color="white"
                        icon="mdi-set mdi-source-branch"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ branch.app.name }}</q-item-label>
                      <q-item-label caption>
                        <span v-if="branch.branch_name !== ''">{{
                          branch.branch_name
                        }}</span>
                        <span v-else class="text-warning">未创建/关联分支</span>
                      </q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-icon name="keyboard_arrow_right" color="grey-7" />
                    </q-item-section>
                  </q-item>
                </q-list>
              </template>
              <template v-slot:after>
                <div class="q-ma-xl" v-if="branch.branch_name === ''">
                  <div class="text-h4 text-weight-light">关联-新建分支</div>
                  <div class="row q-my-lg">
                    <div class="offset-2 col-6">
                      <q-form ref="form" @submit="handleAdd(branch)">
                        <Field label="代码分支" :label-col="4" align="right">
                          <q-option-group
                            v-model="addModel.addBranchType"
                            :options="addBranchTypes"
                            color="primary"
                            class="q-mb-sm"
                          />
                          <q-input
                            outlined
                            v-model="$v.addModel.branch_name.$model"
                            type="text"
                            dense
                            :rules="[
                              () =>
                                !$v.addModel.branch_name.$error ||
                                '请输入分支名称'
                            ]"
                            v-if="addModel.addBranchType === '1'"
                          />
                          <q-select
                            outlined
                            v-model="$v.addModel.ref.$model"
                            :options="gitBranches"
                            dense
                            :rules="[
                              () => !$v.addModel.ref.$error || '请关联代码分支'
                            ]"
                          />
                        </Field>
                        <div class="text-right q-mt-lg">
                          <q-btn
                            type="submit"
                            unelevated
                            color="primary"
                            label="创建"
                            :loading="loading['project/add']"
                          />
                        </div>
                      </q-form>
                    </div>
                  </div>
                </div>
                <q-list class="q-pa-md" separator v-else>
                  <q-item v-for="commit in commits" :key="commit.id">
                    <q-item-section>
                      <q-item-label>{{ commit.message }}</q-item-label>
                      <q-item-label caption>
                        {{ commit.author_name }} 提交
                        {{
                          commit.committed_date
                            | moment('YYYY年MM月DD日')
                        }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </template>
            </q-splitter>
          </Page>
        </q-tab-panel>

        <q-tab-panel name="_c">
          <q-list dense>
            <q-item v-for="log in logs" :key="log.id">
              <q-item-section>
                <q-item-label class="text-grey-7 q-gutter-x-sm">
                  <q-avatar size="24px">
                    <q-img :src="log.user.avatar_url" />
                  </q-avatar>
                  <span>{{ log.user.name }}</span>
                  <span>于</span>
                  <span class="text-weight-medium text-blue-grey-9">{{
                    log.created_at | moment('YYYY年MM月DD日')
                  }}</span>
                  <span class="text-italic">{{
                    formatSelectDisplay(logActions, log.action)
                  }}</span>
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>
      </q-tab-panels>
    </Loading>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import DescriptionList from '@/components/DescriptionList';
import Description from '@/components/DescriptionList/Description';
import Page from '@/components/Page';
import { queryFeature } from '@/services/project';
import { queryLog } from '@/services/api';
import { formatSelectDisplay, successNotify } from '@/utils/utils';
import { createFeatureModel, createBranchModel, vars } from '../model';
import { vars as globalVars } from '@/views/model';

export default {
  name: 'Profile',
  components: {
    PageHeaderWrapper,
    Loading,
    Field,
    DescriptionList,
    Description,
    Page
  },
  data() {
    return {
      globalLoading: true,
      feature: createFeatureModel(),
      tab: '_b',
      logs: [],

      ...vars,
      logActions: globalVars.logActions,

      branch: createBranchModel(),
      addModel: createBranchModel()
    };
  },
  validations: {
    addModel: {
      branch_name: {
        nameRequired(value) {
          if (this.addModel.addBranchType === '1') {
            return required(value);
          }
          return true;
        }
      },
      ref: {
        refRequired(value) {
          if (this.addModel.addBranchType === '2') {
            return required(value);
          }
          return true;
        }
      }
    }
  },
  watch: {},
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('feature', {
      branches: 'branches'
    }),
    ...mapState('app', {
      gitBranches: 'branches',
      commits: 'commits'
    }),
    projectId() {
      return this.$route.params.projectId;
    },
    featureId() {
      return this.$route.params.featureId;
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('feature', {
      queryBranch: 'fetchBranch',
      addBranch: 'addBranch'
    }),
    ...mapActions('app', {
      queryGitBranch: 'fetchBranch',
      queryCommit: 'fetchCommit'
    }),
    async handleSelectBranch(branch) {
      this.branches.forEach(branch => (branch.active = false));
      branch.active = true;
      this.branch = branch;
      this.addModel = createBranchModel();

      if (branch.branch_name === '') {
        await this.queryGitBranch({
          projectId: this.projectId,
          appId: branch.app.id
        });
      } else {
        await this.queryCommit({
          projectId: this.projectId,
          appId: branch.app.id
        });
      }
    },
    async handleAdd(branch) {
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      if (this.addModel.addBranchType !== '1') {
        this.addModel.branch_name = this.addModel.ref.name;
      }
      await this.addBranch({
        projectId: this.projectId,
        featureId: this.featureId,
        ...this.addModel,
        app: branch.app.id,
        feature: this.featureId
      });
      successNotify("创建成功")
    },
  },
  async created() {
    let project = {
      projectId: this.projectId,
      featureId: this.featureId
    };
    this.feature = await queryFeature(this.projectId, this.featureId);
    this.logs = await queryLog({
      project_id: this.projectId,
      resource_id: this.featureId,
      resource_type: 'features',
    });
    await this.queryBranch(project);
    if (this.branches.length > 0) {
      this.handleSelectBranch(this.branches[0]);
    }
    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.label
  color: $grey-7;
  text-align: right;
.value
  text-align: right;
  font-size: 20px;
  color: $grey-9;
</style>

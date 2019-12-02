<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page full-height>
        <q-splitter :value="25" disable class="full-height">
          <template v-slot:before>
            <div class="column full-height">
              <q-input
                v-model="term"
                dense
                outlined
                class="q-ma-md"
                placeholder="迭代查询"
              >
                <template v-slot:after>
                  <q-btn
                    class="btn-add"
                    color="primary"
                    icon="mdi-set mdi-shape-circle-plus"
                    unelevated
                    @click="handleAddModalOpen"
                  />
                </template>
              </q-input>
              <q-list class="col scroll" separator>
                <template v-for="iteration in iterations">
                  <q-item
                    :key="iteration.id"
                    clickable
                    v-ripple
                    :active="iteration.active"
                    active-class="bg-teal-1"
                    @click="handleSelectIteration(iteration)"
                  >
                    <q-item-section>
                      <q-item-label>
                        <span>{{ iteration.title }}</span>
                        <q-badge
                          align="middle"
                          :class="iteration.cls"
                          class="q-ml-sm"
                          >{{ iteration.tip }}</q-badge
                        >
                      </q-item-label>
                      <q-item-label caption>{{
                        iteration.owner.name
                      }}</q-item-label>
                      <q-item-label caption class="row items-center">
                        <q-linear-progress
                          stripe
                          rounded
                          style="height: 6px;"
                          :value="iteration.progress / 100"
                          class="col-6 q-mr-sm"
                          color="secondary"
                        />
                        {{ iteration.progress }}%
                      </q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-icon name="keyboard_arrow_right" color="grey-7" />
                    </q-item-section>
                  </q-item>
                </template>
              </q-list>
            </div>
          </template>
          <template v-slot:after>
            <q-splitter :value="66.66" disable>
              <template v-slot:before>
                <div class="q-pa-md column full-height relative-position">
                  <div class="text-h6">
                    <span>{{ iteration.title }}</span>
                    <q-badge
                      align="middle"
                      :class="iteration.cls"
                      class="q-mx-sm"
                      >{{ iteration.tip }}</q-badge
                    >
                  </div>
                  <div class="text-subtitle2 text-grey-7">
                    {{ iteration.owner.name }}
                  </div>
                  <div class="text-subtitle2 text-grey-7">
                    {{ iteration.start_date | moment('MM月DD日') }} -
                    {{ iteration.end_date | moment('MM月DD日') }}
                  </div>
                  <div
                    class="col row flex-center text-grey-5"
                    v-if="iterationFeatures.length === 0"
                  >
                    <span class="text-h6">添加一条需求</span>
                    <q-icon
                      size="28px"
                      class="q-ml-sm"
                      name="mdi-set mdi-hand-pointing-right"
                    />
                  </div>
                  <q-list class="col scroll" separator v-else>
                    <q-item
                      v-for="feature in iterationFeatures"
                      :key="feature.id"
                      class="q-py-md"
                    >
                      <q-item-section class="col-2">
                        <q-item-label class="text-grey-8">
                          {{
                            formatSelectDisplay(featureStatus, feature.status)
                          }}
                        </q-item-label>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label lines="1">
                          <span class="text-weight-medium">{{
                            feature.title
                          }}</span>
                          <span class="text-grey-7 q-mx-sm">{{
                            feature.owner.name
                          }}</span>
                          <router-link
                            :to="`feature/${feature.id}`"
                            class="link"
                          >
                            <q-icon name="mdi-set mdi-link-variant" />
                          </router-link>
                        </q-item-label>
                        <q-item-label caption lines="2">{{
                          feature.description
                        }}</q-item-label>
                        <q-item-label>
                          <q-badge
                            class="q-mr-xs"
                            v-for="label in feature.labels"
                            :key="label.color"
                            align="middle"
                            :style="`background: ${label.color}`"
                            >{{ label.title }}</q-badge
                          >
                        </q-item-label>
                      </q-item-section>
                      <q-item-section class="col-2 text-right">
                        <div class="text-grey-8 q-gutter-xs">
                          <template v-if="feature.status === 1">
                            <q-btn
                              size="12px"
                              flat
                              dense
                              round
                              icon="delete"
                              @click="handleRemoveIterationFeature(feature)"
                              :loading="loading['feature/update']"
                            />
                            <q-btn
                              size="12px"
                              flat
                              dense
                              round
                              icon="done"
                              @click="handleFinishFeature(feature)"
                              :loading="loading['feature/update']"
                            />
                          </template>
                        </div>
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <q-circular-progress
                    show-value
                    font-size="12px"
                    :value="iteration.progress"
                    size="50px"
                    :thickness="0.22"
                    color="secondary"
                    track-color="grey-3"
                    class="absolute-top-right text-grey-7 q-ma-md"
                    >{{ iteration.progress }}%</q-circular-progress
                  >
                </div>
              </template>
              <template v-slot:after>
                <div class="q-ma-md q-gutter-sm">
                  <q-btn
                    class="btn-add-feature"
                    color="blue-grey-6"
                    dense
                    size="sm"
                    unelevated
                    v-for="feature in otherFeatures"
                    :key="feature.id"
                    @click="handleAddIterationFeature(feature)"
                  >
                    <span>{{ feature.title }}</span>
                    <q-icon name="add" class="on-right" />
                    <q-tooltip
                      transition-show="fade"
                      transition-hide="fade"
                      anchor="bottom left"
                      self="top left"
                      :offset="[0, 8]"
                      max-width="310px"
                      content-class="shadow-1 bg-white text-grey-9"
                    >
                      <div class="row no-wrap q-pa-md">
                        <div class="col-6 q-gutter-y-sm">
                          <div class="text-h6">{{ feature.title }}</div>
                          <div class="q-gutter-xs">
                            <q-badge
                              v-for="label in feature.labels"
                              :key="label.color"
                              align="middle"
                              :style="`background: ${label.color}`"
                              >{{ label.color }}</q-badge
                            >
                          </div>
                          <div class="text-grey-7">
                            {{ feature.description }}
                          </div>
                        </div>
                        <q-separator vertical inset class="q-mx-lg" />
                        <div class="col column items-center">
                          <q-avatar size="72px">
                            <q-img :src="feature.owner.avatar_url" />
                          </q-avatar>
                          <div class="text-subtitle1 q-mt-md">
                            {{ feature.owner.name }}
                          </div>
                        </div>
                      </div>
                    </q-tooltip>
                  </q-btn>
                </div>
              </template>
            </q-splitter>
          </template>
        </q-splitter>
      </Page>
    </Loading>

    <q-dialog seamless v-model="addModalOpened" position="right" maximized>
      <q-layout view="lHh lpr lFf" container class="modal-content-col-4">
        <q-form @submit="handleAdd" ref="form">
          <q-header bordered class="bg-primary text-white">
            <q-toolbar>
              <q-btn flat v-close-popup round dense icon="arrow_back" />
              <q-toolbar-title>新增迭代</q-toolbar-title>
            </q-toolbar>
          </q-header>

          <q-page-container>
            <q-page padding>
              <Field :label-col="3" label="迭代名称">
                <q-input
                  filled
                  v-model="$v.addModel.title.$model"
                  type="text"
                  autofocus
                  dense
                  :rules="[() => !$v.addModel.title.$error || '请输入迭代名称']"
                />
              </Field>
              <Field :label-col="3" label="负责人">
                <q-select
                  filled
                  v-model="$v.addModel.owner.$model"
                  :options="users"
                  dense
                  :rules="[() => !$v.addModel.owner.$error || '请选择负责人']"
                />
              </Field>
              <Field :label-col="3" label="开始日期">
                <q-input
                  filled
                  v-model="$v.addModel.start_date.$model"
                  type="text"
                  dense
                  :rules="[
                    () => !$v.addModel.start_date.$error || '请选择开始日期'
                  ]"
                  mask="date"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy>
                        <q-date
                          dense
                          v-model="$v.addModel.start_date.$model"
                          :options="ltEndDate"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </Field>
              <Field :label-col="3" label="结束日期">
                <q-input
                  filled
                  v-model="$v.addModel.end_date.$model"
                  type="text"
                  dense
                  :rules="[
                    () => !$v.addModel.end_date.$error || '请选择结束日期'
                  ]"
                  mask="date"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy>
                        <q-date
                          v-model="$v.addModel.end_date.$model"
                          :options="gtStartDate"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </Field>
            </q-page>
          </q-page-container>

          <q-footer class="bg-white text-primary shadow-3">
            <q-toolbar>
              <q-space />
              <q-btn
                color="primary"
                unelevated
                type="submit"
                label="提交"
                :loading="loading['project/addIteration']"
              />
            </q-toolbar>
          </q-footer>
        </q-form>
      </q-layout>
    </q-dialog>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除迭代</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除迭代{{ this.removeModel.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemove"
          />
          <q-btn flat label="取消" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import Page from '@/components/Page';
import { successNotify, formatSelectDisplay } from '@/utils/utils';
import { createIterationModel, vars } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'iteration/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'List',
  components: { PageHeaderWrapper, Loading, Field, Page },
  data() {
    return {
      globalLoading: true,

      columns: [
        {
          name: 'title',
          label: '迭代名称',
          align: 'left',
          field: 'title',
          style: 'width: 15%'
        },
        {
          name: 'owner',
          label: '负责人',
          align: 'center',
          field: row => row.owner.name,
          style: 'width: 15%'
        },
        {
          name: 'start_date',
          label: '开始日期',
          align: 'center',
          field: 'start_date',
          style: 'width: 15%'
        },
        {
          name: 'end_date',
          label: '结束日期',
          align: 'center',
          field: 'end_date',
          style: 'width: 15%'
        },
        {
          name: 'progress',
          label: '进度',
          align: 'center',
          field: 'progress',
          style: 'width: 15%'
        },
        {
          name: 'operation',
          label: '操作',
          align: 'right',
          field: row => row,
          style: 'width: 25%'
        }
      ],
      pagination: getPagination(),

      addModalOpened: false,
      addModel: createIterationModel(),
      removeModalOpened: false,
      removeModel: '',

      ...vars,
      term: '',
      iteration: createIterationModel(),
      formatSelectDisplay
    };
  },
  validations: {
    addModel: {
      title: { required },
      owner: { required },
      start_date: { required },
      end_date: { required }
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
    ...mapState('iteration', {
      iterationOptions: 'list'
    }),
    ...mapState('feature', {
      features: 'list'
    }),
    ...mapGetters('project', ['users']),
    projectId() {
      return this.$route.params.projectId;
    },
    iterations() {
      const today = new Date();
      let iterations = this.iterationOptions.filter(
        iteration =>
          iteration.title.toLowerCase().indexOf(this.term.toLowerCase()) > -1
      );
      iterations.forEach(each => {
        if (new Date(each.start_date) > today) {
          each.cls = 'bg-grey-5';
          each.tip = '未开始';
        } else if (new Date(each.end_date) < today) {
          each.cls = 'bg-red-5';
          each.tip = '已过期';
        } else {
          each.cls = 'bg-green-5';
          each.tip = '进行中 ';
        }
      });
      return iterations;
    },
    iterationFeatures() {
      return this.features.filter(
        feature => feature.iteration.id === this.iteration.id
      );
    },
    otherFeatures() {
      return this.features.filter(feature => feature.iteration === '');
    }
  },
  methods: {
    ...mapActions('project', {
      queryMember: 'fetchMember'
    }),
    ...mapActions('feature', {
      queryFeature: 'fetch',
      updateFeature: 'update'
    }),
    ...mapActions('iteration', {
      addIteration: 'add',
      queryIteration: 'fetch',
      removeIteration: 'remove',
      updateIteration: 'update'
    }),
    handleAddModalOpen() {
      this.addModel = createIterationModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    },
    handleRemoveModalOpened(module) {
      this.removeModalOpened = true;
      this.removeModel = module;
    },
    async handleRemove() {
      await this.removeIteration({
        projectId: this.projectId,
        ...this.removeModel
      });
      this.removeModalOpened = false;
      successNotify('删除成功');
    },
    async handleAdd() {
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      await this.addIteration({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    },

    gtStartDate(date) {
      if (!this.addModel.start_date) {
        return true;
      }
      return new Date(date) >= new Date(this.addModel.start_date);
    },
    ltEndDate(date) {
      if (!this.addModel.end_date) {
        return true;
      }
      return new Date(date) <= new Date(this.addModel.end_date);
    },

    handleSelectIteration(iteration) {
      this.iterations.forEach(iteration => (iteration.active = false));
      iteration.active = true;
      this.iteration = iteration;
    },
    async handleFinishFeature(feature) {
      await this.updateFeature({
        projectId: this.projectId,
        ...feature,
        status: 2
      });
    },
    async handleRemoveIterationFeature(feature) {
      await this.updateFeature({
        projectId: this.projectId,
        ...feature,
        iteration: ''
      });
    },
    async handleAddIterationFeature(feature) {
      await this.updateFeature({
        projectId: this.projectId,
        ...feature,
        iteration: this.iteration.id
      });
      successNotify('添加成功');
    }
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryMember(project);
    await this.queryIteration(project);
    await this.queryFeature(project);
    if (this.iterationOptions.length > 0) {
      this.handleSelectIteration(this.iterationOptions[0]);
    }
    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.btn-add
  width: 40px;
.btn-add-feature
  padding: 4px 8px;
  transition: opacity .3s;
  opacity: 0.3;
  &:hover
    opacity: 1;
</style>

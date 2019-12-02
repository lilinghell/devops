<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page>
        <q-table
          :data="features"
          :columns="columns"
          row-key="id"
          :pagination.sync="pagination"
          flat
          class="q-ma-md"
        >
          <template v-slot:top-right>
            <q-btn
              color="primary"
              unelevated
              class="table-head-btn"
              @click="handleAddModalOpen"
            >
              新增需求<q-icon name="add" class="q-ml-sm" />
            </q-btn>
          </template>

          <template v-slot:body-cell-operation="props">
            <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
              <router-link :to="`feature/${props.row.id}`" class="link"
                >开发分支</router-link
              >
              <router-link :to="`feature/${props.row.id}`" class="link"
                >管理</router-link
              >
            </q-td>
          </template>
        </q-table>
      </Page>
    </Loading>

    <q-dialog seamless v-model="addModalOpened" position="right" maximized>
      <q-layout view="lHh lpr lFf" container class="modal-content-col-6">
        <q-form @submit="handleAdd" ref="form">
          <q-header bordered class="bg-primary text-white">
            <q-toolbar>
              <q-btn flat v-close-popup round dense icon="arrow_back" />
              <q-toolbar-title>新增需求</q-toolbar-title>
            </q-toolbar>
          </q-header>

          <q-page-container>
            <q-page class="column">
              <q-splitter :value="70" disable class="col">
                <template v-slot:before>
                  <div class="q-pa-lg">
                    <q-input
                      label="需求名称"
                      v-model="$v.addModel.title.$model"
                      type="text"
                      autofocus
                      dense
                      :rules="[
                        () => !$v.addModel.title.$error || '请输入需求名称'
                      ]"
                    />
                    <Field contracted label="描述">
                      <q-editor
                        v-model="addModel.description"
                        dense
                        :definitions="{
                          bold: {
                            label: 'Bold',
                            icon: null,
                            tip: 'My bold tooltip'
                          }
                        }"
                        class="q-mb-md"
                      />
                    </Field>
                    <Field contracted label="标签">
                      <q-select
                        filled
                        use-chips
                        multiple
                        v-model="addModel.labels"
                        :options="labels"
                        dense
                        hint=""
                      >
                        <template v-slot:option="scope">
                          <q-item
                            v-bind="scope.itemProps"
                            v-on="scope.itemEvents"
                          >
                            <q-item-section side>
                              <q-icon
                                name="mdi-set mdi-tag"
                                :style="`color: ${scope.opt.color}`"
                              />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>{{ scope.opt.title }}</q-item-label>
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
                    <q-uploader
                      :url="`${domain}/api/v1/attachments`"
                      :headers="[
                        { name: 'X-CSRFToken', value: getCookie('csrftoken') }
                      ]"
                      auto-upload
                      multiple
                      flat
                      bordered
                      class="uploader-container"
                      @uploaded="handleUploaded"
                    >
                      <template v-slot:header></template>
                      <template v-slot:list="scope">
                        <div class="uploader-content">
                          <div class="text-center q-py-lg text-grey-9">
                            拖拽文件<span class="text-weight-bold"> 至此 </span
                            >或者<a class="uploader-link"
                              >上传文件
                              <q-uploader-add-trigger />
                            </a>
                          </div>
                          <q-list
                            separator
                            inset
                            v-if="scope.files.length > 0"
                            class="q-px-md bg-white"
                          >
                            <q-item
                              v-for="file in scope.files"
                              :key="file.name"
                            >
                              <q-item-section>
                                <q-item-label
                                  class="text-weight-bold full-width ellipsis"
                                  >{{ file.name }}</q-item-label
                                >
                                <q-item-label caption>
                                  {{ file.__sizeLabel }} /
                                  {{ file.__progressLabel }}
                                </q-item-label>
                              </q-item-section>
                              <q-item-section top side>
                                <q-btn
                                  flat
                                  dense
                                  round
                                  icon="clear"
                                  color="grey-9"
                                  @click="scope.removeFile(file)"
                                />
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                      </template>
                    </q-uploader>
                  </div>
                </template>
                <template v-slot:after>
                  <div class="q-pa-lg">
                    <q-select
                      label="关联应用"
                      filled
                      use-chips
                      multiple
                      v-model="addModel.apps"
                      :options="apps"
                      dense
                      options-dense
                      :rules="[
                        () => !$v.addModel.apps.$error || '请选择关联应用'
                      ]"
                    />
                    <q-select
                      label="处理人"
                      filled
                      v-model="$v.addModel.owner.$model"
                      :options="users"
                      dense
                      options-dense
                      :rules="[
                        () => !$v.addModel.owner.$error || '请选择处理人'
                      ]"
                    />
                    <q-input
                      label="开始日期"
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
                            />
                          </q-popup-proxy>
                        </q-icon>
                      </template>
                    </q-input>
                    <q-input
                      label="结束日期"
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
                            <q-date v-model="$v.addModel.end_date.$model" />
                          </q-popup-proxy>
                        </q-icon>
                      </template>
                    </q-input>
                    <q-select
                      label="优先级"
                      filled
                      v-model="$v.addModel.priority.$model"
                      :options="priorities"
                      dense
                      options-dense
                      :rules="[
                        () => !$v.addModel.priority.$error || '请选择优先级'
                      ]"
                    />
                    <q-select
                      label="重要程度"
                      filled
                      v-model="$v.addModel.important.$model"
                      :options="important"
                      dense
                      options-dense
                      :rules="[
                        () => !$v.addModel.important.$error || '请选择优先级'
                      ]"
                    />
                    <q-select
                      label="模块"
                      filled
                      v-model="$v.addModel.module.$model"
                      :options="modules"
                      dense
                      options-dense
                      :rules="[
                        () => !$v.addModel.module.$error || '请选择模块'
                      ]"
                    />
                  </div>
                </template>
              </q-splitter>
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
                :loading="loading['project/addFeature']"
              />
            </q-toolbar>
          </q-footer>
        </q-form>
      </q-layout>
    </q-dialog>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除需求</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除需求{{ this.removeModel.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveFeature"
          />
          <q-btn flat label="取消" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import Page from '@/components/Page';
import { successNotify, formatSelectDisplay } from '@/utils/utils';
import { createFeatureModel, vars } from '../model';
import { set, get } from '@/views/setting';
import { Cookies } from 'quasar';
const paginationKey = 'feature/pagination';
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
          name: 'id',
          label: '编号',
          align: 'left',
          field: 'id',
          style: 'width: 12.5%'
        },
        {
          name: 'title',
          label: '标题',
          align: 'center',
          field: 'title',
          style: 'width: 12.5%'
        },
        {
          name: 'iteration',
          label: '迭代',
          align: 'center',
          field: row => row.iteration.title,
          style: 'width: 12.5%'
        },
        {
          name: 'owner',
          label: '处理人',
          align: 'center',
          field: row => row.owner.name,
          style: 'width: 12.5%'
        },
        {
          name: 'priority',
          label: '优先级',
          align: 'center',
          field: row => formatSelectDisplay(this.priorities, row.priority),
          style: 'width: 12.5%'
        },
        {
          name: 'status',
          label: '状态',
          align: 'center',
          field: row => formatSelectDisplay(this.featureStatus, row.status),
          style: 'width: 12.5%'
        },
        {
          name: 'end_date',
          label: '结束日期',
          align: 'center',
          field: 'end_date',
          style: 'width: 12.5%'
        },
        {
          name: 'operation',
          label: '操作',
          align: 'right',
          field: row => row,
          style: 'width: 12.5%'
        }
      ],
      pagination: getPagination(),

      addModalOpened: false,
      addModel: createFeatureModel(),
      removeModalOpened: false,
      removeModel: '',
      domain: window.location.origin,

      ...vars
    };
  },
  validations: {
    addModel: {
      title: { required },
      apps: { required },
      owner: { required },
      start_date: { required },
      end_date: { required },
      priority: { required },
      important: { required },
      module: { required },
      labels: { required }
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
    ...mapState('feature', {
      features: 'list'
    }),
    ...mapState('project', {
      labels: 'labels',
      members: 'members',
      modules: 'modules'
    }),
    ...mapState('app', {
      apps: 'list'
    }),
    projectId() {
      return this.$route.params.projectId;
    },
    users() {
      return this.members.map(member => member.user);
    }
  },
  methods: {
    ...mapActions('feature', {
      addFeature: 'add',
      queryFeature: 'fetch',
      removeFeature: 'remove'
    }),
    ...mapActions('project', {
      queryLabel: 'fetchLabel',
      queryMember: 'fetchMember',
      queryModule: 'fetchModule'
    }),
    ...mapActions('app', {
      queryApp: 'fetch'
    }),
    handleAddModalOpen() {
      this.addModel = createFeatureModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    },
    handleRemoveModalOpened(module) {
      this.removeModalOpened = true;
      this.removeModel = module;
    },
    async handleRemoveFeature() {
      await this.removeFeature({
        projectId: this.projectId,
        ...this.removeModel
      });
      this.removeModalOpened = false;
    },
    async handleAdd() {
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      await this.addFeature({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    handleUploaded({ files, xhr }) {
      const resp = JSON.parse(xhr.responseText);
      this.addModel.attachments.push(resp.data.id);
    },
    getCookie(key) {
      return Cookies.get(key);
    }
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryFeature(project);
    await this.queryLabel(project);
    await this.queryApp(project);
    await this.queryMember(project);
    await this.queryModule(project);
    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped></style>

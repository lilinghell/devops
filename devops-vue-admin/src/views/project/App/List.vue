<template>
  <PageHeaderWrapper>
    <Loading :visible="globalLoading">
      <Page>
        <q-table
          :data="apps"
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
              新增应用<q-icon name="add" class="q-ml-sm" />
            </q-btn>
          </template>

          <template v-slot:body-cell-operation="props">
            <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
              <router-link to="" class="link">流水线</router-link>
              <router-link :to="`app/${props.row.id}`" class="link"
                >管理</router-link
              >
              <a @click="handleRemoveModalOpened(props.row)" class="link"
                >删除</a
              >
            </q-td>
          </template>
        </q-table>
      </Page>
    </Loading>

    <q-dialog seamless v-model="addModalOpened" position="right" maximized>
      <q-layout view="lHh lpr lFf" container class="modal-content-col-4">
        <q-form @submit="handleAdd" ref="form">
          <q-header bordered class="bg-primary text-white">
            <q-toolbar>
              <q-btn flat v-close-popup round dense icon="arrow_back" />
              <q-toolbar-title>新增应用</q-toolbar-title>
            </q-toolbar>
          </q-header>

          <q-page-container>
            <q-page padding>
              <Field :label-col="3" label="应用名称">
                <q-input
                  filled
                  v-model="$v.addModel.name.$model"
                  type="text"
                  autofocus
                  dense
                  :rules="[() => !$v.addModel.name.$error || '请输入应用名称']"
                />
              </Field>
              <Field :label-col="3" label="描述">
                <q-input
                  filled
                  v-model="addModel.description"
                  type="text"
                  autogrow
                  dense
                  hint=""
                />
              </Field>
              <Field :label-col="3" label="应用类型">
                <q-select
                  filled
                  v-model="$v.addModel.type.$model"
                  :options="appTypes"
                  dense
                  :rules="[() => !$v.addModel.type.$error || '请选择应用类型']"
                />
              </Field>
              <div class="row">
                <a
                  @click="otherVisible = !otherVisible"
                  class="offset-3 link other-link"
                >
                  <q-icon
                    size="20px"
                    name="mdi-set mdi-chevron-right"
                    :class="otherVisible ? 'rotate-90' : ''"
                  />高级项
                </a>
              </div>
              <q-slide-transition>
                <div v-show="otherVisible">
                  <Field :label-col="3" label="SCM类型">
                    <q-select
                      filled
                      v-model="addModel.repo.type"
                      :options="scmTypes"
                      dense
                      hint=""
                    />
                  </Field>
                  <Field :label-col="3" label="SCM URL">
                    <q-input
                      filled
                      v-model="addModel.repo.scm_url"
                      type="text"
                      dense
                      hint=""
                    />
                  </Field>
                  <Field :label-col="3" label="认证token">
                    <q-input
                      filled
                      v-model="addModel.repo.auth_token"
                      type="text"
                      dense
                      hint=""
                    />
                  </Field>
                </div>
              </q-slide-transition>
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
                :loading="loading['project/addApp']"
              />
            </q-toolbar>
          </q-footer>
        </q-form>
      </q-layout>
    </q-dialog>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除应用</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除应用{{ this.removeModel.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveApp"
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
import { successNotify } from '@/utils/utils';
import { createAppModel, vars } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'app/pagination';
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
          name: 'name',
          label: '应用名称',
          align: 'left',
          field: 'name',
          style: 'width: 25%'
        },
        {
          name: 'type',
          label: '类型',
          align: 'center',
          field: 'type',
          style: 'width: 25%'
        },
        {
          name: 'scm_url',
          label: '仓库地址',
          align: 'center',
          field: row => row.repo.scm_url,
          style: 'width: 25%'
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
      addModel: createAppModel(),
      removeModalOpened: false,
      removeModel: '',

      ...vars,

      otherVisible: false
    };
  },
  validations: {
    addModel: {
      name: { required },
      type: { required }
    }
  },
  watch: {
    pagination(val) {
      setPagination({
        rowsPerPage: val.rowsPerPage
      });
    },
    otherVisible(val) {}
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('app', {
      apps: 'list'
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    ...mapActions('app', {
      addApp: 'add',
      queryApp: 'fetch',
      removeApp: 'remove'
    }),
    handleAddModalOpen() {
      this.addModel = createAppModel();
      this.$v.addModel.$reset();
      this.otherVisible = false;
      this.addModalOpened = true;
    },
    handleRemoveModalOpened(module) {
      this.removeModalOpened = true;
      this.removeModel = module;
    },
    async handleRemoveApp() {
      await this.removeApp({
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
      await this.addApp({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    }
  },
  async created() {
    await this.queryApp({
      projectId: this.projectId
    });
    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.other-link
  margin-bottom: 12px;
  i
    transition: .3s;
</style>

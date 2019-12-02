<template>
  <div class="bg-white q-pa-md">
    <q-table
      :data="modules"
      :columns="columns"
      row-key="id"
      :pagination.sync="pagination"
      flat
      class="overflow-hidden"
      wrap-cells
    >
      <template v-slot:top-right>
        <q-btn
          color="primary"
          unelevated
          class="table-head-btn"
          @click="handleAddModalOpen"
        >
          新增模块<q-icon name="add" class="q-ml-sm" />
        </q-btn>
      </template>
      <template v-slot:body-cell-operation="props">
        <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
          <a @click="handleRemoveModalOpened(props.row)" class="link">删除</a>
        </q-td>
      </template>
      <template v-slot:body-cell-description="props">
        <q-td :class="props.col.__tdClass">
          <div class="ellipsis-2-lines">
            {{ props.row.description }}
            <q-tooltip
              transition-show="fade"
              transition-hide="fade"
              max-width="300px"
              anchor="top right"
              self="top left"
              >{{ props.row.description }}</q-tooltip
            >
          </div>
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="addModalOpened">
      <q-card class="modal-content-xs">
        <q-toolbar class="bg-primary text-white">
          <q-btn flat v-close-popup round dense icon="arrow_back" />
          <q-toolbar-title>新增模块</q-toolbar-title>
        </q-toolbar>
        <q-form @submit="handleAdd" ref="form">
          <q-card-section>
            <q-input
              label="模块名称"
              v-model="$v.addModel.name.$model"
              type="text"
              autofocus
              dense
              :rules="[() => !$v.addModel.name.$error || '请输入模块名称']"
            />
            <q-input
              label="描述"
              v-model="addModel.description"
              type="text"
              autogrow
              dense
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

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除模块</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除模块{{ this.removeModel.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveModule"
          />
          <q-btn flat label="取消" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import { successNotify } from '@/utils/utils';
import { createModuleModel } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'setting/module/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'Module',
  components: {},
  data() {
    return {
      globalLoading: true,

      columns: [
        {
          name: 'name',
          label: '模块名称',
          align: 'left',
          field: 'name',
          style: 'width: 20%'
        },
        {
          name: 'description',
          label: '描述',
          align: 'center',
          field: 'description',
          style: 'width: 40%'
        },
        {
          name: 'created_at',
          label: '创建时间',
          align: 'center',
          field: 'created_at',
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

      addModalOpened: false,
      userTerm: '',
      users: [],
      addModel: createModuleModel(),
      removeModel: createModuleModel(),
      removeModalOpened: false
    };
  },
  validations: {
    addModel: {
      name: { required }
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
      modules: 'modules'
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    ...mapActions('project', {
      addModule: 'addModule',
      removeModule: 'removeModule',
      queryModule: 'fetchModule'
    }),

    handleAddModalOpen() {
      this.addModel = createModuleModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    },
    handleRemoveModalOpened(module) {
      this.removeModalOpened = true;
      this.removeModel = module;
    },
    async handleRemoveModule() {
      await this.removeModule({
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
      await this.addModule({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    }
  },
  async created() {
    await this.queryModule({
      projectId: this.projectId
    });

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped></style>

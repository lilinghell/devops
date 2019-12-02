<template>
  <div class="bg-white q-pa-md">
    <q-table
      :data="labels"
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
          新增标签<q-icon name="add" class="q-ml-sm" />
        </q-btn>
      </template>
      <template v-slot:body-cell-operation="props">
        <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
          <a @click="handleRemoveModalOpened(props.row)" class="link">删除</a>
        </q-td>
      </template>
      <template v-slot:body-cell-title="props">
        <q-td :class="props.col.__tdClass">
          <q-badge
            align="middle"
            :style="`background: ${props.row.color}`"
            class="q-mr-sm"
            >{{ props.row.color }}</q-badge
          >{{ props.row.title }}
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="addModalOpened">
      <q-card class="modal-content-xs">
        <q-toolbar class="bg-primary text-white">
          <q-btn flat v-close-popup round dense icon="arrow_back" />
          <q-toolbar-title>新增标签</q-toolbar-title>
        </q-toolbar>
        <q-form @submit="handleAdd" ref="form">
          <q-card-section>
            <q-input
              label="标签名称"
              v-model="$v.addModel.title.$model"
              type="text"
              autofocus
              dense
              :rules="[() => !$v.addModel.title.$error || '请输入标签名称']"
            />
            <div class="q-gutter-x-sm">
              <q-btn
                v-for="each in colors"
                :key="each.label"
                :style="`background: ${each.value}`"
                class="label-btn"
                @click="addModel.color = each.value"
              >
                <transition
                  enter-active-class="animated fadeIn"
                  leave-active-class="animated fadeOut"
                >
                  <q-icon
                    name="done"
                    class="text-weight-bolder"
                    color="white"
                    v-show="addModel.color === each.value"
                  />
                </transition>
              </q-btn>
            </div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              color="primary"
              unelevated
              type="submit"
              label="提交"
              :loading="loading['project/addLabel']"
            />
            <q-btn color="primary" flat label="取消" v-close-popup />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除标签</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">
            确认删除标签{{ this.removeModel.title }}
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            unelevated
            label="确认"
            color="primary"
            @click="handleRemoveLabel"
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
import { createLabelModel, vars } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'setting/label/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'Label',
  components: {},
  data() {
    return {
      globalLoading: true,

      columns: [
        {
          name: 'title',
          label: '标签名称',
          align: 'left',
          field: 'title',
          style: 'width: 60%'
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
      addModel: createLabelModel(),
      removeModel: createLabelModel(),
      removeModalOpened: false,

      colors: vars.label_colors
    };
  },
  validations: {
    addModel: {
      title: { required },
      color: { required }
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
      labels: 'labels'
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    ...mapActions('project', {
      addLabel: 'addLabel',
      removeLabel: 'removeLabel',
      queryLabel: 'fetchLabel'
    }),

    handleAddModalOpen() {
      this.addModel = createLabelModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    },
    handleRemoveModalOpened(label) {
      this.removeModalOpened = true;
      this.removeModel = label;
    },
    async handleRemoveLabel() {
      await this.removeLabel({
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
      await this.addLabel({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    }
  },
  async created() {
    await this.queryLabel({
      projectId: this.projectId
    });

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.label-btn
  width: 32px;
  height: 32px;
  min-height: 32px;
</style>

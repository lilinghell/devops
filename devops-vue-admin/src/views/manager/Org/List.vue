<template>
  <PageHeaderWrapper>
    <Loading :visible="loading['org/fetch']">
      <Page class="bg-transparent" full-height>
        <div class="col">
          <div class="container scroll">
            <q-table
              :data="list"
              :columns="columns"
              :filter="filter"
              row-key="id"
              :pagination.sync="pagination"
              flat
            >
              <template v-slot:top-left>
                <q-input v-model="filter" dense class="table-head-input">
                  <template v-slot:append>
                    <q-icon name="search" color="primary" />
                  </template>
                </q-input>
              </template>
              <template v-slot:top-right>
                <q-btn
                  color="primary"
                  unelevated
                  class="table-head-btn"
                  @click="handleAddModalOpen"
                >
                  新增企业<q-icon name="add" class="q-ml-sm" />
                </q-btn>
              </template>
              <template v-slot:body-cell-operation="props">
                <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
                  <router-link :to="`org/${props.row.id}`" class="link"
                    >管理</router-link
                  >
                  <a @click="handleRemove(props.row)" class="link">删除</a>
                </q-td>
              </template>
            </q-table>
          </div>
        </div>
      </Page>
    </Loading>
    <q-dialog v-model="addModalOpened">
      <q-card class="modal-content-xs">
        <q-form @submit="handleAdd" ref="form">
          <q-card-section>
            <div class="text-h6">新增企业</div>
          </q-card-section>

          <q-card-section>
            <q-input
              label="企业名称"
              v-model="$v.addOrgModel.name.$model"
              type="text"
              autofocus
              dense
              :rules="[() => !$v.addOrgModel.name.$error || '请输入企业名称']"
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn
              unelevated
              type="submit"
              label="提交"
              :loading="loading['org/add']"
            />
            <q-btn flat label="取消" v-close-popup />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </PageHeaderWrapper>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import Loading from '@/components/Loading';
import Page from '@/components/Page';
import { set, get } from '@/views/setting';
import { createOrgModel } from '@/views/model';
import { successNotify } from '@/utils/utils';
const paginationKey = 'org/list/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'List',
  components: { PageHeaderWrapper, Loading, Page },
  data() {
    return {
      columns: [
        {
          name: 'name',
          label: '企业名称',
          align: 'left',
          field: 'name',
          style: 'width: 50%'
        },
        {
          name: 'created_date',
          label: '加入时间',
          align: 'center',
          field: 'created_date',
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
      filter: '',

      addModalOpened: false,
      addOrgModel: createOrgModel()
    };
  },
  validations: {
    addOrgModel: {
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
    ...mapState('org', ['list']),
    ...mapState('global', ['loading'])
  },
  methods: {
    ...mapActions('org', ['add', 'remove', 'fetch']),
    handleAddModalOpen() {
      this.addOrgModel = createOrgModel();
      this.$v.addOrgModel.$reset();
      this.addModalOpened = true;
    },
    async handleAdd() {
      this.$v.addOrgModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addOrgModel.$invalid) {
        return;
      }
      await this.add(this.addOrgModel);
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    async handleRemove(org) {
      await this.remove(org);
      successNotify('删除成功');
    }
  },
  async created() {
    await this.fetch();
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.container
  background: white;
  margin: 0 auto;
  padding: 16px;
  width: 100%;
  height: 100%;
  max-width: 820px;
</style>

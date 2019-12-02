<template>
  <div class="container">
    <div class="row q-col-gutter-x-lg">
      <div class="col-9 q-gutter-y-md">
        <SlideBar v-model="projectVisible" title="我的项目">
          <Loading :visible="globalLoading">
            <div class="row grid-container">
              <div class="col-3">
                <q-card square bordered flat class="grid-border">
                  <q-item
                    class="fit row flex-center text-grey-7"
                    clickable
                    v-ripple
                    @click="$root.$emit('toggleProjectAddModal')"
                  >
                    <q-icon flat name="add" class="q-mr-sm" />新建项目
                  </q-item>
                </q-card>
              </div>
              <div
                class="col-3"
                v-for="project in currentProjects"
                :key="project.id"
              >
                <q-card square bordered flat class="grid-border">
                  <q-item
                    clickable
                    v-ripple
                    :to="`/project/${project.id}/home`"
                    class="q-pa-md"
                  >
                    <q-item-section>
                      <div class="text-h6 text-title">{{ project.name }}</div>
                      <q-item-label class="q-mb-md" caption>{{
                        project.team.name
                      }}</q-item-label>
                      <q-item-label caption lines="1">{{
                        project.description
                      }}</q-item-label>
                    </q-item-section>
                    <q-item-section avatar top>
                      <q-avatar size="36px">
                        <q-img :src="project.owner.avatar_url" />
                      </q-avatar>
                    </q-item-section>
                  </q-item>
                  <q-separator />
                  <q-card-actions class="text-teal-9">
                    <q-btn
                      flat
                      dense
                      :to="`/project/${project.id}/feature`"
                      icon="mdi-set mdi-card-bulleted-outline"
                    >
                      <q-tooltip
                        content-class="bg-grey-10"
                        transition-show="fade"
                        transition-hide="fade"
                        anchor="top middle"
                        self="bottom middle"
                        :offset="[0, 4]"
                        >需求</q-tooltip
                      >
                    </q-btn>
                    <q-btn
                      flat
                      dense
                      :to="`/project/${project.id}/workItem`"
                      icon="developer_board"
                    >
                      <q-tooltip
                        content-class="bg-grey-10"
                        transition-show="fade"
                        transition-hide="fade"
                        anchor="top middle"
                        self="bottom middle"
                        :offset="[0, 4]"
                        >任务</q-tooltip
                      >
                    </q-btn>
                    <q-btn
                      flat
                      dense
                      :to="`/project/${project.id}`"
                      label="流水线"
                    />
                  </q-card-actions>
                </q-card>
              </div>
            </div>
          </Loading>
        </SlideBar>
        <SlideBar
          v-model="workItemVisible"
          :title="`我的任务${createdByMySelf ? '（我创建的）' : ''}`"
        >
          <template v-slot:before>
            <q-btn dense flat icon="menu">
              <q-menu>
                <q-list dense class="text-blue-grey-9">
                  <q-item>
                    <q-toggle label="我创建的" v-model="createdByMySelf" />
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </template>
          <Loading :visible="globalLoading">
            <q-table
              :data="currentWorkItems"
              :columns="columns"
              row-key="id"
              :pagination.sync="pagination"
              flat
            />
          </Loading>
        </SlideBar>
      </div>
      <div class="col-3">
        <q-card square flat>
          <q-bar class="bg-primary text-white">
            <q-btn dense flat icon="menu" />
            <div>最近活动</div>
            <q-space />
            <q-btn dense flat icon="minimize" />
            <q-btn dense flat icon="crop_square" />
            <q-btn dense flat icon="close" />
          </q-bar>
          <q-card-section> </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Loading from '@/components/Loading';
import SlideBar from '@/components/SlideBar';
import { set, get } from '@/views/setting';
const paginationKey = 'workplace';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'Workplace',
  components: { Loading, SlideBar },
  data() {
    return {
      globalLoading: true,
      projectVisible: true,
      workItemVisible: true,
      createdByMySelf: false,

      columns: [
        {
          name: 'title',
          label: '任务名称',
          align: 'center',
          field: 'title',
          style: 'width: 25%'
        },
        {
          name: 'feature',
          label: '关联需求',
          align: 'center',
          field: row => row.feature.title,
          style: 'width: 25%'
        },
        {
          name: 'status',
          label: '状态',
          align: 'center',
          field: 'status',
          style: 'width: 25%'
        },
        {
          name: 'end_date',
          label: '截止日期',
          align: 'center',
          field: 'end_date',
          style: 'width: 25%'
        }
      ],
      pagination: getPagination()
    };
  },
  watch: {
    pagination(val) {
      setPagination({
        rowsPerPage: val.rowsPerPage
      });
    }
  },
  computed: {
    ...mapState('project', ['currentProjects']),
    ...mapState('workItem', ['currentWorkItems'])
  },
  methods: {
    ...mapActions('project', {
      queryProject: 'fetchCurrent'
    }),
    ...mapActions('workItem', {
      queryWorkItem: 'fetchCurrent'
    })
  },
  async created() {
    await this.queryProject();
    await this.queryWorkItem();

    this.globalLoading = false;
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.container
  padding: 24px 24px 0;
</style>

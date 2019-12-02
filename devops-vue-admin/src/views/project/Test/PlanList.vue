<template>
  <div class="bg-white q-pa-md flex-center">
    <Loading :visible="globalLoading">
      <template>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-grey-7"
          active-color="primary"
          indicator-color="primary"
        >
          <q-tab name="_a" label="Plan" />
          <q-tab name="_b" label="AutoPlan" />
        </q-tabs>
      </template>
      <q-tab-panels v-model="tab">
        <q-tab-panel name="_a" style="height: 680px">
          <q-splitter :value="25" disable class="full-height">
            <template v-slot:before>
              <div class="column full-height">
                <q-input v-model="term" dense outlined class="q-ma-md" placeholder="计划查询">
                  <template v-slot:after>
                    <q-btn
                      class="btn-add"
                      color="primary"
                      icon="mdi-set mdi-shape-circle-plus"
                      unelevated
                      @click="medium = true"
                    />
                  </template>
                </q-input>
                <q-list class="col scroll" separator>
                  <template v-for="testplan in testPlans">
                    <q-item
                      :key="testplan.id"
                      clickable
                      v-ripple
                      :active="testplan.active"
                      active-class="bg-teal-1"
                      @click="handleSelectTestPlan(testplan)"
                    >
                      <q-item-section>
                        <q-item-label>
                          <span>{{ testplan.name }}</span>
                          <q-badge
                            align="middle"
                            :class="testplan.cls"
                            class="q-ml-sm"
                          >{{ testplan.tip }}</q-badge>
                        </q-item-label>
                        <q-item-label caption>
                          {{
                          formatSelectDisplay(users, testplan.user)
                          }}
                        </q-item-label>
                        <div class="text-subtitle2 text-grey-7">
                          {{ testplan.start_date | moment('MM月DD日') }} -
                          {{ testplan.end_date | moment('MM月DD日') }}
                        </div>
                        <q-item-label caption class="row items-center">
                          <q-linear-progress
                            stripe
                            rounded
                            style="height: 6px;"
                            :value="getProgress(testplan)/100"
                            class="col-6 q-mr-sm"
                            color="secondary"
                          />
                          {{ getProgress(testplan) }}%
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
                      <span>{{ testPlan.name }}</span>
                      <q-badge
                        align="middle"
                        :class="testPlan.cls"
                        class="q-mx-sm"
                      >{{ testPlan.tip }}</q-badge>
                    </div>
                    <div
                      class="text-subtitle2 text-grey-7"
                    >{{ formatSelectDisplay(users, testPlan.user) }}</div>
                    <div class="text-subtitle2 text-grey-7">
                      {{ testPlan.start_date | moment('MM月DD日') }} -
                      {{ testPlan.end_date | moment('MM月DD日') }}
                    </div>
                    <div class="text-subtitle2 text-grey-7">{{ testPlan.description }}</div>
                    <div class="col row flex-center text-grey-5" v-if="!testPlan.case">
                      <span class="text-h6">添加一条用例</span>
                      <q-icon size="28px" class="q-ml-sm" name="mdi-set mdi-hand-pointing-right" />
                    </div>

                    <q-list class="col scroll" separator v-else>
                      <q-item v-for="testCase in planCases" :key="testCase.id" class="q-py-md">
                        <q-item-section class="col-3">
                          <q-item-label class="text-grey-8">
                            <q-select
                              filled
                              :display-value="formatSelectDisplay(caseStatus, testCase.status)"
                              v-model="testCase.status"
                              :options="caseStatus"
                              @input="handUpdateTestCase(testCase)"
                              dense
                              hint
                              emit-value
                              bg-color="white"
                              hide-bottom-space
                            />
                          </q-item-label>
                        </q-item-section>
                        <q-item-section>
                          <q-item-label lines="1">
                            <span class="text-weight-medium">
                              {{
                              testCase.name
                              }}
                            </span>
                            <span class="text-grey-7 q-mx-sm">
                              {{
                              formatSelectDisplay(users, testCase.user)
                              }}
                            </span>
                            <router-link :to="`caseProfile`" class="link">
                              <q-icon name="mdi-set mdi-link-variant" />
                            </router-link>
                          </q-item-label>
                          <q-item-label caption lines="2">
                            {{
                            testCase.desc
                            }}
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-circular-progress
                      show-value
                      font-size="12px"
                      :value="getProgress(testPlan)"
                      size="50px"
                      :thickness="0.22"
                      color="secondary"
                      track-color="grey-3"
                      class="absolute-top-right text-grey-7 q-ma-md"
                    >{{ getProgress(testPlan) }}%</q-circular-progress>
                  </div>
                </template>
                <template v-slot:after>
                  <div class="q-ma-md q-gutter-sm" v-if="showTree">
                    <q-tree
                      :nodes="planUpdateGroupInfo"
                      node-key="id"
                      tick-strategy="leaf"
                      selected-color="primary"
                      :selected.sync="selected"
                      :ticked.sync="planTicked"
                      :expanded.sync="expanded"
                      default-expand-all
                    ></q-tree>
                    <q-toolbar>
                      <q-space />
                      <q-btn color="primary" @click="handleAddPlanCase()" label="修改"></q-btn>
                    </q-toolbar>
                  </div>
                </template>
              </q-splitter>
            </template>
          </q-splitter>
        </q-tab-panel>
        <!--自动计划-->
        <q-tab-panel name="_b" style="height: 680px">
          <AutoPlanList></AutoPlanList>
        </q-tab-panel>
      </q-tab-panels>

      <q-dialog v-if="medium" v-model="medium">
        <q-card style="width: 500px;">
          <q-form @submit="handlePlanAdd" ref="form">
            <q-stepper v-model="plan_step" color="primary" animated>
              <q-step :name="1" title="输入基本信息" icon="settings" :done="plan_step > 1">
                <q-stepper-navigation>
                  <div class="q-pa-lg">
                    <q-input
                      label="计划名称"
                      v-model="addPlanModel.name"
                      type="text"
                      autofocus
                      dense
                      :rules="[
                         () => !$v.addPlanModel.name.$error || '请输入计划名称'
                        ]"
                    />
                    <q-select
                      label="处理人"
                      filled
                      v-model="addPlanModel.user"
                      :options="users"
                      dense
                      options-dense
                      :rules="[
                         () => !$v.addPlanModel.user.$error || '请输入处理人'
                        ]"
                    />
                    <q-editor
                      label="描述"
                      v-model="addPlanModel.description"
                      dense
                      :definitions="{
                          bold: {
                            label: 'Bold',
                            icon: null,
                            tip: 'My bold tooltip'
                          }
                        }"
                      class="q-mb-md"
                      :rules="[
                         () => !$v.addPlanModel.description.$error || '请输入描述'
                        ]"
                    />
                  </div>
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn @click="plan_step = 2" color="primary" label="Continue" />
                </q-stepper-navigation>
              </q-step>
              <q-step :name="2" title="选择计划时间" icon="add_comment" :done="plan_step > 2">
                <q-stepper-navigation>
                  <div class="row">
                    <div style="width:45%;">
                      <q-input
                        label="开始日期"
                        filled
                        v-model="addPlanModel.start_date"
                        type="text"
                        dense
                        mask="date"
                        :rules="[
                       () => !$v.addPlanModel.start_date.$error || '请输入开始日期'
                      ]"
                      >
                        <template v-slot:append>
                          <q-icon name="event" class="cursor-pointer">
                            <q-popup-proxy>
                              <q-date dense v-model="addPlanModel.start_date" />
                            </q-popup-proxy>
                          </q-icon>
                        </template>
                      </q-input>
                    </div>
                    <div style="width:10%;"></div>
                    <div style="width:45%;">
                      <q-input
                        label="结束日期"
                        filled
                        v-model="addPlanModel.end_date"
                        type="text"
                        dense
                        mask="date"
                        :rules="[
                       () => !$v.addPlanModel.end_date.$error || '请输入结束日期'
                      ]"
                      >
                        <template v-slot:append>
                          <q-icon name="event" class="cursor-pointer">
                            <q-popup-proxy>
                              <q-date v-model="addPlanModel.end_date" />
                            </q-popup-proxy>
                          </q-icon>
                        </template>
                      </q-input>
                    </div>
                  </div>
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn @click="plan_step = 3" color="primary" label="Continue" />
                  <q-btn flat @click="plan_step = 1" color="primary" label="Back" class="q-ml-sm" />
                </q-stepper-navigation>
              </q-step>
              <q-step :name="3" title="选择用例" icon="add_comment">
                <q-stepper-navigation>
                  <div class="col row flex-center text-grey-5" v-if="testCaseOptions.length==0">
                    <router-link :to="`caseProfile`" class="link">添加一条用例</router-link>
                    <q-icon size="28px" class="q-ml-sm" name="mdi-set mdi-hand-pointing-right" />
                  </div>
                  <div class="q-pa-md">
                    <q-input ref="filter" dense v-model="filter" class="table-head-input">
                      <template v-slot:append>
                        <q-icon name="search" color="primary" @click="resetFilter" />
                      </template>
                    </q-input>
                    <div class="q-pa-md row q-col-gutter-sm">
                      <q-tree
                        :nodes="simple"
                        node-key="id"
                        tick-strategy="leaf"
                        selected-color="primary"
                        :selected.sync="selected"
                        :ticked.sync="addPlanModel.case"
                        :expanded.sync="expanded"
                        :filter="filter"
                        default-expand-all
                      ></q-tree>
                      <!-- <div class="col-6 col-sm-6 q-gutter-sm">
                      <div class="text-h6">{{getInfo.name}}</div>
                      <q-separator spaced />
                      <div>{{getInfo.description}}</div>
                      </div>-->
                    </div>
                  </div>
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn
                    color="primary"
                    type="submit"
                    label="Finish"
                    :disable="this.$v.addPlanModel.$invalid"
                  />
                  <q-btn flat @click="plan_step = 2" color="primary" label="Back" class="q-ml-sm" />
                </q-stepper-navigation>
              </q-step>
            </q-stepper>
          </q-form>
        </q-card>
      </q-dialog>
    </Loading>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import Loading from "@/components/Loading";
import { formatSelectDisplay, successNotify } from "@/utils/utils";
import { createTestPlanModel, vars } from "../model";
import moment from "moment";
import AutoPlanList from "@/views/project/Test/AutoPlanList.vue";

export default {
  name: "PlanList",
  components: {
    Loading,
    AutoPlanList
  },
  data() {
    return {
      //Common
      globalLoading: true,
      tab: "_a",
      expanded: [],
      simple: [],

      ...vars,
      selected: "",

      //Plan
      medium: false,
      term: "",
      testPlan: createTestPlanModel(),
      plan_step: 1,
      addPlanModel: createTestPlanModel(),
      filter: "",
      runRightNow: true,
      time: "00:00",
      timeGroup: [],
      weekGroup: [],
      planTicked: [],
      formatSelectDisplay,
      showTree: false
    };
  },
  validations: {
    addPlanModel: {
      name: { required },
      user: { required },
      description: { required },
      start_date: { required },
      end_date: { required }
    }
  },
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("test", {
      groups: "testGroups",
      testPlanOptions: "plans",
      testCaseOptions: "cases"
    }),
    ...mapState("project", {
      members: "members"
    }),
    users() {
      return this.members.map(member => member.user);
    },
    projectId() {
      return this.$route.params.projectId;
    },
    //当前测试计划中的用例
    planCases() {
      return this.testCaseOptions.filter(cases =>
        this.testPlan.case.includes(cases.id)
      );
    },
    planUpdateGroupInfo() {
      let caseList = this.otherCases.map(testcase => {
        const a = {
          id: "testcase_" + testcase.id,
          name: testcase.name,
          parent: testcase.group,
          description: testcase.desc,
          type: "testcase"
        };
        return a;
      });
      let tree = this.groups.concat(caseList);
      return subTree(null, tree);
      // this.clickTree();
    },
    getInfo() {
      let info = {};
      for (let i = 0; i < this.testCaseOptions.length; i++) {
        if (this.testCaseOptions[i].id == this.selected) {
          info.name = this.testCaseOptions[i].name;
          info.description = this.testCaseOptions[i].desc;
          info.status = this.testCaseOptions[i].status;
          if (info.status == null) break;
          return info;
        }
      }
      for (let i = 0; i < this.groups.length; i++) {
        if (this.groups[i].id == this.selected) {
          info.name = this.groups[i].name;
          info.description = this.groups[i].description;
          return info;
        }
      }
      return info;
    },
    //不在当前测试计划中的用例
    otherCases() {
      this.planTicked = this.testPlan.case.map(tick => {
        return "testcase_" + tick;
      });
      return this.testCaseOptions;
      // return this.testCaseOptions.filter(
      //   cases => !this.testPlan.case.includes(cases.id)
      // );
    },
    testPlans() {
      const today = new Date();
      let testPlans = this.testPlanOptions.filter(
        testPlan =>
          testPlan.name.toLowerCase().indexOf(this.term.toLowerCase()) > -1
      );
      testPlans.forEach(each => {
        if (
          new Date(moment(each.start_date).format("YYYY/MM/DD")).getTime() >
          today
        ) {
          each.cls = "bg-grey-5";
          each.tip = "未开始";
        } else if (
          new Date(moment(each.end_date).format("YYYY/MM/DD")).getTime() < today
        ) {
          each.cls = "bg-red-5";
          each.tip = "已过期";
        } else {
          each.cls = "bg-green-5";
          each.tip = "进行中";
        }
      });
      return testPlans;
    }
  },
  methods: {
    ...mapActions("test", {
      addPlan: "addPlan",
      queryPlan: "fetchPlan",
      removePlan: "removePlan",
      updatePlan: "updatePlan",
      queryTestGroup: "fetchTestGroup",
      queryTestCase: "fetchTestCase",
      queryEnv: "fetchEnv",
      updateTestCase: "updateTestCase"
    }),
    ...mapActions("project", {
      queryMember: "fetchMember"
    }),
    resetFilter() {
      this.filter = "";
      this.$refs.filter.focus();
    },
    /* 将groups信息转换成标准的树形结构 */
    createGroupInfo() {
      let caseList = this.testCaseOptions.map(testcase => {
        const a = {
          id: "testcase_" + testcase.id,
          name: testcase.name,
          parent: testcase.group,
          description: testcase.desc,
          type: "testcase"
        };
        return a;
      });
      let tree = this.groups.concat(caseList);
      this.simple = subTree(null, tree);
      // this.clickTree();
    },

    getPlanCasesPassed(testPlan) {
      return this.testCaseOptions.filter(
        cases => testPlan.case.includes(cases.id) && cases.status > 1
      );
    },
    getProgress(testPlan) {
      let progress =
        (this.getPlanCasesPassed(testPlan).length / testPlan.case.length) * 100;
      return parseInt(progress);
    },
    handleSelectTestPlan(testplan) {
      this.testPlans.forEach(testplan => (testplan.active = false));
      testplan.active = true;
      this.testPlan = testplan;
    },
    async handleAddPlanCase() {
      this.globalLoading = true;
      this.testPlan.case = this.planTicked;
      await this.updatePlan({
        projectId: this.projectId,
        ...this.testPlan,
        case: this.testPlan.case.map(c => {
          return c.split("_")[1];
        })
      });
      successNotify("添加成功");
      this.handleSelectTestPlan(this.testPlan);
      this.globalLoading = false;
    },
    async handlePlanAdd() {
      this.$v.addPlanModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addPlanModel.$invalid) {
        return;
      }
      this.globalLoading = true;
      await this.addPlan({
        projectId: this.projectId,
        ...this.addPlanModel,
        case: this.addPlanModel.case.map(plan => {
          return plan.split("_")[1];
        })
      });
      successNotify("新增成功");
      this.medium = false;
      this.globalLoading = false;
    },
    async handUpdateTestCase(testCase) {
      await this.updateTestCase({
        projectId: this.projectId,
        ...testCase
      });
      successNotify("更新成功");
    }
  },

  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryMember(project);
    await this.queryPlan(project);
    if (this.testPlanOptions.length > 0) {
      this.handleSelectTestPlan(this.testPlanOptions[0]);
      this.showTree = true;
    }
    await this.queryTestGroup(project);
    await this.queryTestCase(project);
    this.createGroupInfo();

    this.globalLoading = false;
  }
};
function subTree(parent, gs) {
  let sub = [];
  for (let index in gs) {
    let re = {};
    if (parent == gs[index].parent) {
      re.id = String(gs[index].id);
      re.label = gs[index].name;
      re.description = gs[index].description;
      if ("testcase" == gs[index].type) {
        re.icon = "format_size";
      } else {
        re.icon = "style";
      }
      re.children = subTree(gs[index].id, gs);
      sub.push(re);
    }
  }
  return sub;
}
</script>

<style lang="stylus" scoped>
.label {
  color: $grey-7;
  text-align: right;
}

.value {
  text-align: right;
  font-size: 20px;
  color: $grey-9;
}
</style>

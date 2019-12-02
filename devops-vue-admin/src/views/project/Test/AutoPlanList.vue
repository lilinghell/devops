<template>
  <div class="bg-white q-pa-md flex-center">
    <Loading :visible="globalLoading">
      <q-splitter :value="25" disable class="full-height">
        <template v-slot:before>
          <div class="column full-height">
            <q-input v-model="autoTerm" dense outlined class="q-ma-md" placeholder="计划查询">
              <template v-slot:after>
                <q-btn
                  class="btn-add"
                  color="primary"
                  icon="mdi-set mdi-shape-circle-plus"
                  unelevated
                  @click="AddAutoPlanFlag = true"
                />
              </template>
            </q-input>
            <q-list class="col scroll" separator>
              <template v-for="autoplan in autoTestPlans">
                <q-item
                  :key="autoplan.id"
                  clickable
                  v-ripple
                  :active="autoplan.active"
                  active-class="bg-teal-1"
                  @click="handleSelectAutoPlan(autoplan)"
                >
                  <q-item-section>
                    <q-item-label>
                      <span>{{ autoplan.name }}</span>
                    </q-item-label>
                    <q-item-label caption>
                      {{
                      formatSelectDisplay(users, autoplan.user)
                      }}
                    </q-item-label>
                    <div class="text-subtitle2 text-grey-7">
                      每
                      <a
                        v-for="day in autoplan.week.split(',')"
                        :key="day"
                      >{{formatSelectDisplay(weekdays, day)}}</a>
                      {{ autoplan.time }}
                    </div>
                    <q-item-label caption class="row items-center">
                      <q-linear-progress
                        stripe
                        rounded
                        style="height: 6px;"
                        :value="getProgress(autoplan)/100"
                        class="col-6 q-mr-sm"
                        color="secondary"
                      />
                      {{ getProgress(autoplan) }}%
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
                  <span>{{ AutoPlan.name }}-{{formatSelectDisplay(envs,AutoPlan.env)}}</span>
                </div>
                <div
                  class="text-subtitle2 text-grey-7"
                >{{ formatSelectDisplay(users, AutoPlan.user) }}</div>
                <div class="text-subtitle2 text-grey-7">
                  每
                  <a
                    v-for="day in AutoPlan.week.split(',')"
                    :key="day"
                  >{{formatSelectDisplay(weekdays, day)}}</a>
                  {{ AutoPlan.time }}
                </div>
                <div class="text-subtitle2 text-grey-7">{{ AutoPlan.description }}</div>
                <div class="col row flex-center text-grey-5" v-if="!AutoPlan.case">
                  <span class="text-h6">添加一条用例</span>
                  <q-icon size="28px" class="q-ml-sm" name="mdi-set mdi-hand-pointing-right" />
                </div>

                <q-list class="col scroll" separator v-else>
                  <q-item v-for="testCase in autoPlanCases" :key="testCase.id" class="q-py-md">
                    <q-item-section class="col-2">
                      <q-item-label class="text-grey-8">
                        {{
                        formatSelectDisplay(caseStatus, testCase.status)
                        }}
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
                    <q-item-section class="col-2 text-right">
                      <div class="text-grey-8 q-gutter-xs">
                        <template v-if="testCase.status === 1">
                          <q-btn
                            size="12px"
                            flat
                            dense
                            round
                            icon="delete"
                            @click="handleRemoveIterationFeature(testCase)"
                            :loading="loading['case/update']"
                          />
                          <q-btn
                            size="12px"
                            flat
                            dense
                            round
                            icon="done"
                            @click="handleFinishFeature(testCase)"
                            :loading="loading['case/update']"
                          />
                        </template>
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-circular-progress
                  show-value
                  font-size="12px"
                  :value="getProgress(AutoPlan)"
                  size="50px"
                  :thickness="0.22"
                  color="secondary"
                  track-color="grey-3"
                  class="absolute-top-right text-grey-7 q-ma-md"
                >{{ getProgress(AutoPlan) }}%</q-circular-progress>
              </div>
            </template>
            <template v-slot:after>
              <div class="q-ma-md q-gutter-sm" v-if="showTree">
                <q-tree
                  :nodes="autoPlanUpdateGroupInfo"
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
                  <q-btn color="primary" @click="handleAddAutoPlanCase()" label="修改"></q-btn>
                </q-toolbar>
              </div>
            </template>
          </q-splitter>
        </template>
      </q-splitter>
      <q-dialog v-if="AddAutoPlanFlag" v-model="AddAutoPlanFlag">
        <q-card style="width: 500px;">
          <q-form @submit="handleAutoPlanAdd" ref="autoForm">
            <q-stepper v-model="autoPlan_step" color="primary" animated>
              <q-step :name="1" title="输入基本信息" icon="settings" :done="autoPlan_step > 1">
                <q-stepper-navigation>
                  <q-input
                    label="计划名称"
                    v-model="addAutoPlanModel.name"
                    type="text"
                    autofocus
                    dense
                    :rules="[
                   () => !$v.addAutoPlanModel.name.$error || '请输入计划名称'
                  ]"
                  />
                  <q-select
                    label="处理人"
                    filled
                    v-model="addAutoPlanModel.user"
                    :options="users"
                    dense
                    options-dense
                    :rules="[
                   () => !$v.addAutoPlanModel.user.$error || '请输入处理人'
                  ]"
                  />
                  <q-select
                    label="测试环境"
                    filled
                    v-model="addAutoPlanModel.env"
                    :options="envs"
                    dense
                    options-dense
                    :rules="[
                   () => !$v.addAutoPlanModel.env.$error || '请输入环境'
                  ]"
                  />
                  <q-editor
                    label="描述"
                    v-model="addAutoPlanModel.description"
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
                   () => !$v.addAutoPlanModel.description.$error || '请输入描述'
                  ]"
                  />
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn
                    @click="autoPlan_step = 2"
                    color="primary"
                    label="Continue"
                    :disable="this.$v.addAutoPlanModel.$invalid"
                  />
                </q-stepper-navigation>
              </q-step>
              <q-step :name="2" title="选择计划时间" icon="add_comment" :done="autoPlan_step > 2">
                <q-stepper-navigation>
                  <div class="q-px-sm">
                    <strong>计划时刻：</strong>
                  </div>
                  <div class="q-pa-md">
                    <div class="q-gutter-sm">
                      <q-chip
                        removable
                        v-for="timeItem in timeGroup"
                        :key="timeItem"
                        :val="timeItem"
                        :label="timeItem"
                        color="teal"
                        text-color="white"
                        @remove="removeTimeItem(timeItem)"
                      />
                      <q-btn
                        dense
                        size="md"
                        rounded
                        color="teal"
                        icon-right="add"
                        class="cursor-pointer"
                      >
                        <q-popup-proxy transition-show="scale" transition-hide="scale">
                          <div class="column">
                            <q-time v-model="time" />
                            <q-btn dense size="md" color="teal" label="确定" @click="addAutoTime" />
                          </div>
                        </q-popup-proxy>
                      </q-btn>
                    </div>
                  </div>
                  <div class="q-px-sm">
                    <strong>计划星期：</strong>
                  </div>
                  <div class="q-pa-md">
                    <div class="q-gutter-sm">
                      <q-checkbox
                        v-for="week in weekdays"
                        v-bind:key="week.value"
                        v-model="weekGroup"
                        :val="week.value"
                        :label="week.label"
                        color="teal"
                      />
                    </div>
                  </div>
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn
                    @click="autoPlan_step = 3"
                    color="primary"
                    label="Continue"
                    :disable="weekGroup.length==0"
                  />
                  <q-btn
                    flat
                    @click="autoPlan_step = 1"
                    color="primary"
                    label="Back"
                    class="q-ml-sm"
                  />
                </q-stepper-navigation>
              </q-step>
              <q-step :name="3" title="选择用例" icon="add_comment">
                <q-stepper-navigation>
                  <div class="q-pa-md">
                    <q-input ref="filter" dense v-model="filter" class="table-head-input">
                      <template v-slot:append>
                        <q-icon name="search" color="primary" @click="resetFilter" />
                      </template>
                    </q-input>
                    <div class="col row flex-center text-grey-5" v-if="testCaseOptions.length==0">
                      <router-link :to="`caseProfile`" class="link">添加一条用例</router-link>
                      <q-icon size="28px" class="q-ml-sm" name="mdi-set mdi-hand-pointing-right" />
                    </div>
                    <div class="q-pa-md row q-col-gutter-sm">
                      <q-tree
                        :nodes="simple"
                        node-key="id"
                        tick-strategy="leaf"
                        selected-color="primary"
                        :selected.sync="selected"
                        :ticked.sync="addAutoPlanModel.case"
                        :expanded.sync="expanded"
                        :filter="filter"
                        default-expand-all
                      ></q-tree>
                      <!-- <div class="col-6 col-sm-6 q-gutter-sm">
                        <div class="text-h6">{{getInfo.name ? getInfo.name : '用例信息'}}</div>
                        <q-separator spaced />
                        <div>{{getInfo.description ? getInfo.description : '用例描述'}}</div>
                        <div>{{addAutoPlanModel.case}}</div>
                      </div>-->
                    </div>
                  </div>
                </q-stepper-navigation>
                <q-stepper-navigation>
                  <q-btn color="primary" type="submit" label="Finish" />
                  <q-btn
                    flat
                    @click="autoPlan_step = 2"
                    color="primary"
                    label="Back"
                    class="q-ml-sm"
                  />
                  <q-toggle label="立即执行一次" v-model="runRightNow" color="green" />
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
import { createAutoPlanModel, vars } from "../model";
import moment from "moment";

export default {
  name: "AutoPlanList",
  components: {
    Loading
  },
  data() {
    return {
      //Common
      globalLoading: true,
      expanded: [],
      simple: [],

      ...vars,
      selected: "",

      //AutoPlan
      autoTerm: "",
      filter: "",
      AddAutoPlanFlag: false,
      AutoPlan: createAutoPlanModel(),
      addAutoPlanModel: createAutoPlanModel(),
      autoPlan_step: 1,
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
    addAutoPlanModel: {
      name: { required },
      user: { required },
      description: { required },
      env: { required }
    }
  },
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("test", {
      groups: "testGroups",
      testCaseOptions: "cases",
      envs: "envs",
      autoPlanOptions: "autoPlans"
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
    //当前自动计划中的用例
    autoPlanCases() {
      return this.testCaseOptions.filter(cases =>
        this.AutoPlan.case.includes(cases.id)
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
    autoPlanUpdateGroupInfo() {
      let caseList = this.otherAutoCases.map(testcase => {
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
    //不在当前自动测试计划中的用例
    otherAutoCases() {
      this.planTicked = this.AutoPlan.case.map(tick => {
        return "testcase_" + tick;
      });
      return this.testCaseOptions;
      // return this.testCaseOptions.filter(
      //   cases => !this.AutoPlan.case.includes(cases.id)
      // );
    },
    autoTestPlans() {
      let autoTestPlans = this.autoPlanOptions.filter(
        autoTestPlan =>
          autoTestPlan.name.toLowerCase().indexOf(this.autoTerm.toLowerCase()) >
          -1
      );
      return autoTestPlans;
    }
  },
  methods: {
    ...mapActions("test", {
      addAutoPlan: "addAutoPlan",
      queryAutoPlan: "fetchAutoPlan",
      removeAutoPlan: "removeAutoPlan",
      updateAutoPlan: "updateAutoPlan",
      queryTestGroup: "fetchTestGroup",
      queryTestCase: "fetchTestCase",
      queryEnv: "fetchEnv"
    }),
    ...mapActions("project", {
      queryMember: "fetchMember"
    }),
    resetFilter() {
      this.filter = "";
      this.$refs.filter.focus();
    },
    //添加自动计划时刻
    addAutoTime() {
      this.timeGroup.push(this.time);
      this.timeGroup = Array.from(new Set(this.timeGroup)); //去重
      this.timeGroup.sort(); //排序
    },
    //删除自动计划时刻
    removeTimeItem(timeItem) {
      this.timeGroup.splice(this.timeGroup.indexOf(timeItem), 1);
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
    handleSelectAutoPlan(autoplan) {
      this.autoPlanOptions.forEach(autoplan => (autoplan.active = false));
      autoplan.active = true;
      this.AutoPlan = autoplan;
    },
    async handleAddAutoPlanCase() {
      this.globalLoading = true;
      this.AutoPlan.case = this.planTicked;
      await this.updateAutoPlan({
        projectId: this.projectId,
        ...this.AutoPlan,
        case: this.AutoPlan.case.map(c => {
          return c.split("_")[1];
        })
      });
      successNotify("添加成功");
      this.handleSelectAutoPlan(this.AutoPlan);
      this.globalLoading = false;
    },
    async handleAutoPlanAdd() {
      for (let i = 0; i < this.timeGroup.length; i++) {
        this.addAutoPlanModel.time += this.timeGroup[i];
        if (i !== this.timeGroup.length - 1) this.addAutoPlanModel.time += ",";
      }
      for (let i = 0; i < this.weekGroup.length; i++) {
        this.addAutoPlanModel.week += this.weekGroup[i];
        if (i !== this.weekGroup.length - 1) this.addAutoPlanModel.week += ",";
      }
      this.$v.addAutoPlanModel.$touch();
      this.$refs.autoForm.validate();
      if (this.$v.addAutoPlanModel.$invalid) {
        return;
      }
      await this.addAutoPlan({
        projectId: this.projectId,
        ...this.addAutoPlanModel,
        case: this.addAutoPlanModel.case.map(plan => {
          return plan.split("_")[1];
        })
      });
      successNotify("新增成功");
      this.AddAutoPlanFlag = false;
    }
  },

  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryEnv(project);
    await this.queryAutoPlan(project);
    if (this.autoPlanOptions.length > 0) {
      this.handleSelectAutoPlan(this.autoPlanOptions[0]);
      this.showTree = true;
    }
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

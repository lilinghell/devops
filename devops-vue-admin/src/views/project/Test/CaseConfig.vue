<template>
  <div class="bg-white q-pa-md flex-center">
    <Loading :visible="globalLoading">
      <q-splitter v-model="splitterModel" style="height: 100%;min-height:500px;
      ">
        <template v-slot:before>
          <div class="q-pa-md" @click="clickTree()">
            <q-input ref="filter" dense v-model="filter" class="table-head-input">
              <template v-slot:append>
                <q-icon name="search" color="primary" @click="resetFilter" />
              </template>
              <template v-slot:after>
                <q-btn
                  class="btn-add"
                  color="primary"
                  icon="mdi-set mdi-shape-circle-plus"
                  unelevated
                  @click="handleAddRootGroupOpen"
                />
              </template>
            </q-input>

            <q-tree
              :nodes="simple"
              node-key="id"
              selected-color="primary"
              :selected.sync="selected"
              :filter="filter"
              default-expand-all
            ></q-tree>
          </div>
        </template>

        <template v-slot:after>
          <q-tab-panels
            v-model="selected"
            animated
            transition-prev="jump-up"
            transition-next="jump-up"
          >
            <q-tab-panel :name="`${group.id}`">
              <div class="text-h6">
                <div>
                  <q-form ref="form" @submit="handUpdateGroup">
                    <q-toolbar class="text-primary">
                      <q-space />
                      <q-btn-dropdown stretch flat label="Dropdown">
                        <q-list>
                          <q-item-label header>接口导出</q-item-label>
                          <q-item clickable v-close-popup>
                            <q-item-section avatar>
                              <q-avatar icon="assignment" color="primary" text-color="white" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Word</q-item-label>
                              <q-item-label caption>February 22, 2016</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                              <q-icon name="info" />
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </q-btn-dropdown>
                      <q-btn
                        flat
                        size="12px"
                        color="red"
                        v-show="editable"
                        @click="handleRemoveGroupOpened()"
                        round
                        icon="delete"
                      ></q-btn>
                      <q-separator dark vertical />
                      <q-btn
                        flat
                        size="12px"
                        round
                        icon="edit"
                        @click="editable = true"
                        v-show="!editable"
                      />

                      <template v-if="editable">
                        <q-btn
                          type="submit"
                          flat
                          size="12px"
                          round
                          icon="done"
                          :loading="loading['']"
                        />
                        <q-btn flat size="12px" round icon="clear" @click="handleReset()" />
                      </template>
                    </q-toolbar>
                    <q-card-section class="q-gutter-y-sm">
                      <q-input
                        class="text-h4 q-mb-md"
                        filled
                        square
                        v-model="group.name"
                        type="text"
                        bg-color="white"
                        dense
                        :rules="[
                                () => !$v.group.name.$error || '请输入'
                              ]"
                        hide-bottom-space
                        :disable="!editable"
                      />
                      <q-input
                        filled
                        square
                        v-model="group.description"
                        type="textarea"
                        bg-color="white"
                        dense
                        hide-bottom-space
                        :disable="!editable"
                      />
                      <p>
                        <span>
                          总共用例数量
                          <span class="text-primary text-h5">({{groupCaseNums}})</span>个,
                        </span>
                        现在你可以
                        <a
                          class="link text-primary"
                          @click="handleAddGroupOpen"
                        >添加组</a>
                        <span>&nbsp;或&nbsp;</span>
                        <a class="link text-primary text-h5" @click="handleAddTestCaseOpen">添加用例</a>
                      </p>
                    </q-card-section>
                  </q-form>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel :name="`testcaseId_${testcase.id}`">
              <template>
                <q-tabs
                  align="left"
                  v-model="tab"
                  class="text-grey-7"
                  active-color="primary"
                  indicator-color="primary"
                >
                  <q-tab name="_a" label="预览" />
                  <q-tab name="_b" label="运行" />
                </q-tabs>
              </template>
              <Loading>
                <q-tab-panels v-model="tab">
                  <q-tab-panel name="_a">
                    <div>
                      <q-form ref="caseForm" @submit="handUpdateTestCase">
                        <q-toolbar class="text-primary">
                          <q-space />
                          <q-btn-dropdown stretch flat label="Dropdown">
                            <q-list>
                              <q-item-label header>导出</q-item-label>
                              <q-item clickable v-close-popup>
                                <q-item-section avatar>
                                  <q-avatar icon="assignment" color="primary" text-color="white" />
                                </q-item-section>
                                <q-item-section>
                                  <q-item-label>Word</q-item-label>
                                  <q-item-label caption>February 22, 2016</q-item-label>
                                </q-item-section>
                                <q-item-section side>
                                  <q-icon name="info" />
                                </q-item-section>
                              </q-item>
                            </q-list>
                          </q-btn-dropdown>
                          <q-separator dark vertical />
                          <q-btn
                            flat
                            size="12px"
                            round
                            icon="edit"
                            @click="editable = true"
                            v-show="!editable"
                          />

                          <template v-if="editable">
                            <q-btn
                              type="submit"
                              flat
                              size="12px"
                              round
                              icon="done"
                              :loading="loading['']"
                            />
                            <q-btn flat size="12px" round icon="clear" @click="handleReset()" />
                          </template>
                        </q-toolbar>
                        <q-card-section class="q-gutter-y-sm">
                          <div class="row">
                            <!--<q-badge style="height: 20px;">{{ testcase.version }}</q-badge>-->
                            <q-input
                              class="text-h4 q-mb-md"
                              filled
                              square
                              v-model="testcase.name"
                              type="text"
                              bg-color="white"
                              dense
                              :rules="[
                                () => !$v.testcase.name.$error || '请输入'
                              ]"
                              hide-bottom-space
                              :disable="!editable"
                            />
                          </div>
                          <q-input
                            label="用例描述"
                            style="height: 60px;"
                            filled
                            square
                            v-model="testcase.desc"
                            type="textarea"
                            dense
                            hide-bottom-space
                            :disable="!editable"
                          />
                          <div class="row">
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">维护用户:</span>
                              </template>
                              <q-select
                                filled
                                :display-value="formatSelectDisplay(users, testcase.user)"
                                v-model="testcase.user"
                                :options="users"
                                dense
                                hint
                                emit-value
                                bg-color="white"
                                hide-dropdown-icon
                                :disable="!editable"
                                hide-bottom-space
                              />
                            </Field>
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">用例状态:</span>
                              </template>
                              <q-select
                                filled
                                :display-value="formatSelectDisplay(caseStatus, testcase.status)"
                                v-model="testcase.status"
                                :options="caseStatus"
                                dense
                                hint
                                emit-value
                                bg-color="white"
                                hide-dropdown-icon
                                :disable="!editable"
                                hide-bottom-space
                              />
                            </Field>
                          </div>

                          <div class="row">
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">用例类型:</span>
                              </template>
                              <q-select
                                filled
                                :display-value="formatSelectDisplay(caseTypes, testcase.type)"
                                v-model="testcase.type"
                                :options="caseTypes"
                                dense
                                hint
                                emit-value
                                bg-color="white"
                                hide-dropdown-icon
                                :disable="!editable"
                                hide-bottom-space
                              />
                            </Field>
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">用例等级:</span>
                              </template>
                              <q-select
                                filled
                                :display-value="formatSelectDisplay(caseLevels, testcase.level)"
                                v-model="testcase.level"
                                :options="caseLevels"
                                dense
                                hint
                                emit-value
                                bg-color="white"
                                hide-dropdown-icon
                                :disable="!editable"
                                hide-bottom-space
                              />
                            </Field>
                          </div>

                          <div class="row">
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">归属需求:</span>
                              </template>
                              <q-select
                                filled
                                v-model="testcase.feature"
                                :options="featuresMap"
                                multiple
                                emit-value
                                map-options
                                dense
                                hint
                                bg-color="white"
                                hide-dropdown-icon
                                :disable="!editable"
                                hide-bottom-space
                              >
                                <template v-slot:option="scope">
                                  <q-item v-bind="scope.itemProps" v-on="scope.itemEvents">
                                    <q-item-section>
                                      <q-item-label v-html="scope.opt.label"></q-item-label>
                                    </q-item-section>
                                  </q-item>
                                </template>
                              </q-select>
                            </Field>
                          </div>
                          <div class="row">
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">前置条件:</span>
                              </template>
                              <q-input
                                bg-color="white"
                                style="height: 60px;width: 80%;"
                                filled
                                square
                                v-model="testcase.prerequisites"
                                type="textarea"
                                dense
                                hide-bottom-space
                                :disable="!editable"
                              />
                            </Field>
                            <Field :label-col="3" align="right" style="width:50%;">
                              <template v-slot:label>
                                <span class="field">预期结果:</span>
                              </template>
                              <q-input
                                bg-color="white"
                                style="height: 60px;width: 80%;"
                                filled
                                square
                                v-model="testcase.expected"
                                type="textarea"
                                dense
                                hide-bottom-space
                                :disable="!editable"
                              />
                            </Field>
                          </div>
                        </q-card-section>
                      </q-form>
                    </div>
                  </q-tab-panel>
                  <q-tab-panel name="_b">
                    <div class="row" name="top_url">
                      <div class="col-1">
                        <q-select
                          outlined
                          dense
                          v-model="method"
                          :options="methodTypes"
                          label="Method"
                          style="background-color: aliceblue"
                        />
                      </div>
                      <div class="col-3">
                        <q-select
                          outlined
                          dense
                          v-model="test.env"
                          :options="envsMap"
                          label="Environment"
                          style="background-color: aliceblue"
                        />
                      </div>
                      <div class="col">
                        <q-select
                          outlined
                          dense
                          v-model="test.interface"
                          use-input
                          input-debounce="0"
                          label="Interface"
                          :options="URLOptions"
                          @filter="filterFn"
                          behavior="menu"
                          style="background-color: aliceblue"
                        >
                          <template v-slot:no-option>
                            <q-item>
                              <q-item-section class="text-grey">No results</q-item-section>
                            </q-item>
                          </template>
                        </q-select>
                      </div>
                      <div class="row">
                        <q-btn-dropdown
                          split
                          style="margin-left: 10px"
                          color="teal"
                          label="Send"
                          @click="send(test.interface)"
                        >
                          <!--@click="onMainClick"-->
                          <q-list>
                            <q-item clickable v-close-popup @click="sendAndSave()">
                              <q-item-section avatar>
                                <q-item-label>Send and Download</q-item-label>
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </q-btn-dropdown>
                        <q-btn split style="margin-left: 10px" label="Save">
                          <!--@click="onMainClick"-->
                          <!--<q-list>-->
                          <!--<q-item clickable v-close-popup @click="saveJson">-->
                          <!--<q-item-section avatar>-->
                          <!--<q-item-label>Save as...</q-item-label>-->
                          <!--</q-item-section>-->
                          <!--</q-item>-->
                          <!--</q-list>-->
                        </q-btn>
                      </div>
                    </div>
                    <div style="padding-top: 10px">
                      <q-tabs v-model="tab_form" dense unelevated class="bg- text-black shadow-2">
                        <q-tab name="_Header" label="Header" />
                        <q-tab name="_Authorization" label="Authorization" />
                        <q-tab name="_Params" label="Params" />
                      </q-tabs>
                    </div>
                    <q-tab-panels v-model="tab_form">
                      <q-tab-panel name="_Header" style="padding: 0px">
                        <q-card class="my-card" bordered>
                          <q-markup-table dense>
                            <thead>
                              <tr>
                                <th class="text-left" width="30%">Key</th>
                                <th class="text-left">Value</th>
                                <th class="text-left" width="10px"></th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="headerIndex in headerGroup.length" :key="headerIndex">
                                <td class="text-left">
                                  <q-input
                                    filled
                                    type="text"
                                    v-model="headerGroup[headerIndex-1].key"
                                    dense
                                    hide-bottom-space
                                    bg-color="white"
                                  ></q-input>
                                </td>
                                <td class="text-left">
                                  <q-input
                                    filled
                                    v-model="headerGroup[headerIndex-1].value"
                                    type="text"
                                    dense
                                    hide-bottom-space
                                    bg-color="white"
                                  ></q-input>
                                </td>
                                <td class="text-left">
                                  <q-btn
                                    dense
                                    flat
                                    text-color="primary"
                                    @click="headerGroup.splice(headerIndex-1,1)"
                                    icon-right="delete"
                                    class="cursor-pointer"
                                  />
                                </td>
                              </tr>
                            </tbody>
                          </q-markup-table>
                          <q-btn
                            style="width: 100%"
                            @click="headerGroup.push({deItemFlag:true})"
                            icon="add"
                          ></q-btn>
                        </q-card>
                      </q-tab-panel>
                    </q-tab-panels>
                    <q-card flat bordered class="my-card">
                      <q-card-section>
                        <div class="text-h6">Response Body</div>
                      </q-card-section>
                      <q-card-section>
                        <pre style="background-color: black;color:white">{{body}}</pre>
                      </q-card-section>
                    </q-card>
                  </q-tab-panel>
                </q-tab-panels>
              </Loading>
            </q-tab-panel>
          </q-tab-panels>
        </template>
      </q-splitter>

      <q-dialog v-if="addGroupOpened" v-model="addGroupOpened">
        <q-card style="width: 500px;">
          <q-stepper v-model="step" vertical color="primary" animated>
            <q-step :name="1" :title="(group.name?group.name:'根')+'-添加组'" icon="add_comment">
              <q-stepper-navigation>
                <q-form @submit="handleAddGroup" ref="groupForm">
                  <Field :label-col="2" label="组名称">
                    <q-input
                      filled
                      v-model="addGroupModel.name"
                      type="text"
                      autofocus
                      dense
                      :rules="[() => !$v.addGroupModel.name.$error || '请输入组名称']"
                    />
                  </Field>
                  <Field :label-col="2" label="描述">
                    <q-input filled v-model="addGroupModel.description" type="textarea" dense />
                  </Field>
                  <q-btn color="primary" type="submit" label="提交" />
                  <q-btn
                    flat
                    @click="addGroupOpened = false"
                    color="primary"
                    label="Close"
                    class="q-ml-sm"
                  />
                </q-form>
              </q-stepper-navigation>
            </q-step>
          </q-stepper>
        </q-card>
      </q-dialog>
      <q-dialog seamless v-model="addTestCaseOpened" position="right" maximized>
        <q-layout view="lHh lpr lFf" container class="modal-content-col-5">
          <q-form @submit="handleAddTestCase" ref="testcaseForm">
            <q-header bordered class="bg-primary text-white">
              <q-toolbar>
                <q-btn flat v-close-popup round dense icon="arrow_back" />
                <q-toolbar-title>{{group.name}} - 添加用例-基本信息</q-toolbar-title>
              </q-toolbar>
            </q-header>

            <q-page-container>
              <q-page padding>
                <Field contracted>
                  <template v-slot:label>
                    <span class="field">用例名称：</span>
                  </template>
                  <q-input
                    filled
                    v-model="addTestCaseModel.name"
                    type="text"
                    autofocus
                    dense
                    :rules="[() => !$v.addTestCaseModel.name.$error || '请输入用例名称']"
                  />
                </Field>
                <div class="row">
                  <div class="col-4">
                    <Field contracted>
                      <template v-slot:label>
                        <span class="field">维护负责：</span>
                      </template>
                      <q-select
                        filled
                        v-model="addTestCaseModel.user"
                        :options="users"
                        dense
                        options-dense
                        :rules="[() => !$v.addTestCaseModel.user.$error || '请选择维护用户']"
                      />
                    </Field>
                  </div>
                  <div class="col-8">
                    <Field contracted>
                      <template v-slot:label>
                        <span class="field">归属需求：</span>
                      </template>
                      <q-select
                        filled
                        use-chips
                        multiple
                        dense
                        hint
                        hide-bottom-space
                        v-model="addTestCaseModel.feature"
                        :options="features"
                        :rules="[
                        () => !$v.addTestCaseModel.feature.$error || '请选择关联需求'
                      ]"
                      />
                    </Field>
                  </div>
                </div>
                <div class="row">
                  <div class="col-4">
                    <Field contracted>
                      <template v-slot:label>
                        <span class="field">用例类型：</span>
                      </template>
                      <q-select
                        filled
                        v-model="addTestCaseModel.type"
                        :display-value="formatSelectDisplay(caseTypes, addTestCaseModel.type)"
                        :options="caseTypes"
                        emit-value
                        dense
                        hint
                        hide-bottom-space
                        :rules="[() => !$v.addTestCaseModel.type.$error || '请选择用例类型']"
                      />
                    </Field>
                  </div>
                  <div class="col-4">
                    <Field contracted>
                      <template v-slot:label>
                        <span class="field">用例等级：</span>
                      </template>
                      <q-select
                        filled
                        v-model="addTestCaseModel.level"
                        :options="caseLevels"
                        align="right"
                        emit-value
                        dense
                        hint
                        hide-bottom-space
                        :rules="[() => !$v.addTestCaseModel.level.$error || '请选择用例等级']"
                      />
                    </Field>
                  </div>
                  <div class="col-4">
                    <Field contracted>
                      <template v-slot:label>
                        <span class="field">用例状态：</span>
                      </template>
                      <q-select
                        filled
                        v-model="addTestCaseModel.status"
                        :display-value="formatSelectDisplay(caseStatus, addTestCaseModel.status)"
                        :options="caseStatus"
                        align="right"
                        emit-value
                        dense
                        hint
                        hide-bottom-space
                        :rules="[() => !$v.addTestCaseModel.status.$error || '请选择用例等级']"
                      />
                    </Field>
                  </div>
                </div>

                <Field contracted>
                  <template v-slot:label>
                    <span class="field">前置条件：</span>
                  </template>
                  <q-input
                    filled
                    v-model="addTestCaseModel.prerequisites"
                    type="textarea"
                    dense
                    :rules="[() => !$v.addTestCaseModel.prerequisites.$error || '请输入前置条件']"
                  />
                </Field>
                <Field contracted>
                  <template v-slot:label>
                    <span class="field">用例描述：</span>
                  </template>
                  <q-input
                    filled
                    v-model="addTestCaseModel.desc"
                    type="textarea"
                    dense
                    :rules="[() => !$v.addTestCaseModel.desc.$error || '请输入用例描述']"
                  />
                </Field>
                <Field contracted>
                  <template v-slot:label>
                    <span class="field">预期结果：</span>
                  </template>
                  <q-input
                    filled
                    v-model="addTestCaseModel.expected"
                    type="textarea"
                    dense
                    :rules="[() => !$v.addTestCaseModel.expected.$error || '请输入预期结果']"
                  />
                </Field>
              </q-page>
            </q-page-container>

            <q-footer class="bg-white text-primary shadow-3">
              <q-toolbar>
                <q-space />
                <q-btn color="primary" unelevated type="submit" label="提交" :loading="loading['']" />
              </q-toolbar>
            </q-footer>
          </q-form>
        </q-layout>
      </q-dialog>
      <q-dialog v-model="removeGroupOpened">
        <q-card class="modal-content-xs">
          <q-card-section>
            <div class="text-h6">删除组</div>
          </q-card-section>
          <q-card-section>
            <div class="text-grey-7">确认删除组{{ this.group.name }}</div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn color="red" unelevated label="确认" @click="handleRemoveGroup" />
            <q-btn flat label="取消" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </Loading>
  </div>
</template>


<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import {
  createTestGroupModel,
  createTestCaseModel,
  createTestModel,
  vars
} from "../model";
import Loading from "@/components/Loading";
import Field from "@/components/Field";
import { formatSelectDisplay, successNotify } from "@/utils/utils";
import request from "@/utils/request";
import axios from "axios";
import FileSaver from "file-saver";

export default {
  name: "Group",
  components: {
    Loading,
    Field
  },
  data() {
    return {
      addGroupModel: createTestGroupModel(),
      globalLoading: true,
      removeGroupOpened: false,
      tab: "_a",
      step: 1,
      splitterModel: 25,
      filter: "",
      selected: "",
      group: createTestGroupModel(),
      simple: [],
      editable: false,
      addGroupOpened: false,
      showGroup: true,
      testcase: createTestCaseModel(),
      addTestCaseModel: createTestCaseModel(),
      ...vars,
      addTestCaseOpened: false,
      addGroupFlag: true,
      groupCaseNums: 0,

      body: {},
      tab_form: "_Header",
      headerGroup: [],
      method: "",
      test: createTestModel(),
      URLOptions: []
    };
  },
  validations: {
    group: {
      name: { required }
    },
    addGroupModel: {
      name: { required }
    },
    testcase: {
      name: { required },
      user: { required },
      status: { required },
      type: { required },
      level: { required },
      feature: { required },
      prerequisites: { required },
      desc: { required },
      expected: { required }
    },
    addTestCaseModel: {
      name: { required },
      user: { required },
      status: { required },
      type: { required },
      level: { required },
      feature: { required },
      prerequisites: { required },
      desc: { required },
      expected: { required }
    }
  },
  watch: {},
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("test", {
      groups: "testGroups",
      groupInfo: "group",
      testCases: "cases",
      testcaseInfo: "testcase",
      testInfo: "test",
      envs: "envs"
    }),
    ...mapState("designs", {
      interfaces: "interfaceList"
    }),
    ...mapState("project", {
      members: "members"
    }),
    ...mapState("feature", {
      features: "list"
    }),
    users() {
      return this.members.map(member => member.user);
    },
    featuresMap() {
      return this.features.map(features => features);
    },
    envsMap() {
      return this.envs.map(envs => envs.name + "  " + envs.domain);
    },
    interfaceMap() {
      return this.interfaces.map(interfaces => interfaces.url);
    },
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions("test", {
      queryTestGroup: "fetchTestGroup",
      updateTestGroup: "updateTestGroup",
      addTestGroup: "addTestGroup",
      removeTestGroup: "removeTestGroup",
      queryTestCase: "fetchTestCase",
      updateTestCase: "updateTestCase",
      addTestCase: "addTestCase",
      queryTest: "fetchTest",
      addTest: "addTest",
      updateTest: "updateTest",
      queryEnv: "fetchEnv"
      // updateGroupModel: "updateGroup"
    }),
    ...mapActions("designs", {
      queryInterface: "fetchInterface"
    }),
    ...mapActions("project", {
      queryMember: "fetchMember"
    }),
    ...mapActions("feature", {
      queryFeature: "fetch"
    }),

    filterFn(val, update, abort) {
      update(() => {
        const needle = val.toLowerCase();
        this.URLOptions = this.interfaceMap.filter(
          v => v.toLowerCase().indexOf(needle) > -1
        );
      });
    },
    send() {
      this.body = {};
      let domain = this.test.env ? this.test.env.split(" ").pop() : {};
      let intFa = this.test.interface;
      console.log(this.method);
      if (this.method.value === "GET") {
        axios.get(domain + "/api/v1" + intFa).then(response => {
          this.body = response.data;
        });
      }
    },
    sendAndSave() {
      this.send().then(val => {
        const data = JSON.stringify(this.body);
        const blob = new Blob([data], { type: "" });
        FileSaver.saveAs(blob, this.test.interface + ".json");
      });
    },
    resetFilter() {
      this.filter = "";
      this.$refs.filter.focus();
    },
    handleReset() {
      this.editable = false;
    },
    /* 将groups信息转换成标准的树形结构 */
    createGroupInfo() {
      let caseList = this.testCases.map(testcase => {
        const a = {
          id: "testcaseId_" + testcase.id,
          name: testcase.name,
          parent: testcase.group,
          description: testcase.desc,
          type: "testcase"
        };
        return a;
      });
      let tree = this.groups.concat(caseList);
      this.simple = subTree(null, tree);
      if ("" === this.group.id && this.simple.length > 0) {
        this.selected = this.simple[0].id;
      }

      this.clickTree();
    },
    clickTree() {
      this.group = [];
      this.testcase = [];
      this.qryGroup();
      this.editable = false;
    },
    /* 获取当前选中的group详细信息 */
    qryGroup() {
      if (Number(this.selected)) {
        //组
        for (let i = 0; i < this.groups.length; i++) {
          if (this.selected == this.groups[i].id) {
            this.group = this.groups[i];
            //查询有多少个接口
            let num = 0;
            for (let i = 0; i < this.testCases.length; i++) {
              if (this.selected == this.testCases[i].group.id) {
                num = num + 1;
              }
            }
            if (num > 0) {
              this.addGroupFlag = false;
            } else {
              this.addGroupFlag = true;
            }
            this.groupCaseNums = num;
            break;
          }
        }
      } else {
        //接口
        for (let i = 0; i < this.testCases.length; i++) {
          if (this.selected == "testcaseId_" + this.testCases[i].id) {
            this.testcase = this.testCases[i];
            let pro_case = {
              projectId: this.projectId,
              caseId: this.testcase.id
            };
            this.queryTest(pro_case);
            this.test = this.testInfo;
            break;
          }
        }
      }
    },
    async handUpdateGroup() {
      this.$v.group.$touch();
      this.$refs.form.validate();
      if (this.$v.group.$invalid) {
        return;
      }
      await this.updateTestGroup({
        projectId: this.projectId,
        ...this.group
      });
      this.createGroupInfo();
      this.editable = false;
      successNotify("更新成功");
    },
    async handUpdateTestCase() {
      this.$v.testcase.$touch();
      this.$refs.caseForm.validate();
      if (this.$v.testcase.$invalid) {
        return;
      }
      await this.updateTestCase({
        projectId: this.projectId,
        ...this.testcase
      });
      this.createGroupInfo();
      this.editable = false;
      successNotify("更新成功");
    },
    handleRemoveGroupOpened() {
      this.removeGroupOpened = true;
      // this.removeModel = module;
    },
    async handleRemoveGroup() {
      await this.removeTestGroup({
        projectId: this.projectId,
        ...this.group
      });
      this.removeGroupOpened = false;
      this.createGroupInfo();
      successNotify("删除成功");
    },
    //添加根组
    handleAddRootGroupOpen() {
      this.addGroupModel = createTestGroupModel();
      this.$v.addGroupModel.$reset();
      this.selected = "";
      this.addGroupOpened = true;
    },
    handleAddGroupOpen() {
      this.addGroupModel = createTestGroupModel();
      this.$v.addGroupModel.$reset();
      this.addGroupOpened = true;
    },
    handleAddTestCaseOpen() {
      this.addTestCaseModel = createTestCaseModel();
      this.$v.addTestCaseModel.$reset();
      this.addTestCaseOpened = true;
    },
    async handleAddGroup() {
      this.$v.addGroupModel.$touch();
      this.$refs.groupForm.validate();
      if (this.$v.addGroupModel.$invalid) {
        return;
      }
      await this.addTestGroup({
        projectId: this.projectId,
        ...this.addGroupModel,
        parent: this.group
      });
      this.selected = String(this.groupInfo.id);
      this.createGroupInfo();
      this.addGroupOpened = false;
      successNotify("添加成功");
    },
    async handleAddTestCase() {
      this.$v.addTestCaseModel.$touch();
      this.$refs.testcaseForm.validate();
      if (this.$v.addTestCaseModel.$invalid) {
        return;
      }
      await this.addTestCase({
        projectId: this.projectId,
        ...this.addTestCaseModel,
        group: this.group
      });
      this.selected = "testcaseId_" + this.testcaseInfo.id;
      this.createGroupInfo();
      this.addTestCaseOpened = false;
      successNotify("添加成功");
      // await this.addTest({
      //   projectId: this.projectId,
      //   caseId: this.testcase.id,
      //   body: this.body
      // });
      // successNotify("测试模块添加成功");
    }
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    //查询组信息
    await this.queryTestGroup(project);
    await this.queryTestCase(project);
    await this.queryFeature(project);
    await this.queryEnv(project);
    await this.queryInterface(project);
    //组装tree
    await this.queryMember(project);
    this.createGroupInfo();
    this.globalLoading = false;
  },
  mounted() {}
};
function subTree(parent, gs) {
  let sub = [];
  for (let index in gs) {
    let re = {};
    if (parent == gs[index].parent) {
      re.id = String(gs[index].id);
      re.label = gs[index].name;
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

.q-tab-panel {
  padding: 16px 16px;
}

.in_layout {
  width: 500px;
}
</style>

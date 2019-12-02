<template>
  <div class="bg-white q-pa-md flex-center">
    <Loading :visible="globalLoading">
    <q-splitter v-model="splitterModel" style="height: 100%; min-height: 500px;">
      <template v-slot:before>
        <div class="q-pa-md" @click="clickTree()">
          <q-input ref="filter" dense v-model="filter" class="table-head-input">
            <template v-slot:append>
              <q-icon name="search" color="primary" @click="resetFilter" />
            </template>
          </q-input>

          <q-tree
            :nodes="simple"
            node-key="id"
            selected-color="primary"
            :selected.sync="selected"
            :filter="filter"
            default-expand-all
          />
        </div>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="selected"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel v-if="groupFlag" :name="`${group.id}`">
            <div class="text-h6">
              <div>
                <q-form ref="form" @submit="handUpdateGroup">
                  <q-toolbar class="text-primary">
                    <q-space />
                    <q-btn-dropdown stretch flat label="Dropdown">
                      <q-list>
                        <q-item-label header>骨架生成</q-item-label>
                        <q-item clickable v-close-popup>
                          <q-item-section avatar>
                            <q-avatar icon="folder" color="secondary" text-color="white" />
                          </q-item-section>
                          <q-item-section>
                            <q-item-label>生成Mock</q-item-label>
                            <q-item-label caption>February 22, 2016</q-item-label>
                          </q-item-section>
                          <q-item-section side>
                            <q-icon name="info" />
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup>
                          <q-item-section avatar>
                            <q-avatar icon="folder" color="secondary" text-color="white" />
                          </q-item-section>
                          <q-item-section>
                            <q-item-label>生成代码</q-item-label>
                            <q-item-label caption>February 22, 2016</q-item-label>
                          </q-item-section>
                          <q-item-section side>
                            <q-icon name="info" />
                          </q-item-section>
                        </q-item>
                        <q-separator inset spaced />
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
                        总共接口数量
                        <span class="text-primary text-h5">({{groupInterNums}})</span>个,
                      </span>
                      现在你可以
                      <a
                        class="link text-primary"
                        @click="handleAddGroupOpen"
                      >添加组</a>
                      <span>&nbsp;或&nbsp;</span>
                      <a class="link text-primary text-h5" @click="handleAddInterfaceOpen">添加接口</a>
                    </p>
                  </q-card-section>
                </q-form>
              </div>
            </div>
          </q-tab-panel>
          <q-tab-panel v-if="interFlag" :name="`interId_${inter.id}`">
            <template>
              <q-tabs
                align="left"
                v-model="tab"
                class="text-grey-7"
                active-color="primary"
                indicator-color="primary"
              >
                <q-tab name="_a" label="预览" />
                <q-tab name="_b" label="编辑" />
                <q-tab name="_c" label="运行" />
              </q-tabs>
            </template>

            <q-tab-panels v-model="tab">
              <q-tab-panel name="_a">
                <div>
                  <q-form ref="interForm" @submit="handUpdateInterface('ui')">
                    <q-toolbar class="text-primary">
                      <q-space />
                      <q-btn-dropdown stretch flat label="Dropdown">
                        <q-list>
                          <q-item-label header>骨架生成</q-item-label>
                          <q-item clickable v-close-popup>
                            <q-item-section avatar>
                              <q-avatar icon="folder" color="secondary" text-color="white" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>生成Mock</q-item-label>
                              <q-item-label caption>February 22, 2016</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                              <q-icon name="info" />
                            </q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup>
                            <q-item-section avatar>
                              <q-avatar icon="folder" color="secondary" text-color="white" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>生成代码</q-item-label>
                              <q-item-label caption>February 22, 2016</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                              <q-icon name="info" />
                            </q-item-section>
                          </q-item>
                          <q-separator inset spaced />
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
                        <q-badge style="height: 20px;">{{ inter.version }}</q-badge>
                        <q-input
                          class="text-h4 q-mb-md"
                          filled
                          square
                          v-model="inter.name"
                          type="text"
                          bg-color="white"
                          dense
                          :rules="[
                                () => !$v.inter.name.$error || '请输入'
                              ]"
                          hide-bottom-space
                          :disable="!editable"
                        />
                      </div>
                      <q-input
                        style="height: 60px;"
                        filled
                        square
                        v-model="inter.description"
                        type="textarea"
                        dense
                        hide-bottom-space
                        :disable="!editable"
                      />
                      <div class="row">
                        <Field :label-col="3" align="right" style="width:10%;">
                          <template v-slot:label>
                            <span class="field"></span>
                          </template>
                          <q-select
                            filled
                            :display-value="formatSelectDisplay(methodTypes, inter.method)"
                            v-model="inter.method"
                            :options="methodTypes"
                            emit-value
                            dense
                            hint
                            bg-color="white"
                            hide-dropdown-icon
                            :disable="!editable"
                            hide-bottom-space
                          />
                        </Field>
                        <Field :label-col="1" align="right" style="width:90%;">
                          <template v-slot:label>
                            <span class="field"></span>
                          </template>
                          <q-input
                            filled
                            square
                            v-model="inter.url"
                            type="text"
                            bg-color="white"
                            dense
                            :rules="[
                                () => !$v.inter.url.$error || '请输入'
                              ]"
                            hide-bottom-space
                            :disable="!editable"
                          />
                        </Field>
                      </div>
                      <div class="row">
                        <Field :label-col="3" align="right" style="width:50%;">
                          <template v-slot:label>
                            <span class="field">状态:</span>
                          </template>
                          <q-select
                            filled
                            :display-value="formatSelectDisplay(interfaceStatus, inter.status)"
                            v-model="inter.status"
                            :options="interfaceStatus"
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
                            <span class="field">开放接口:</span>
                          </template>
                          <q-toggle :disable="!editable" v-model="inter.open" label />
                        </Field>
                      </div>
                      <div class="row">
                        <Field :label-col="3" align="right" style="width:50%;">
                          <template v-slot:label>
                            <span class="field">负责人:</span>
                          </template>
                          <span class="field" style="padding-left:10px;">liling</span>
                        </Field>
                        <Field :label-col="3" align="right" style="width:50%;">
                          <template v-slot:label>
                            <span class="field">更新时间:</span>
                          </template>
                          <span class="field" style="padding-left:10px;">{{inter.updated_at}}</span>
                        </Field>
                      </div>
                      <Field :label-col="3" align="right" style="width:50%;">
                        <template v-slot:label>
                          <span class="field">Mock地址:</span>
                        </template>
                        <span class="field" style="padding-left:10px;">
                          <label>http://localhost:8080</label>
                          {{inter.url}}
                        </span>
                      </Field>
                      <Field :label-col="3" align="right" style="width:50%;">
                        <template v-slot:label>
                          <span class="field">编辑:</span>
                        </template>
                        <span class="field" style="padding-left:10px;">
                          <a class="link text-primary" @click="toggleInterfaceEditModal">code模式</a>
                          &nbsp;
                          <a
                            class="link text-primary"
                            @click="tab = '_b'"
                          >ui模式</a>
                        </span>
                      </Field>
                    </q-card-section>
                  </q-form>
                </div>

                <div>
                  <InterProfile ref="interProfile" :inter="inter"></InterProfile>
                </div>
              </q-tab-panel>

              <q-tab-panel name="_b">
                <InterUIEdit ref="interUIEdit" :inter="inter"></InterUIEdit>
              </q-tab-panel>
              <q-tab-panel name="_c">
                <InterfaceTest :inter="inter"></InterfaceTest>
              </q-tab-panel>
            </q-tab-panels>
          </q-tab-panel>
        </q-tab-panels>
      </template>
    </q-splitter>
    
    <q-dialog seamless v-if="addGroupOpened" v-model="addGroupOpened" position="right" maximized>
      <q-layout view="lHh lpr lFf" container class="modal-content-col-4">
        <q-form @submit="handleAddGroup" ref="groupForm">
          <q-header bordered class="bg-primary text-white">
            <q-toolbar>
              <q-btn flat v-close-popup round dense icon="arrow_back" />
              <q-toolbar-title>{{group.name}} - 添加组</q-toolbar-title>
            </q-toolbar>
          </q-header>

          <q-page-container>
            <q-page padding>
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
    <q-dialog v-if="addInterfaceOpened" v-model="addInterfaceOpened">
      <q-card style="width: auto;max-width: 80vw;">
        <q-stepper v-model="step" vertical color="primary" animated>
          <q-step :name="1" title="导入yaml文件" icon="settings" :done="step > 1">
            从scum信息中导入已有的yaml文件,否者Continue创建新的接口.
            <q-stepper-navigation>
              <div v-if="group.scm_url === ''">
                未找到应用的scm信息
                <router-link
                  :to="`/project/${group.project}/app/${group.application.id}`"
                  class="link"
                >&nbsp;添加</router-link>
              </div>
              <div v-else>
                <span>yaml地址:</span>
                <q-input
                  filled
                  square
                  v-model="addInterfaceModel.yaml_path"
                  type="text"
                  dense
                  hide-bottom-space
                  placeholder="分支名/src/test.yaml"
                />
                {{group.scm_url + "blob/" + addInterfaceModel.yaml_path}}
              </div>
            </q-stepper-navigation>
            <q-stepper-navigation>
              <q-btn @click="importYaml" color="primary" label="Continue" />
            </q-stepper-navigation>
          </q-step>
          <q-step :name="2" title="创建接口" icon="add_comment">
            添加接口的基本信息.
            <q-stepper-navigation>
              <q-form @submit="handleAddInterface" ref="interfaceForm">
                <Field contracted>
                  <template v-slot:label>
                    <span class="field">接口名称：</span>
                  </template>
                  <q-input
                    filled
                    v-model="addInterfaceModel.name"
                    type="text"
                    autofocus
                    dense
                    :rules="[() => !$v.addInterfaceModel.name.$error || '请输入接口名称']"
                  />
                </Field>
                <div class="row" style="width: 490px;">
                  <Field contracted class="col-4">
                    <template v-slot:label>
                      <span class="field">接口路径：</span>
                    </template>
                    <q-select
                      filled
                      v-model="addInterfaceModel.method"
                      :options="methodTypes"
                      emit-value
                      dense
                      hint
                      hide-bottom-space
                      :rules="[() => !$v.addInterfaceModel.method.$error || '请输入method']"
                    />
                  </Field>
                  <Field contracted class="col-8">
                    <template v-slot:label>
                      <span class="field"></span>
                    </template>
                    <q-input
                      placeholder="/"
                      align="right"
                      filled
                      v-model="addInterfaceModel.url"
                      type="text"
                      dense
                      :rules="[() => !$v.addInterfaceModel.url.$error || '请输入接口路径']"
                    />
                  </Field>
                </div>
                <Field contracted>
                  <template v-slot:label>
                    <span class="field">接口描述：</span>
                  </template>
                  <q-input filled v-model="addInterfaceModel.description" type="textarea" dense />
                </Field>
              </q-form>
            </q-stepper-navigation>
            <q-stepper-navigation>
              <q-btn color="primary" @click="handleAddInterface" label="Finish" />
              <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm" />
            </q-stepper-navigation>
          </q-step>
        </q-stepper>
      </q-card>
    </q-dialog>
    <InterfaceEdit v-model="interfaceEditModalOpened" :inter="inter"></InterfaceEdit>
    </Loading>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import PageHeaderWrapper from "@/components/PageHeaderWrapper";
import Loading from "@/components/Loading";
import Field from "@/components/Field";
import DescriptionList from "@/components/DescriptionList";
import Description from "@/components/DescriptionList/Description";
import Page from "@/components/Page";
import {
  formatSelectDisplay,
  successNotify,
  errorNotify,
  resolveResponseError
} from "@/utils/utils";
import { vars as globalVars } from "@/views/model";
import {
  createDesignGroupModel,
  createDesignInterfaceModel,
  vars
} from "../model";
import { isNumber } from "util";
import InterfaceEdit from "@/views/project/Designs/InterEdit.vue";
import InterfaceTest from "@/views/project/Designs/InterTest.vue";
import InterProfile from "@/views/project/Designs/InterProfile.vue";
import InterUIEdit from "@/views/project/Designs/InterUIEdit.vue";
import SwaggerEditorBundle from "swagger-editor-dist/swagger-editor-bundle";
import SwaggerEditorStandalonePreset from "swagger-editor-dist/swagger-editor-standalone-preset";
import { importYaml } from "@/services/api";
import YAML from "js-yaml";

export default {
  name: "Group",
  components: {
    PageHeaderWrapper,
    Loading,
    Field,
    DescriptionList,
    Description,
    Page,
    InterfaceEdit,
    InterfaceTest,
    InterProfile,
    InterUIEdit
  },
  data() {
    return {
      globalLoading: true,
      tab: "_a",
      splitterModel: 25,
      filter: "",
      selected: "",
      group: createDesignGroupModel(),
      simple: [],
      editable: false,
      addGroupOpened: false,
      addGroupModel: createDesignGroupModel(),
      showGroup: true,
      inter: createDesignInterfaceModel(),
      addInterfaceModel: createDesignInterfaceModel(),
      ...vars,
      addInterfaceOpened: false,
      addGroupFlag: true,
      groupInterNums: 0,
      interfaceEditModalOpened: false,
      opened: false,
      interFlag: false,
      groupFlag: false,
      editor: "",
      step: 1
    };
  },
  validations: {
    group: {
      name: { required },
      application: { required }
    },
    addGroupModel: {
      name: { required }
    },
    inter: {
      name: { required },
      url: { required },
      method: { required },
      version: { required },
      status: { required },
      application: { required },
      group: { required }
    },
    addInterfaceModel: {
      name: { required },
      url: { required },
      method: { required }
    }
  },
  watch: {},
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("designs", {
      groups: "groupList",
      groupInfo: "group",
      interfaces: "interfaceList",
      interfaceInfo: "interface"
    }),

    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions("designs", {
      queryGroup: "fetchGroup",
      updateGroup: "updateGroup",
      addGroup: "addGroup",
      queryInterface: "fetchInterface",
      updateInterface: "updateInterface",
      addInterface: "addInterface"
    }),
    resetFilter() {
      this.filter = "";
      this.$refs.filter.focus();
    },
    handleReset() {
      this.editable = false;
    },
    /* 将groups信息转换成标准的树形结构 */
    createGroupInfo() {
      let interList = this.interfaces.map(inter => {
        const a = {
          id: "interId_" + inter.id,
          name: inter.name,
          parent: inter.group.id,
          application: inter.application,
          description: inter.description,
          type: "interface"
        };
        return a;
      });
      let tree = this.groups.concat(interList);
      this.simple = subTree(null, tree);
      if ("" === this.group.id) {
        this.selected = this.simple[0].id;
      }

      this.clickTree();
    },
    clickTree() {
      this.group = [];
      this.inter = {};
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
            this.group.scm_url = this.groups[
              i
            ].application.repo.scm_url.replace(".git", "/");
            //查询有多少个接口
            let num = 0;
            for (let i = 0; i < this.interfaces.length; i++) {
              if (this.selected == this.interfaces[i].group.id) {
                num = num + 1;
              }
            }
            if (num > 0) {
              this.addGroupFlag = false;
            } else {
              this.addGroupFlag = true;
            }
            this.groupInterNums = num;

            this.interFlag = false;
            this.groupFlag = true;

            break;
          }
        }
      } else {
        //接口
        for (let i = 0; i < this.interfaces.length; i++) {
          if (this.selected == "interId_" + this.interfaces[i].id) {
            this.inter = this.interfaces[i];
            this.inter.savePath = this.interfaces[
              i
            ].application.repo.scm_url.replace(".git", "/");
            this.interFlag = true;
            this.groupFlag = false;
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
      await this.updateGroup({
        projectId: this.projectId,
        ...this.group
      });
      this.createGroupInfo();
      this.editable = false;
      successNotify("更新成功");
    },
    async handUpdateInterface(model) {
      if ("ui" === model && "" !== this.inter.info) {
        try {
          let jsContent = YAML.safeLoad(this.inter.info);
          let path = Object.keys(jsContent.paths);
          let method = Object.keys(jsContent.paths[path[0]])[0];

          jsContent.paths[path[0]][method].description = this.inter.description;
          jsContent.paths[path[0]][method].operationId = this.inter.name;
          jsContent.info.version = this.inter.version;

          jsContent.paths[this.inter.url] = jsContent.paths[path[0]];
          if (Object.keys(jsContent.paths).length > 1) {
            delete jsContent.paths[path[0]]; //删除原来的
          }

          let newMethod = this.inter.method.toLowerCase();
          jsContent.paths[this.inter.url][newMethod] =
            jsContent.paths[this.inter.url][method];
          if (Object.keys(jsContent.paths[this.inter.url]).length > 1) {
            delete jsContent.paths[this.inter.url][method]; //删除原来的
          }
          this.inter.info = YAML.safeDump(jsContent);
        } catch (error) {
          errorNotify("错误");
          console.error(error);
          return;
        }
      } else if("code" === model) {
        //code模式
        try {
          let str = this.editor.specSelectors.specStr();
          this.inter.info = str;
          if ("" !== str) {
            let jsContent = YAML.safeLoad(str);
            let path = Object.keys(jsContent.paths);
            this.inter.url = path[0];

            let method = Object.keys(jsContent.paths[path[0]])[0];
            this.inter.method = method.toUpperCase();

            this.inter.description =
              jsContent.paths[path[0]][method].description;

            this.inter.name = jsContent.paths[path[0]][method].operationId;

            this.inter.version = jsContent.info.version;
          }
        } catch (error) {
          errorNotify("错误");
          console.log(error);
          return;
        }
      }
      this.$v.inter.$touch();
      this.$refs.interForm.validate();
      if (this.$v.inter.$invalid) {
        return;
      }
      await this.updateInterface({
        projectId: this.projectId,
        ...this.inter
      });
      this.createGroupInfo();
      this.editable = false;

      this.$refs.interProfile.properties();
      successNotify("更新成功");
    },
    handleAddGroupOpen() {
      this.addGroupModel = createDesignGroupModel();
      this.$v.addGroupModel.$reset();
      this.addGroupOpened = true;
    },
    handleAddInterfaceOpen() {
      this.addInterfaceModel = createDesignInterfaceModel();
      this.$v.addInterfaceModel.$reset();
      this.addInterfaceOpened = true;
      // this.addInterfaceModel.yaml_path = "master/src/interface/test.yaml";//test
      this.step = 1;
    },
    async handleAddGroup() {
      this.$v.addGroupModel.$touch();
      this.$refs.groupForm.validate();
      if (this.$v.addGroupModel.$invalid) {
        return;
      }
      await this.addGroup({
        ...this.addGroupModel,
        projectId: this.projectId,
        application: this.group.application,
        parent: this.group
      });
      this.selected = String(this.groupInfo.id);
      this.createGroupInfo();
      this.addGroupOpened = false;
      successNotify("添加成功");
    },
    async handleAddInterface() {
      this.$v.addInterfaceModel.$touch();
      this.$refs.interfaceForm.validate();
      if (this.$v.addInterfaceModel.$invalid) {
        return;
      }
      await this.addInterface({
        ...this.addInterfaceModel,
        projectId: this.projectId,
        application: this.group.application,
        group: this.group,
        version: "0.1",
        status: "1"
      });
      this.selected = "interId_" + this.interfaceInfo.id;
      this.createGroupInfo();
      this.addInterfaceOpened = false;
      successNotify("添加成功");
    },
    async toggleInterfaceEditModal() {
      await this.chag();
      this.swaggerHtml();
    },
    chag() {
      this.interfaceEditModalOpened = !this.interfaceEditModalOpened;
    },
    swaggerHtml() {
      this.editor = SwaggerEditorBundle({
        dom_id: "#swagger-editor",
        layout: "EditorLayout",
        presets: [SwaggerEditorStandalonePreset]
      });
      window.editor = this.editor;
      this.editor.specActions.updateSpec(this.inter.info);
      var v = document.getElementsByClassName("opblock-summary");
      v[0].click();
    },
    async importYaml() {
      if (
        null === this.addInterfaceModel.yaml_path ||
        undefined === this.addInterfaceModel.yaml_path ||
        "" === this.addInterfaceModel.yaml_path
      ) {
        this.addInterfaceModel = createDesignInterfaceModel();
        this.step = 2;
      } else {
        const response = await resolveResponseError(() =>
          importYaml({
            application_id: this.group.application.id,
            yaml_path: this.addInterfaceModel.yaml_path
          })
        );
        try {
          let jsContent = YAML.safeLoad(response);
          let path = Object.keys(jsContent.paths);
          this.addInterfaceModel.url = path[0];
          this.addInterfaceModel.name = path[0];
          let method = Object.keys(jsContent.paths[path[0]])[0];

          this.addInterfaceModel.method = method.toUpperCase();
          this.addInterfaceModel.description =
            jsContent.paths[path[0]][method].description;
          this.addInterfaceModel.info = response;
          this.step = 2;
        } catch (e) {
          errorNotify("错误");
          console.error(e);
          return;
        }
      }
    }
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    //查询组信息
    await this.queryGroup(project);
    await this.queryInterface(project);
    //组装tree
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
      if ("interface" == gs[index].type) {
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

<style lang="stylus" scoped></style>

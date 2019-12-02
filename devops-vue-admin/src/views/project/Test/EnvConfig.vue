<template>
    <div>
    <template>
      <Loading :visible="globalLoading">
        <Page>
          <q-splitter  v-model="splitterModel">
            <template v-slot:before>
              <div class="column full-height">
                <q-input
                  dense
                  outlined
                  class="q-ma-md"
                  placeholder="环境查询"
                >
                  <!--v-model="term"-->
                  <template v-slot:after>
                    <q-btn
                      class="btn-add"
                      color="primary"
                      icon="mdi-set mdi-shape-circle-plus"
                      unelevated
                      @click="handleAddModalOpen"
                    />
                  </template>
                </q-input>
                <q-list class="col scroll" separator>
                  <template v-for="env in envs">
                    <q-item
                      :key="env.id"
                      clickable
                      v-ripple
                      :active="env.active"
                      active-class="bg-teal-1"
                      @click="handleSelectEnv(env)"
                    >
                      <q-item-section>
                        <q-item-label>
                          <span>{{ env.name }}</span>
                        </q-item-label>
                        <q-item-label caption>
                          {{ env.domain }}
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
              <q-form ref="EnvForm" @submit="handleUpdateEnv">
                <q-card no-bordered flat class="my-card text-primary">
                  <q-card-section>
                    <div>
                      <q-toolbar class="text-primary">
                        <q-space />
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
                          <q-btn flat size="12px" color="red" v-show="editable" @click="handleRemoveModalOpened()" round icon="delete"></q-btn>
                          <q-btn type="submit" flat size="12px" round icon="done" :loading="loading['test/updateEnv']" />
                          <q-btn flat size="12px" round icon="clear" @click="handleResetEnv()" />
                        </template>
                      </q-toolbar>
                      <q-card-section class="q-gutter-y-sm">
                          <q-input
                            bg-color="white"
                            class="text-h4 q-mb-md"
                            filled
                            square
                            v-model="resetModel.name"
                            type="text"
                            dense
                            :rules="[
                              () => !$v.resetModel.name.$error || '请输入'
                            ]"
                            hide-bottom-space
                            :disable="!editable"
                          />
                        <q-input
                          label="域名地址"
                          filled
                          square
                          v-model="resetModel.domain"
                          :rules="[
                              () => !$v.resetModel.domain.$error || '请输入'
                            ]"
                          type="text"
                          dense
                          hide-bottom-space
                          :disable="!editable"
                          bg-color="white"
                        />
                        <div class="row">
                          <div class="column  col-6" style="padding:10px;">
                            <q-card class="my-card" flat bordered>
                              <q-card-section>
                                <div class="text-h6">Header</div>
                              </q-card-section>
                              <q-markup-table>
                                <thead>
                                  <tr>
                                    <th class="text-left" width="30%">Key</th>
                                    <th class="text-left">Value</th>
                                    <th class="text-left" width="10px" v-if="editable"></th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="headerIndex in resetHeaderGroup.length" :key="headerIndex" >
                                    <td class="text-left">
                                      <q-input
                                        filled
                                        type="text"
                                        v-model="resetHeaderGroup[headerIndex-1].key"
                                        dense
                                        hide-bottom-space
                                        :disable="!editable"
                                        bg-color="white"
                                      >
                                      </q-input>
                                    </td>
                                    <td class="text-left">
                                      <q-input
                                        filled
                                        v-model="resetHeaderGroup[headerIndex-1].value"
                                        type="text"
                                        dense
                                        hide-bottom-space
                                        :disable="!editable"
                                        bg-color="white"
                                      >
                                      </q-input>
                                    </td>
                                    <td class="text-left" v-if="editable">
                                      <q-btn dense
                                             flat
                                             text-color="primary"
                                             @click="resetHeaderGroup.splice(headerIndex-1,1)"
                                             icon-right="delete"
                                             class="cursor-pointer"
                                      />
                                    </td>
                                  </tr>
                                </tbody>
                              </q-markup-table>
                              <q-btn style="width: 100%" @click="resetHeaderGroup.push({deItemFlag:true})" icon="add" v-if="editable"></q-btn>
                            </q-card>
                          </div>
                          <div class="column  col-6" style="padding:10px;">
                            <q-card class="my-card" flat bordered>
                              <q-card-section>
                                <div class="text-h6">Cookie</div>
                              </q-card-section>
                              <q-markup-table>
                                <thead>
                                <tr>
                                  <th class="text-left" width="30%">Key</th>
                                  <th class="text-left">Value</th>
                                  <th class="text-left" width="10px" v-if="editable"></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr  v-for="cookieIndex in resetCookieGroup.length" :key="cookieIndex">
                                  <td class="text-left">
                                    <q-input
                                      filled
                                      v-model="resetCookieGroup[cookieIndex-1].key"
                                      type="text"
                                      dense
                                      hide-bottom-space
                                      :disable="!editable"
                                      bg-color="white"
                                    >
                                    </q-input>
                                  </td>
                                  <td class="text-left">
                                    <q-input
                                      filled
                                      v-model="resetCookieGroup[cookieIndex-1].value"
                                      type="text"
                                      dense
                                      hide-bottom-space
                                      :disable="!editable"
                                      bg-color="white"
                                    >
                                    </q-input>
                                  </td>
                                  <td class="text-left" v-if="editable">
                                    <q-btn dense
                                           flat
                                           text-color="primary"
                                           @click="resetCookieGroup.splice(cookieIndex-1,1)"
                                           icon-right="delete"
                                           class="cursor-pointer"
                                    />
                                  </td>
                                </tr>
                                </tbody>
                              </q-markup-table>
                              <q-btn style="width: 100%" @click="resetCookieGroup.push({deItemFlag:true})" icon="add" v-if="editable"></q-btn>
                            </q-card>
                          </div>
                        </div>
                      </q-card-section>
                    </div>
                  </q-card-section>
                </q-card>
              </q-form>
            </template>
          </q-splitter>
        </Page>
      </Loading>
    </template>

      <q-dialog v-if="addModalOpened" v-model="addModalOpened">
        <q-card style="width: auto;max-width: 80vw;">
          <q-stepper v-model="step" vertical color="primary" animated>
            <q-step :name="1" title="创建环境" icon="add_comment">
              添加接口的基本信息.
              <q-stepper-navigation>
                <q-form @submit="handleAdd" ref="form">
                  <Field contracted>
                    <template v-slot:label>
                      <span class="field">环境名称：</span>
                    </template>
                    <q-input
                      filled
                      v-model="$v.addModel.name.$model"
                      type="text"
                      autofocus
                      dense
                      :rules="[() => !$v.addModel.name.$error || '请输入环境名称']"
                    />
                  </Field>
                  <div class="row" style="width: 490px;">
                    <Field contracted class="col-5">
                      <template v-slot:label>
                        <span class="field">环境域名：</span>
                      </template>
                      <q-select
                        style="width: 100%"
                        filled
                        v-model="URLHeaderModel"
                        dense
                        use-input
                        hide-selected
                        fill-input
                        input-debounce="0"
                        :options="URLOptions"
                        @filter="filterFn"
                        :rules="[]"
                      />
                    </Field>
                    <Field contracted class="col-7">
                      <template v-slot:label>
                        <span class="field"></span>
                      </template>
                      <q-input
                        style="width: 100%"
                        filled
                        v-model="URLFooterModel"
                        type="text"
                        dense
                        :rules="[() => !$v.addModel.domain.$error || '请输入环境域名']"
                      />
                    </Field>
                  </div>
                  <div v-for="headerIndex in HeaderGroup.length" :key="headerIndex+'-label1'" class="row" style="width: 490px;">
                    <Field contracted class="col-5">
                      <template v-slot:label>
                        <span class="field">&nbsp;Header{{headerIndex}}：</span>
                      </template>
                      <q-input
                        filled
                        v-model="HeaderGroup[headerIndex-1].key"
                        type="text"
                        dense
                        label="header名"
                        hide-bottom-space
                      >
                      </q-input>
                    </Field>
                    <Field contracted class="col-6">
                      <template v-slot:label>
                        <span class="field"></span>
                      </template>
                      <q-input
                        filled
                        v-model="HeaderGroup[headerIndex-1].value"
                        type="text"
                        dense
                        label="header值"
                        :rules="[]"
                      >
                      </q-input>
                    </Field>
                    <Field contracted class="col-1">
                      <template v-slot:label>
                        <span class="field"></span>
                      </template>
                      <q-btn dense size="md"
                             rounded color="teal"
                             @click="addOrDeleteGroupItem(HeaderGroup,headerIndex)"
                             v-bind:icon-right="HeaderGroup[headerIndex-1].deItemFlag?'delete':'add'"
                             class="cursor-pointer"
                      />
                    </Field>
                  </div>
                  <div v-for="cookieIndex in CookieGroup.length" :key="cookieIndex+'-label'"  class="row" style="width: 490px;">
                    <Field contracted class="col-5">
                      <template v-slot:label>
                        <span class="field">&nbsp;Cookie{{cookieIndex}}：</span>
                      </template>
                      <q-input
                        filled
                        v-model="CookieGroup[cookieIndex-1].key"
                        type="text"
                        dense
                        label="cookie名"
                        :rules="[]"
                      >
                      </q-input>
                    </Field>
                    <Field contracted class="col-6">
                      <template v-slot:label>
                        <span class="field"></span>
                      </template>
                      <q-input
                        filled
                        v-model="CookieGroup[cookieIndex-1].value"
                        type="text"
                        dense
                        label="cookie值"
                        :rules="[]"
                      >
                      </q-input>
                    </Field>
                    <Field contracted class="col-1">
                      <template v-slot:label>
                        <span class="field"></span>
                      </template>
                      <!--<q-btn dense size="md"-->
                             <!--rounded color="teal"-->
                             <!--@click="addOrDeleteCookieItem(cookieIndex)"-->
                             <!--v-bind:icon-right="CookieGroup[cookieIndex-1].deleteCookieItemFlag?'delete':'add'"-->
                             <!--class="cursor-pointer"-->
                      <!--/>-->
                      <q-btn dense size="md"
                             rounded color="teal"
                             @click="addOrDeleteGroupItem(CookieGroup,cookieIndex)"
                             v-bind:icon-right="CookieGroup[cookieIndex-1].deItemFlag?'delete':'add'"
                             class="cursor-pointer"
                      />
                    </Field>
                  </div>
                  <q-btn color="primary"
                         type="submit"
                         label="提交"
                         :loading="loading['test/addEnv']" />
                  <q-btn flat @click="addModalOpened = false" color="primary" label="Close" class="q-ml-sm" />
                </q-form>
              </q-stepper-navigation>
            </q-step>
          </q-stepper>
        </q-card>
      </q-dialog>

    <q-dialog v-model="removeModalOpened">
      <q-card class="modal-content-xs">
        <q-card-section>
          <div class="text-h6">删除环境</div>
        </q-card-section>
        <q-card-section>
          <div class="text-grey-7">确认删除环境{{ this.env.name }}</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            color="red"
            unelevated
            label="确认"
            @click="handleRemove"
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
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import Page from '@/components/Page';
import { successNotify, formatSelectDisplay } from '@/utils/utils';
import { createEnvModel, vars } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'env/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'List',
  components: { Loading, Field, Page },
  data() {
    return {
      splitterModel: 30,
      URLHeaderModel: null,
      URLFooterModel : null,
      globalLoading: true,
      tab: "_a",
      pagination: getPagination(),
      addModalOpened: false,
      addModel: createEnvModel(),
      removeModalOpened: false,
      removeModel: '',
      editable: false,
      ...vars,
      // envs: '',
      step: 1 ,
      HeaderGroup: [
        {key:"",value:""}
      ],
      CookieGroup: [
        {key:"",value:""}
      ],
      env: createEnvModel(),
      resetModel: createEnvModel(),
      resetHeaderGroup: [],
      resetCookieGroup: [],
      URLOptions: vars.testEnvURL,
      formatSelectDisplay
    };
  },
  validations: {
    addModel: {
      name: { required },
      domain: { required },
    },
    resetModel: {
      name: { required },
      domain: { required },
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
    ...mapState('test', {
      envs: 'envs',
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  methods: {
    filterFn (val, update, abort) {
      update(() => {
        const needle = val.toLowerCase();
        this.URLOptions = vars.testEnvURL.filter(v => v.toLowerCase().indexOf(needle) > -1);
      })
    },
    // ...mapActions('project', {
    //   queryMember: 'fetchMember'
    // }),
    ...mapActions('test', {
      addEnv: 'addEnv',
      queryEnv: 'fetchEnv',
      removeEnv: 'removeEnv',
      updateEnv: 'updateEnv'
    }),//添加或者删除HeaderItem
    addOrDeleteGroupItem(Group,index){
      Group[index-1].deItemFlag = !Group[index-1].deItemFlag;
      if(Group[index-1].deItemFlag)
        Group.push({key:'',value:'',deItemFlag:false});
      else
        Group.splice(index - 1, 1);
    },
    handleAddModalOpen() {
      this.addModel = createEnvModel();
      this.$v.addModel.$reset();
      this.addModalOpened = true;
    },
    handleRemoveModalOpened() {
      this.removeModalOpened = true;
      // this.removeModel = module;
    },
    async handleRemove() {
      await this.removeEnv({
        projectId: this.projectId,
        ...this.resetModel
      });
      this.removeModalOpened = false;
      successNotify('删除成功');
    },
    async handleAdd() {
      this.addModel.header="";
      this.addModel.cookie="";
      this.addModel.domain = this.URLHeaderModel+this.URLFooterModel;
      let HGLength = this.HeaderGroup.length;
      let CGLength = this.CookieGroup.length;
      for(let i=0;i<HGLength;i++){
        if (i===HGLength-1)
          this.addModel.header += this.HeaderGroup[i].key+","+this.HeaderGroup[i].value;
        else
          this.addModel.header += this.HeaderGroup[i].key+","+this.HeaderGroup[i].value+";";
      }
      for(let i=0;i<CGLength;i++){
        if (i===CGLength-1)
          this.addModel.cookie += this.CookieGroup[i].key+","+this.CookieGroup[i].value;
        else
          this.addModel.cookie += this.CookieGroup[i].key+","+this.CookieGroup[i].value+";";
      }
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      await this.addEnv({
        projectId: this.projectId,
        ...this.addModel
      });
      successNotify('新增成功');
      this.addModalOpened = false;
    },
    async handleUpdateEnv() {

      this.resetModel.header="";
      this.resetModel.cookie="";
      let HGLength = this.resetHeaderGroup.length;
      let CGLength = this.resetCookieGroup.length;
      for(let i=0;i<HGLength;i++){
        if (i===HGLength-1)
          this.resetModel.header += this.resetHeaderGroup[i].key+","+this.resetHeaderGroup[i].value;
        else
          this.resetModel.header += this.resetHeaderGroup[i].key+","+this.resetHeaderGroup[i].value+";";
      }
      for(let i=0;i<CGLength;i++){
        if (i===CGLength-1)
          this.resetModel.cookie += this.resetCookieGroup[i].key+","+this.resetCookieGroup[i].value;
        else
          this.resetModel.cookie += this.resetCookieGroup[i].key+","+this.resetCookieGroup[i].value+";";
      }

      this.$v.resetModel.$touch();
      this.$refs.EnvForm.validate();
      if (this.$v.resetModel.$invalid) {
        return;
      }
      await this.updateEnv({
        projectId: this.projectId,
        ...this.resetModel
      });
      this.editable = false;
      successNotify('更新成功');
    },
    handleSelectEnv(env) {
      this.envs.forEach(env => (env.active = false));
      env.active = true;
      this.env = env;
      this.resetHeaderGroup = this.stringToGroup(this.resetHeaderGroup,this.env.header);
      this.resetCookieGroup = this.stringToGroup(this.resetCookieGroup,this.env.cookie);
      this.resetModel = {...env};
    },
    //分割cookie header字段转化成组
    stringToGroup(Group,str){
      Group = [];
      let items = str.split(";");
      for(let i=0;i<items.length;i++){
        let KV = items[i].split(",");
        Group.push({key:KV[0],value:KV[1],deItemFlag:true});
      }
      return Group;
    },
    handleResetEnv() {
      this.resetModel = {...this.env || createEnvModel()};
      this.resetHeaderGroup = this.stringToGroup(this.resetHeaderGroup,this.env.header);
      this.resetCookieGroup = this.stringToGroup(this.resetCookieGroup,this.env.cookie);
      this.editable = false;
    },
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryEnv(project);
    this.globalLoading = false;
    if (this.envs.length > 0) {
      this.handleSelectEnv(this.envs[0]);
    }
  },

  mounted() {}
};
</script>

<style lang="stylus" scoped>
.btn-add
  width: 40px;
  padding: 4px 8px;
.btn-add-feature
  &:hover
    opacity: 1;
.envInfoDiv {
  margin-top 20px;
}
.q-btn__content{
  text-align right;
  padding: 4px 8px;
}
</style>

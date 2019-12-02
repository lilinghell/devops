<template>
  <div class="q-pa-md">
    <p class="text-h5">请求参数</p>
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">Headers:</div>
      </q-card-section>

      <q-markup-table>
        <thead>
          <tr>
            <th class="text-left">参数名称</th>
            <th class="text-left">参数值</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, key, index) in interHeaders" :key="index">
            <td class="text-left">{{key}}</td>
            <td class="text-left">{{item}}</td>
          </tr>
        </tbody>
      </q-markup-table>
    </q-card>
    <q-card-section></q-card-section>
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">Query:</div>
      </q-card-section>

      <q-markup-table>
        <thead>
          <tr>
            <th class="text-left">参数名称</th>
            <th class="text-left">参数描述</th>
            <th class="text-left">类型</th>
            <th class="text-left">是否必输</th>
            <th class="text-left">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(query, index) in interQuerys" :key="index">
            <td class="text-left">{{query.name}}</td>
            <td class="text-left">{{query.description}}</td>
            <td class="text-left">{{query.type}}</td>
            <td class="text-left">{{query.required}}</td>
            <td class="text-left">
              <div v-if="query.items !== undefined">
                {{query.items.enum}}
                <br />
                default：{{query.items.default}}
              </div>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </q-card>
    <q-card-section></q-card-section>
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">Body:</div>
      </q-card-section>

      <q-markup-table>
        <thead>
          <tr>
            <th class="text-left">字段名称</th>
            <th class="text-left">字段描述</th>
            <th class="text-left">类型</th>
            <th class="text-left">是否必输</th>
            <th class="text-left">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in interBodyData" :key="index">
            <td class="text-left">
              <div v-html="data.name"></div>
            </td>
            <td class="text-left">{{data.description}}</td>
            <td class="text-left">{{data.type}}</td>
            <td class="text-left">{{data.required}}</td>
            <td class="text-left">
              <div v-if="data.items !== undefined">{{data.items.enum}}</div>
              <div v-if="data.default !== undefined">default：{{data.default}}</div>
              <div>{{data.enum}}</div>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </q-card>
    <p>
      <q-space />
    </p>
    <p class="text-h5">返回数据</p>
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">200:</div>
      </q-card-section>

      <q-markup-table>
        <thead>
          <tr>
            <th class="text-left">字段名称</th>
            <th class="text-left">字段描述</th>
            <th class="text-left">类型</th>
            <th class="text-left">是否必输</th>
            <th class="text-left">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in interResponse" :key="index">
            <td class="text-left">
              <div v-html="data.name"></div>
            </td>
            <td class="text-left">{{data.description}}</td>
            <td class="text-left">{{data.type}}</td>
            <td class="text-left">{{data.required}}</td>
            <td class="text-left">
              <div v-if="data.items !== undefined">
                {{data.items.type}}&nbsp;
                {{data.items.enum}}
              </div>
              <div v-if="data.default !== undefined">default：{{data.default}}</div>
              <div>{{data.enum}}</div>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </q-card>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import Loading from "@/components/Loading";
import Field from "@/components/Field";
import { formatSelectDisplay, successNotify, errorNotify } from "@/utils/utils";
import { vars as globalVars } from "@/views/model";
import { createDesignInterfaceModel, vars } from "../model";
import { isNumber } from "util";
import "swagger-editor-dist/swagger-editor.css";
import YAML from "js-yaml";

export default {
  name: "InterProfile",
  components: {
    Loading,
    Field
  },
  props: {
    inter: {
      type: Object
    }
  },
  data() {
    return {
      globalLoading: true,
      ...vars,
      interHeaders: {},
      interQuerys: [],
      interBodyData: [],
      interResponse: []
    };
  },
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("designs", {
      interfaceInfo: "interface"
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  validations: {},
  watch: {
    inter: {
      handler(newValue, oldValue) {},
      deep: true
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions("designs", {
      queryInterface: "fetchInterface"
    }),
    openRef(data, jsContent, num) {
      let p = [];
      if (undefined !== data.name) {
        p.push(data);
      } else {
        num = num - 30;
      }
      let definitions = jsContent.definitions;
      let schema = data.$ref.split("/");
      
      let d = schema[schema.length - 1];

      let properties = definitions[d].properties;
      let arr =
        definitions[d].required === undefined ? [] : definitions[d].required;
      let proKeys = Object.keys(properties);
      
      for (var i = 0; i < proKeys.length; i++) {
        let isRequired = false;
        let nameVal = proKeys[i];
        for (var jj = 0; jj < arr.length; jj++) {
          if (arr[jj] === nameVal) {
            isRequired = true;
            break;
          }
        }
        let pro = {
          name:
            '<div style="padding-left:' + num + 'px;">' + nameVal + "</div>",
          ...properties[proKeys[i]]
        };
        if ("object" === pro.type) {
          p = p.concat(this.subProperties(pro, jsContent, num + 30));
        } else if(undefined !== pro.$ref){
          p = p.concat(this.openRef(pro, jsContent, num + 30));
        } else if("array" === pro.type && undefined !== pro.items.$ref){
          let a = {};
          a.name = pro.name;
          a.$ref = pro.items.$ref;
          p = p.concat(this.openRef(a, jsContent, num + 30));
        } else {
          pro.required = isRequired;
          p.push(pro);
        }
      }
      return p;
    },
    openBody(data, jsContent) {
      let p = [];
      if (undefined !== data.schema.$ref) {
        p = this.openRef(data.schema, jsContent, 30);
      } else {
        if ("object" === data.schema.type) {
          p = p.concat(this.subProperties(data.schema, jsContent, 30));
        } else if("array" === data.schema.type && undefined !== data.schema.items.$ref){
          let a = {};
          a.$ref = data.schema.items.$ref;
          p = p.concat(this.openRef(a, jsContent, 30));
        }else {
          p.push(data.schema);
        }
      }

      return p;
    },
    subProperties(data, jsContent, num) {
      let pros = [];
      if (undefined !== data.name) {
        pros.push(data);
      } else {
        num = num - 30;
      }

      let prroperties = data.properties;
      let proKeys = Object.keys(prroperties);
      let arr = undefined !== data.required ? data.required : [];
      for (var i = 0; i < proKeys.length; i++) {
        let isRequired = false;
        let nameVal = proKeys[i];
        for (var jj = 0; jj < arr.length; jj++) {
          if (arr[jj] === nameVal) {
            isRequired = true;
            break;
          }
        }
        let pro = {
          name:
            '<div style="padding-left:' + num + 'px;">' + nameVal + "</div>",
          ...prroperties[nameVal]
        };
        if (undefined !== pro.$ref) {
          pros = pros.concat(this.openRef(pro, jsContent, num + 30));
        } else if ("object" === pro.type) {
          pros = pros.concat(this.subProperties(pro, jsContent, num + 30));
        }else if("array" === pro.type && undefined !== pro.items.$ref){
          let a = {};
          a.name = pro.name;
          a.$ref = pro.items.$ref;
          pros = pros.concat(this.openRef(a, jsContent, num + 30));
        } else {
          pro.required = isRequired;
          pros.push(pro);
        }
      }
      return pros;
    },
    properties() {
      if ("" === this.inter.info) {
        return;
      }
      this.interHeaders = {};
      this.interQuerys = [];
      this.interBodyData = [];
      try {
        let jsContent = YAML.safeLoad(this.inter.info);
        let path = Object.keys(jsContent.paths);
        let method = Object.keys(jsContent.paths[path[0]])[0];

        let contentType =
          jsContent.paths[path[0]][method].consumes === undefined
            ? ""
            : jsContent.paths[path[0]][method].consumes[0];
        this.interHeaders["Content-Type"] = contentType;
        let accept =
          jsContent.paths[path[0]][method].produces === undefined
            ? ""
            : jsContent.paths[path[0]][method].produces[0];
        this.interHeaders["Accept"] = accept;

        let parameters = jsContent.paths[path[0]][method].parameters;//请求字段
        for (var i = 0; i < parameters.length; i++) {
          if ("query" === parameters[i].in) {
            this.interQuerys.push(parameters[i]); //query
          } else if ("body" === parameters[i].in) {
            this.interBodyData = this.openBody(parameters[i], jsContent); //json
          } else {
            this.interBodyData.push(parameters[i]); //formData
          }
        }
        let responses = jsContent.paths[path[0]][method].responses;//应答字段
        this.interResponse = this.openBody(responses['200'], jsContent); //json
      } catch (e) {
        errorNotify("错误");
        console.error(e);
        return;
      }
    }
  },
  async created() {
    this.properties();
  },
  mounted() {}
};
</script>

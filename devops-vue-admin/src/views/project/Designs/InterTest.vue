<template>
  <div>
    <q-toolbar class="text-primary">
      <!-- <q-space /> -->
      <q-select
        filled
        :display-value="formatSelectDisplay(methodTypes, inter.method)"
        v-model="inter.method"
        :options="methodTypes"
        emit-value
        dense
        hint
        bg-color="white"
        :disable="true"
        hide-bottom-space
      />
      <q-separator dark vertical />
      <q-select
        style="width: 400px;"
        filled
        :display-value="formatSelectDisplay(envTypes, testEnv.id)"
        v-model="testEnv.id"
        :options="envTypes"
        emit-value
        dense
        hint
        hide-bottom-space
      />
      <q-separator dark vertical />
    </q-toolbar>
    <q-card-section class="q-gutter-y-sm">
      <div id="swagger-ui"></div>
    </q-card-section>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import Loading from "@/components/Loading";
import Field from "@/components/Field";
import { formatSelectDisplay, successNotify } from "@/utils/utils";
import { vars as globalVars } from "@/views/model";
import { isNumber } from "util";
import { SwaggerUIBundle, SwaggerUIStandalonePreset } from "swagger-ui-dist";
import "swagger-ui-dist/swagger-ui.css";
import YAML from "js-yaml";
import { vars, createTestEnvMode } from "../model";

export default {
  name: "InterTest",
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
      envTypes: [],
      testEnv: createTestEnvMode()
    };
  },
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("test", {
      envs: "envs"
    }),
    projectId() {
      return this.$route.params.projectId;
    }
  },
  validations: {},
  watch: {
    inter: {
      handler(newValue, oldValue) {
        console.log("nihao");
      },
      deep: true
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions("test", {
      queryEnv: "fetchEnv"
    }),
    tryRequest(t) {
      var x = t.url.indexOf("/");
      for (var i = 0; i < 2; i++) {
        x = t.url.indexOf("/", x + 1);
      }
      let host = t.url.substring(x, t.url.length);
      let url = "";
      for (var i = 0; i < this.envs.length; i++) {
        if (this.envs[i].id === this.testEnv.id) {
          url = this.envs[i].domain + host;
          break;
        }
      }
      t.url = url;
      console.log(t);
      return t;
    },
    swaggerUi() {
      let jsContent = YAML.safeLoad(this.inter.info);
      const ui = SwaggerUIBundle({
        spec: jsContent,
        dom_id: "#swagger-ui",
        layout: "BaseLayout",
        requestInterceptor: this.tryRequest
      });
      window.ui = ui;

      var v = document.getElementsByClassName("opblock-summary");
      v[0].click();
    }
  },
  async created() {
    await this.queryEnv({ projectId: this.projectId });
    let e = this.envs.map(env => {
      const a = {
        ...env,
        label: env.name + ": " + env.domain
      };
      return a;
    });
    this.envTypes = e;
    if (this.envTypes.length > 0) {
      this.testEnv = this.envTypes[0];
    }
    await this.swaggerUi();
  },
  async mounted() {}
};
</script>

<style>
</style>


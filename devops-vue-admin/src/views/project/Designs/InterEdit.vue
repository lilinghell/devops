<template>
  <div class="q-pa-md q-gutter-sm">
    <q-dialog v-model="opened" transition-show="slide-up" transition-hide="slide-down" maximized>
      <q-splitter v-model="splitterModel" style="height: 100%" class="bg-white">
        <template v-slot:before>
          <q-layout view="Lhh lpR fff" container class="bg-white">
            <q-page-container>
              <q-page padding class="column">
                <q-toolbar>
                  <q-btn flat v-close-popup round dense icon="arrow_back" size="lg" />
                </q-toolbar>
                <q-form @submit="handleEditInterface" ref="interfaceForm">
                  <q-card-section class="q-gutter-y-sm">
                    <div class="row">
                      <q-badge style="height: 20px;">{{inter.version}}</q-badge>
                      <q-input
                        style="width:85%"
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
                        :disable="true"
                      />
                    </div>

                    <Field :label-col="3" align="right">
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
                        hide-bottom-space
                      />
                    </Field>
                    <Field :label-col="3" align="right">
                      <template v-slot:label>
                        <span class="field">开放:</span>
                      </template>
                      <q-toggle v-model="inter.open" label />
                    </Field>
                    <div style="margin-top: 100px;" align="center" id="interSaveDiv">
                      <q-btn
                        style="width: 100px;"
                        color="primary"
                        unelevated
                        type="submit"
                        label="保存"
                      />
                    </div>
                  </q-card-section>
                </q-form>
              </q-page>
            </q-page-container>
          </q-layout>
        </template>
        <template v-slot:after>
          <div id="swagger-editor"></div>
        </template>
      </q-splitter>
    </q-dialog>
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
  name: "InterEdit",
  components: {
    Loading,
    Field
  },
  props: {
    value: {
      type: Boolean,
      default: false
    },
    inter: {
      type: Object
    }
  },
  data() {
    return {
      globalLoading: true,
      opened: false,
      splitterModel: 20,
      ...vars
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
  validations: {
    inter: {
      name: { required },
      url: { required },
      method: { required },
      version: { required },
      status: { required },
      application: { required },
      group: { required }
    }
  },
  watch: {
    value(val) {
      this.opened = val;
    },
    opened(val) {
      this.$emit("input", val);
      if (false === val) {
        // window.location.reload();
      }
    },
    inter: {
      handler(newValue, oldValue) {
        this.$parent.tab = "_a";
      },
      deep: true
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions("designs", {
      queryInterface: "fetchInterface",
      updateInterface: "updateInterface"
    }),
    async handleEditInterface() {
      await this.$parent.handUpdateInterface("code");
      this.opened = false;
    }
  },
  async created() {},
  mounted() {}
};
</script>

<style>
.Pane2 {
  overflow-y: scroll;
}

.swagger-ui .wrapper .models {
  display: none;
}

.swagger-ui .information-container {
  display: none;
}
.scheme-container {
  display: none;
}
/* .try-out {
  display: none;
} */
</style>


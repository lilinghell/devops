<template>
  <div class="q-pa-md">
    ui模式编辑
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
import YAML from "js-yaml";

export default {
  name: "InterUIEdit",
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
    })
  },
  async created() {
  },
  mounted() {}
};
</script>

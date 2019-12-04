<template>
  <div class="bg-white q-pa-md flex-center">
    <Loading :visible="globalLoading">
      pipelines
    </Loading>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
import Loading from "@/components/Loading";
import Field from "@/components/Field";
import { formatSelectDisplay, successNotify, errorNotify } from "@/utils/utils";
import { vars as globalVars } from "@/views/model";
import { isNumber } from "util";

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
      globalLoading: true
    };
  },
  computed: {
    ...mapState("global", ["loading"]),
    ...mapState("pipelines", {
      
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
    ...mapActions("pipelines", {
    })
  },
  async created() {
      this.globalLoading = false;
  },
  mounted() {}
};
</script>

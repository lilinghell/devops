<template>
  <footer class="footer" :class="color === 'white' ? 'white' : ''">
    <div class="links">
      <a href="http://devops-vue-admin.master.minikube/" target="_blank"
        >devops 首页</a
      >
      <a
        href="http://127.0.0.1/devops/devops-vue-admin"
        target="_blank"
      >
        <i class="mdi-set mdi-gitlab"></i>
      </a>
    </div>
    <div class="copyright">
      Copyright <q-icon name="copyright" /> 2019 XXX XXX
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  props: {
    color: {
      default: 'grey',
      type: String
    }
  },
  components: {},
  data() {
    return {};
  },
  computed: {},
  methods: {},
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.footer
  text-align: center;
  margin: 48px 0 24px 0;
  color: $grey-7;
  &.white
    color: white;
.links
  margin-bottom: 8px;
  a
    color: currentColor;
    &:not(:last-child)
      margin-right: 40px;
    &:hover
      color: $grey-9;
      footer.white &
        color: $grey-5;
</style>

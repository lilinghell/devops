<template>
  <div class="page-header">
    <q-breadcrumbs
      class="breadcrumbs"
      separator-color="grey-6"
      active-color="grey-6"
      gutter="xs"
    >
      <q-breadcrumbs-el
        class="breadcrumbs-el"
        v-for="crumb in breadCrumbList"
        :key="crumb.path"
        :to="crumb.path"
        :label="crumb.name"
        :icon="crumb.icon"
      />
    </q-breadcrumbs>
    <slot />
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  components: {},
  data() {
    return {
      breadCrumbList: []
    };
  },
  watch: {
    $route() {
      this.convert2BreadcrumbList(this.$route);
    }
  },
  computed: {},
  methods: {
    convert2BreadcrumbList(route) {
      const breadCrumbList = [];
      route.matched.forEach((matched, index) => {
        let { path } = matched;
        if (index === 0) {
          breadCrumbList.push({
            ...matched,
            name: '首页',
            icon: 'home'
          });
        } else {
          for (let key in route.params) {
            path = path.replace(`:${key}`, route.params[key]);
          }
          breadCrumbList.push({
            path,
            ...matched.meta,
            icon: ''
          });
        }
      });
      this.breadCrumbList = breadCrumbList;
    }
  },
  created() {
    this.convert2BreadcrumbList(this.$route);
  },
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.page-header
  background: white;
  padding: 16px 32px 0 32px;
  border-bottom: 1px solid $grey-4;
.breadcrumbs
  color: $grey-8;
  margin-bottom: 16px;
  .breadcrumbs-el
    &:hover
      color: $primary;
</style>

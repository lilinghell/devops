<template>
  <div>
    <PageHeader>
      <slot name="header" />
    </PageHeader>
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script>
import PageHeader from '../PageHeader';
export default {
  name: 'PageHeaderWrapper',
  components: { PageHeader },
  data() {
    return {};
  },
  computed: {},
  methods: {},
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.content
  margin: 24px 24px 0;
</style>

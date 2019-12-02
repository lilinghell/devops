<template>
  <div
    class="bg-white column"
    ref="page"
    :style="
      fullHeight
        ? { height: calculatedHeight }
        : { minHeight: calculatedHeight }
    "
  >
    <slot />
  </div>
</template>

<script>
import { dom } from 'quasar';
const { offset } = dom;

export default {
  name: 'Page',
  props: {
    fullHeight: Boolean
  },
  data() {
    return {
      minHeight: 250,
      offsetTop: 0,
      calculatedHeight: '',
      timeout: ''
    };
  },
  computed: {
    footerHeight() {
      return this.$route.meta && this.$route.meta.footerHidden ? 0 : 123;
    }
  },
  watch: {
    offsetTop(val) {
      let offset = this.footerHeight + this.offsetTop;
      this.calculatedHeight = `calc(100vh - ${offset}px)`;
    }
  },
  methods: {},
  created() {},
  mounted() {},
  updated: function() {
    this.timeout = setTimeout(() => {
      this.offsetTop = offset(this.$refs.page).top - offset(document.body).top;
    });
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style lang="stylus" scoped></style>

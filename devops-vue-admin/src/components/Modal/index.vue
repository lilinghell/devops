<template>
  <q-dialog
    v-model="opened"
    transition-show="slide-up"
    transition-hide="slide-down"
    maximized
  >
    <q-layout view="Lhh lpR fff" container class="bg-white">
      <q-page-container>
        <q-page padding class="column">
          <q-toolbar class="text-grey-9">
            <q-btn flat v-close-popup round dense icon="arrow_back" size="lg" />
          </q-toolbar>
          <div class="container col column">
            <div class="text-h2">{{ title }}</div>
            <slot />
          </div>
        </q-page>
      </q-page-container>
      <q-footer class="bg-transparent">
        <Footer />
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script>
import Footer from '@/layouts/Footer';

export default {
  name: 'Modal',
  components: { Footer },
  props: {
    value: {
      type: Boolean,
      default: false
    },
    title: {
      type: String
    }
  },
  data() {
    return {
      opened: false
    };
  },
  computed: {},
  watch: {
    value(val) {
      this.opened = val;
    },
    opened(val) {
      this.$emit('input', val);
    }
  },
  methods: {}
};
</script>

<style lang="stylus" scoped>
.container
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 60px;
</style>

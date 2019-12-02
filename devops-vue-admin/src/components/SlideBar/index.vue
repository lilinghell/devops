<template>
  <div>
    <q-bar class="bg-primary text-white">
      <slot name="before" />
      <div>{{ title }}</div>
      <q-space />
      <q-btn dense flat icon="minimize" @click="opened = false" />
      <q-btn dense flat icon="crop_square" @click="opened = true" />
      <q-btn dense flat icon="close" />
    </q-bar>
    <q-slide-transition>
      <div v-show="opened">
        <slot />
      </div>
    </q-slide-transition>
  </div>
</template>

<script>
export default {
  name: 'SlideBar',
  components: {},
  props: {
    value: {
      type: Boolean,
      default: true
    },
    title: {
      type: String
    }
  },
  data() {
    return {
      opened: true
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

<style lang="stylus" scoped></style>

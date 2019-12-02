<template>
  <div class="relative-position">
    <slot />
    <q-inner-loading :showing="visible">
      <slot name="spinner" v-if="!!$slots.spinner"></slot>
      <q-spinner-gears v-else size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>
export default {
  name: 'Loading',
  props: {
    visible: {
      default: false,
      type: Boolean
    }
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style lang="stylus" scoped></style>

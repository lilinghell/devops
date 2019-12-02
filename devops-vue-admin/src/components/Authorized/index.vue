<template>
  <div>
    <slot v-if="check()" />
    <slot v-else name="exception" />
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import { stringify } from 'qs';
import router from '@/router';

export default {
  name: 'Authorized',
  props: {
    authority: Array,
    transAuthority: Array,
    roleAuthority: String,
    includeMe: Array,
    noMatch: {}
  },
  computed: {
    ...mapGetters('authorized', ['checkPermissions', 'checkTransPermissions']),
    ...mapState('user', ['currentUser'])
  },
  data() {
    return {};
  },
  methods: {
    check() {
      let isChecked = true,
        isTransChecked = true,
        isRoleChecked = true,
        includeMe = true;

      if (this.authority) {
        isChecked = this.checkPermissions(this.authority);
      }
      if (this.transAuthority) {
        isTransChecked = this.checkTransPermissions(this.transAuthority);
      }
      if (this.roleAuthority) {
        isRoleChecked = this.currentUser.role.name === this.roleAuthority;
      }
      if (this.includeMe) {
        includeMe = this.includeMe.indexOf(this.currentUser.id) > -1;
      }

      if (isChecked && isTransChecked && isRoleChecked && includeMe) {
        return true;
      }

      if (typeof this.noMatch === 'function') {
        return this.noMatch();
      }
      if (Object.prototype.toString.call(this.noMatch) === '[object String]') {
        return router.push({
          path:
            this.noMatch +
            '?' +
            stringify({
              ...this.$route.query,
              redirect: this.$route.query.redirect || this.$route.path
            })
        });
      }
      return false;
    }
  },
  created() {},
  mounted() {}
};
</script>

<style lang="stylus" scoped></style>

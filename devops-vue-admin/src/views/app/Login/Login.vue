<template>
  <div>
    <q-form ref="form" @submit="handleLogin" class="form">
      <Loading :visible="loading">
        <q-input
          outlined
          bg-color="white"
          ref="username"
          dense
          class="col"
          v-model="$v.username.$model"
          type="text"
          placeholder="账号"
          autofocus
          :rules="[() => !$v.username.$error || '请输入账号']"
        >
          <template v-slot:prepend>
            <q-icon name="mdi-set mdi-account-outline" color="grey-6" />
          </template>
        </q-input>
        <q-input
          outlined
          bg-color="white"
          ref="password"
          dense
          class="col q-mb-md"
          v-model="$v.password.$model"
          type="password"
          placeholder="密码"
          :rules="[() => !$v.password.$error || '请输入密码']"
        >
          <template v-slot:prepend>
            <q-icon name="lock" color="grey-6" />
          </template>
        </q-input>
        <q-btn
          type="submit"
          color="primary"
          class="full-width"
          label="登录"
          :loading="loading['login/login']"
        />
      </Loading>
    </q-form>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import Loading from '@/components/Loading';

export default {
  name: 'Login',
  components: { Loading },
  data() {
    return {
      username: '',
      password: '',
      loading: false
    };
  },
  validations: {
    username: { required },
    password: { required }
  },
  computed: {},
  methods: {
    async handleLogin() {
      this.$v.$touch();
      this.$refs.form.validate();
      if (this.$v.$invalid) {
        return;
      }

      await this.$store.dispatch('login/login', {
        type: 'account',
        username: this.username,
        password: this.password
      });
    }
  },
  created() {},
  mounted() {}
};
</script>

<style lang="stylus" scoped>

.form
  margin: 0 auto;
  padding: 24px;
  border-radius: 3px;
  width: 368px;
.email
  height: 38px;
  width: 140px;
  text-overflow: ellipsis;
  overflow: hidden;

@media screen and (max-width: $sizes.sm)
  .form
    width: 95%;
</style>

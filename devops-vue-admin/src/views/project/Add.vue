<template>
  <div class="col row flex-center">
    <div class="col-4">
      <q-form ref="form" @submit="handleAdd">
        <Field stack-label label="名称">
          <q-input
            outlined
            v-model="$v.addModel.name.$model"
            type="text"
            autofocus
            dense
            :rules="[() => !$v.addModel.name.$error || '请输入项目名称']"
            placeholder="输入项目名称"
          />
        </Field>
        <Field stack-label label="项目描述" :label-col="4" align="right">
          <q-input
            outlined
            v-model="addModel.description"
            type="textarea"
            dense
          />
        </Field>
        <Field label="公开性" contracted>
          <q-option-group
            v-model="addModel.visit_level"
            :options="visit_levels"
            color="primary"
            inline
          />
        </Field>
        <div class="text-right q-mt-lg">
          <q-btn
            type="submit"
            unelevated
            color="primary"
            label="创建"
            :loading="loading['project/add']"
          />
        </div>
      </q-form>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import Field from '@/components/Field';
import { createProjectModel, vars } from './model';

export default {
  name: 'Add',
  components: { Field },
  props: {
    onProjectAdd: Function
  },
  data() {
    return {
      globalLoading: true,
      addModel: createProjectModel(),
      visit_levels: vars.visit_levels
    };
  },
  validations: {
    addModel: {
      name: {
        required
      },
      visit_level: {
        required
      }
    }
  },
  watch: {},
  computed: {
    ...mapState('global', ['loading'])
  },
  methods: {
    ...mapActions('project', {
      add: 'add'
    }),
    async handleAdd() {
      this.$v.addModel.$touch();
      this.$refs.form.validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      await this.add(this.addModel);
      await this.onProjectAdd();
    }
  },
  async created() {},
  mounted() {}
};
</script>

<style lang="stylus" scoped>
.kanban
  width: 300px;
  max-height: 40px;
</style>

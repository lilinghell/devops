import {
  addEnv,
  removeEnv,
  updateEnv,
  queryEnv,
  addTestCase,
  removeTestCase,
  updateTestCase,
  queryTestCase,
  addTestGroup,
  removeTestGroup,
  updateTestGroup,
  queryTestGroup,
  addPlan,
  removePlan,
  updatePlan,
  queryPlan,
  addAutoPlan,
  removeAutoPlan,
  updateAutoPlan,
  queryAutoPlan,
  addTest,
  removeTest,
  updateTest,
  queryTest,
} from '@/services/test';
import { resolveResponseError, formatOption } from '@/utils/utils';

export default {
  namespaced: true,

  state: {
    envs: [],
    testGroups: [],
    group: {},
    cases: [],
    testcase: {},
    plans: [],
    plan: {},
    autoPlans: [],
    test: {}
  },

  getters: {
  },

  actions: {
    // env
    async addEnv({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addEnv(projectId, payload)
      );
      const list = [...state.envs, formatOption(response)];
      commit('saveEnv', list);
    },
    async removeEnv({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeEnv(projectId, id));
      const list = state.envs.filter(item => id !== item.id);
      commit('saveEnv', list);
    },
    async updateEnv({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateEnv(projectId, id, payload)
      );
      let item = state.envs.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.envs];
        commit('saveEnv', list);
      }
    },
    async fetchEnv({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryEnv(projectId, id, payload)
      );
      commit('saveEnv', formatOption(response));
    },
    // Case
    async addTestCase({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addTestCase(projectId, payload)
      );
      commit('saveTestcase', response);
      const list = [...state.cases, formatOption(response)];
      commit('saveCase', list);
    },
    async removeTestCase({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeTestCase(projectId, id));
      const list = state.cases.filter(item => id !== item.id);
      commit('saveCase', list);
    },
    async updateTestCase({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateTestCase(projectId, id, payload)
      );
      let item = state.cases.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.cases];
        commit('saveCase', list);
      }
    },
    async fetchTestCase({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryTestCase(projectId, id, payload)
      );
      commit('saveCase', formatOption(response));
    },

    // TestGroup
    async addTestGroup({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addTestGroup(projectId, payload)
      );
      commit('saveGroup', response);
      const list = [...state.testGroups, formatOption(response)];
      commit('saveTestGroup', list);
    },
    async removeTestGroup({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeTestGroup(projectId, id));
      const list = state.testGroups.filter(item => id !== item.id);
      commit('saveTestGroup', list);
    },
    async updateTestGroup({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateTestGroup(projectId, id, payload)
      );
      let item = state.testGroups.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.testGroups];
        commit('saveTestGroup', list);
      }
    },
    async fetchTestGroup({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryTestGroup(projectId, id, payload)
      );
      commit('saveTestGroup', formatOption(response));
    },
    // plan
    async addPlan({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addPlan(projectId, payload)
      );
      const list = [...state.plans, formatOption(response)];
      commit('savePlan', list);
    },
    async removePlan({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removePlan(projectId, id));
      const list = state.plans.filter(item => id !== item.id);
      commit('savePlan', list);
    },
    async updatePlan({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updatePlan(projectId, id, payload)
      );
      let item = state.plans.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.plans];
        commit('savePlan', list);
      }
    },
    async fetchPlan({ commit, state }, {projectId,  id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryPlan(projectId, id, payload)
      );
      commit('savePlan', formatOption(response));
    },
    // AutoPlan
    async addAutoPlan({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addAutoPlan(projectId, payload)
      );
      const list = [...state.autoPlans, formatOption(response)];
      commit('saveAutoPlan', list);
    },
    async removeAutoPlan({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeAutoPlan(projectId, id));
      const list = state.autoPlans.filter(item => id !== item.id);
      commit('saveAutoPlan', list);
    },
    async updateAutoPlan({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateAutoPlan(projectId, id, payload)
      );
      let item = state.autoPlans.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.autoPlans];
        commit('saveAutoPlan', list);
      }
    },
    async fetchAutoPlan({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryAutoPlan(projectId, id, payload)
      );
      commit('saveAutoPlan', formatOption(response));
    },
    // Test
    async addTest({ commit, state }, { projectId, caseId, ...payload }) {
      const response = await resolveResponseError(() =>
        addTest(projectId, caseId, payload)
      );
      const list = [...state.test, formatOption(response)];
      commit('saveTest', list);
    },
    async removeTest({ commit, state }, { projectId, caseId, id }) {
      await resolveResponseError(() => removeTest(projectId, caseId , id));
      const list = state.test.filter(item => id !== item.id);
      commit('saveTest', list);
    },
    async updateTest({ commit, state }, { projectId, caseId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateTest(projectId, caseId, id, payload)
      );
      let item = state.test.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.test];
        commit('saveTest', list);
      }
    },
    async fetchTest({ commit, state }, { projectId, caseId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryTest(projectId, caseId, id, payload)
      );
      commit('saveTest', formatOption(response));
    },
  },

  mutations: {
    saveEnv(state, payload) {
      state.envs = payload;
    },
    saveCase(state, payload) {
      state.cases = payload;
    },
    saveTestcase(state, payload) {
      state.testcase = payload;
    },
    saveTestGroup(state, payload) {
      state.testGroups = payload;
    },
    saveGroup(state, payload){
      state.group = payload
    },
    savePlan(state, payload) {
      state.plans = payload;
    },
    saveAutoPlan(state, payload) {
      state.autoPlans = payload;
    },
    saveTest(state, payload) {
      state.test = payload;
    },
  }
};

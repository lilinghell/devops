import {
  addFeature,
  removeFeature,
  updateFeature,
  queryFeature,
  addFeatureBranch as addBranch,
  removeFeatureBranch as removeBranch,
  updateFeatureBranch as updateBranch,
  queryFeatureBranch as queryBranch
} from '@/services/project';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: [],
    branches: []
  },

  actions: {
    async add({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addFeature(projectId, payload)
      );
      const list = [...state.list, formatOption(response, 'title')];
      commit('save', list);
    },
    async remove({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeFeature(projectId, id));
      const list = state.list.filter(item => id !== item.id);
      commit('save', list);
    },
    async update({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateFeature(projectId, id, payload)
      );
      let item = state.list.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response, 'title'));
        const list = [...state.list];
        commit('save', list);
      }
    },
    async fetch({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryFeature(projectId, id, payload)
      );
      commit('save', formatOption(response, 'title'));
    },

    // branch
    async addBranch({ commit, state }, { projectId, featureId, ...payload }) {
      const response = await resolveResponseError(() =>
        addBranch(projectId, featureId, payload)
      );
      const list = [...state.branches, formatOption(response)];
      //commit('saveBranch', list);
    },
    async removeBranch({ commit, state }, { projectId, featureId, id }) {
      await resolveResponseError(() => removeBranch(projectId, featureId, id));
      const list = state.branches.filter(item => id !== item.id);
      commit('saveBranch', list);
    },
    async updateBranch(
      { commit, state },
      { projectId, featureId, id, ...payload }
    ) {
      const response = await resolveResponseError(() =>
        updateBranch(projectId, featureId, id, payload)
      );
      let item = state.branches.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.branches];
        commit('saveBranch', list);
      }
    },
    async fetchBranch(
      { commit, state },
      { projectId, featureId, id, ...payload } = {}
    ) {
      const response = await resolveResponseError(() =>
        queryBranch(projectId, featureId, id, payload)
      );
      let branches = response.map(branch => ({
        ...branch,
        user: formatOption(branch.user)
      }));
      commit('saveBranch', formatOption(branches));
    }
  },

  mutations: {
    save(state, payload) {
      state.list = payload;
    },
    saveBranch(state, payload) {
      state.branches = payload;
    }
  }
};

import {
  addApp,
  removeApp,
  updateApp,
  queryApp,
  addBranch,
  removeBranch,
  updateBranch,
  queryBranch,
  addCommit,
  removeCommit,
  updateCommit,
  queryCommit,
  updateRepo
} from '@/services/project';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: [],
    branches: [],
    commits: []
  },

  actions: {
    async add({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addApp(projectId, payload)
      );
      const list = [...state.list, formatOption(response)];
      commit('save', list);
    },
    async remove({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeApp(projectId, id));
      const list = state.list.filter(item => id !== item.id);
      commit('save', list);
    },
    async update({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateApp(projectId, id, payload)
      );
      let item = state.list.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.list];
        commit('save', list);
      }
    },
    async fetch({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryApp(projectId, id, payload)
      );
      commit('save', formatOption(response));
    },

    // branch
    async addBranch({ commit, state }, { projectId, appId, ...payload }) {
      const response = await resolveResponseError(() =>
        addBranch(projectId, appId, payload)
      );
      const list = [...state.branches, formatOption(response)];
      commit('saveBranch', list);
    },
    async removeBranch({ commit, state }, { projectId, appId, id }) {
      await resolveResponseError(() => removeBranch(projectId, appId, id));
      const list = state.branches.filter(item => id !== item.id);
      commit('saveBranch', list);
    },
    async updateBranch(
      { commit, state },
      { projectId, appId, id, ...payload }
    ) {
      const response = await resolveResponseError(() =>
        updateBranch(projectId, appId, id, payload)
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
      { projectId, appId, id, ...payload } = {}
    ) {
      const response = await resolveResponseError(() =>
        queryBranch(projectId, appId, id, payload)
      );
      let branches = response.map(branch => ({
        ...branch,
        user: formatOption(branch.user)
      }));
      commit('saveBranch', formatOption(branches));
    },

    // commit
    async addCommit({ commit, state }, { projectId, appId, ...payload }) {
      const response = await resolveResponseError(() =>
        addCommit(projectId, appId, payload)
      );
      const list = [...state.commits, formatOption(response)];
      commit('saveCommit', list);
    },
    async removeCommit({ commit, state }, { projectId, appId, id }) {
      await resolveResponseError(() => removeCommit(projectId, appId, id));
      const list = state.commits.filter(item => id !== item.id);
      commit('saveCommit', list);
    },
    async updateCommit(
      { commit, state },
      { projectId, appId, id, ...payload }
    ) {
      const response = await resolveResponseError(() =>
        updateCommit(projectId, appId, id, payload)
      );
      let item = state.commits.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.commits];
        commit('saveCommit', list);
      }
    },
    async fetchCommit(
      { commit, state },
      { projectId, appId, id, ...payload } = {}
    ) {
      const response = await resolveResponseError(() =>
        queryCommit(projectId, appId, id, payload)
      );
      let commits = response.map(branch => ({
        ...branch,
        user: formatOption(branch.user)
      }));
      commit('saveCommit', formatOption(commits));
    },

    async updateRepo({ commit, state }, { projectId, appId, ...payload }) {
      const response = await resolveResponseError(() =>
        updateRepo(projectId, appId, payload)
      );
      let item = state.list.find(item => item.id === appId);
      if (item) {
        Object.assign(item.repo, response);
        const list = [...state.commits];
        commit('saveBranch', list);
      }
    }
  },

  mutations: {
    save(state, payload) {
      state.list = payload;
    },
    saveBranch(state, payload) {
      state.branches = payload;
    },
    saveCommit(state, payload) {
      state.commits = payload;
    }
  }
};

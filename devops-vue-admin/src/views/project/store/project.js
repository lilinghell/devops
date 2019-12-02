import {
  query,
  queryCurrent,
  add,
  remove,
  update,
  addMember,
  removeMember,
  updateMember,
  queryMember,
  addModule,
  removeModule,
  updateModule,
  queryModule,
  addLabel,
  removeLabel,
  updateLabel,
  queryLabel
} from '@/services/project';
import { resolveResponseError, formatOption } from '@/utils/utils';

export default {
  namespaced: true,

  state: {
    list: [],
    currentProjects: [],
    members: [],
    modules: [],
    labels: []
  },

  getters: {
    users({ members }) {
      return members.map(member => member.user);
    }
  },

  actions: {
    async add({ commit, state }, { ...payload }) {
      const response = await resolveResponseError(() => add(payload));
      const list = [...state.list, formatOption(response)];
      commit('saveProject', list);
      const currentList = [...state.currentProjects, formatOption(response)];
      commit('saveCurrentProject', currentList);
    },
    async remove({ commit, state }, { id }) {
      await resolveResponseError(() => remove(id));
      const list = state.list.filter(item => id !== item.id);
      commit('saveProject', list);
    },
    async update({ commit, state }, { id, ...payload }) {
      const response = await resolveResponseError(() => update(id, payload));
      let org = state.list.find(item => item.id === id);
      if (org) {
        Object.assign(org, formatOption(response));
        const list = [...state.list];
        commit('saveProject', list);
      }
    },
    async fetch({ commit, state }, { id, ...payload } = {}) {
      const response = await resolveResponseError(() => query(id, payload));
      commit('saveProject', formatOption(response));
    },

    async fetchCurrent({ commit, state, dispatch }, payload) {
      const response = await resolveResponseError(queryCurrent);
      commit('saveCurrentProject', response);
    },

    // member
    async addMember({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addMember(projectId, payload)
      );
      const list = [...state.members, formatOption(response, 'user.name')];
      commit('saveMember', list);
    },
    async removeMember({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeMember(projectId, id));
      const list = state.members.filter(item => id !== item.id);
      commit('saveMember', list);
    },
    async updateMember({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateMember(projectId, id, payload)
      );
      let item = state.members.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response, 'user.name'));
        const list = [...state.members];
        commit('saveMember', list);
      }
    },
    async fetchMember({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryMember(projectId, id, payload)
      );
      let members = response.map(member => ({
        ...member,
        user: formatOption(member.user)
      }));
      commit('saveMember', formatOption(members));
    },

    // module
    async addModule({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addModule(projectId, payload)
      );
      const list = [...state.modules, formatOption(response)];
      commit('saveModule', list);
    },
    async removeModule({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeModule(projectId, id));
      const list = state.modules.filter(item => id !== item.id);
      commit('saveModule', list);
    },
    async updateModule({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateModule(projectId, id, payload)
      );
      let item = state.modules.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.modules];
        commit('saveModule', list);
      }
    },
    async fetchModule({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryModule(projectId, id, payload)
      );
      commit('saveModule', formatOption(response));
    },

    // label
    async addLabel({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addLabel(projectId, payload)
      );
      const list = [...state.labels, formatOption(response, 'title')];
      commit('saveLabel', list);
    },
    async removeLabel({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeLabel(projectId, id));
      const list = state.labels.filter(item => id !== item.id);
      commit('saveLabel', list);
    },
    async updateLabel({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateLabel(projectId, id, payload)
      );
      let item = state.labels.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response, 'title'));
        const list = [...state.labels];
        commit('saveLabel', list);
      }
    },
    async fetchLabel({ commit, state }, { projectId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryLabel(projectId, id, payload)
      );
      commit('saveLabel', formatOption(response, 'title'));
    }
  },

  mutations: {
    saveCurrentProject(state, payload) {
      state.currentProjects = payload;
    },
    saveProject(state, payload) {
      state.list = payload;
    },
    saveMember(state, payload) {
      state.members = payload;
    },
    saveModule(state, payload) {
      state.modules = payload;
    },
    saveLabel(state, payload) {
      state.labels = payload;
    }
  }
};

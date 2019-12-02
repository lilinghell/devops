import {
  addIteration,
  removeIteration,
  updateIteration,
  queryIteration
} from '@/services/project';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: []
  },

  actions: {
    async add({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addIteration(projectId, payload)
      );
      const list = [...state.list, formatOption(response, 'title')];
      commit('save', list);
    },
    async remove({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeIteration(projectId, id));
      const list = state.list.filter(item => id !== item.id);
      commit('save', list);
    },
    async update({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateIteration(projectId, id, payload)
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
        queryIteration(projectId, id, payload)
      );
      commit('save', formatOption(response, 'title'));
    }
  },

  mutations: {
    save(state, payload) {
      state.list = payload;
    }
  }
};

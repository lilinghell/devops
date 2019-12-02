import {
  addWorkItem,
  removeWorkItem,
  updateWorkItem,
  queryWorkItem,
  queryCurrentWorkItem as queryCurrent,
  addComment,
  removeComment,
  updateComment,
  queryComment
} from '@/services/project';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: [],
    currentWorkItems: [],
    comments: []
  },

  actions: {
    async add({ commit, state }, { projectId, ...payload }) {
      const response = await resolveResponseError(() =>
        addWorkItem(projectId, payload)
      );
      const list = [...state.list, formatOption(response)];
      commit('save', list);
    },
    async remove({ commit, state }, { projectId, id }) {
      await resolveResponseError(() => removeWorkItem(projectId, id));
      const list = state.list.filter(item => id !== item.id);
      commit('save', list);
    },
    async update({ commit, state }, { projectId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateWorkItem(projectId, id, payload)
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
        queryWorkItem(projectId, id, payload)
      );
      commit('save', formatOption(response));
    },
    async fetchCurrent({ commit, state, dispatch }, payload) {
      const response = await resolveResponseError(queryCurrent);
      commit('saveCurrentWorkItem', response);
    },

    // comment
    async addComment({ commit, state }, { projectId, workItemId, ...payload }) {
      const response = await resolveResponseError(() =>
        addComment(projectId, workItemId, payload)
      );
      const list = [...state.comments, formatOption(response)];
      commit('saveComment', list);
    },
    async removeComment({ commit, state }, { projectId, workItemId, id }) {
      await resolveResponseError(() =>
        removeComment(projectId, workItemId, id)
      );
      const list = state.comments.filter(item => id !== item.id);
      commit('saveComment', list);
    },
    async updateComment(
      { commit, state },
      { projectId, workItemId, id, ...payload }
    ) {
      const response = await resolveResponseError(() =>
        updateComment(projectId, workItemId, id, payload)
      );
      let item = state.comments.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.comments];
        commit('saveComment', list);
      }
    },
    async fetchComment(
      { commit, state },
      { projectId, workItemId, id, ...payload } = {}
    ) {
      const response = await resolveResponseError(() =>
        queryComment(projectId, workItemId, id, payload)
      );
      let comments = response.map(comment => ({
        ...comment,
        user: formatOption(comment.user)
      }));
      commit('saveComment', formatOption(comments));
    }
  },

  mutations: {
    save(state, payload) {
      state.list = payload;
    },
    saveCurrentWorkItem(state, payload) {
      state.currentWorkItems = payload;
    },
    saveComment(state, payload) {
      state.comments = payload;
    }
  }
};

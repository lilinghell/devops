import {
  query as queryUser,
  queryCurrent,
  add as addUser,
  remove as removeUser,
  update as updateUser
} from '@/services/user';
import { resolveResponseError, formatOption } from '@/utils/utils';
import { setAuthority } from '@/utils/authority';
import { createUserModel } from '@/views/model';

export default {
  namespaced: true,

  state: {
    list: [],
    currentUser: createUserModel(),
  },

  actions: {
    async add({ commit, state }, payload) {
      const response = await resolveResponseError(() => addUser(payload));
      const list = [...state.list, formatOption(response)];
      commit('save', list);
    },
    async remove({ commit, state }, { id }) {
      await resolveResponseError(() => removeUser(id));
      const list = state.list.filter(item => item.id !== id);
      commit('save', list);
    },
    async update({ commit, state }, { id, ...payload }) {
      const response = await resolveResponseError(() => updateUser(id, payload));
      let item = state.list.find(item => item.id === id);
      Object.assign(item, formatOption(response));
      const list = [...state.list];
      commit('save', list);
    },
    async fetch({ commit, state }, { id, ...payload } = {}) {
      const response = await resolveResponseError(() => queryUser(id, payload));
      commit('save', formatOption(response));
    },
    async fetchCurrent({ commit, state, dispatch }, payload) {
      const response = await queryCurrent();
      if (response.status === 'error') {
        return dispatch('login/logout', {}, { root: true });
      }

      commit('saveCurrentUser', response);
      commit('authorized/reloadAuthorized', null, { root: true });
    }
  },

  mutations: {
    save(state, payload) {
      state.list = payload
    },
    saveCurrentUser(state, payload) {
      state.currentUser = payload || {};
      setAuthority(payload.authority);
    },
    changeNotifyCount(state, payload) {
      state.currentUser =  {
        ...state.currentUser,
        notifyCount: payload,
      };
    },
  },
};

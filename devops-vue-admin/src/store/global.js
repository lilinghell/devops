import { queryNotice } from '@/services/api';

export default {
  namespaced: true,

  state: {
    notices: [],
    loading: {}
  },

  actions: {
    async fetchNotices({ commit, state }, payload) {
      const data = await queryNotice();
      commit('saveNotices', data);
      commit('user/changeNotifyCount', data.length, { root: true });
    },
    async clearNotices({ commit, state }, payload) {
      commit('saveClearedNotices', payload);
      const count = state.notices.length;
      commit('user/changeNotifyCount', count, { root: true });
    }
  },

  mutations: {
    saveLoading(state, payload) {
      state.loading = {
        ...state.loading,
        ...payload
      };
    },
    saveNotices(state, payload) {
      // state.notices = payload;
      state.notices = payload.filter(item => item.type === 'notification');
    },
    saveClearedNotices(state, payload) {
      state.notices = state.notices.filter(item => item.type !== payload);
    }
  }
};

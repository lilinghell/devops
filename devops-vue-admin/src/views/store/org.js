import {
  add,
  remove,
  update,
  query,
  addMember,
  removeMember,
  updateMember,
  queryMember,
  updateCurrentOrg
} from '@/services/org';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: [],
    members: []
  },

  actions: {
    async add({ commit, state }, payload) {
      const response = await resolveResponseError(() => add(payload));
      const list = [...state.list, response];
      commit('saveOrg', list);
    },
    async remove({ commit, state }, { id }) {
      await resolveResponseError(() => remove(id));
      const list = state.list.filter(item => id !== item.id);
      commit('saveOrg', list);
    },
    async update({ commit, state }, { id, ...payload }) {
      const response = await resolveResponseError(() => update(id, payload));
      let org = state.list.find(item => item.id === id);
      if (org) {
        Object.assign(org, response);
        const list = [...state.list];
        commit('saveOrg', list);
      }
    },
    async fetch({ commit, state }, { id, ...payload } = {}) {
      const response = await resolveResponseError(() => query(id, payload));
      commit('saveOrg', response);
    },

    // member
    async addMember({ commit, state }, { orgId, ...payload }) {
      const response = await resolveResponseError(() =>
        addMember(orgId, payload)
      );
      const list = [...state.members, formatOption(response)];
      commit('saveMember', list);
    },
    async removeMember({ commit, state }, { orgId, id }) {
      await resolveResponseError(() => removeMember(orgId, id));
      const list = state.members.filter(item => id !== item.id);
      commit('saveMember', list);
    },
    async updateMember({ commit, state }, { orgId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateMember(orgId, id, payload)
      );
      let item = state.members.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.members];
        commit('saveMember', list);
      }
    },
    async fetchMember({ commit, state }, { orgId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryMember(orgId, id, payload)
      );
      commit('saveMember', formatOption(response));
    },

    /**
     *  当前用户更新企业信息
     */
    async updateCurrentOrg({ commit, state }, { id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateCurrentOrg(payload)
      );
      let org = state.list.find(item => item.id === id);
      if (org) {
        Object.assign(org, response);
        const list = [...state.list];
        commit('saveOrg', list);
      }
    }
  },

  mutations: {
    saveOrg(state, payload) {
      state.list = payload;
    },
    saveMember(state, payload) {
      state.members = payload;
    }
  }
};

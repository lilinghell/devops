import {
  add,
  remove,
  update,
  query,
  addMember,
  removeMember,
  updateMember,
  queryMember
} from '@/services/team';
import { resolveResponseError, formatOption } from '@/utils/utils';
export default {
  namespaced: true,

  state: {
    list: [],
    members: []
  },

  actions: {
    async add({ commit, state }, { ...payload }) {
      const response = await resolveResponseError(() => add(payload));
      const list = [...state.list, formatOption(response)];
      commit('saveTeam', list);
    },
    async remove({ commit, state }, { id }) {
      await resolveResponseError(() => remove(id));
      const list = state.list.filter(item => id !== item.id);
      commit('saveTeam', list);
    },
    async update({ commit, state }, { id, ...payload }) {
      const response = await resolveResponseError(() => update(id, payload));
      let org = state.list.find(item => item.id === id);
      if (org) {
        Object.assign(org, formatOption(response));
        const list = [...state.list];
        commit('saveTeam', list);
      }
    },
    async fetch({ commit, state }, { id, ...payload } = {}) {
      const response = await resolveResponseError(() => query(id, payload));
      commit('saveTeam', formatOption(response));
    },

    // member
    async addMember({ commit, state }, { teamId, ...payload }) {
      const response = await resolveResponseError(() =>
        addMember(teamId, payload)
      );
      const list = [...state.members, formatOption(response)];
      commit('saveMember', list);
    },
    async removeMember({ commit, state }, { teamId, id }) {
      await resolveResponseError(() => removeMember(teamId, id));
      const list = state.members.filter(item => id !== item.id);
      commit('saveMember', list);
    },
    async updateMember({ commit, state }, { teamId, id, ...payload }) {
      const response = await resolveResponseError(() =>
        updateMember(teamId, id, payload)
      );
      let item = state.members.find(item => item.id === id);
      if (item) {
        Object.assign(item, formatOption(response));
        const list = [...state.members];
        commit('saveMember', list);
      }
    },
    async fetchMember({ commit, state }, { teamId, id, ...payload } = {}) {
      const response = await resolveResponseError(() =>
        queryMember(teamId, id, payload)
      );
      commit('saveMember', formatOption(response));
    }
  },

  mutations: {
    saveTeam(state, payload) {
      state.list = payload;
    },
    saveMember(state, payload) {
      state.members = payload;
    }
  }
};

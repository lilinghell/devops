import {
    addGroup,
    removeGroup,
    updateGroup,
    queryGroup,
    addInterface,
    removeInterface,
    updateInterface,
    queryInterface
} from '@/services/designs';
import { resolveResponseError } from '@/utils/utils';

export default {
    namespaced: true,

    state: {
        groupList: [],
        group: {},
        interfaceList: [],
        interface: {}
    },

    actions: {
        /* 组 */
        async addGroup({ commit, state }, { projectId, ...payload }) {
            const response = await resolveResponseError(() =>
                addGroup(projectId, payload)
            );
            commit('saveGroup', response);
            const list = [...state.groupList, response];
            commit('saveGroupList', list);
        },
        async removeGroup({ commit, state }, { projectId, id }) {
            await resolveResponseError(() => removeGroup(projectId, id));
            const list = state.groupList.filter(item => id !== item.id);
            commit('saveGroupList', list);
        },
        async updateGroup({ commit, state }, { projectId, id, ...payload }) {
            const response = await resolveResponseError(() =>
                updateGroup(projectId, id, payload)
            );
            let item = state.groupList.find(item => item.id === id);
            if (item) {
                Object.assign(item, response);
                const list = [...state.groupList];
                commit('saveGroupList', list);
            }
        },
        async fetchGroup({ commit, state }, { projectId, id, ...payload } = {}) {
            const response = await resolveResponseError(() =>
                queryGroup(projectId, id, payload)
            );
            commit('saveGroupList', response);
        },
        /* 接口 */
        async addInterface({ commit, state }, { projectId, ...payload }) {
            const response = await resolveResponseError(() =>
                addInterface(projectId, payload)
            );
            commit('saveInterface', response);
            const list = [...state.interfaceList, response];
            commit('saveInterfaceList', list);
        },
        async removeInterface({ commit, state }, { projectId, id }) {
            await resolveResponseError(() => removeInterface(projectId, id));
            const list = state.interfaceList.filter(item => id !== item.id);
            commit('saveInterfaceList', list);
        },
        async updateInterface({ commit, state }, { projectId, id, ...payload }) {
            const response = await resolveResponseError(() =>
                updateInterface(projectId, id, payload)
            );
            let item = state.interfaceList.find(item => item.id === id);
            if (item) {
                Object.assign(item, response);
                const list = [...state.interfaceList];
                commit('saveInterfaceList', list);
            }
        },
        async fetchInterface({ commit, state }, { projectId, id, ...payload } = {}) {
            const response = await resolveResponseError(() =>
                queryInterface(projectId, id, payload)
            );
            commit('saveInterfaceList', response);
        }
    },

    mutations: {
        saveGroup(state, payload){
            state.group = payload
        },
        saveGroupList(state, payload) {
            state.groupList = payload;
        },
        saveInterface(state, payload){
            state.interface = payload
        },
        saveInterfaceList(state, payload) {
            state.interfaceList = payload;
        }
    }
};
import { stringify } from 'qs';
import { LocalStorage } from 'quasar';
import router from '@/router';
import { login, logout } from '@/services/api';
import { setAuthority } from '@/utils/authority';
import {getPageQuery, resolveResponseError} from '@/utils/utils';
import {addApp} from "@/services/project";

export default {
  namespaced: true,

  state: {
    status: undefined
  },

  actions: {
    async login({ commit, state }, payload) {
      // const response = await login(payload);
      const response = await resolveResponseError(() =>
        login(payload)
      );
      const { status } = response;
      response.currentAuthority =
        status !== 'error' ? response.user.authority : 'guest';

      commit('changeLoginStatus', response);

      const params = getPageQuery();
      // eslint-disable-next-line no-unused-vars
      let { redirect, ...other } = params;

      if (status !== 'error') {
        commit('authorized/reloadAuthorized', null, { root: true });
        if (response.currentAuthority === 'superuser') {
          router.push('/manager');
        } else if (response.currentAuthority === 'admin') {
          router.push('/admin');
        } else {
          router.push('/project');
        }
        // router.push(`/${redirect? redirect: '/'}` + (other? `?${stringify(other)}`: ''));
      }
    },

    async logout({ commit, state }, payload) {
      logout(payload);
      commit('changeLoginStatus', {
        status: false,
        currentAuthority: 'guest',
        token: null
      });
      commit('authorized/reloadAuthorized', null, { root: true });

      router.push(
        '/login?' +
          stringify({
            redirect: window.location.hash.substring(2)
          })
      );
    }
  },

  mutations: {
    changeLoginStatus(state, payload) {
      LocalStorage.set('devops-vue-admin-jwt', payload.token);
      setAuthority(payload.currentAuthority);
      state.status = payload.status;
      state.type = payload.type;
    }
  }
};

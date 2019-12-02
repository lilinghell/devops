import routes from '@/config/router.config';

export default {
  namespaced: true,

  state: {
    menus: []
  },

  getters: {
    getMenu({ menus }) {
      return (key, params) => {
        let menuData = menus.find(menu => menu.name === key).menu;
        return fillParams(menuData, params);
      };
    }
  },
  actions: {
    // TODO: menu might be fetched from server
    initMenu({ commit, state }, payload) {
      let menuData = routes
        .filter(route => route.name !== 'login')
        .map(route => ({
          name: route.name,
          menu: format(route.children, route.meta.authority, route.path).filter(
            item => item.path && item.meta && item.meta.name
          )
        }));
      commit('setMenu', menuData);
    }
  },
  mutations: {
    setMenu(state, payload) {
      state.menus = payload;
    }
  }
};

function fillParams(data, params) {
  return data.map(item => {
    const result = {
      ...item
    };
    for (let key in params) {
      result.path = result.path.replace(`:${key}`, params[key]);
    }
    if (result.children) {
      result.children = fillParams(result.children, params);
    }
    return result;
  });
}

function format(data, parentAuthority, parentPath = '') {
  return data.map(item => {
    const { path } = item;
    if (!path || path === '**') {
      return {};
    }

    let result = {
      ...item,
      ...item.meta
    };

    result.path = path.startsWith('/')
      ? path
      : parentPath.endsWith('/')
      ? `${parentPath}${path}`
      : `${parentPath}/${path}`;

    result.authority =
      item.meta && item.meta.authority ? item.meta.authority : parentAuthority;

    if (item.children) {
      const children = format(item.children, result.authority, result.path);
      // Reduce memory usage
      result.children = children;
    }
    return result;
  });
}

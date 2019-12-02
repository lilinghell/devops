import Vue from 'vue';
import Router from 'vue-router';
import { join } from 'path';
import Noop from './views/Noop.vue';
import pageRoutes from './config/router.config';

Vue.use(Router);
const router = new Router({
  routes: format(pageRoutes)
});

router.beforeEach((to, from, next) => {
  const { meta } = to;
  if (meta && meta.name) {
    document.title = `${meta.name} - devops`;
  } else {
    document.title = 'devops';
  }
  next();
});

function format(data) {
  return data.map(item => {
    const result = {
      ...item
    };
    let { component, children, redirect, path } = result;
    if (!component) {
      result.component = Noop;
    }

    if (children) {
      if (!redirect) {
        result.redirect = join(path, children[0].path);
      }

      const child = format(children);
      // Reduce memory usage
      result.children = child;
    }
    return result;
  });
}

export default router;

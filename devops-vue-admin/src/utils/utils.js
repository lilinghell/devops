import moment from 'moment';
import nzh from 'nzh/cn';
import { parse, stringify } from 'qs';
import { Notify, scroll } from 'quasar';
const { getScrollTarget, setScrollPosition } = scroll;

export function fixedZero(val) {
  return val * 1 < 10 ? `0${val}` : val;
}

export function getTimeDistance(type) {
  const now = new Date();
  const oneDay = 1000 * 60 * 60 * 24;

  if (type === 'today') {
    now.setHours(0);
    now.setMinutes(0);
    now.setSeconds(0);
    return [moment(now), moment(now.getTime() + (oneDay - 1000))];
  }

  if (type === 'week') {
    let day = now.getDay();
    now.setHours(0);
    now.setMinutes(0);
    now.setSeconds(0);

    if (day === 0) {
      day = 6;
    } else {
      day -= 1;
    }

    const beginTime = now.getTime() - day * oneDay;

    return [moment(beginTime), moment(beginTime + (7 * oneDay - 1000))];
  }

  if (type === 'month') {
    const year = now.getFullYear();
    const month = now.getMonth();
    const nextDate = moment(now).add(1, 'months');
    const nextYear = nextDate.year();
    const nextMonth = nextDate.month();

    return [
      moment(`${year}-${fixedZero(month + 1)}-01 00:00:00`),
      moment(
        moment(
          `${nextYear}-${fixedZero(nextMonth + 1)}-01 00:00:00`
        ).valueOf() - 1000
      )
    ];
  }

  const year = now.getFullYear();
  return [moment(`${year}-01-01 00:00:00`), moment(`${year}-12-31 23:59:59`)];
}

export function getPlainNode(nodeList, parentPath = '') {
  const arr = [];
  nodeList.forEach(node => {
    const item = node;
    item.path = `${parentPath}/${item.path || ''}`.replace(/\/+/g, '/');
    item.exact = true;
    if (item.children && !item.component) {
      arr.push(...getPlainNode(item.children, item.path));
    } else {
      if (item.children && item.component) {
        item.exact = false;
      }
      arr.push(item);
    }
  });
  return arr;
}

export function digitUppercase(n) {
  return nzh.toMoney(n);
}

function getRelation(str1, str2) {
  if (str1 === str2) {
    console.warn('Two path are equal!'); // eslint-disable-line
  }
  const arr1 = str1.split('/');
  const arr2 = str2.split('/');
  if (arr2.every((item, index) => item === arr1[index])) {
    return 1;
  }
  if (arr1.every((item, index) => item === arr2[index])) {
    return 2;
  }
  return 3;
}

function getRenderArr(routes) {
  let renderArr = [];
  renderArr.push(routes[0]);
  for (let i = 1; i < routes.length; i += 1) {
    // 去重
    renderArr = renderArr.filter(item => getRelation(item, routes[i]) !== 1);
    // 是否包含
    const isAdd = renderArr.every(item => getRelation(item, routes[i]) === 3);
    if (isAdd) {
      renderArr.push(routes[i]);
    }
  }
  return renderArr;
}

/**
 * Get router routing configuration
 * { path:{name,...param}}=>Array<{name,path ...param}>
 * @param {string} path
 * @param {routerData} routerData
 */
export function getRoutes(path, routerData) {
  let routes = Object.keys(routerData).filter(
    routePath => routePath.indexOf(path) === 0 && routePath !== path
  );
  // Replace path to '' eg. path='user' /user/name => name
  routes = routes.map(item => item.replace(path, ''));
  // Get the route to be rendered to remove the deep rendering
  const renderArr = getRenderArr(routes);
  // Conversion and stitching parameters
  const renderRoutes = renderArr.map(item => {
    const exact = !routes.some(
      route => route !== item && getRelation(route, item) === 1
    );
    return {
      exact,
      ...routerData[`${path}${item}`],
      key: `${path}${item}`,
      path: `${path}${item}`
    };
  });
  return renderRoutes;
}

export function getPageQuery() {
  return parse(window.location.href.split('?')[1]);
}

export function getQueryPath(path = '', query = {}) {
  const search = stringify(query);
  if (search.length) {
    return `${path}?${search}`;
  }
  return path;
}

export function formatWan(val) {
  const v = val * 1;
  if (!v || Number.isNaN(v)) return '';

  let result = val;
  if (val > 10000) {
    result = Math.floor(val / 10000);
    result = `${result}万`;
  }
  return result;
}

export function formatSelectDisplay(options, selected, defaultDisplay) {
  let display = defaultDisplay ? defaultDisplay : '请选择',
    val,
    option;

  if (!selected) {
    return display;
  }
  if (!Array.isArray(options)) {
    return selected;
  }

  if (Array.isArray(selected)) {
    val = selected.map(sel => (sel.value ? sel.value : sel));
    option = options.filter(option => val.indexOf(option.value) > -1);
    return option;
  }

  val = selected.value ? selected.value : selected;
  option = options.find(option => option.value === val);

  if (!option) {
    return display;
  }
  return option.label;
}

function flatOption(obj, name) {
  if (!obj) {
    return {
      label: '',
      value: ''
    };
  }
  return {
    ...obj,
    label: name.split('.').reduce((pre, next) => pre[next], obj),
    value:
      name
        .replace(/(.*)(\.)[a-zA-Z_]*$|[a-zA-Z_]*/, '$1$2id')
        .split('.')
        .reduce((pre, next) => pre[next], obj) ||
      name.split('.').reduce((pre, next) => pre[next], obj)
  };
}
export function formatOption(obj, name = 'name') {
  if (Array.isArray(obj)) {
    return obj.map(each => formatSelectable(flatOption(each, name)));
  }
  return formatSelectable(flatOption(obj, name));
}

export function wrapOptionsTotal(options) {
  return [{ label: '全部', value: 'total' }, ...options];
}

export function successNotify(message) {
  let setting = {
    color: 'positive',
    icon: 'check_circle_outline',
    position: 'top',
    classes: 'notify-inline'
  };

  if (typeof message === 'string') {
    setting.message = message;
  } else {
    Object.assign(setting, message);
  }
  Notify.create(setting);
}

export function errorNotify(message) {
  let setting = {
    color: 'negative',
    icon: 'cancel',
    position: 'top'
  };

  if (typeof message === 'string') {
    setting.message = message;
  } else {
    Object.assign(setting, message);
  }
  Notify.create(setting);
}

export async function resolveResponseError(task) {
  let response = await task();
  if (response.status !== 'error') {
    return response;
  } else {
    const { code, msg } = response;
    errorNotify(msg);

    const error = new Error(msg);
    error.name = code;
    error.response = response;
    throw error;
  }
}

export function validate(ref) {
  if (Array.isArray(ref)) {
    ref.forEach(each => {
      if (each && each.validate) {
        each.validate();
      }
    });
  } else {
    for (let el in ref) {
      if (ref.hasOwnProperty(el)) {
        if (ref[el].validate) {
          ref[el].validate();
        }
      }
    }
  }
}

export function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

export function formatSelectable(obj) {
  return {
    ...obj,
    active: false
  };
}

export function scrollToElement(el) {
  let target = getScrollTarget(el);
  let offset = el.offsetTop;
  let duration = 100;
  setScrollPosition(target, offset, duration);
}

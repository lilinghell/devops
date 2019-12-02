import axios from 'axios';
import { Notify, SessionStorage, LocalStorage, Cookies } from 'quasar';
import hash from 'hash.js';
import store from '@/views/.storee';

let isExpirys = false;
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://10.134.13.25:8080/';
  // TODO offline support
  // isExpirys = true;
}

const codeMessage = {
  200: '服务器成功返回请求的数据。',
  201: '新建或修改数据成功。',
  202: '一个请求已经进入后台排队（异步任务）。',
  204: '删除数据成功。',
  400: '发出的请求有错误，服务器没有进行新建或修改数据的操作。',
  401: '用户没有权限（令牌、用户名、密码错误）。',
  403: '用户得到授权，但是访问是被禁止的。',
  404: '发出的请求针对的是不存在的记录，服务器没有进行操作。',
  406: '请求的格式不可得。',
  410: '请求的资源被永久删除，且不会再得到的。',
  422: '当创建一个对象时，发生一个验证错误。',
  500: '服务器发生错误，请检查服务器。',
  502: '网关错误。',
  503: '服务不可用，服务器暂时过载或维护。',
  504: '网关超时。'
};

const cachedSave = (response, hashcode) => {
  /**
   * store response data in SessionStorage
   * Does not support data other than json, Cache only json
   */
  const contentType = response.headers['content-type'];
  if (contentType && contentType.match(/application\/json/i)) {
    // All data is saved as text
    let text = JSON.stringify(response);
    SessionStorage.set(hashcode, text);
    SessionStorage.set(`${hashcode}:timestamp`, Date.now());
  }
  return response;
};

const resolveResponse = response => {
  const respData = response.data;
  let { msg, code, data } = respData;
  data = data === null ? {} : data;

  if (code === 'AAAAAAA') {
    return data;
  }
  return {
    ...data,
    code,
    msg,
    status: 'error',
    originalData: data
  };
};

/**
 * Requests a URL, returning a promise.
 *
 * @param  {string} url       The URL we want to request
 * @param  {object} [option] The options we want to pass to "fetch"
 */
export default function request(url, option) {
  const options = {
    expirys: isExpirys,
    ...option
  };
  /**
   * Produce fingerprints based on url and parameters
   * Maybe url has the same parameters
   */
  const fingerprint = url + (options.body ? JSON.stringify(options.body) : '');
  const hashcode = hash
    .sha256()
    .update(fingerprint)
    .digest('hex');

  const defaultOptions = {
    credentials: 'include',
    headers: {
      Authorization: LocalStorage.getItem('devops-vue-admin-jwt'),
      'X-CSRFToken': Cookies.get('csrftoken')
    }
  };
  const newOptions = { ...defaultOptions, ...options };
  if (
    newOptions.method === 'POST' ||
    newOptions.method === 'PUT' ||
    newOptions.method === 'DELETE'
  ) {
    if (!(newOptions.body instanceof FormData)) {
      newOptions.headers = {
        Accept: 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        ...newOptions.headers
      };
      newOptions.body = JSON.stringify(newOptions.body);
    } else {
      // newOptions.body is FormData
      newOptions.headers = {
        Accept: 'application/json',
        ...newOptions.headers
      };
    }
  }

  const expirys = options.expirys && 60;
  // options.expirys !== false, return the cache,
  if (options.expirys === false) {
    const cached = SessionStorage.getItem(hashcode);
    const whenCached = SessionStorage.getItem(`${hashcode}:timestamp`);
    if (cached !== null && whenCached !== null) {
      const age = (Date.now() - whenCached) / 1000;
      if (age < expirys) {
        const response = new Response(new Blob([cached]));
        return response.json();
      }
      SessionStorage.remove(hashcode);
      SessionStorage.remove(`${hashcode}:timestamp`);
    }
  }
  return axios(url, newOptions)
    .then(response => cachedSave(response, hashcode))
    .then(response => resolveResponse(response))
    .catch(e => {
      const response = e.response;
      const { status, statusText, request } = response;
      const errortext = codeMessage[status] || statusText;

      Notify.create({
        message: `请求错误 ${status}: ${request.responseURL}`,
        color: 'negative',
        icon: 'wifi',
        position: 'top-right'
      });

      if (status === 401) {
        store.dispatch('login/logout');
      }

      const error = new Error(errortext);
      error.name = status;
      error.response = response;
      throw error;

      /*// environment should not be used
      if (status === 403) {
        router.push('/exception/403');
        return;
      }
      if (status <= 504 && status >= 500) {
        router.push('/exception/500');
        return;
      }
      if (status >= 404 && status < 422) {
        router.push('/exception/404');
      }*/
    });
}

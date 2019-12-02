import request from '@/utils/request';

export async function login(params) {
  return request('/api/v1/login', {
    method: 'POST',
    data: {
      ...params
    }
  });
}

export async function logout(params) {
  return request('/api/v1/logout', {
    method: 'POST',
    data: {}
  });
}

export async function queryNotice() {
  return request('/fuser/api/notice/query', {
    method: 'POST',
    data: {}
  });
}

export async function queryAuth() {
  return request('/fuser/api/permission/query', {
    method: 'POST',
    data: {}
  });
}
export async function updateAuth(params) {
  return request('/fuser/api/permission/update', {
    method: 'POST',
    data: {
      ...params
    }
  });
}

export async function queryLog(params) {
  return request('/api/v1/logs', {
    params
  });
}

export async function importYaml(params) {
  return request('/api/v1/designs/interface_yaml/query', {
    params
  });
}
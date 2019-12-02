import request from '@/utils/request';
import { join } from 'path';

export async function add(params) {
  return request('/api/v1/users', {
    method: 'POST',
    data: {
      ...params
    }
  });
}

export async function remove(id) {
  return request(`/api/v1/users/${id}`, {
    method: 'DELETE'
  });
}

export async function update(id, params) {
  return request(`/api/v1/users/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}

export async function query(id = '', params) {
  return request(join('/api/v1/users', id), {
    params
  });
}

export async function queryCurrent() {
  return request('/api/v1/user/profile');
}

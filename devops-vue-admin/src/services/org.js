import request from '@/utils/request';
import { join } from 'path';

export async function add(params) {
  return request('/api/v1/admin/orgs', {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function remove(id) {
  return request(`/api/v1/admin/orgs/${id}`, {
    method: 'DELETE'
  });
}
export async function update(id, params) {
  return request(`/api/v1/admin/orgs/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function query(id = '', params) {
  return request(join('/api/v1/admin/orgs', id), {
    params
  });
}

export async function addMember(orgId, params) {
  return request(`/api/v1/admin/orgs/${orgId}/users`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeMember(orgId, id) {
  return request(`/api/v1/admin/orgs/${orgId}/users/${id}`, {
    method: 'DELETE'
  });
}
export async function updateMember(orgId, id, params) {
  return request(`/api/v1/admin/orgs/${orgId}/users/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryMember(orgId, id = '', params) {
  return request(join(`/api/v1/admin/orgs/${orgId}/users`, id), {
    params
  });
}

/**
 * 当前用户更新企业信息
 */
export async function updateCurrentOrg(params) {
  return request('/api/v1/org', {
    method: 'PUT',
    data: {
      ...params
    }
  });
}

import request from '@/utils/request';
import { join } from 'path';

export async function add(params) {
  return request('/api/v1/teams', {
    method: 'POST',
    data: {
      ...params,
      owner: params.owner.id
    }
  });
}
export async function remove(id) {
  return request(`/api/v1/teams/${id}`, {
    method: 'DELETE'
  });
}
export async function update(id, params) {
  return request(`/api/v1/teams/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function query(id = '', params) {
  return request(join('/api/v1/teams', id), {
    params
  });
}

export async function addMember(teamId, params) {
  return request(`/api/v1/teams/${teamId}/members`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeMember(teamId, id) {
  return request(`/api/v1/teams/${teamId}/members/${id}`, {
    method: 'DELETE'
  });
}
export async function updateMember(teamId, id, params) {
  return request(`/api/v1/teams/${teamId}/members/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryMember(teamId, id = '', params) {
  return request(join(`/api/v1/teams/${teamId}/members`, id), {
    params
  });
}

import request from '@/utils/request';
import { join } from 'path';
/* 接口组 */
export async function addGroup(projectId, params) {
    return request(`/api/v1/designs/${projectId}/groups`, {
        method: 'POST',
        data: {
            ...params,
            parent: params.parent.id,
            application: params.application.id,
            project: projectId
        },
    });
}

export async function removeGroup(projectId, id) {
    return request(`/api/v1/designs/${projectId}/groups/${id}`, {
        method: 'DELETE'
    });
}
export async function updateGroup(projectId, id, params) {
    return request(`/api/v1/designs/${projectId}/groups/${id}`, {
        method: 'PUT',
        data: {
            ...params,
            application: params.application.id
        }
    });
}
export async function queryGroup(projectId, id = '', params) {
    return request(join(`/api/v1/designs/${projectId}/groups`, id), {
        ...params
    });
}
/* 接口 */
export async function addInterface(projectId, params) {
    return request(`/api/v1/designs/${projectId}/interfaces`, {
        method: 'POST',
        data: {
            ...params,
            application: params.application.id,
            group: params.group.id,
            project: projectId
        },
    });
}
export async function removeInterface(projectId, id) {
    return request(`/api/v1/designs/${projectId}/interfaces/${id}`, {
        method: 'DELETE'
    });
}
export async function updateInterface(projectId, id, params) {
    return request(`/api/v1/designs/${projectId}/interfaces/${id}`, {
        method: 'PUT',
        data: {
            ...params,
            application: params.application.id,
            group: params.group.id
        }
    });
}
export async function queryInterface(projectId, id = '', params) {
    return request(join(`/api/v1/designs/${projectId}/interfaces`, id), {
        ...params
    });
}
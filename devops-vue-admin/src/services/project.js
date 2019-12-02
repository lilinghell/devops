import request from '@/utils/request';
import moment from 'moment';
import { join } from 'path';

export async function add(params) {
  return request('/api/v1/projects', {
    method: 'POST',
    data: {
      ...params
    }
  });
}

export async function remove(id) {
  return request(`/api/v1/projects/${id}`, {
    method: 'DELETE'
  });
}

export async function update(id, params) {
  return request(`/api/v1/projects/${id}`, {
    method: 'PUT',
    data: {
      ...params,
      team: params.team.id,
      owner: params.owner.id
    }
  });
}

export async function query(id = '', params) {
  return request(join('/api/v1/projects', id), {
    params
  });
}

export async function queryCurrent() {
  return request('/api/v1/user/projects');
}

export async function addMember(projectId, params) {
  return request(`/api/v1/projects/${projectId}/members`, {
    method: 'POST',
    data: {
      ...params,
      access_level: params.access_level.value,
      user: params.user.id
    },
  });
}
export async function removeMember(projectId, id) {
  return request(`/api/v1/projects/${projectId}/members/${id}`, {
    method: 'DELETE'
  });
}
export async function updateMember(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/members/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryMember(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/members`, id), {
    params
  });
}

export async function addModule(projectId, params) {
  return request(`/api/v1/projects/${projectId}/modules`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeModule(projectId, id) {
  return request(`/api/v1/projects/${projectId}/modules/${id}`, {
    method: 'DELETE'
  });
}
export async function updateModule(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/modules/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryModule(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/modules`, id), {
    params
  });
}

export async function addLabel(projectId, params) {
  return request(`/api/v1/projects/${projectId}/labels`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeLabel(projectId, id) {
  return request(`/api/v1/projects/${projectId}/labels/${id}`, {
    method: 'DELETE'
  });
}
export async function updateLabel(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/labels/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryLabel(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/labels`, id), {
    params
  });
}

export async function addApp(projectId, params) {
  return request(`/api/v1/projects/${projectId}/apps`, {
    method: 'POST',
    data: {
      ...params,
      repo: {
        ...params.repo,
        type: params.repo.type.value
      },
      type: params.type.value
    }
  });
}
export async function removeApp(projectId, id) {
  return request(`/api/v1/projects/${projectId}/apps/${id}`, {
    method: 'DELETE'
  });
}
export async function updateApp(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/apps/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryApp(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/apps`, id), {
    params
  });
}

export async function addFeature(projectId, params) {
  return request(`/api/v1/projects/${projectId}/features`, {
    method: 'POST',
    data: {
      ...params,
      labels: params.labels.map(label => label.id),
      apps: params.apps.map(app => app.id),
      owner: params.owner.id,
      priority: params.priority.value,
      important: params.important.value,
      module: params.module.id,
      start_date: moment(params.start_date).format('YYYYMMDD'),
      end_date: moment(params.end_date).format('YYYYMMDD')
    }
  });
}
export async function removeFeature(projectId, id) {
  return request(`/api/v1/projects/${projectId}/features/${id}`, {
    method: 'DELETE'
  });
}
export async function updateFeature(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/features/${id}`, {
    method: 'PUT',
    data: {
      ...params,
      labels: params.labels.map(label => label.id),
      apps: params.apps.map(app => app.id),
      owner: params.owner.id,
      attachments: params.attachments.map(attachment => attachment.id),
      module: params.module.id
    }
  });
}
export async function queryFeature(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/features`, id), {
    params
  });
}

export async function addWorkItem(projectId, params) {
  return request(`/api/v1/projects/${projectId}/workItems`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeWorkItem(projectId, id) {
  return request(`/api/v1/projects/${projectId}/workItems/${id}`, {
    method: 'DELETE'
  });
}
export async function updateWorkItem(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/workItems/${id}`, {
    method: 'PUT',
    data: {
      ...params,
      start_date: params.start_date !== '' ? moment(params.start_date).format('YYYYMMDD') : '',
      end_date: params.end_date !== '' ? moment(params.end_date).format('YYYYMMDD') : ''
    },
  });
}
export async function queryWorkItem(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/workItems`, id), {
    params
  });
}
export async function queryCurrentWorkItem() {
  return request('/api/v1/user/workItems');
}

export async function addIteration(projectId, params) {
  return request(`/api/v1/projects/${projectId}/iterations`, {
    method: 'POST',
    data: {
      ...params,
      end_date: moment(params.end_date).format('YYYYMMDD'),
      start_date: moment(params.start_date).format('YYYYMMDD'),
      owner: params.owner.id
    }
  });
}
export async function removeIteration(projectId, id) {
  return request(`/api/v1/projects/${projectId}/iterations/${id}`, {
    method: 'DELETE'
  });
}
export async function updateIteration(projectId, id, params) {
  return request(`/api/v1/projects/${projectId}/iterations/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryIteration(projectId, id = '', params) {
  return request(join(`/api/v1/projects/${projectId}/iterations`, id), {
    params
  });
}

export async function addBranch(projectId, appId, params) {
  return request(`/api/v1/projects/${projectId}/apps/${appId}/git_branchs`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeBranch(projectId, appId, id) {
  return request(
    `/api/v1/projects/${projectId}/apps/${appId}/git_branchs/${id}`,
    {
      method: 'DELETE'
    }
  );
}
export async function updateBranch(projectId, appId, id, params) {
  return request(
    `/api/v1/projects/${projectId}/apps/${appId}/git_branchs/${id}`,
    {
      method: 'PUT',
      data: {
        ...params
      }
    }
  );
}
export async function queryBranch(projectId, appId, id = '', params) {
  return request(
    join(`/api/v1/projects/${projectId}/apps/${appId}/git_branchs`, id),
    {
      params
    }
  );
}

export async function updateRepo(projectId, appId, params) {
  return request(`/api/v1/projects/${projectId}/apps/${appId}/repos`, {
    method: 'PUT',
    data: {
      ...params,
      auth_type: params.auth_type.value,
      type: params.type.value
    }
  });
}
// feature/branch
export async function addFeatureBranch(projectId, featureId, params) {
  return request(`/api/v1/projects/${projectId}/features/${featureId}/branchs`, {
    method: 'POST',
    data: {
      ...params,
      ref: params.ref.name
    },
  });
}
export async function removeFeatureBranch(projectId, featureId, id) {
  return request(
    `/api/v1/projects/${projectId}/features/${featureId}/branchs/${id}`,
    {
      method: 'DELETE'
    }
  );
}
export async function updateFeatureBranch(projectId, featureId, id, params) {
  return request(
    `/api/v1/projects/${projectId}/features/${featureId}/branchs/${id}`,
    {
      method: 'PUT',
      data: {
        ...params
      }
    }
  );
}
export async function queryFeatureBranch(
  projectId,
  featureId,
  id = '',
  params
) {
  return request(
    join(`/api/v1/projects/${projectId}/features/${featureId}/branchs`, id),
    {
      params
    }
  );
}

export async function addComment(projectId, workItemId, params) {
  return request(
    `/api/v1/projects/${projectId}/workItems/${workItemId}/comments`,
    {
      method: 'POST',
      data: {
        ...params
      }
    }
  );
}
export async function removeComment(projectId, workItemId, id) {
  return request(
    `/api/v1/projects/${projectId}/workItems/${workItemId}/comments/${id}`,
    {
      method: 'DELETE'
    }
  );
}
export async function updateComment(projectId, workItemId, id, params) {
  return request(
    `/api/v1/projects/${projectId}/workItems/${workItemId}/comments/${id}`,
    {
      method: 'PUT',
      data: {
        ...params
      }
    }
  );
}
export async function queryComment(projectId, workItemId, id = '', params) {
  return request(
    join(`/api/v1/projects/${projectId}/workItems/${workItemId}/comments`, id),
    {
      params
    }
  );
}

export async function addCommit(projectId, appId, params) {
  return request(`/api/v1/projects/${projectId}/apps/${appId}/commits`, {
    method: 'POST',
    data: {
      ...params
    }
  });
}
export async function removeCommit(projectId, appId, id) {
  return request(`/api/v1/projects/${projectId}/apps/${appId}/commits/${id}`, {
    method: 'DELETE'
  });
}
export async function updateCommit(projectId, appId, id, params) {
  return request(`/api/v1/projects/${projectId}/apps/${appId}/commits/${id}`, {
    method: 'PUT',
    data: {
      ...params
    }
  });
}
export async function queryCommit(projectId, appId, id = '', params) {
  return request(
    join(`/api/v1/projects/${projectId}/apps/${appId}/commits`, id),
    {
      params
    }
  );
}

import request from '@/utils/request';
import { join } from 'path';
import moment from 'moment';

export async function addEnv(projectId, params) {
  return request(`/api/v1/test/${projectId}/env`, {
    method: 'POST',
    data: {
      ...params,
      project: projectId
    }
  });
}

export async function removeEnv(projectId, id) {
  return request(`/api/v1/test/${projectId}/env/${id}`, {
    method: 'DELETE'
  });
}

export async function updateEnv(projectId, id, params) {
  return request(`/api/v1/test/${projectId}/env/${id}`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryEnv(projectId, id = '', params) {
  return request(join(`/api/v1/test/${projectId}/env`, id), {
    params,
    project: projectId
  });
}

//CASE
export async function addTestCase(projectId,params) {
  return request(`/api/v1/test/${projectId}/cases`, {
    method: 'POST',
    data: {
      ...params,
      group : params.group.id,
      user : params.user.id,
      feature: params.feature.map(feature => feature.id),
      project: projectId
    }
  });
}

export async function removeTestCase(projectId,id) {
  return request(`/api/v1/test/${projectId}/cases/${id}`, {
    method: 'DELETE'
  });
}

export async function updateTestCase(projectId,id, params) {
  return request(`/api/v1/test/${projectId}/cases/${id}`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryTestCase(projectId,id = '', params) {
  return request(join(`/api/v1/test/${projectId}/cases`, id), {
    params,
    project: projectId
  });
}

//GROUP
export async function addTestGroup(projectId, params) {
  return request(`/api/v1/test/${projectId}/group`, {
    method: 'POST',
    data: {
      ...params,
      parent: params.parent.id,
      project: projectId
    }
  });
}

export async function removeTestGroup(projectId, id) {
  return request(`/api/v1/test/${projectId}/group/${id}`, {
    method: 'DELETE'
  });
}

export async function updateTestGroup(projectId, id, params) {
  return request(`/api/v1/test/${projectId}/group/${id}`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryTestGroup(projectId, id = '', params) {
  return request(join(`/api/v1/test/${projectId}/group`, id), {
    params,
    project: projectId
  });
}

//Plan
export async function addPlan(projectId, params) {
  return request(`/api/v1/test/${projectId}/plan`, {
    method: 'POST',
    data: {
      ...params,
      case: params.case,
      user : params.user.id,
      start_date: moment(params.start_date).format('YYYYMMDD'),
      end_date: moment(params.end_date).format('YYYYMMDD'),
      project: projectId
    }
  });
}

export async function removePlan(projectId, id) {
  return request(`/api/v1/test/${projectId}/plan/${id}`, {
    method: 'DELETE'
  });
}

export async function updatePlan(projectId, id, params) {
  return request(`/api/v1/test/${projectId}/plan/${id}`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryPlan(projectId, id = '', params) {
  return request(join(`/api/v1/test/${projectId}/plan`, id), {
    params,
    project: projectId
  });
}
//AutoPlan
export async function addAutoPlan(projectId, params) {
  return request(`/api/v1/test/${projectId}/auto_plan`, {
    method: 'POST',
    data: {
      ...params,
      case: params.case,
      user : params.user.id,
      env: params.env.id,
      project: projectId
    }
  });
}

export async function removeAutoPlan(projectId, id) {
  return request(`/api/v1/test/${projectId}/auto_plan/${id}`, {
    method: 'DELETE'
  });
}

export async function updateAutoPlan(projectId, id, params) {
  return request(`/api/v1/test/${projectId}/auto_plan/${id}`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryAutoPlan(projectId, id = '', params) {
  return request(join(`/api/v1/test/${projectId}/auto_plan`, id), {
    params,
    project: projectId
  });
}
//Test
export async function addTest(projectId, caseId, params) {
  return request(`/api/v1/test/${projectId}/${caseId}/test`, {
    method: 'POST',
    data: {
      ...params,
      project: projectId,
      case: caseId
    }
  });
}

export async function removeTest(projectId, caseId, id) {
  return request(`/api/v1/test/${projectId}/${caseId}/test`, {
    method: 'DELETE'
  });
}

export async function updateTest(projectId, caseId, id, params) {
  return request(`/api/v1/test/${projectId}/${caseId}/test`, {
    method: 'PUT',
    data: {
      ...params,
    }
  });
}

export async function queryTest(projectId, caseId, id = '', params) {
  return request(join(`/api/v1/test/${projectId}/${caseId}/test`, id), {
    params,
    project: projectId,
    case: caseId
  });
}
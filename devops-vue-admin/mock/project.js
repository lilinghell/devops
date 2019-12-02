const mockjs = require('mockjs');

const project = {
  id: '@id',
  owner: {
    id: '@id',
    name: '@cname',
    email: '@email',
    avatar_url: mockjs.Random.image('100x100')
  },
  team: {
    id: '@id',
    name: '@string'
  },
  created_at: '@date',
  updated_at: '@date',
  name: '@string',
  description: '@cparagraph',
  logo: mockjs.Random.image('100x100'),
  visit_level: 90,
  org: '@string',
  created_by: '@id',
  parent: '@string'
};

const member = {
  id: '@id',
  user: {
    id: '@id',
    name: '@cname',
    username: '@string',
    email: '@email',
    avatar_url: mockjs.Random.image('100x100'),
    wechat: '@string',
    phone: '13000000001',
    description: '@cparagraph',
    source: '@string',
    is_valid: '@boolean',
    is_expired: '@boolean',
    is_active: '@boolean',
    created_by: '@id',
    is_first_login: '@boolean',
    is_superuser: '@boolean',
    is_team_admin: '@boolean',
    date_password_last_updated: '@date',
    date_expired: '@date'
  },
  created_at: '@date',
  updated_at: '@date',
  source_id: '@id',
  source_type: 'team',
  type: 'TeamMember',
  access_level: 0,
  notification_level: 0,
  org: '@cname',
  created_by: '@id'
};

const _module = {
  id: '@id',
  created_at: '@date',
  updated_at: '@date',
  name: '@string',
  description: '@cparagraph',
  org: '@string',
  created_by: '@id',
  project: '@string'
};

const label = {
  id: '@id',
  created_at: '@date',
  updated_at: '@date',
  title: '@string',
  color: '@color',
  description: '@cparagraph',
  type: '@string',
  org: '@string',
  created_by: '@id',
  team: '@string',
  project: '@string'
};

const repo = {
  app: '@id',
  created_at: '@date',
  updated_at: '@date',
  type: 'git',
  web_url: '@url',
  scm_url: '@url',
  branch: '@string',
  auth_type: '@string',
  auth_token: '@string',
  auth_username: '@string',
  auth_pwd: '@string',
  org: '@string',
  created_by: '@id',
  project: '@id'
};

const app = {
  id: '@id',
  repo,
  created_at: '@date',
  updated_at: '@date',
  name: '@string',
  description: '@cparagraph',
  'type|1': ['mircoservice', 'web', 'batch', 'j2se'],
  status: '0',
  org: '@id',
  created_by: '@id',
  project: '@id',
  owner: '@id'
};

const iteration = {
  id: '@id',
  'feature_count|1-5': 100,
  'workItem_count|1-5': 100,
  created_at: '@date',
  updated_at: '@date',
  title: '@string',
  description: '@cparagraph',
  start_date: '@date',
  end_date: '@date',
  'status|1': [1, 2, 3, 4],
  org: '@id',
  created_by: member.user,
  owner: member.user,
  'progress|1-100': 100,
  project: project
};

const feature = {
  id: '@id',
  'labels|3-5': [
    {
      id: '@id',
      title: '@string',
      color: '@color'
    }
  ],
  'attachments|3-5': [
    {
      id: '@id',
      file: '@url',
      filename: '@string',
      filesize: 100
    }
  ],
  created_at: '@date',
  updated_at: '@date',
  title: '@string',
  description: '@cparagraph',
  description_html: '@url',
  start_date: '@date',
  end_date: '@date',
  'important|1-3': 100,
  'priority|1-3': 100,
  estimate_time: '@date',
  'progress|1-100': 100,
  'status|1-2': 100,
  closed_at: '@date',
  org: '@id',
  created_by: '@id',
  owner: member.user,
  closed_by: '@id',
  app: '@id',
  project: '@id',
  requirement: '@id',
  iteration: iteration,
  module: _module
};

const workItem = {
  id: '@id',
  'assignee_users|3-5': [
    {
      id: '@id',
      name: '@cname',
      email: '@email',
      phone: '13013013012',
      avatar_url: mockjs.Random.image('100x100')
    }
  ],
  labels: [
    {
      id: '@id',
      title: '@string',
      color: '@color'
    }
  ],
  'attachments|3-5': [
    {
      id: '@id',
      file: '@url',
      filename: '@string',
      filesize: 100
    }
  ],
  created_at: '@date',
  updated_at: '@date',
  title: '@string',
  description: '@cparagraph',
  type: '1',
  description_html: '@url',
  start_date: '@date',
  end_date: '@date',
  'important|1-3': 100,
  'priority|1-3': 100,
  estimate_time: '@date',
  'progress|1-100': 100,
  'status|1-4': 100,
  closed_at: '@date',
  org: '@id',
  created_by: '@id',
  owner: member.user,
  closed_by: '@id',
  project: '@id',
  module: _module,
  feature: feature,
  parent: '@id',
  iteration: '@id'
};

const branch = {
  id: '@id',
  feature,
  app,
  created_at: '@date',
  updated_at: '@date',
  branch_name: '@string',
  ref: '@string',
  status: '@string',
  org: '@id',
  created_by: member.user
};

const gitBranch = {
  commit: {
    author_name: '@name',
    author_email: '@email',
    title: '@string',
    created_at: '@date',
    message: '@cparagraph',
    id: '@id',
    authored_date: '@date',
    short_id: '@id',
    parent_ids: ['@id'],
    committer_name: '@name',
    committed_date: '@date',
    committer_email: '@email'
  },
  merged: '@boolean',
  name: '@string',
  developers_can_merge: 'boolean',
  developers_can_push: 'boolean',
  web_url: '@url',
  protected: 'boolean'
};

const comment = {
  id: '@id',
  comment: '@cparagraph',
  created_by: member.user,
  created_at: '@date'
};

const commit = {
  merged: '@boolean',
  developers_can_merge: '@boolean',
  commit: {
    title: '@cname',
    id: '@id',
    committer_name: '@cname',
    message: '@cparagraph', //merge branch 'dev-liling' into 'master'
    parent_ids: ['@id'],
    created_at: '@date',
    committed_date: '@date', //date
    short_id: '@id', //id
    author_email: '@email',
    committer_email: '@email',
    author_name: '@cname', //shaoyonghua
    authored_date: '@date'
  },
  developers_can_push: '@boolean',
  name: 'dev-liling',
  protected: '@boolean',
  web_url: '@url'
};

module.exports = {
  'POST /api/:version/projects/:projectId/apps/:appId/commits': mockjs.mock(
    commit
  ),
  'DELETE /api/:version/projects/:projectId/apps/:appId/commits/:id': mockjs.mock(
    commit
  ),
  'PUT /api/:version/projects/:projectId/apps/:appId/commits/:id': mockjs.mock(
    commit
  ),
  'GET /api/:version/projects/:projectId/apps/:appId/commits': mockjs.mock({
    'list|5': [commit]
  })['list'],
  'GET /api/:version/projects/:projectId/apps/:appId/commits/:id': mockjs.mock(
    commit
  ),

  'POST /api/:version/projects/:projectId/workItems/:workItemId/comments': mockjs.mock(
    comment
  ),
  'DELETE /api/:version/projects/:projectId/workItems/:workItemId/comments/:id': mockjs.mock(
    comment
  ),
  'PUT /api/:version/projects/:projectId/workItems/:workItemId/comments/:id': mockjs.mock(
    comment
  ),
  'GET /api/:version/projects/:projectId/workItems/:workItemId/comments': mockjs.mock(
    {
      'list|20': [comment]
    }
  )['list'],
  'GET /api/:version/projects/:projectId/workItems/:workItemId/comments/:id': mockjs.mock(
    comment
  ),

  'POST /api/:version/projects/:projectId/features/:featureId/branchs': mockjs.mock(
    branch
  ),
  'DELETE /api/:version/projects/:projectId/features/:featureId/branchs/:id': mockjs.mock(
    branch
  ),
  'PUT /api/:version/projects/:projectId/features/:featureId/branchs/:id': mockjs.mock(
    branch
  ),
  'GET /api/:version/projects/:projectId/features/:featureId/branchs': mockjs.mock(
    {
      'list|5': [branch]
    }
  )['list'],
  'GET /api/:version/projects/:projectId/features/:featureId/branchs/:id': mockjs.mock(
    branch
  ),

  'PUT /api/:version/projects/:projectId/apps/:appId/repos': mockjs.mock(repo),

  'POST /api/:version/projects/:projectId/apps/:appId/git_branchs': mockjs.mock(
    gitBranch
  ),
  'DELETE /api/:version/projects/:projectId/apps/:appId/git_branchs/:id': mockjs.mock(
    gitBranch
  ),
  'PUT /api/:version/projects/:projectId/apps/:appId/git_branchs/:id': mockjs.mock(
    gitBranch
  ),
  'GET /api/:version/projects/:projectId/apps/:appId/git_branchs': mockjs.mock({
    'list|5': [gitBranch]
  })['list'],
  'GET /api/:version/projects/:projectId/apps/:appId/git_branchs/:id': mockjs.mock(
    gitBranch
  ),

  'POST /api/:version/projects/:projectId/iterations': mockjs.mock(iteration),
  'DELETE /api/:version/projects/:projectId/iterations/:id': mockjs.mock(
    iteration
  ),
  'PUT /api/:version/projects/:projectId/iterations/:id': mockjs.mock(
    iteration
  ),
  'GET /api/:version/projects/:projectId/iterations': mockjs.mock({
    'list|20': [iteration]
  })['list'],
  'GET /api/:version/projects/:projectId/iterations/:id': mockjs.mock(
    iteration
  ),

  'POST /api/:version/projects/:projectId/workItems': mockjs.mock(workItem),
  'DELETE /api/:version/projects/:projectId/workItems/:id': mockjs.mock(
    workItem
  ),
  'PUT /api/:version/projects/:projectId/workItems/:id': mockjs.mock(workItem),
  'GET /api/:version/projects/:projectId/workItems': mockjs.mock({
    'list|20': [workItem]
  })['list'],
  'GET /api/:version/projects/:projectId/workItems/:id': mockjs.mock(workItem),

  'POST /api/:version/projects/:projectId/features': mockjs.mock(feature),
  'DELETE /api/:version/projects/:projectId/features/:id': mockjs.mock(feature),
  'PUT /api/:version/projects/:projectId/features/:id': mockjs.mock(feature),
  'GET /api/:version/projects/:projectId/features': mockjs.mock({
    'list|5': [feature]
  })['list'],
  'GET /api/:version/projects/:projectId/features/:id': mockjs.mock(feature),

  'POST /api/:version/projects/:projectId/apps': mockjs.mock(app),
  'DELETE /api/:version/projects/:projectId/apps/:id': mockjs.mock(app),
  'PUT /api/:version/projects/:projectId/apps/:id': mockjs.mock(app),
  'GET /api/:version/projects/:projectId/apps': mockjs.mock({
    'list|5': [app]
  })['list'],
  'GET /api/:version/projects/:projectId/apps/:id': mockjs.mock(app),

  'POST /api/:version/projects/:projectId/labels': mockjs.mock(label),
  'DELETE /api/:version/projects/:projectId/labels/:id': mockjs.mock(label),
  'PUT /api/:version/projects/:projectId/labels/:id': mockjs.mock(label),
  'GET /api/:version/projects/:projectId/labels': mockjs.mock({
    'list|5': [label]
  })['list'],
  'GET /api/:version/projects/:projectId/labels/:id': mockjs.mock(label),

  'POST /api/:version/projects/:projectId/modules': mockjs.mock(_module),
  'DELETE /api/:version/projects/:projectId/modules/:id': mockjs.mock(_module),
  'PUT /api/:version/projects/:projectId/modules/:id': mockjs.mock(_module),
  'GET /api/:version/projects/:projectId/modules': mockjs.mock({
    'list|5': [_module]
  })['list'],
  'GET /api/:version/projects/:projectId/modules/:id': mockjs.mock(_module),

  'POST /api/:version/projects/:projectId/members': mockjs.mock(member),
  'DELETE /api/:version/projects/:projectId/members/:id': mockjs.mock(member),
  'PUT /api/:version/projects/:projectId/members/:id': mockjs.mock(member),
  'GET /api/:version/projects/:projectId/members': mockjs.mock({
    'list|5': [member]
  })['list'],
  'GET /api/:version/projects/:projectId/members/:id': mockjs.mock(member),

  'POST /api/:version/projects': mockjs.mock(project),
  'DELETE /api/:version/projects/:id': mockjs.mock(project),
  'PUT /api/:version/projects/:id': mockjs.mock(project),
  'GET /api/:version/projects/:id': mockjs.mock(project),
  'GET /api/:version/projects': mockjs.mock({
    'list|5': [project]
  })['list']
};

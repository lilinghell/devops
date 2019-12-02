const mockjs = require('mockjs');

const user = {
  id: '@id',
  name: '@name',
  username: '@name',
  email: '@email',
  avatar_url: mockjs.Random.image('100x100'),
  wechat: 'wechat',
  phone: '13013013013',
  description: '@cparagraph',
  source: 'local',
  is_valid: '@boolean',
  is_expired: '@boolean',
  is_active: '@boolean',
  created_by: 'System',
  is_first_login: '@boolean',
  is_superuser: true,
  is_org_admin: false,
  date_password_last_updated: '@date',
  date_expired: '@date',
  date_joined: '@date',
  authority: 'admin'
};

const log = {
  id: '@id',
  created_by: user,
  created_at: '@date',
  updated_at: '@date',
  user: user,
  'action|1': ['create', 'update', 'delete'],
  resource_type: 'string',
  resource_id: '@id',
  remote_addr: '@url',
  datetime: '@date',
  project_id: '@id',
  org: '@id'
};

module.exports = {
  'POST /api/:version/attachments': mockjs.mock({
    id: '@id'
  }),

  'GET /api/:version/logs': mockjs.mock({
    'list|20': [log]
  })['list']
};

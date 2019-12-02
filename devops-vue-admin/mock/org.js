const mockjs = require('mockjs');
const { wrap7A, wrapError } = require('./utils/utils');

const org = {
  id: '@id',
  name: '@name',
  logo: mockjs.Random.image('100x100'),
  created_by: '@id',
  created_date: '@date',
  description: '@cparagraph'
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

module.exports = {
  'POST /api/:version/admin/orgs/:orgId/members': mockjs.mock(member),
  'DELETE /api/:version/admin/orgs/:orgId/members/:id': mockjs.mock(member),
  'PUT /api/:version/admin/orgs/:orgId/members/:id': mockjs.mock(member),
  'GET /api/:version/admin/orgs/:orgId/members': mockjs.mock({
    'list|20': [member]
  })['list'],
  'GET /api/:version/admin/orgs/:orgId/members/:id': mockjs.mock(member),

  'POST /api/:version/admin/orgs': mockjs.mock(org),
  'DELETE /api/:version/admin/orgs/:id': mockjs.mock(org),
  'PUT /api/:version/admin/orgs/:id': mockjs.mock(org),
  'GET /api/:version/admin/orgs/:id': mockjs.mock(org),
  'GET /api/:version/admin/orgs': mockjs.mock({
    'list|20': [org]
  })['list'],
  'PUT /api/:version/org': mockjs.mock(org)
};

const mockjs = require('mockjs');

const team = {
  id: '@id',
  owner: {
    id: '@id',
    name: '@name',
    email: '@email'
  },
  created_at: '@date',
  updated_at: '@date',
  name: '@string',
  description: '@cparagraph',
  team: '@string',
  created_by: '@name',
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

module.exports = {
  'POST /api/:version/teams/:teamId/members': mockjs.mock(member),
  'DELETE /api/:version/teams/:teamId/members/:id': mockjs.mock(member),
  'PUT /api/:version/teams/:teamId/members/:id': mockjs.mock(member),
  'GET /api/:version/teams/:teamId/members': mockjs.mock({
    'list|5': [member]
  })['list'],
  'GET /api/:version/teams/:teamId/members/:id': mockjs.mock(member),

  'POST /api/:version/teams': mockjs.mock(team),
  'DELETE /api/:version/teams/:id': mockjs.mock(team),
  'PUT /api/:version/teams/:id': mockjs.mock(team),
  'GET /api/:version/teams/:id': mockjs.mock(team),
  'GET /api/:version/teams': mockjs.mock({
    'list|5': [team]
  })['list']
};

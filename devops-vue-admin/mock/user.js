const mockjs = require('mockjs');
const { wrap7A, wrapError } = require('./utils/utils');

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

const org = {
  id: '@id',
  name: '@name',
  logo: mockjs.Random.image('100x100'),
  created_by: '@id',
  created_date: '@date',
  description: '@cparagraph'
};

const currentUser = {
  user,
  org
};

const project = {
  id: '@id',
  owner: {
    id: '@id',
    name: '@name',
    email: '@email'
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
  owner: user,
  closed_by: '@id',
  project: '@id',
  module: '@id',
  feature: '@id',
  parent: '@id',
  iteration: '@id'
};

module.exports = {
  'GET /api/:version/user/profile': mockjs.mock(currentUser),
  'GET /api/:version/users': mockjs.mock({
    'list|20': [user]
  })['list'],
  'POST /api/:version/users': mockjs.mock(user),
  'DEconstE /api/:version/users/:id': mockjs.mock(user),
  'POST /api/:version/logout': mockjs.mock(user),
  'POST /api/:version/login': (req, res) => {
    const { password, username, type } = req.body;
    if (password === '888888' && username === 'admin') {
      res.send(
        wrap7A({
          type,
          ...currentUser,
          permission: {
            id: 'id',
            name_en: 'admin',
            name_cn: '企业管理员',
            permissions: ['/api/user/add']
          },
          token: 'jwt'
        })
      );
      return;
    }
    if (password === '123456' && username === 'user') {
      res.send(
        wrap7A({
          type,
          ...user,
          permission: {
            id: 'id',
            name_en: 'user',
            name_cn: '普通人员',
            permissions: ['/api/user/add']
          },
          token: 'jwt'
        })
      );
      return;
    }
    res.send(
      wrapError({
        type,
        msg: '账户或密码错误（admin/888888）'
      })
    );
  },

  'GET /api/:version/user/projects': mockjs.mock({
    'list|5': [project]
  })['list'],
  'GET /api/:version/user/workItems': mockjs.mock({
    'list|5': [workItem]
  })['list']
};

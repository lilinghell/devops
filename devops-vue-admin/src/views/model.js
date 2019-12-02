export function createOrgModel() {
  return {
    name: '',
    owner: {}
  };
}
export function createMemberModel() {
  return {
    id: '',
    user: createUserModel(),
    created_at: '',
    updated_at: '',
    source_id: '',
    source_type: '',
    type: '',
    access_level: '',
    notification_level: 0,
    org: '',
    created_by: ''
  };
}
export function createUserModel() {
  return {
    id: '',
    name: '',
    username: '',
    email: '',
    avatar_url: '',
    wechat: '',
    phone: '',
    description: '',
    source: '',
    is_valid: '',
    is_expired: '',
    is_active: '',
    created_by: '',
    is_first_login: '',
    is_superuser: '',
    is_org_admin: '',
    date_password_last_updated: '',
    date_expired: '',
    password: '',
    password2: '',
    type: ''
  };
}
export function createTeamModel() {
  return {
    id: '',
    owner: '',
    created_at: '',
    updated_at: '',
    name: '',
    description: '',
    org: '',
    created_by: '',
    parent: ''
  };
}

export const vars = {
  types: ['admin', 'user'],
  teamRoles: [{ label: '管理员', value: 50 }, { label: '成员', value: 10 }],
  userRoles: [
    { label: '超级管理员', value: 'superuser' },
    { label: '企业管理员', value: 'admin' },
    { label: '企业成员', value: 'user' }
  ],
  logActions: [
    { label: '新增', value: 'create' },
    { label: '修改', value: 'update' },
    { label: '删除', value: 'delete' }
  ]
};

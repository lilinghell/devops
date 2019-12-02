export function createProjectModel() {
  return {
    id: '',
    owner: '',
    team: '',
    created_at: '',
    updated_at: '',
    name: '',
    description: '',
    logo: '',
    visit_level: 10,
    org: '',
    created_by: '',
    parent: '',
    member: []
  };
}
export function createTestGroupModel() {
  return {
    id: '',
    name: '',
    parent: '',
    description: '',
  };
}
export function createTestCaseModel() {
  return {
    id: '',
    name: '',
    group: '',
    user: '',
    status: '',
    type: '',
    level: '',
    feature: [],
    prerequisites: '',
    desc: '',
    expected: '',
  };
}
export function createTestPlanModel() {
  return {
    id: '',
    name: '',
    user: '',
    start_date: '',
    end_date: '',
    description: '',
    case: [],
  };
}
export function createAutoPlanModel() {
  return {
    id: '',
    name: '',
    user: '',
    env: '',
    time: '',
    week: '',
    description: '',
    case: [],
  };
}
export function createTestModel() {
  return {
    id: '',
    case: '',
    env: '',
    interface: '',
    prerequisites: '',
    body: '',
    expected: '',
    response: '',
  };
}
export function createModuleModel() {
  return {
    id: '',
    created_at: '',
    updated_at: '',
    name: '',
    description: '',
    org: '',
    created_by: '',
    project: ''
  };
}

export function createLabelModel() {
  return {
    id: '',
    created_at: '',
    updated_at: '',
    title: '',
    color: vars.label_colors[0].value,
    description: '',
    type: '',
    org: '',
    created_by: '',
    team: '',
    project: ''
  };
}

export function createRepoModel() {
  return {
    app: '',
    created_at: '',
    updated_at: '',
    type: '',
    web_url: '',
    scm_url: '',
    branch: '',
    auth_type: '',
    auth_token: '',
    auth_username: '',
    auth_pwd: '',
    org: '',
    created_by: '',
    project: ''
  };
}

export function createEnvModel() {
  return {
    id: '',
    name: '',
    domain: '',
    header: '',
    cookie: '',
  };
}

export function createAppModel() {
  return {
    id: '',
    repo: createRepoModel(),
    created_at: '',
    updated_at: '',
    name: '',
    description: '',
    type: '',
    status: '',
    org: '',
    created_by: '',
    project: '',
    owner: ''
  };
}

export function createFeatureModel() {
  return {
    id: '',
    labels: [],
    attachments: [],
    created_at: '',
    updated_at: '',
    title: '',
    description: '',
    description_html: '',
    start_date: '',
    end_date: '',
    important: '',
    priority: '',
    estimate_time: '',
    progress: 0,
    status: '0',
    closed_at: '',
    org: '',
    created_by: '',
    owner: '',
    closed_by: '',
    apps: [],
    project: '',
    requirement: '',
    iteration: '',
    module: ''
  };
}

export function createWorkItemModel() {
  return {
    id: '',
    assignee_users: [],
    labels: [],
    attachments: [],
    created_at: '',
    updated_at: '',
    title: '',
    description: '',
    type: '',
    description_html: '',
    start_date: '',
    end_date: '',
    important: 2,
    priority: 2,
    estimate_time: '',
    progress: '',
    status: '',
    closed_at: '',
    org: '',
    created_by: '',
    owner: '',
    closed_by: '',
    project: '',
    module: '',
    feature: '',
    parent: '',
    iteration: ''
  };
}

export function createIterationModel() {
  return {
    id: '',
    feature_count: '',
    workItem_count: '',
    created_at: '',
    updated_at: '',
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    status: '',
    org: '',
    created_by: '',
    owner: '',
    project: ''
  };
}

export function createBranchModel() {
  return {
    id: '',
    feature: '',
    app: '',
    created_at: '',
    updated_at: '',
    branch_name: '',
    ref: '',
    status: '',
    org: '',
    created_by: '',
    addBranchType: '1'
  };
}

export function createDesignGroupModel() {
  return {
    id: '',
    name: '',
    parent: null,
    application: null,
    description: '',
    type: ''
  };
}

export function createDesignInterfaceModel() {
  return {
    id: '',
    name: '',
    url: '',
    method: '',
    description: '',
    version: '',
    status: '',
    open: true,
    application: null,
    group: null,
    project: null,
    info: '',
    yaml_path: ''
  };
}

export function createTestEnvMode() {
  return {
    id: '',
    name: '',
    domain: '',
    header: '',
    cookie: '',
    org: ''
  }
}

export const vars = {
  stages: [
    { code: 0, label: '开发', value: 'develop' },
    { code: 1, label: 'sit测试', value: 'sit' },
    { code: 2, label: 'uat测试', value: 'uat' },
    { code: 3, label: 'rel测试', value: 'rel' },
    {
      code: 4,
      label: '投产',
      value: 'production',
      type: 'success',
      title: '任务已投产',
      description: '任务已投产'
    },
    {
      code: 5,
      label: '取消',
      value: 'cancel',
      type: 'error',
      title: '任务已取消',
      description: '任务已取消'
    },
    {
      code: 6,
      label: '归档',
      value: 'file',
      type: 'success',
      title: '任务已归档',
      description: '任务已归档'
    }
  ],
  networks: [
    { label: '业务', value: '业务' },
    { label: '网银dmz', value: '网银dmz' },
    { label: '其他', value: '其他' }
  ],

  visit_levels: [{ label: '公开', value: 10 }, { label: '私有', value: 90 }],
  label_colors: [
    { label: 'primary', value: '#027BE3' },
    { label: 'secondary', value: '#26A69A' },
    { label: 'accent', value: '#9C27B0' },
    { label: 'positive', value: '#21BA45' },
    { label: 'negative', value: '#C10015' },
    { label: 'warning', value: '#F2C037' }
  ],
  appTypes: [
    { label: 'mircoservice', value: 'mircoservice' },
    { label: 'web', value: 'web' },
    { label: 'batch', value: 'batch' },
    { label: 'j2se', value: 'j2se' }
  ],
  priorities: [
    { label: '低', value: 1 },
    { label: '中', value: 2 },
    { label: '高', value: 3 }
  ],
  important: [
    { label: '低', value: 1 },
    { label: '中', value: 2 },
    { label: '高', value: 3 }
  ],
  requirementTypes: [
    { label: '低', value: 1 },
    { label: '中', value: 2 },
    { label: '高', value: 3 }
  ],
  scmTypes: [{ label: 'git', value: 'git' }, { label: 'svn', value: 'svn' }],
  workItemTypes: [
    { label: '待分配', value: '1' },
    { label: '待处理', value: '2' },
    { label: '处理中', value: '3' },
    { label: '已完成', value: '4' }
  ],
  caseStatus: [
    { label: '待评审', value: "0" },
    { label: '待测试', value: "1" },
    { label: '自测通过', value: "2" },
    { label: '已通过', value: "3" },
  ],
  caseTypes: [
    { label: '功能测试', value: "0" },
    { label: '性能测试', value: "1" },
  ],
  caseLevels: [
    {label:'P0',value: 'P0'},
    {label:'P1',value: 'P1'},
    {label:'P2',value: 'P2'},
    {label:'P3',value: 'P3'},
  ],
  access_levels: [
    { label: '项目管理员', value: 50 },
    { label: '项目经理', value: 40 },
    { label: '项目组长', value: 30 },
    { label: '项目开发', value: 20 },
    { label: '项目访客', value: 10 }
  ],
  featureStatus: [
    { label: '待处理', value: '0' },
    { label: '进行中', value: '1' },
    { label: '测试中', value: '2' },
    { label: '待发布', value: '3' },
    { label: '已完成', value: '4' },
    { label: '已取消', value: '5' },
    { label: '已归档', value: '6' }
  ],
  authTypes: [
    { label: 'pwd', value: 'pwd' },
    { label: 'token', value: 'token' }
  ],
  addBranchTypes: [
    { label: '新建分支', value: '1' },
    { label: '关联现有分支', value: '2' }
  ],
  interfaceStatus: [
    { label: '开发中', value: '1' },
    { label: '开发完成', value: '0' }
  ],
  methodTypes: [
    { label: 'GET', value: 'GET' },
    { label: 'POST', value: 'POST' },
    { label: 'PUT', value: 'PUT' },
    { label: 'PATCH', value: 'PATCH' },
    { label: 'DELETE', value: 'DELETE' }
  ],
  testEnvURL: [
    'http://', 'https://'
  ],
  weekdays: [
    { label: '周一', value: '1' },
    { label: '周二', value: '2' },
    { label: '周三', value: '3' },
    { label: '周四', value: '4' },
    { label: '周五', value: '5' },
    { label: '周六', value: '6' },
    { label: '周日', value: '7' }
  ]
};

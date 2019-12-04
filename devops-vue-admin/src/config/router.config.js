import BasicLayout from '@/layouts/BasicLayout';
import LoginLayout from '@/layouts/LoginLayout';
import BlankLayout from '@/layouts/BlankLayout';
// app
import Login from '@/views/app/Login/Login';
import Workplace from '@/views/app/Dashboard/Workplace';
import Exception404 from '@/views/app/Exception/404';
//project
import ProjectIndex from '@/views/project/Setting/Index';
import ProjectProfile from '@/views/project/Setting/Profile';
import ProjectMember from '@/views/project/Setting/Member';
import ProjectModule from '@/views/project/Setting/Module';
import ProjectLabel from '@/views/project/Setting/Label';
import AppList from '@/views/project/App/List';
import AppProfile from '@/views/project/App/Profile';
import FeatureList from '@/views/project/Feature/List';
import FeatureProfile from '@/views/project/Feature/Profile';
import WorkItemList from '@/views/project/WorkItem/List';
import IterationList from '@/views/project/Iteration/List';
// admin
import UserList from '@/views/admin/User/List';
import UserTeam from '@/views/admin/User/Team';
import SettingOrg from '@/views/admin/Setting/Org';
// manager
import ManagerOrgList from '@/views/manager/Org/List';
import ManagerOrgProfile from '@/views/manager/Org/Profile';
//designs
import DesignsIndex from '@/views/project/Designs/Index';
import GroupList from '@/views/project/Designs/GroupList';
// test
import TestIndex from '@/views/project/Test/Index';
import EnvProfile from '@/views/project/Test/EnvConfig';
import CaseProfile from '@/views/project/Test/CaseConfig';
import PlanList from '@/views/project/Test/PlanList';
//Pipelines
import PipelinesIndex from '@/views/project/Pipelines/Index';
import PipelinesList from '@/views/project/Pipelines/List';

export default [
  // login
  {
    path: '/login',
    component: LoginLayout,
    name: 'login',
    children: [
      {
        path: '/',
        component: Login
      }
    ]
  },
  // admin
  {
    path: '/admin',
    component: BasicLayout,
    name: 'admin',
    meta: {
      authority: ['admin'],
      noMatch: '/login'
    },
    children: [
      {
        path: 'setting',
        meta: {
          name: '通用',
          icon: 'settings'
        },
        children: [
          {
            path: 'org',
            meta: {
              name: '企业信息'
            },
            component: SettingOrg
          }
        ]
      },
      {
        path: 'user',
        meta: {
          name: '用户',
          icon: 'supervisor_account'
        },
        children: [
          {
            path: 'list',
            meta: {
              name: '用户管理'
            },
            component: UserList
          },
          {
            path: 'team',
            meta: {
              name: '团队管理'
            },
            component: UserTeam
          }
        ]
      },
      {
        path: '**',
        component: Exception404
      }
    ]
  },
  // manager
  {
    path: '/manager',
    component: BlankLayout,
    name: 'manager',
    meta: {
      authority: ['superuser'],
      noMatch: '/login'
    },
    children: [
      {
        path: 'org',
        meta: {
          name: '企业管理'
        },
        component: ManagerOrgList
      },
      {
        path: 'org/:id',
        meta: {
          name: '企业详情'
        },
        component: ManagerOrgProfile
      },
      {
        path: '**',
        component: Exception404
      }
    ]
  },
  // app
  {
    path: '/',
    component: BasicLayout,
    name: 'app',
    meta: {
      authority: ['admin', 'user'],
      noMatch: '/login'
    },
    children: [
      {
        path: 'dashboard',
        meta: {
          name: 'Dashboard',
          icon: 'dashboard',
          hideInMenu: true
        },
        children: [
          {
            path: 'workplace',
            meta: {
              name: '工作台',
              siderHidden: true,
              mini: true
            },
            component: Workplace
          }
        ]
      },
      {
        path: 'project/:projectId/home',
        meta: {
          name: 'Home',
          icon: 'home',
          mini: true
        }
      },
      {
        path: 'project/:projectId/app',
        meta: {
          name: '应用',
          icon: 'mdi-set mdi-application',
          mini: true
        },
        component: AppList
      },
      {
        path: 'project/:projectId/app/:appId',
        meta: {
          name: '应用详情',
          mini: true,
          hideInMenu: true
        },
        component: AppProfile
      },
      {
        path: 'project/:projectId/feature',
        meta: {
          name: '需求',
          icon: 'mdi-set mdi-card-bulleted-outline',
          mini: true
        },
        component: FeatureList
      },
      {
        path: 'project/:projectId/feature/:featureId',
        meta: {
          name: '需求详情',
          mini: true,
          hideInMenu: true
        },
        component: FeatureProfile
      },
      {
        path: 'project/:projectId/workItem',
        meta: {
          name: '任务',
          icon: 'developer_board',
          footerHidden: true,
          mini: true
        },
        component: WorkItemList
      },
      {
        path: 'project/:projectId/iteration',
        meta: {
          name: '迭代',
          icon: 'mdi-set mdi-sync',
          mini: true
        },
        component: IterationList
      },
      {
        path: 'project/:projectId/designs',
        meta: {
          name: '设计',
          icon: 'font_download',
          behave: 'link'
        },
        component: DesignsIndex,
        children: [
          {
            path: 'group',
            meta: {
              name: '服务接口',
              footerHidden: true,
              mini: true
            },
            component: GroupList
          },
          /* {
            path: 'esb_interface',
            meta: {
              name: 'ESB接口',
              footerHidden: true,
              mini: true
            }
          }, */
          {
            path: 'dictionary',
            meta: {
              name: '字典',
              footerHidden: true,
              mini: true
            }
          }
        ]
      },
      {
        path: 'project/:projectId/Pipelines',
        meta: {
          name: 'Pipelines',
          icon: 'style',
          behave: 'link'
        },
        component: PipelinesIndex,
        children: [
          {
            path: 'Pipelines',
            meta: {
              name: 'Pipelines',
              footerHidden: true,
              mini: true
            },
            component: PipelinesList
          },
          {
            path: '环境设置',
            meta: {
              name: '环境设置',
              footerHidden: true,
              mini: true
            }
          },
          {
            path: '发布',
            meta: {
              name: '发布',
              footerHidden: true,
              mini: true
            }
          }
        ]
      },
      {
        path: 'test/:projectId',
        meta: {
          name: '测试',
          icon: 'my_location',
          behave: 'link' // link,expansion
        },
        component: TestIndex,
        children: [
          {
            path: 'envProfile',
            meta: {
              name: '环境配置',
              footerHidden: true,
              mini: true
            },
            component: EnvProfile
          },
          {
            path: 'caseProfile',
            meta: {
              name: '用例库',
              footerHidden: true,
              mini: true
            },
            component: CaseProfile
          },
          {
            path: 'planList',
            meta: {
              name: '测试计划',
              footerHidden: true,
              mini: true
            },
            component: PlanList
          },
        ]
      },
      {
        path: 'project/:projectId/setting',
        meta: {
          name: '设置',
          icon: 'settings',
          behave: 'link' // link,expansion
        },
        component: ProjectIndex,
        children: [
          {
            path: 'profile',
            meta: {
              name: '基本信息',
              footerHidden: true,
              mini: true
            },
            component: ProjectProfile
          },
          {
            path: 'member',
            meta: {
              name: '成员',
              footerHidden: true,
              mini: true
            },
            component: ProjectMember
          },
          {
            path: 'module',
            meta: {
              name: '模块',
              footerHidden: true,
              mini: true
            },
            component: ProjectModule
          },
          {
            path: 'label',
            meta: {
              name: '标签',
              footerHidden: true,
              mini: true
            },
            component: ProjectLabel
          }
        ]
      },
      {
        path: 'project/:projectId/**',
        component: Exception404
      }
    ]
  }
];

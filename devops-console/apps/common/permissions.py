# -*- coding: utf-8 -*-
#

from rest_framework import permissions
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.http.response import HttpResponseForbidden
from django.conf import settings

from teams.models import Member
from .access import Access
from features.models import Feature
from workitems.models import WorkItem
from applications.models import Application
from orgs.models import ProductRole
from orgs.utils import current_org

"""

    整体管理权限
    超级管理员 管理企业
        企业管理员 - 管理用户 团队  产品
                产品管理员 - 管理产品功能
                    项目ADMIN  新建项目下所有权限
                    项目经理    新建应用 + 项目组长
                    项目组长    新建需求和分支、处理自己新建的需求和负责的需求、新建任务、处理自己建立的任务和负责的任务 + 项目开发
                    项目开发    只能处理被分配任务，其他读
                    项目参与者  所有只读
"""


class ProjectIdMixin:

    @staticmethod
    def check_project_id_get_access_level(request, view):
        assert view.kwargs['project_id'] is not None, "request path must have project_id"
        project_id = view.kwargs['project_id']
        member = Member.objects.get(source_id=project_id, source_type=Member.SOURCE_PROJECT, user=request.user)
        assert member is not None, "request user is a member of project"
        return project_id, member.access_level

    @staticmethod
    def check_project_id_and_pk(view):
        assert view.kwargs['project_id'] is not None, "request path must have project_id"
        project_id = view.kwargs['project_id']
        assert view.kwargs['pk'] is not None, "request path must have pk"
        pk = view.kwargs['pk']
        return project_id, pk

    @staticmethod
    def check_pk_get_access_level(request, view):
        view.kwargs['pk'] is not None, "request path must have project_id"
        pk = view.kwargs['pk']
        member = Member.objects.get(source_id=pk, source_type=Member.SOURCE_PROJECT, user=request.user)
        assert member is not None, "request user is a member of project"
        return pk, member.access_level


class IsValidUser(permissions.IsAuthenticated, permissions.BasePermission):
    """Allows access to valid user, is active and not expired"""

    def has_permission(self, request, view):
        return super(IsValidUser, self).has_permission(request, view) \
               and request.user.is_valid


class IsValidUserAndReadonly(IsValidUser):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.method in permissions.SAFE_METHODS)


class IsProjectGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_GUEST


class IsProjectDev(permissions.BasePermission):
    """
    项目开发人员
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_DEV


class IsWorkItemAssigneeOrCreater(permissions.BasePermission):
    """

    任务创建者或负责人
    """

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            project_id, pk = ProjectIdMixin.check_project_id_and_pk(view)
            instance = WorkItem.objects.get(project_id=project_id, id=pk)
            assert instance is not None, "request workitem is not exsit"
            return instance.created_by == request.user.id or instance.owner_id == request.user.id


class IsProjectLeader(permissions.BasePermission):
    """

    项目leader
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_LEADER


class IsFeatureOwnerOrCreater(permissions.BasePermission):
    """

    需求创建者或负责人
    """

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            project_id, pk = ProjectIdMixin.check_project_id_and_pk(view)
            instance = Feature.objects.get(project_id=project_id, id=pk)
            assert instance is not None, "request feature is not exsit"
            return instance.created_by == request.user.id or instance.owner_id == request.user.id


class IsProjectManager(permissions.BasePermission):
    """

    项目经理
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_MANAGE


class IsApplicationOwnerOrCreater(permissions.BasePermission):
    """

    需求创建者或负责人
    """

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            project_id, pk = ProjectIdMixin.check_project_id_and_pk(view)
            instance = Application.objects.get(project_id=project_id, id=pk)
            assert instance is not None, "request application is not exsit"
            return instance.created_by == request.user.id or instance.owner_id == request.user.id


class IsProjectAdmin(permissions.BasePermission):
    """

    项目管理员
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_ADMIN


class IsProjectAdmin(permissions.BasePermission):
    """

    项目管理员
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_project_id_get_access_level(request, view)
        return access_level >= Access.PROJECT_ADMIN


class IsProjectViewAdmin(permissions.BasePermission):
    """

    项目管理员
    """

    def has_permission(self, request, view):
        project_id, access_level = ProjectIdMixin.check_pk_get_access_level(request, view)
        return access_level >= Access.PROJECT_ADMIN


class ProductProjectAdmin(permissions.BasePermission):
    """

    产品管理---项目ADMIN，可以新建、删除自己建立项目
    """

    def has_permission(self, request, view):
        instances = ProductRole.objects.filter(user_id=request.user.id, product=ProductRole.PROJECT)
        return len(instances) != 0 and instances[0].role == ProductRole.ADMIN


class IsAppUser(IsValidUser):
    """Allows access only to app user """

    def has_permission(self, request, view):
        return super(IsAppUser, self).has_permission(request, view) \
               and request.user.is_app


class IsSuperUser(IsValidUser):
    def has_permission(self, request, view):
        return super(IsSuperUser, self).has_permission(request, view) \
               and request.user.is_superuser


class IsSuperUserOrAppUser(IsSuperUser):
    def has_permission(self, request, view):
        return super(IsSuperUserOrAppUser, self).has_permission(request, view) \
               and (request.user.is_superuser or request.user.is_app)


class IsOrgAdmin(IsValidUser):
    """Allows access only to superuser"""

    def has_permission(self, request, view):
        return super(IsOrgAdmin, self).has_permission(request, view) \
               and current_org.can_admin_by(request.user)


class IsOrgAdminOrAppUser(IsValidUser):
    """Allows access between superuser and app user"""

    def has_permission(self, request, view):
        return super(IsOrgAdminOrAppUser, self).has_permission(request, view) \
               and (current_org.can_admin_by(request.user) or request.user.is_app)


class IsOrgAdminOrAppUserOrUserReadonly(IsOrgAdminOrAppUser):
    def has_permission(self, request, view):
        if IsValidUser.has_permission(self, request, view) \
                and request.method in permissions.SAFE_METHODS:
            return True
        else:
            return IsOrgAdminOrAppUser.has_permission(self, request, view)


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    """

    修改当前用户
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsReadyOnlyRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsPostRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "POST"


class IsPutRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "PUT"


class IsPatchRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "PATCH"


class IsDeleteRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "DELETE"


class AdminUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not current_org.can_admin_by(self.request.user):
            self.raise_exception = True
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if not current_org:
            return redirect('orgs:switch-a-org')

        if not current_org.can_admin_by(request.user):
            if request.user.is_org_admin:
                return redirect('orgs:switch-a-org')
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class WithBootstrapToken(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        if not authorization:
            return False
        request_bootstrap_token = authorization.split()[-1]
        return settings.BOOTSTRAP_TOKEN == request_bootstrap_token

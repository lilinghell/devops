from rest_condition import Or
from rest_framework import viewsets
from rest_framework.response import Response

from common.checkmsg import CheckMsg
from common.exception import DevException
from common.permissions import IsOrgAdmin, IsValidUserAndReadonly, IsProjectManager
from common.utils import git
from devops.swagger import CustomDjangoFilterBackend
from projects.mixins import ProjectViewSetMixin
from .models import Application, Repository, AppSpec
from .serializers import ApplicationSerializer, RepositorySerializer, AppSpecSerializer


class ApplicationViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """

    应用的增删该查信息
    retrieve:
    描述:应用基本信息详情
    权限:普通成员

    list:
    描述:获取应用列表
    权限:普通成员

    create:
    描述:新建工作组
    权限:项目负责人

    delete:
    描述:删除应用，删除会把应用数据都删除
    权限:项目负责人

    update:
    描述:更新应用信息
    权限:项目负责人

    """
    queryset = Application.objects.select_related("repo")
    serializer_class = ApplicationSerializer
    permission_classes = [Or(IsValidUserAndReadonly, IsProjectManager, )]


class RepositoryAPIView(ProjectViewSetMixin, viewsets.generics.UpdateAPIView):
    """

    SCM修改信息管理仓库信息
    update:
    描述:更新应用仓库信息
    权限:项目负责人
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [IsOrgAdmin, ]

    def dispatch(self, request, *args, **kwargs):
        self.application_id = kwargs.get('application_id')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return Repository.objects.get(application_id=self.application_id)


class AppSpecAPIView(viewsets.generics.CreateAPIView):
    queryset = AppSpec.objects.all()
    serializer_class = AppSpecSerializer
    permission_classes = [IsOrgAdmin, ]

    def dispatch(self, request, *args, **kwargs):
        self.application_id = kwargs.get('application_id')
        return super().dispatch(request, *args, **kwargs)


class BranchAPIView(viewsets.generics.RetrieveAPIView):
    """

    获取应用分支信息
    """
    permission_classes = [Or(IsValidUserAndReadonly)]

    def get(self, request, *args, **kwargs):
        app_id = kwargs.get('application_id')
        repository = Repository.objects.get(application_id=app_id)
        branches = []
        if repository.scm_url != '':
            try:
                gl = git(repository.scm_url, repository.auth_token)
                project = gl[0].projects.get(gl[1])
                branches_list = project.branches.list()
                for branch in branches_list:
                    b = branch._attrs
                    b["web_url"] = gl[2] + "/" + gl[1] + "/tree/" + b["name"]
                    branches.append(b)
            except:
                raise DevException(CheckMsg.VALIDATION_SCM_URL_ERROR)
        return Response(branches)


class CommitAPIView(viewsets.generics.ListAPIView):
    """

    获取git提交记录
    """
    permission_classes = [Or(IsValidUserAndReadonly)]
    filter_backends = (CustomDjangoFilterBackend,)
    filter_fields = ('branchName',)

    @staticmethod
    def get_gitlab_commits(repository, branch_name):
        re_commits = []
        if repository.scm_url != '':
            try:
                gl = git(repository.scm_url, repository.auth_token)
                project = gl[0].projects.get(gl[1])
                if branch_name is not None:
                    commits = project.commits.list(ref_name=branch_name)
                else:
                    commits = project.commits.list()
                for commit in commits:
                    re_commits.append(commit._attrs)
            except:
                raise DevException(CheckMsg.VALIDATION_SCM_URL_ERROR)
        return re_commits

    def list(self, request, *args, **kwargs):
        app_id = kwargs.get('application_id')
        repository = Repository.objects.get(application_id=app_id)
        re_data = self.get_gitlab_commits(repository, request.query_params.get("branchName"))
        return Response(re_data)

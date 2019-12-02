from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_condition import And, Or, Not

from teams.models import Member
from teams.serializers import MemberReadSerializer, MemberSerializer, MemberUpdateSerializer
from django.db.models import Subquery
from .serializers import ProjectSerializer, ProjectOwnerSerializer, ProjectLabelSerializer, ProjectReadSerializer, \
    ProjectModuleSerializer
from .models import Project, Module, Label
from .mixins import ProjectViewSetMixin, ProjectMemberViewSetMixin
from common import permissions


class ProjectViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    描述:单个项目详情
    权限:项目管理员

    list:
    描述:获取项目列表
    权限:项目管理员

    create:
    描述:新建项目
    权限:项目管理员

    delete:
    描述:删除项目，删除会把关联数据都删除
    权限:项目管理员
    """

    filter_fields = ('name',)
    search_fields = ('name',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.select_related("owner", "team")
    permission_classes = [Or(permissions.IsValidUserAndReadonly,
                             permissions.ProductProjectAdmin,
                             permissions.IsOrgAdmin,
                             And(Not(permissions.IsPostRequest), permissions.IsProjectViewAdmin)), ]

    # parser_classes = (FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProjectReadSerializer
        else:
            return super().get_serializer_class()


class ProjectMemberViewSet(ProjectMemberViewSetMixin, viewsets.ModelViewSet):
    """
    retrieve:
    描述:获取项目成员信息
    权限:项目管理员/项目经理

    list:
    描述:获取项目成员列表
    权限:项目管理员/项目经理

    create:
    描述:添加项目成员
    权限:项目管理员/项目经理

    delete:
    描述:删除项目成员
    权限:项目管理员/项目经理
    """
    serializer_class = MemberSerializer
    queryset = Member.objects.select_related("user")
    permission_classes = [
        Or(permissions.IsValidUserAndReadonly, permissions.ProductProjectAdmin, permissions.IsProjectAdmin), ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return MemberReadSerializer
        elif self.action in ('update', 'partial_update'):
            return MemberUpdateSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Member.objects.none()
        source_id = self.kwargs.get('project_id', '')
        source_type = Member.SOURCE_PROJECT
        self.queryset = super().get_queryset()
        self.queryset = self.queryset.filter(source_id=source_id, source_type=source_type)
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data["source_id"] = self.source_id
        serializer.validated_data["source_type"] = Member.SOURCE_PROJECT
        return super().perform_create(serializer)


class ProjectOwnerAPIView(viewsets.generics.UpdateAPIView):
    """

    put:
    描述:修改项目负责人，一个项目只能有一个项目负责人
    权限:组织管理员
    """
    serializer_class = ProjectOwnerSerializer
    queryset = Project.objects.all()


class ProjectListAPIView(viewsets.generics.ListAPIView):
    """

    get:
    描述:获取用户所有的项目列表
    权限:登陆用户
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.select_related("owner")

    def get_queryset(self):
        user = self.request.user
        members = Member.objects.filter(user=user, source_type=Member.SOURCE_PROJECT)
        self.queryset = super().get_queryset()
        owner_projects = self.queryset.filter(id__in=Subquery(members.values('source_id')))
        public_projects = self.queryset.filter(visit_level=Project.VISIT_LEVEL_PUBLIC)
        projects = set(owner_projects).union(public_projects)
        return projects


class LabelFilter(FilterSet):
    class Meta:
        model = Label
        fields = ['title', 'type']


class ProjectLabelViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """
    retrieve:
    描述:单个label详情
    权限:组织管理员

    list:
    描述:获取labels列表
    权限:组织管理员

    create:
    描述:新建label
    权限:组织管理员

    delete:
    描述:删除label
    权限:组织管理员
    """
    serializer_class = ProjectLabelSerializer
    queryset = Label.objects.all()
    permission_classes = [Or(permissions.IsValidUserAndReadonly, permissions.IsProjectManager), ]
    filter_class = LabelFilter
    filter_fields = ("type", "title")


class ProjectModuleViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """
    retrieve:
    描述:单个模块
    权限:项目管理员/项目经理

    list:
    描述:获取模块列表
    权限:项目管理员/项目经理

    create:
    描述:新建模块
    权限:项目管理员/项目经理

    delete:
    描述:删除模块
    权限:项目管理员/项目经理
    """
    serializer_class = ProjectModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [Or(permissions.IsValidUserAndReadonly, permissions.IsProjectManager), ]

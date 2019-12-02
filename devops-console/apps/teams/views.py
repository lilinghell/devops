from django.db.models import Subquery
from rest_condition import Or
from rest_framework import viewsets

from common.permissions import IsOrgAdmin, IsValidUserAndReadonly
from orgs.utils import current_org
from teams.mixins import TeamMemberModelViewSetMixin
from .models import Team, Member
from .serializers import TeamSerializer, MemberSerializer, MemberReadSerializer, \
    MemberUpdateSerializer, TeamOwnerSerializer, TeamQuerySerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    描述:单个工作组详情
    权限:组织管理员

    list:
    描述:获取工作组列表
    权限:组织管理员

    create:
    描述:新建工作组
    权限:组织管理员

    delete:
    描述:删除工作组，删除会把关联数据都删除
    权限:组织管理员
    """
    filter_fields = ('parent', 'name')
    search_fields = ('name',)
    serializer_class = TeamSerializer
    queryset = Team.objects.select_related("owner")
    permission_classes = [Or(IsValidUserAndReadonly, IsOrgAdmin, )]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TeamQuerySerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        if current_org:
            self.queryset = self.queryset.filter(org_id=current_org.id)
            return self.queryset
        return None


class TeamMemberViewSet(TeamMemberModelViewSetMixin, viewsets.ModelViewSet):
    """
    retrieve:
    描述:获取单个工作组成员信息
    权限:工作组负责人

    list:
    描述:获取工作组成员列表
    权限:工作组负责人

    create:
    描述:添加工作组成员
    权限:工作组负责人

    delete:
    描述:删除工作组成员
    权限:工作组负责人
    """
    serializer_class = MemberSerializer
    queryset = Member.objects.select_related('user')
    permission_classes = [Or(IsValidUserAndReadonly, IsOrgAdmin, )]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return MemberReadSerializer
        elif self.action in ('update', 'partial_update'):
            return MemberUpdateSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        source_id = self.source_id
        source_type = Member.SOURCE_TEAM
        self.queryset = super().get_queryset()
        self.queryset = self.queryset.filter(source_id=source_id, source_type=source_type)
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data["source_id"] = self.source_id
        serializer.validated_data["source_type"] = Member.SOURCE_TEAM
        return super().perform_create(serializer)


class TeamOwnerAPIView(viewsets.generics.UpdateAPIView):
    """

    put:
    描述:修改小组负责人，一个team只能有一个小组负责人
    权限:组织管理员
    """
    serializer_class = TeamOwnerSerializer
    queryset = Team.objects.all()


class TeamListAPIView(viewsets.generics.ListAPIView):
    """

    get:
    描述:获取用户所有的team列表
    权限:登陆用户
    """
    serializer_class = TeamQuerySerializer
    queryset = Team.objects.select_related("owner")

    def get_queryset(self):
        user = self.request.user
        members = Member.objects.filter(user=user, source_type=Member.SOURCE_TEAM)
        self.queryset = super().get_queryset()
        self.queryset = self.queryset.filter(id__in=Subquery(members.values('source_id')))
        return self.queryset


class TeamChildListView(viewsets.generics.ListAPIView):
    """

    get:
    描述:获取指定团队的子团队
    权限:登陆用户
    """
    serializer_class = TeamQuerySerializer
    queryset = Team.objects.select_related("owner")

    def get_queryset(self):
        team = Team.objects.get(id=self.kwargs.get('pk'))
        self.queryset = team.child_teams
        return self.queryset

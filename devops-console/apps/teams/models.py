from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from common.mixin import BaseModelMixin

__all__ = ["Team", "Member"]


class Team(BaseModelMixin):
    name = models.CharField(max_length=128, null=True, unique=True, verbose_name=_("TeamName"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述信息"))
    parent = models.ForeignKey('Team', null=True, blank=True, related_name="child_teams", on_delete=models.SET_NULL,
                               verbose_name=_("上级team"))
    owner = models.ForeignKey(User, related_name="owner_teams", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("小组负责人"))

    class Meta:
        ordering = ["-created_at"]
        db_table = "teams"


class Member(BaseModelMixin):
    """

    成员，包含团队成员、项目成员、应用成员等等
    """
    TEAM_MEMBER = "TeamMember"
    TEAM_ADMIN = "TeamAdmin"
    APP_MEMBER = "AppMember"
    PROJECT_MEMBER = "ProjectMember"
    TYPE_CHOICES = ((TEAM_MEMBER, "TeamMember"), (APP_MEMBER, "AppMember"), (PROJECT_MEMBER, "ProjectMember"))
    SOURCE_APP = "application"
    SOURCE_TEAM = "team"
    SOURCE_PROJECT = "project"
    SOURCE_CHOICES = ((SOURCE_TEAM, "team"), (SOURCE_APP, "application"), (SOURCE_PROJECT, "project"))

    user = models.ForeignKey(User, related_name="members", on_delete=models.CASCADE)
    source_id = models.IntegerField(verbose_name=_("来源ID"))
    source_type = models.CharField(choices=SOURCE_CHOICES, max_length=32, null=False,
                                   verbose_name=_("member type ，比如team、project、app等"))
    type = models.CharField(choices=TYPE_CHOICES, max_length=32, verbose_name=_("成员类型"))
    access_level = models.IntegerField(verbose_name=_("访问权限"), default=10)
    notification_level = models.IntegerField(null=True, verbose_name=_("notification_level"))

    class Meta:
        ordering = ["-created_at", "access_level"]
        unique_together = [('source_id', 'source_type', 'user')]
        db_table = "members"

from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from teams.models import Team
from common.mixin import BaseModelMixin

__all__ = ["Project", "Module", "Label"]


class Project(BaseModelMixin):
    """

    项目
    """
    VISIT_LEVEL_PUBLIC = 10
    VISIT_LEVEL_PRIVATE = 90
    VISIT_CHOICES = ((VISIT_LEVEL_PUBLIC, "公开"), (VISIT_LEVEL_PRIVATE, "私有"))

    name = models.CharField(max_length=128, null=False, verbose_name=_("TeamName"))
    description = models.TextField()
    # TODO
    # logo = models.ImageField(null=True, verbose_name=_("项目LOGO"))
    visit_level = models.IntegerField(choices=VISIT_CHOICES, null=False, verbose_name=_("可见性 10 可见 90 不可见"))
    parent = models.ForeignKey('Project', null=True, related_name="child_projects",
                               on_delete=models.SET_NULL,
                               verbose_name=_("上级项目 预留"))
    owner = models.ForeignKey(User, related_name="owner_projects", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("项目负责人"))
    team = models.ForeignKey(Team, related_name="team_projects", on_delete=models.SET_NULL, null=True,
                             verbose_name=_("归属团队"))

    class Meta:
        db_table = "projects"
        ordering = ["-created_at"]


class Module(BaseModelMixin):
    """

    模块
    """
    name = models.CharField(max_length=128, null=False, unique=True, verbose_name=_("模块名称"))
    description = models.TextField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_("所属项目"))

    class Meta:
        db_table = "modules"
        ordering = ["-created_at"]


class Label(BaseModelMixin):
    """

    标签
    """
    TYPE_USER = "userlabel"
    TYPE_APP = "applabel"
    TYPE_TASK = "tasklabel"
    TYPE_FEATURE = "featurelabel"
    TYPE_REQ = "reqlabel"
    TYPE_CHOICES = ((TYPE_USER, _("userlabel")), (TYPE_APP, _("applabel")), (TYPE_TASK, _("tasklabel")),
                    (TYPE_FEATURE, _("featurelabel")), (TYPE_REQ, _("reqlabel")))
    title = models.CharField(max_length=128, verbose_name=_("标签名称 唯一"))
    color = models.CharField(max_length=16, verbose_name=_("颜色 #****"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述 预留"))
    type = models.CharField(choices=TYPE_CHOICES, max_length=16, null=True, blank=True, verbose_name=_("类别 预留"))
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, verbose_name=_("标签所属team"))
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, verbose_name=_("标签所属project"))

    class Meta:
        db_table = "labels"
        ordering = ["-created_at"]
        unique_together = ['title', 'project']

    def __str__(self):
        return '{0.title} : {0.team} : {0.type}'.format(self)


class Comment(BaseModelMixin):
    """

    需求/任务 评论
    """
    WORKITEM = "workitem"
    FEATURE = "feature"
    TYPE_CHOICE = ((WORKITEM, "workitem"), (FEATURE, "feature"))

    comment = models.TextField(null=True, verbose_name=_("评论"))
    comment_html = models.TextField(null=True, blank=True, verbose_name=_("评论HTML"))
    relate_type = models.CharField(choices=TYPE_CHOICE, max_length=16, verbose_name=_("关联类型"))
    relate_id = models.IntegerField(verbose_name=_("关联ID"))
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, verbose_name=_("评论所属project"))

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]

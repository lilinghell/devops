from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.mixin import BaseModelMixin
from projects.models import Project
from teams.models import Member


class Application(BaseModelMixin):
    """

    应用
    """

    APP_TYPE_MIRCO = "mircoservice"
    APP_TYPE_WEB = "web"
    APP_TYPE_BATCH = "batch"
    APP_TYPE_J2SE = "j2se"
    APP_TYPE_CHOICES = ((APP_TYPE_MIRCO, ""), (APP_TYPE_WEB, ""), (APP_TYPE_BATCH, ""), (APP_TYPE_J2SE, ""))

    STATUS_VALID = "1"
    STATUS_INIT = "0"
    STATUS_INVALID = "2"
    STATUS_CHOICE = ((STATUS_INIT, "0"), (STATUS_VALID, "1"), (STATUS_INVALID, "2"))

    name = models.CharField(max_length=128, unique=True, verbose_name=_("应用名称,唯一"))
    description = models.TextField(verbose_name=_("应用描述"))
    project = models.ForeignKey(Project, related_name="project_applications", null=True, on_delete=models.CASCADE)
    type = models.CharField(choices=APP_TYPE_CHOICES, verbose_name=_("应用类型"), max_length=16)
    status = models.CharField(choices=STATUS_CHOICE, verbose_name=_("应用状态"), null=True, max_length=2)
    owner = models.ForeignKey(Member, related_name="own_apps", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("项目应用")
        db_table = "appliations"

    def __str__(self):
        return "{0.name}({0.type}".format(self)


class AppSetting(models.Model):
    """

    应用配置信息
    """
    pass

    class Meta:
        # TODO
        managed = False


class AppSpec(models.Model):
    """

    微服务定义
    """
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="spec", unique=True,
                                       primary_key=True)
    service_id = models.CharField(max_length=128, unique=True, verbose_name=_("app_service_id"))
    description = models.TextField(verbose_name=_("app_spec_desc"))

    dependency = models.ManyToManyField("Application", related_name="ref_apps", verbose_name=_("依赖的服务"))

    class Meta:
        verbose_name = _("app_spec")


# class AppEnv(BaseModelMixin):
#     """
#
#     应用环境信息
#     """
#     pass
#
#     class Meta:
#         # TODO
#         managed = False


class Repository(BaseModelMixin):
    """

    应用对应的代码仓库
    """

    SCM_SVN = "svn"
    SCM_GIT = "git"
    SCM_CHOICE = ((SCM_GIT, "git"), (SCM_SVN, "svn"))

    AUTH_PWD = "pwd"
    AUTH_TOKEN = "token"
    AUTH_CHOICE = ((AUTH_PWD, "pwd"), (AUTH_TOKEN, "token"))

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="repo", unique=True,
                                       primary_key=True)
    type = models.CharField(choices=SCM_CHOICE, blank=True, max_length=8, null=True)
    web_url = models.CharField(max_length=128, blank=True, verbose_name=_("SCM主页"), null=True)
    scm_url = models.CharField(max_length=128, blank=True, verbose_name=_("SCM_url"), null=True)
    project = models.ForeignKey(Project, related_name="project_repositorys", null=True, on_delete=models.CASCADE)
    branch = models.CharField(max_length=128, blank=True, null=True)
    auth_type = models.CharField(choices=AUTH_CHOICE, blank=True, verbose_name=_("auth_type"), max_length=8, null=True)
    auth_token = models.CharField(max_length=128, blank=True, null=True)
    auth_username = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = _("代码仓库")
        db_table = "repositorys"

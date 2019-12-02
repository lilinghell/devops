from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from common.utils import upload_file_path
from users.models import User
from .mixin import BaseModelMixin


class PrivateToken(Token):
    """Inherit from auth token, otherwise migration is boring"""

    class Meta:
        verbose_name = _('Private Token')
        managed = False


class Attachment(BaseModelMixin):
    """

    通用附件表
    """
    file = models.FileField(upload_to=upload_file_path, null=False, verbose_name=_(""))
    filename = models.CharField(max_length=256, verbose_name=_("原附件名称"))
    filesize = models.IntegerField(verbose_name=_("文件大小"))
    orgin = models.CharField(max_length=256, verbose_name=_("来源"), null=True)
    type = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = _("附件表")
        db_table = "attachments"


class OperateLog(BaseModelMixin):
    """

    操作日志
    """
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_CHOICES = (
        (ACTION_CREATE, _("Create")),
        (ACTION_UPDATE, _("Update")),
        (ACTION_DELETE, _("Delete"))
    )
    user = models.ForeignKey(User, related_name="user", on_delete=models.SET_NULL, null=True,)
    action = models.CharField(max_length=16, choices=ACTION_CHOICES, verbose_name=_("Action"))
    resource_type = models.CharField(max_length=64, verbose_name=_("Resource Type"))
    resource_id = models.IntegerField(null=True, verbose_name=_("Resource_id"))
    remote_addr = models.CharField(max_length=15, verbose_name=_("Remote addr"), blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
    project_id = models.IntegerField(null=True, blank=True, verbose_name=_("关联项目，非项目操作可为空"))

    class Meta:
        verbose_name = _("操作日志表")
        db_table = "operate_logs"

    def __str__(self):
        return "<{}> {} <{}>".format(self.user, self.action, self.resource)

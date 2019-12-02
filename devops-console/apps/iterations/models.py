from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.mixin import BaseModelMixin
from projects.models import Project
from users.models import User


class Iteration(BaseModelMixin):
    STATUS_INIT = 0
    STATUS_OPENED = 1
    STATUS_CLOSED = 2
    STATUS_OVERDUE = 3
    STATUS_CHOICES = (
        (STATUS_INIT, '0'), (STATUS_OPENED, '1'), (STATUS_CLOSED, '2'), (STATUS_OVERDUE, '3'))
    title = models.CharField(max_length=128, verbose_name=_("迭代名称"))
    description = models.TextField(null=True, blank=True, verbose_name=_("迭代描述"))
    start_date = models.CharField(max_length=8, verbose_name=_("迭代开始日期YYYYMMDD"))
    end_date = models.CharField(max_length=8, verbose_name=_("迭代结束日期YYYYMMDD"))

    owner = models.ForeignKey(User, related_name="own_iterations", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("迭代责任人"))
    project = models.ForeignKey(Project, related_name="project_iterations", null=True, blank=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("关联项目"))
    status = models.CharField(null=True, blank=True, choices=STATUS_CHOICES, max_length=2, verbose_name=_("迭代状态"))

    class Meta:
        db_table = 'iterations'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from applications.models import Application
from common.mixin import BaseModelMixin
from common.models import Attachment
from iterations.models import Iteration
from projects.models import Project, Label, Module
from requirements.models import Requirement
from users.models import User


class Feature(BaseModelMixin):
    """

    开发需求
    0 待处理 0%
    1 开发中 10%
    2 测试中 40%
    3 待发布 70%
    4 已完成 100%
    5 已取消 0%
    6 已归档 100%
    """
    STATUS_INIT = "0"
    STATUS_DOING = "1"
    STATUS_TEST = "2"
    STATUS_DONE = "3"
    STATUS_CLOSED = "4"
    STATUS_CANCEL = "5"
    STATUS_ARCHIVE = "6"
    STATUS_CHOICES = (
        (STATUS_INIT, '0'), (STATUS_DOING, '1'), (STATUS_TEST, '2'), (STATUS_DONE, '3'), (STATUS_CLOSED, '4'),
        (STATUS_CANCEL, '5'), (STATUS_ARCHIVE, '6'))

    title = models.CharField(max_length=128, unique=True, verbose_name=_("标题"))
    description = models.TextField(null=True, verbose_name=_("描述"))
    description_html = models.TextField(null=True, blank=True, verbose_name=_("描述HTML"))
    start_date = models.CharField(max_length=8, verbose_name=_("开始日期YYYYMMDD"))
    end_date = models.CharField(max_length=8, verbose_name=_("结束日期YYYYMMDD"))
    important = models.IntegerField(verbose_name=_("重要性"))
    priority = models.IntegerField(verbose_name=_("优先级"))
    estimate_time = models.CharField(max_length=8, null=True, blank=True, verbose_name=_("时间预估"))
    progress = models.IntegerField(verbose_name=_("进度"), null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, verbose_name=_('需求状态'))
    owner = models.ForeignKey(User, related_name="own_features", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("责任人"))
    closed_by = models.ForeignKey(User, related_name="close_features", on_delete=models.SET_NULL, null=True,
                                  verbose_name=_("关闭人"))
    closed_at = models.DateTimeField(null=True, verbose_name=_("关闭时间"))

    apps = models.ManyToManyField(Application, related_name="app_features",
                                  verbose_name=_("关联应用"))

    project = models.ForeignKey(Project, related_name="pro_features", on_delete=models.CASCADE,
                                verbose_name=_("关联项目"))

    requirement = models.ForeignKey(Requirement, related_name="req_features", null=True,
                                    on_delete=models.SET_NULL, verbose_name=_("上级需求"))

    labels = models.ManyToManyField(Label, related_name="label_features", blank=True, verbose_name=_("需求标签"))

    attachments = models.ManyToManyField(Attachment, related_name="feature_attachments", blank=True,
                                         verbose_name=_("需求附件"))

    iteration = models.ForeignKey(Iteration, related_name="iteration_features", null=True, on_delete=models.SET_NULL,
                                  verbose_name=_("归属迭代"))

    module = models.ForeignKey(Module, related_name="module_features", on_delete=models.CASCADE, null=True,
                               verbose_name=_("模块"))

    class Meta:
        verbose_name = _("业务需求表")
        db_table = "features"

    def __str__(self):
        return 'this is features {0.id} : {0.title}'.format(self)


class FeatureBranch(BaseModelMixin):
    """

    需求分支,关联/新建    解除关联/删除
    """
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="feature_branch",
                                verbose_name=_("分支关联需求"))
    app = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="app_branch")
    branch_name = models.CharField(max_length=128, null=True, blank=True)
    ref = models.CharField(max_length=128)
    status = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        verbose_name = _("需求分支表")
        db_table = "feature_branchs"
        unique_together = ("feature", "app")

    def __str__(self):
        return 'this is features {0.id} : {0.branch_name}'.format(self)

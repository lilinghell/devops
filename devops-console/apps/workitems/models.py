from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.mixin import BaseModelMixin
from common.models import Attachment
from projects.models import Project, Label, Module
from users.models import User
from features.models import Feature
from iterations.models import Iteration


class WorkItem(BaseModelMixin):
    """
    1 待处理
    2 开发中
    3 测试中 / 待验证
    4 待发布 / 已解决
    5 已完成
    6 已取消
    7 已归档
    工作项
    """
    STATUS_INIT = "1"
    STATUS_DOING = "2"
    STATUS_TEST = "3"
    STATUS_DONE = "4"
    STATUS_CLOSED = "5"
    STATUS_CANCEL = "6"
    STATUS_ARCHIVE = "7"
    STATUS_CHOICES = (
        (STATUS_INIT, '1'), (STATUS_DOING, '2'), (STATUS_TEST, '3'), (STATUS_DONE, '4'), (STATUS_CLOSED, '5'),
        (STATUS_CANCEL, '6'), (STATUS_ARCHIVE, '7'))

    TYPE_REQ = "1"  # 需求
    TYPE_BUG = "2"  # 缺陷
    TYPE_TASK = "3"  # 任务
    TYPE_OTHER = "9"  # 其他
    TYPE_CHOICES = ((TYPE_REQ, '1'), (TYPE_BUG, '2'), (TYPE_TASK, '3'), (TYPE_OTHER, '9'))

    PRIORITY_LOW = 1
    PRIORITY_MID = 2
    PRIORITY_HIG = 3
    PRIORITY_CHOICES = ((PRIORITY_LOW, 1), (PRIORITY_MID, 2), (PRIORITY_HIG, 3))

    IMPORTANT_LOW = 1
    IMPORTANT_MID = 2
    IMPORTANT_HIG = 3
    IMPORTANT_CHOICES = ((IMPORTANT_LOW, 1), (IMPORTANT_MID, 2), (IMPORTANT_HIG, 3))

    title = models.CharField(max_length=128, verbose_name=_("标题"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))
    type = models.CharField(choices=TYPE_CHOICES, null=True, blank=True, max_length=2)
    description_html = models.TextField(null=True, blank=True, verbose_name=_("描述HTML"))
    start_date = models.CharField(max_length=8, blank=True, null=True, verbose_name=_("开始日期YYYYMMDD"))
    end_date = models.CharField(max_length=8, blank=True, null=True, verbose_name=_("结束日期YYYYMMDD"))
    important = models.IntegerField(verbose_name=_("重要性"), default=IMPORTANT_MID)
    priority = models.IntegerField(verbose_name=_("优先级"), default=PRIORITY_MID)
    estimate_time = models.CharField(max_length=16, verbose_name=_("时间预估"), blank=True, null=True)
    progress = models.CharField(max_length=2, verbose_name=_("进度"), null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default=STATUS_INIT)
    owner = models.ForeignKey(User, related_name="own_workitems", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("责任人"))
    closed_by = models.ForeignKey(User, related_name="close_workitems", on_delete=models.SET_NULL, null=True,
                                  verbose_name=_("关闭人"))
    closed_at = models.DateTimeField(null=True, verbose_name=_("关闭时间"))

    assignee_users = models.ManyToManyField(User, related_name="user_workitems", blank=True, verbose_name=_("分配开发人员"))

    project = models.ForeignKey(Project, related_name="project_workitems", null=True, blank=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("关联项目"))
    module = models.ForeignKey(Module, related_name="module_workitems", null=True,
                               on_delete=models.SET_NULL, verbose_name=_("归属模块"))

    feature = models.ForeignKey(Feature, related_name="feature_workitems", null=True,
                                on_delete=models.SET_NULL, verbose_name=_("关联需求"))

    labels = models.ManyToManyField(Label, related_name="label_workitems", blank=True,
                                    verbose_name=_("工作项标签"))

    attachments = models.ManyToManyField(Attachment, related_name="workitem_attachments", blank=True,
                                         verbose_name=_("工作项附件"))

    parent = models.ForeignKey("workitems.WorkItem", related_name="child_workitems", null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_("父工作项"))
    iteration = models.ForeignKey(Iteration, related_name="iteration_workitems", null=True, on_delete=models.SET_NULL,
                                  verbose_name=_("归属迭代"))

    class Meta:
        verbose_name = _("工作项表")
        db_table = "workitems"

    def __str__(self):
        return 'this is workitems {0.id} : {0.title}'.format(self)

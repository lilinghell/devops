from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.mixin import BaseModelMixin
from teams.models import Team
from users.models import User


class Requirement(BaseModelMixin):
    """

    业务需求
    """
    STATUS_INIT = "0"
    STATUS_DOING = "1"
    STATUS_FIXED = "2"
    STATUS_TEST = "3"
    STATUS_DONE = "4"
    STATUS_CLOSED = "5"
    STATUS_CHOICES = (
        (STATUS_INIT, '0'), (STATUS_DOING, '1'), (STATUS_FIXED, '2'), (STATUS_TEST, '3'), (STATUS_DONE, '4'),
        (STATUS_CLOSED, '5'))

    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    important = models.IntegerField(verbose_name=_("重要性"))
    priority = models.IntegerField(verbose_name=_("优先级"))
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    link_id = models.CharField(max_length=128, verbose_name=_("关联redmine"))
    link_url = models.CharField(max_length=128, verbose_name=_("关联redmine url"))
    owner = models.ForeignKey(User, related_name="own_reqs", on_delete=models.SET_NULL, null=True,
                              verbose_name=_("责任人"))
    assignee_teams = models.ManyToManyField(Team, related_name="assignee_reqs", verbose_name=_("指派小组"))
    parent = models.ForeignKey("requirements.Requirement", related_name="child_req", null=True,
                               on_delete=models.SET_NULL, verbose_name=_("上级需求"))
    relate = models.ForeignKey("requirements.Requirement", related_name="relate_req", null=True,
                               on_delete=models.SET_NULL, verbose_name=_("关联需求"))

    class Meta:
        verbose_name = _("业务需求表")
        db_table = "requirements"

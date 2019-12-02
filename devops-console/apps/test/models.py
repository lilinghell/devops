from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.mixin import BaseModelMixin
from designs.models import Interfaces
from projects.models import Project
from features.models import Feature
from users.models import User


class TestEnv(BaseModelMixin):
    """
    测试环境信息
    """

    name = models.CharField(max_length=128, verbose_name=_("名称"))
    domain = models.URLField(max_length=256, verbose_name=_("域名"))
    header = models.TextField(null=True, blank=True, verbose_name=_("header"))
    cookie = models.TextField(null=True, blank=True, verbose_name=_("cookie"))
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_testEnv", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test_env"
        ordering = ["-created_at"]
        unique_together = ['name']


class TestGroup(BaseModelMixin):
    """
    测试用例组
    """
    name = models.CharField(max_length=128, verbose_name="组名")
    parent = models.ForeignKey('self', null=True, related_name="child_group",
                               on_delete=models.SET_NULL,
                               verbose_name=_("父节点信息"))
    description = models.TextField(null=True, verbose_name="描述")
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_testGroup", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test_group"
        ordering = ["-created_at"]
        unique_together = ['name']


class TestCase(BaseModelMixin):
    """
    测试用例
    """

    # 待评审
    STATUS_0 = "0"
    # 待测试
    STATUS_1 = "1"
    # 自测通过
    STATUS_2 = "2"
    # 已通过
    STATUS_3 = "3"

    # 功能测试
    TYPE_0 = "0"
    # 性能测试
    TYPE_1 = "1"
    #
    LEVEL_P0 = "P0"
    LEVEL_P1 = "P1"
    LEVEL_P2 = "P2"
    LEVEL_P3 = "P3"

    STATUS_CHOICE = ((STATUS_0, _("0")), (STATUS_1, _("1")), (STATUS_2, _("2")), (STATUS_3, _("3")))
    TYPE_CHOICE = ((TYPE_0, _("0")), (TYPE_1, _("1")))
    LEVEL_CHOICE = ((LEVEL_P0, _("P0")), (LEVEL_P1, _("P1")), (LEVEL_P2, _("P2")), (LEVEL_P3, _("P3")))

    name = models.CharField(max_length=128, verbose_name="用例名")
    group = models.ForeignKey(TestGroup, related_name="test_case_group", on_delete=models.CASCADE,
                              verbose_name="归属用例组")
    user = models.ForeignKey(User, related_name="test_case_user", on_delete=models.SET_NULL, null=True,
                             verbose_name="归属用例组")
    status = models.CharField(choices=STATUS_CHOICE, max_length=2, verbose_name="状态")
    type = models.CharField(choices=TYPE_CHOICE, max_length=2, verbose_name="用例类型")
    level = models.CharField(choices=LEVEL_CHOICE, max_length=2, verbose_name="用例等级")
    feature = models.ManyToManyField(Feature, related_name="test_case_feature", blank=True,
                                     verbose_name=_("归属需求"))
    prerequisites = models.TextField(blank=True, null=True, verbose_name="前置条件")
    desc = models.TextField(blank=True, null=True, verbose_name="描述")
    expected = models.TextField(blank=True, null=True, verbose_name="预期结果")
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_testCase", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test_case"
        ordering = ["-created_at"]


class Test(BaseModelMixin):
    case = models.ForeignKey(TestCase, related_name="test_case", on_delete=models.CASCADE, verbose_name="用例")
    env = models.ForeignKey(TestEnv, null=True, related_name="test_env", on_delete=models.SET_NULL, verbose_name="测试环境")
    interface = models.ForeignKey(Interfaces, null=True, related_name="test_interface", on_delete=models.SET_NULL,
                                  verbose_name="接口")
    prerequisites = models.TextField(blank=True, null=True, verbose_name="前置条件")
    body = models.TextField(verbose_name="请求body")
    expected = models.TextField(null=True, blank=True, verbose_name="预期结果")
    response = models.TextField(null=True, blank=True, verbose_name="response")
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_test", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test"
        ordering = ["-created_at"]
        unique_together = ['case']


class TestPlan(BaseModelMixin):
    name = models.CharField(max_length=128, verbose_name="名称")
    user = models.ForeignKey(User, related_name="test_plan_user", on_delete=models.SET_NULL, null=True,
                             verbose_name="负责人")
    start_date = models.CharField(max_length=8, verbose_name="开始日期YYYYMMDD")
    end_date = models.CharField(max_length=8, verbose_name="结束日期YYYYMMDD")
    description = models.TextField(null=True, verbose_name=_("描述"))
    case = models.ManyToManyField(TestCase, related_name="test_plan_case", verbose_name="用例", blank=True)
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_testPlan", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test_plan"
        ordering = ["-created_at"]
        unique_together = ['name']


class TestAutoPlan(BaseModelMixin):
    name = models.CharField(max_length=128, verbose_name="名称")
    user = models.ForeignKey(User, related_name="test_auto_plan_user", on_delete=models.SET_NULL, null=True,
                             verbose_name="负责人")
    env = models.ForeignKey(TestEnv, null=True, related_name="test_auto_plan_env", on_delete=models.SET_NULL,
                            verbose_name="测试环境")
    time = models.CharField(max_length=64, verbose_name="时刻，1-24逗号隔开")
    week = models.CharField(max_length=14, verbose_name="星期几，1-7逗号隔开")
    description = models.TextField(null=True, verbose_name=_("描述"))
    case = models.ManyToManyField(TestCase, related_name="test_auto_plan_case", blank=True,
                                  verbose_name="用例")
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_testAutoPlan", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "test_auto_plan"
        ordering = ["-created_at"]
        unique_together = ['name']

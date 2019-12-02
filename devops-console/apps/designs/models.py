from django.db import models
from django.utils.translation import ugettext_lazy as _

from applications.models import Application
from projects.models import Project
from common.mixin import BaseModelMixin
from common.models import Attachment


class FeatureImpactDesign(BaseModelMixin):
    """

    影响度分析
    """
    pass


class InterfaceGroup(BaseModelMixin):
    """

    API组设计
    """
    name = models.CharField(max_length=128, verbose_name="组名")
    parent = models.ForeignKey('self', null=True, related_name="child_group",
                               on_delete=models.SET_NULL,
                               verbose_name=_("父节点信息"))
    description = models.TextField(null=True, verbose_name="描述")
    application = models.ForeignKey(Application, verbose_name="归属应用", related_name="interface_group_application",
                                    on_delete=models.CASCADE)
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_group", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "interface_group"
        unique_together = ['name', 'application']


class Interfaces(BaseModelMixin):
    """

    API接口设计
    """
    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_PUT = "PUT"
    METHOD_PATCH = "PATCH"
    METHOD_DELETE = "DELETE"
    METHOD_CHOICE = (
        (METHOD_GET, _("GET")), (METHOD_POST, _("POST")), (METHOD_PUT, _("PUT")), (METHOD_PATCH, _("PATCH")), (METHOD_DELETE, _("DELETE")))

    # 开发完成
    STATUS_0 = "0"
    # 开发中
    STATUS_1 = "1"
    STATUS_CHOICE = ((STATUS_0, _("0")), (STATUS_1, _("1")))

    name = models.CharField(max_length=128, verbose_name="接口名")
    url = models.CharField(max_length=64, verbose_name="url")

    #  CharFields must define a 'max_length' attribute
    method = models.CharField(choices=METHOD_CHOICE,
                              max_length=32, verbose_name="http方法")
    description = models.TextField(null=True, verbose_name="描述")
    version = models.CharField(max_length=16, verbose_name="版本")
    status = models.CharField(choices=STATUS_CHOICE,
                              max_length=2, verbose_name="状态")
    open = models.BooleanField(default=True, verbose_name="是否开放")
    application = models.ForeignKey(
        Application, related_name="interface_application", on_delete=models.CASCADE)  # 连级删除
    group = models.ForeignKey(
        InterfaceGroup, related_name="interface_group", on_delete=models.CASCADE)
    project = models.ForeignKey(Project,  verbose_name="归属项目",
                                related_name="project_interface", null=True, on_delete=models.CASCADE)
    info = models.TextField(null=True, blank=True, verbose_name=_("接口信息"))

    # 在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题
    class Meta:
        db_table = "interfaces"
        ordering = ["-created_at"]
        unique_together = ['url']


class InterfaceTest(BaseModelMixin):
    interface = models.ForeignKey(
        Interfaces, related_name="interface_test_interface", on_delete=models.CASCADE)
    body = models.TextField(verbose_name="请求body")
    response = models.TextField(null=True, blank=True, verbose_name="response")

    class Meta:
        db_table = "interface_test"
        ordering = ["-created_at"]
        unique_together = ['interface']


class InterfaceDictionary(BaseModelMixin):
    """
    字典
    """

    TYPE_STRING = "string"
    TYPE_NUMBER = "number"
    TYPE_BOOLEAN = "boolean"
    TYPE_INTEGER = "integer"
    TYPE_ARRAY = "array"
    TYPE_CHOICE = ((TYPE_STRING, _("string")), (TYPE_NUMBER, _("number")),
                   (TYPE_BOOLEAN, _("boolean")), (TYPE_INTEGER, _("integer")), (TYPE_ARRAY, _("array")))

    name = models.CharField(max_length=128, verbose_name=_("名称"))
    # CharFields must define a 'max_length' attribute
    type = models.CharField(choices=TYPE_CHOICE,
                            verbose_name=_("类型"), max_length=20)
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))

    class Meta:
        db_table = "interface_dictionary"
        ordering = ["-created_at"]
        unique_together = ['name', 'type']  # 联合约束


class EsbInterfaces(BaseModelMixin):
    service_name = models.CharField(max_length=128, verbose_name="服务名")
    service_desc = models.CharField(max_length=128, verbose_name="服务描述")
    operation_name = models.CharField(max_length=128, verbose_name="操作名")
    operation_desc = models.CharField(max_length=128, verbose_name="操作描述")
    attachments = models.ManyToManyField(Attachment, related_name="esb_interface_attachments", blank=True,
                                         verbose_name=_("ESB服务附件"))
    server_name = models.CharField(
        max_length=128, verbose_name="服务方", null=True, blank=True)
    url = models.URLField(verbose_name="url", null=True, blank=True)

    class Meta:
        db_table = "interface_esb"
        ordering = ["-created_at"]
        unique_together = ['operation_name']

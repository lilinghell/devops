from rest_framework import viewsets

from test.mixin import TestViewSetMixin
from .models import TestEnv, TestGroup, TestCase, Test, TestPlan, TestAutoPlan
from .serializers import TestEnvSerializer, TestGroupSerializer, TestCaseSerializer, TestSerializer, TestPlanSerializer, \
    TestAutoPlanSerializer
from projects.mixins import ProjectViewSetMixin


class TestEnvViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """
    list:
        描述:获取环境配置
    create:
        描述:添加环境配置
    update:
        描述:修改环境配置
    delete:
        描述:删除环境配置
    """
    search_fields = ('name',)
    serializer_class = TestEnvSerializer
    queryset = TestEnv.objects.all()


class TestGroupView(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TestGroupSerializer
    queryset = TestGroup.objects.all()


class TestCasesView(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TestCaseSerializer
    queryset = TestCase.objects.all()


class TestCaseView(TestViewSetMixin, ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()


class TestPlanView(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TestPlanSerializer
    queryset = TestPlan.objects.all()


class TestAutoPlanView(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TestAutoPlanSerializer
    queryset = TestAutoPlan.objects.all()

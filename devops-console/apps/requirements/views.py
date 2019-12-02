from rest_framework import viewsets
from .serializers import RequirementSerializer, RequirementReadSerializer
from .models import Requirement
from common import permissions


class RequirementViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        描述:单个业务需求详情
        权限:需求人员

        list:
        描述:获取业务需求列表
        权限:需求人员

        create:
        描述:新建业务需求
        权限:需求人员

        delete:
        描述:删除业务需求
        权限:需求人员
        """
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.prefetch_related("assignee_teams")
    permissions = (permissions.IsOrgAdmin,)

    def dispatch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return RequirementReadSerializer
        return self.serializer_class

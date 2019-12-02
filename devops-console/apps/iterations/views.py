from rest_condition import Or, And, Not
from rest_framework import viewsets
from common import permissions
from iterations.serializers import IterationReadSerializer, IterationSerializer, IterationPlanReadSerializer, \
    IterationPlanSerializer
from projects.mixins import ProjectViewSetMixin
from .models import Iteration


class IterationViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    queryset = Iteration.objects.all()
    serializer_class = IterationSerializer
    permission_classes = [
        Or(permissions.IsValidUserAndReadonly, And(permissions.IsPostRequest, permissions.IsProjectManager), )]

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return IterationReadSerializer
        return self.serializer_class


class IterationPlanViewSet(ProjectViewSetMixin, viewsets.generics.RetrieveUpdateAPIView):
    serializer_class = IterationPlanSerializer
    queryset = Iteration.objects.all()
    permissions = (permissions.IsOrgAdmin,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IterationPlanReadSerializer
        return self.serializer_class

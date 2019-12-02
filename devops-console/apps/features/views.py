from django.db import transaction
from rest_condition import And, Or
from rest_framework import viewsets
from rest_framework.response import Response

from applications.models import Repository
from common import permissions
from common.utils import git
from projects.mixins import ProjectViewSetMixin
from .models import Feature, FeatureBranch
from .serializers import FeatureBranchSerializer, FeatureReadSerializer, FeatureSerializer, FeatureBranchReadSerializer


class FeatureViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """

    需求管理
    """
    serializer_class = FeatureSerializer
    queryset = Feature.objects.select_related("owner")
    permission_classes = [Or(permissions.IsValidUserAndReadonly, permissions.IsProjectManager,
                             And(permissions.IsPostRequest, permissions.IsProjectLeader),
                             permissions.IsFeatureOwnerOrCreater), ]

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return FeatureReadSerializer
        return self.serializer_class


class FeatureBranchViewSet(viewsets.ModelViewSet):
    """

    需求分支管理
    """
    serializer_class = FeatureBranchSerializer
    queryset = FeatureBranch.objects.all()
    permission_classes = [Or(permissions.IsValidUserAndReadonly, permissions.IsProjectManager,
                             And(permissions.IsPostRequest, permissions.IsProjectLeader),
                             permissions.IsFeatureOwnerOrCreater), ]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return FeatureBranchReadSerializer
        return self.serializer_class

    @transaction.atomic()
    def perform_create(self, serializer):
        super().perform_create(serializer)
        app_id = serializer.validated_data["app"].id
        repository = Repository.objects.get(
            application_id=app_id)
        if serializer.validated_data['branch_name'] != serializer.validated_data['ref']:
            # gitlab新建分支
            gl = git(repository.scm_url, repository.auth_token)
            project = gl[0].projects.get(gl[1])
            project.branches.create({'branch': serializer.validated_data["branch_name"],
                                     'ref': serializer.validated_data["ref"]})

    @transaction.atomic()
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        repository = Repository.objects.get(
            application_id=instance.app.id)
        # gitlab删除分支
        gl = git(repository.scm_url, repository.auth_token)
        project = gl[0].projects.get(gl[1])
        project.branches.delete(instance.branch_name)

    def list(self, request, *args, **kwargs):
        feature_id = kwargs.get('feature_id')
        instances = FeatureBranch.objects.filter(feature_id=feature_id)
        feature_instance = Feature.objects.get(id=feature_id)
        instance = FeatureReadSerializer(feature_instance).data
        feature_branches = []
        apps = instance.get("apps")

        for app in apps:
            branch = {}
            branch["app"] = app
            branch["branch_name"] = ""
            branch["status"] = ""
            branch["ref"] = ""
            for instance in instances:
                if app.get("id") == instance.app.id:
                    branch["branch_name"] = instance.branch_name
                    branch["status"] = instance.status
                    branch["ref"] = instance.ref
                    break
            feature_branches.append(branch)
        return Response(feature_branches)

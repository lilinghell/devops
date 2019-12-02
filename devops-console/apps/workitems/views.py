from django.db import transaction
from rest_framework import viewsets, views, mixins, status
from rest_framework.response import Response

from projects.mixins import ProjectViewSetMixin
from projects.models import Comment
from projects.serializers import CommentReadSerializer, CommentSerializer, CommentWriteSerializer
from .serializers import WorkItemSerializer, WorkItemReadSerializer, WorkItemCreateSerializer
from .models import WorkItem
from common import permissions


class WorkItemViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    """
        retrieve:
        描述:单个工作项详情
        权限:需求人员

        list:
        描述:获取工作项列表
        权限:需求人员

        create:
        描述:新建工作项
        权限:需求人员

        delete:
        描述:删除工作项
        权限:需求人员
        """
    serializer_class = WorkItemSerializer
    queryset = WorkItem.objects.select_related("feature").prefetch_related("labels", "assignee_users")
    permissions = (permissions.IsOrgAdmin,)

    def dispatch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return WorkItemReadSerializer
        elif self.action in ('create'):
            return WorkItemCreateSerializer
        return self.serializer_class

    # @transaction.atomic
    def update(self, request, *args, **kwargs):
        # 请求数据裁剪
        if request.data.__contains__('assignee_users'):
            request.data['assignee_users'] = list(map(lambda user: user['id'], request.data['assignee_users']))
        if request.data.__contains__('attachments'):
            request.data['attachments'] = list(map(lambda attachment: attachment['id'], request.data['attachments']))
        if request.data.__contains__('labels'):
            request.data['labels'] = list(map(lambda label: label['id'], request.data['labels']))
        if request.data.__contains__('feature'):
            if request.data['feature'] != '':
                request.data['feature'] = request.data['feature']['id']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(WorkItemReadSerializer(instance).data)


# 获取需求下任务列表
class FeatureWorkItemView(views.APIView):
    def get(self, request, *args, **kwargs):
        pass


# 获取子任务列表
class WorkItemChildrenView(views.APIView):
    def get(self, request, *args, **kwargs):
        pass


class WorkItemCommentViewSet(ProjectViewSetMixin, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """

    任务评论
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related("created_by")

    def get_serializer_class(self):
        if self.action in ("list",):
            return CommentReadSerializer
        elif self.action in ("create",):
            return CommentWriteSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['relate_type'] = Comment.WORKITEM
        validated_data['relate_id'] = self.kwargs.get('w_id')
        validated_data['project_id'] = self.kwargs.get('project_id')
        super().perform_create(serializer)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(relate_id=self.kwargs.get('w_id'), relate_type=Comment.WORKITEM,
                                   project_id=self.kwargs.get('project_id'))
        return queryset

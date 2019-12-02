from rest_framework import serializers
from django.db import transaction

from features.models import Feature
from features.serializers import FeatureBasicReadSerializer
from iterations.models import Iteration
from projects.mixins import ProjectSerializerMixin
from workitems.models import WorkItem
from users.serializers import BasicUserSerializer
from workitems.serializers import WorkItemBasicReadSerializer


class IterationSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project']


class IterationReadSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    feature_count = serializers.SerializerMethodField()
    workitem_count = serializers.SerializerMethodField()
    owner = BasicUserSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Iteration
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    def get_feature_count(self, obj):
        return Feature.objects.filter(iteration=obj).count()

    def get_workitem_count(self, obj):
        return WorkItem.objects.filter(iteration=obj).count()

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

    def get_progress(self, obj):
        features = Feature.objects.filter(iteration=obj)
        count = features.count()
        if count == 0:
            return 0
        c = 0
        for index, feature in enumerate(features):
            if (feature.status == Feature.STATUS_CLOSED) | (feature.status == Feature.STATUS_ARCHIVE):
                d = 1
            elif feature.status == Feature.STATUS_DONE:
                d = 0.7
            elif feature.status == Feature.STATUS_TEST:
                d = 0.4
            elif feature.status == Feature.STATUS_DOING:
                d = 0.1
            else:
                d = 0
            c = c + d
        return int((c / count) * 100)

    # 规划迭代


class IterationPlanSerializer(ProjectSerializerMixin, serializers.Serializer):
    features = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(), many=True, allow_null=True)
    workitems = serializers.PrimaryKeyRelatedField(queryset=WorkItem.objects.all(), many=True, allow_null=True)

    class Meta:
        module = Iteration
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    @transaction.atomic()
    def update(self, instance, validated_data):
        instance.iteration_features.clear()
        instance.iteration_workitems.clear()
        if validated_data.__contains__('features'):
            Feature.objects.filter(id__in=map(lambda feature: feature.id, validated_data['features'])).update(
                iteration=instance)
        if validated_data.__contains__('workitems'):
            WorkItem.objects.filter(id__in=map(lambda workitem: workitem.id, validated_data['workitems'])).update(
                iteration=instance)
        return instance

    def to_representation(self, instance):
        return IterationSerializer(instance).data


# 迭代列表
class IterationPlanReadSerializer(ProjectSerializerMixin, serializers.Serializer):
    features = serializers.SerializerMethodField()
    workitems = serializers.SerializerMethodField()
    owner = BasicUserSerializer

    class Meta:
        module = Iteration
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    def update(self, instance, validated_data):
        pass

    def get_features(self, obj):
        return map(lambda feature: FeatureBasicReadSerializer(feature).data, Feature.objects.filter(iteration=obj))

    def get_workitems(self, obj):
        return map(lambda workitem: WorkItemBasicReadSerializer(workitem).data, WorkItem.objects.filter(iteration=obj))

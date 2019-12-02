from rest_framework import serializers

from common.serializers import AttachmentSerializer
from projects.mixins import ProjectSerializerMixin
from projects.serializers import ProjectLabelBaseSerializer
from .models import WorkItem
from features.models import Feature
from features.serializers import FeatureBasicReadSerializer
from users.serializers import BasicUserSerializer


class WorkItemSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project', 'closed_by', 'closed_at']

    def update(self, instance, validated_data):
        if validated_data.__contains__('assignee_users'):
            assignee_users = validated_data.pop('assignee_users')
            instance.assignee_users.clear()
            for assignee_user in assignee_users:
                instance.assignee_users.add(assignee_user)
        if validated_data.__contains__('attachments'):
            attachments = validated_data.pop('attachments')
            instance.attachments.clear()
            for attachment in attachments:
                instance.attachments.add(attachment)
        if validated_data.__contains__('labels'):
            labels = validated_data.pop('labels')
            instance.labels.clear()
            for label in labels:
                instance.labels.add(label)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        item_data = super().to_representation(instance)
        if instance.feature_id:
            feature = Feature.objects.get(id=instance.feature_id)
            item_data['feature'] = FeatureBasicReadSerializer(feature).data
        else:
            item_data['feature'] = ""
        return item_data


class WorkItemCreateSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project', 'closed_by', 'closed_at']

    def create(self, validated_data):
        # 塞入feature的app_id
        validated_data["owner"] = self.context['request']._user
        return super().create(validated_data)

    def to_representation(self, instance):
        item_data = super().to_representation(instance)
        if instance.feature_id:
            feature = Feature.objects.get(id=instance.feature_id)
            item_data['feature'] = FeatureBasicReadSerializer(feature).data
        else:
            item_data['feature'] = ""
        return item_data


class WorkItemBasicReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = ['id', 'title', 'status', 'start_date', 'end_date']


class WorkItemReadSerializer(serializers.ModelSerializer):
    assignee_users = BasicUserSerializer(many=True)
    owner = BasicUserSerializer
    labels = ProjectLabelBaseSerializer(many=True)
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = WorkItem
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    def to_representation(self, instance):
        item_data = super().to_representation(instance)
        if instance.feature_id:
            feature = Feature.objects.get(id=instance.feature_id)
            item_data['feature'] = FeatureBasicReadSerializer(feature).data
        else:
            item_data['feature'] = ""
        return item_data

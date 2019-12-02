from django.db import transaction
from rest_framework import serializers

from applications.serializers import ApplicationSerializer
from common.serializers import AttachmentSerializer
from projects.mixins import ProjectSerializerMixin
from projects.serializers import ProjectLabelBaseSerializer, ProjectModuleSerializer
from users.models import User
from users.serializers import BasicUserSerializer
from .models import Feature, FeatureBranch


class FeatureBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureBranch
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']


class FeatureSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'requirement', 'project', 'closed_by', 'closed_at']

    @transaction.atomic
    def update(self, instance, validated_data):

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
        return super(FeatureSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        user = User.objects.get(id=instance.owner_id)
        team_data = super().to_representation(instance)
        team_data['owner'] = BasicUserSerializer(user).data
        if instance.iteration_id is not None:
            from iterations.models import Iteration
            iteration = Iteration.objects.get(id=instance.iteration_id)
            from iterations.serializers import IterationSerializer
            team_data["iteration"] = IterationSerializer(iteration).data
        else:
            team_data["iteration"] = ""
        return team_data


class FeatureBasicReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'status', 'start_date', 'end_date']


class FeatureReadSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)
    labels = ProjectLabelBaseSerializer(many=True)
    attachments = AttachmentSerializer(many=True)
    apps = ApplicationSerializer(many=True)
    created_by = BasicUserSerializer(read_only=True)
    module = ProjectModuleSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project']

    def to_representation(self, instance):
        tem_data = super().to_representation(instance)
        if instance.iteration_id is None:
            tem_data["iteration"] = ""
            return tem_data
        from iterations.models import Iteration
        iteration = Iteration.objects.get(id=instance.iteration_id)
        from iterations.serializers import IterationSerializer
        tem_data["iteration"] = IterationSerializer(iteration).data
        return tem_data


class FeatureBranchReadSerializer(serializers.ModelSerializer):
    feature = FeatureBasicReadSerializer(read_only=True)
    app = ApplicationSerializer(read_only=True)

    class Meta:
        model = FeatureBranch
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'application', 'feature']

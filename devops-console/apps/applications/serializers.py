from django.db import transaction
from rest_framework import serializers

from projects.mixins import ProjectSerializerMixin
from .models import Application, Repository, AppSpec
from designs.models import InterfaceGroup


class RepositorySerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    """

    增加应用SCM信息
    """

    class Meta:
        model = Repository
        fields = "__all__"
        read_only_fields = ['application', 'project',
                            'created_by', 'updated_at', 'org']


class AppSpecSerializer(serializers.ModelSerializer):
    """

    增加应用定义信息
    """

    class Meta:
        model = AppSpec
        fields = "__all__"
        read_only_fields = ['application', 'created_by', 'updated_at', 'org']

    def create(self, validated_data):
        validated_data['application_id'] = self.context['view'].application_id
        instance = AppSpec.objects.create(**validated_data)
        return instance


class ApplicationSerializer(serializers.ModelSerializer):
    """

    应用信息
    """
    repo = RepositorySerializer(required=False)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ['id', 'project', 'status',
                            'created_by', 'updated_at', 'org']

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['project_id'] = self.context['view'].project_id
            repository = validated_data.pop('repo')
            instance = Application.objects.create(**validated_data)
            if repository:
                Repository.objects.create(application=instance,
                                          project_id=validated_data['project_id'],
                                          **repository)
            # 创建interfaceGroup
            InterfaceGroup.objects.create(
                application=instance, project_id=validated_data['project_id'], name=instance.name, description=instance.description)
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context['request']
            super().update(instance, validated_data)
            if request.data.get('repository'):
                repo = Repository.objects.get(application=instance)
                for k, v in request.data.get('repository').items():
                    setattr(repo, k, v)
                repo.save()
            return instance


class CommitSerialzer(serializers.Serializer):
    branchName = serializers.CharField(
        required=False, write_only=True, allow_blank=True)

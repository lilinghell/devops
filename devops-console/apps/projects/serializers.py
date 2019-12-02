from django.db import transaction
from rest_framework import serializers

from common.access import Access
from teams.models import Member
from teams.serializers import BasicTeamSerializer
from users.serializers import BasicUserSerializer
from .mixins import ProjectSerializerMixin
from .models import Project, Module, Label, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.owner = instance.created_by
            instance.save()
            member = Member(user=instance.created_by, source_type=Member.SOURCE_PROJECT, source_id=instance.id,
                            access_level=Access.PROJECT_ADMIN)
            member.save()
            return instance

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        member = Member.objects.get(source_type=Member.SOURCE_PROJECT, source_id=instance.id,
                                    access_level=Access.PROJECT_ADMIN)
        validated_data['access_level'] = Access.PROJECT_GUEST
        super().update(member, validated_data)

        member = Member.objects.get(source_type=Member.SOURCE_PROJECT, source_id=instance.id, user=instance.owner)
        validated_data['access_level'] = Access.PROJECT_ADMIN

        super().update(member, validated_data)

        return instance

    def to_representation(self, instance):
        item_data = super().to_representation(instance)
        if instance.team is None:
            item_data["team"] = ""
        return item_data


class ProjectReadSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)
    team = BasicTeamSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'team', 'created_by', 'updated_at', 'org']

    def to_representation(self, instance):
        item_data = super().to_representation(instance)
        if instance.team is None:
            item_data["team"] = ""
        return item_data


class ProjectOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['owner']


class ProjectLabelSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'team', 'project']


class ProjectLabelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'color']


class ProjectModuleSerializer(ProjectSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project']


class ProjectModuleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'color']


class CommentReadSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_by', "created_at"]


class CommentWriteSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_by', "created_at"]
        read_only_fields = ['id', 'created_by', "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project']

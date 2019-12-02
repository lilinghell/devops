from rest_framework import serializers
from teams.serializers import TeamSerializer
from projects.serializers import ProjectLabelBaseSerializer
from .models import Requirement
from users.serializers import BasicUserSerializer


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']


class RequirementReadSerializer(serializers.ModelSerializer):
    assignee_teams = TeamSerializer(many=True)
    owner = BasicUserSerializer

    class Meta:
        model = Requirement
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']


class RequirementBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ["id", "title"]

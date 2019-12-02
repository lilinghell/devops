from django.db import transaction
from rest_framework import serializers
from common.access import Access
from .models import Team, Member
from .mixins import TeamMemberSerializerMixin
from users.serializers import BasicUserSerializer
from users.models.user import User


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'updated_at', 'org']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            member = Member(user=instance.owner, source_id=instance.id, access_level=Access.TEAM_ADMIN,
                            type=Member.TEAM_ADMIN, source_type=Member.SOURCE_TEAM)
            member.save()
            return instance

    def to_representation(self, instance):
        user = User.objects.get(id=instance.owner_id)
        teamdata = super().to_representation(instance)
        teamdata['owner'] = BasicUserSerializer(user).data
        return teamdata


class TeamQuerySerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_by', 'updated_at', 'org']


class BasicTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class MemberSerializer(TeamMemberSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'type', 'created_by', 'updated_at', 'org', 'source_id', 'source_type']

    def to_representation(self, instance):
        user = User.objects.get(id=instance.user_id)
        memberdata = super().to_representation(instance)
        memberdata['user'] = BasicUserSerializer(user).data
        return memberdata


class MemberReadSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'type', 'created_by', 'updated_at', 'org', 'source_id', 'source_type']


class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'type', 'type''created_by', 'updated_at', 'user', 'org', 'source_id', 'source_type']


class TeamOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['owner']

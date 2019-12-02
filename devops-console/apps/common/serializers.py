from rest_framework import serializers

from users.models import User
from .models import Attachment, OperateLog
from users.serializers import BasicUserSerializer


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'filename', 'filesize']
        read_only_fields = ['id', 'filename', 'filesize']


class OperateLogSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    class Meta:
        model = OperateLog
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'project']

    def to_representation(self, instance):
        user = User.objects.get(id=instance.user_id)
        team_data = super().to_representation(instance)
        team_data['user'] = BasicUserSerializer(user).data
        return team_data

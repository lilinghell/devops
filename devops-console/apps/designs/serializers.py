from rest_framework import serializers

from applications.serializers import ApplicationSerializer
from common.serializers import AttachmentSerializer
from .models import InterfaceDictionary, Interfaces, InterfaceGroup, InterfaceTest, EsbInterfaces
from applications.models import Application


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceDictionary
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceGroup
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']

    def to_representation(self, instance):
        app = Application.objects.get(id=instance.application_id)
        team_data = super().to_representation(instance)
        team_data['application'] = ApplicationSerializer(app).data
        return team_data


class GroupReadSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = InterfaceGroup
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class InterfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']

    def to_representation(self, instance):

        team_data = super().to_representation(instance)
        app = Application.objects.get(id=instance.application_id)
        team_data['application'] = ApplicationSerializer(app).data

        group = InterfaceGroup.objects.get(id=instance.group_id)
        team_data['group'] = GroupReadSerializer(group).data
        return team_data


class InterfaceReadSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)
    group = GroupReadSerializer(read_only=True)

    class Meta:
        model = Interfaces
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class InterfaceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceTest
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org', 'response']


class EsbInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsbInterfaces
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class EsbInterfaceReadSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = EsbInterfaces
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']

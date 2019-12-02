from django.db import transaction
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from users.serializers import BasicUserSerializer, UserSerializer
from .models import Organization, ProductRole
from users.models import User


class OrgSerializer(ModelSerializer):
    """

    机构信息
    """

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_date']

    def update(self, instance, validated_data):
        if validated_data.__contains__('admins'):
            admins = set(OrgReadSerializer(instance).data['admins'])
            users = set(OrgReadSerializer(instance).data['users'])
            request = self.context['request']
            re_admins = set(request.data.get('admins'))
            a = admins - re_admins
            for item in re_admins:
                users.discard(item)
            users.update(a)
            validated_data['admins'] = re_admins
            validated_data['users'] = users
        super().update(instance, validated_data)
        return instance


class OrgMembershipAdminSerializer(Serializer):
    """

    机构管理员信息
    """
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = (
        (ROLE_ADMIN, 'admin'),
        (ROLE_USER, 'user'),
    )
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    type = serializers.ChoiceField(choices=ROLE_CHOICES, required=True, allow_blank=False, allow_null=False)
    date_expired = serializers.DateTimeField(required=False, read_only=True)
    id = serializers.IntegerField(required=False, read_only=True)
    authority = serializers.CharField(required=False, read_only=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'], name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.created_by = 'System'
        with transaction.atomic():
            user.save()
            if self.context['org'] and validated_data['type'] == self.ROLE_ADMIN:
                user.admin_orgs.add(self.context['org'].id)
            if self.context['org'] and validated_data['type'] == self.ROLE_USER:
                user.orgs.add(self.context['org'].id)
        validated_data['date_expired'] = user.date_expired
        validated_data['name'] = user.name
        validated_data['authority'] = user.authority
        validated_data['id'] = user.id
        return validated_data


class OrgReadSerializer(ModelSerializer):
    """

    机构下所有信息
    """
    admins = serializers.SlugRelatedField(slug_field='id', many=True, read_only=True)
    users = serializers.SlugRelatedField(slug_field='id', many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'


class ProductRoleReadSerializer(ModelSerializer):
    """

    产品角色（目前产品管理员）
    """
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = ProductRole
        fields = '__all__'


class ProductRoleSerializer(ModelSerializer):
    """

    产品角色（目前产品管理员）
    """

    class Meta:
        model = ProductRole
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'updated_at', 'org', 'product', 'role']


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'logo', ]

# -*- coding: utf-8 -*-
#
from collections import OrderedDict
from django.db import transaction
from rest_framework import serializers

from orgs.utils import get_current_org

from .models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'password',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'username', 'email',
            'avatar_url', 'wechat', 'phone',
            'description', 'source',
            'is_valid', 'is_expired', 'is_active',
            'created_by', 'is_first_login', 'is_superuser', "is_org_admin",
            'date_password_last_updated', 'date_expired', 'date_joined', 'authority'
        ]


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'phone', 'avatar'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'username', 'email', 'avatar_url', 'wechat', 'phone', 'org', 'is_org_admin',
            'is_superuser', 'authority'
        ]
        read_only_fields = ['id', 'name', "email", "org"]

    org = serializers.SerializerMethodField()

    def get_org(self, obj):
        return {
            "id": get_current_org().id,
            "name": get_current_org().name,
            "description": get_current_org().description
            # "logo": get_current_org().logo.url
        }


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class UserProfilePasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True, write_only=True)
    new_password = serializers.CharField(max_length=128, required=True, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=128, required=True, min_length=6, write_only=True)

    def to_representation(self, instance):
        return OrderedDict()


class UserCreateSerializer(serializers.Serializer):
    """

    新建用户
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
        user = User(username=validated_data['username'], email=validated_data['email'], name=validated_data['name']);
        user.set_password(validated_data['password'])
        user.created_by = 'System'
        with transaction.atomic():
            user.save()
            if validated_data['type'] == self.ROLE_ADMIN:
                user.admin_orgs.add(get_current_org().id)
            if validated_data['type'] == self.ROLE_USER:
                user.orgs.add(get_current_org().id)
        validated_data['date_expired'] = user.date_expired
        validated_data['id'] = user.id
        validated_data['name'] = user.name
        validated_data['authority'] = user.authority
        return validated_data

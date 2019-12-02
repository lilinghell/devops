from django.db import transaction
from rest_framework import serializers

from .models import TestEnv, TestGroup, TestCase, Test, TestPlan, TestAutoPlan


class TestEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEnv
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.save()
            return instance


class TestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestGroup
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']


class TestAutoPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAutoPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'org']

from rest_framework import serializers
from revauth.settings import api_settings


class ValidationSerializer(serializers.Serializer):
    identity = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField()
    access_token = serializers.CharField()


class ProfileJWTSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    id = serializers.CharField()

    def get_groups(self, obj):
        if obj.is_staff:
            return ['admin']
        return []

    class Meta:
        model = api_settings.DEFAULT_PROFILE_CLASS
        fields = serializers.ALL_FIELDS


class SocialSerializer(serializers.Serializer):
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    identity = serializers.CharField()
    password = serializers.CharField()

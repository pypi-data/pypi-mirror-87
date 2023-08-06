from django.conf import settings
from django.http import HttpResponse
from rest_framework import response
from django.contrib.auth.models import User
from revauth.settings import api_settings
import json


class SocialSDK:
    social_type = None
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_provider_class(self):
        from .providers import FacebookProvider, GoogleProvider, AppleProvider
        if self.social_type == 'facebook':
            return FacebookProvider
        elif self.social_type == 'google':
            return GoogleProvider
        elif self.social_type == 'apple':
            return AppleProvider

    def get_provider(self):
        provider_class = self.get_provider_class()
        return provider_class()

    def login(self, token, **kwargs):
        provider = self.get_provider()
        profile = provider.login(token, **kwargs)
        handler = self.handler_class()
        result = handler.on_login_success(profile)
        return response.Response(result, 200)

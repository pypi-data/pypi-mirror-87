from django.db import models
from revauth.settings import api_settings
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User


class BaseProfile(models.Model):
    PROVIDERS = (('default', 'default'), ('facebook', 'facebook'), ('google', 'google'), ('apple', 'apple'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=api_settings.DEFAULT_IDENTITY != 'email', blank=api_settings.DEFAULT_IDENTITY != 'email')
    phone = models.CharField(max_length=128, null=api_settings.DEFAULT_IDENTITY != 'phone', blank=api_settings.DEFAULT_IDENTITY != 'phone')
    is_staff = models.BooleanField(default=False)
    avatar = models.URLField(blank=True, null=True)
    provider = models.CharField(max_length=128, choices=PROVIDERS, default='default')
    social_id = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        abstract = True


class UserProfile(BaseProfile):
    class Meta:
        abstract = 'revauth' not in settings.INSTALLED_APPS
        app_label = 'revauth'


if not UserProfile._meta.abstract:
    admin.site.register(UserProfile)

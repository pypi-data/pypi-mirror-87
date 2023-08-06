from django.conf import settings
from revauth.settings import api_settings
import urllib
import requests
from django.contrib.auth.models import User
from uuid import uuid4
from revauth.jwt import GoogleCryptor, AppleCryptor
import jwt


class BaseProvider:
    PROFILE_URL = None
    PROFILE_PARAMS = None
    VERSION=api_settings.AUTH_VERSION
    profile_class = api_settings.DEFAULT_PROFILE_CLASS
    handler_class = api_settings.DEFAULT_HANDLER_CLASS
    provider = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_profile(self, access_token, **kwargs):
        params = self.PROFILE_PARAMS.format(access_token=access_token, **kwargs)
        resp = requests.get(self.PROFILE_URL + params)
        resp_json = resp.json()
        resp.raise_for_status()
        return resp_json

    def map_profile_data(self, data):
        raise NotImplementedError('map profile data')

    def process_login(self, name, social_id, email='', phone='', **kwargs):
        profile = self.profile_class.objects.filter(provider=self.provider, social_id=social_id).last()
        if not profile:
            user = User.objects.create_user(username=uuid4().__str__())
            try:
                profile = user.profile
            except:
                profile = self.profile_class.objects.create(user=user, email=email, phone=phone, name=name, provider=self.provider, social_id=social_id)

        return profile
    
    def login(self, token, **kwargs):
        profile_data = self.get_profile(token)
        mapped = self.map_profile_data(profile_data)
        profile = self.process_login(**mapped)
        return profile

    def get_avatar(self, **data):
        raise NotImplementedError


class FacebookProvider(BaseProvider):
    PROFILE_URL = 'https://graph.facebook.com/v8.0/me'
    PROFILE_PARAMS = '?access_token={access_token}&fields=id,name,email'
    provider = 'facebook'

    def map_profile_data(self, data):
        return {
            'social_id': data['id'],
            **data
        }


class GoogleProvider(BaseProvider):
    PROFILE_URL = 'https://people.googleapis.com/v1/people/me'
    PROFILE_PARAMS = '?personFields=emailAddresses,names&access_token={access_token}'
    cryptor_class = GoogleCryptor
    provider = 'google'

    def get_profile(self, access_token):
        headers = jwt.get_unverified_header(access_token)
        cryptor = self.cryptor_class(headers)
        return cryptor.decode(access_token)

    def map_profile_data(self, data):
        return {
            'social_id': data['sub'],
            'email': data['email'],
            'name': data['name']
        }


class AppleProvider(BaseProvider):
    provider = 'apple'
    cryptor_class = AppleCryptor

    def get_profile(self, access_token):
        headers = jwt.get_unverified_header(access_token)
        cryptor = self.cryptor_class(headers)
        return cryptor.decode(access_token)
    
    def map_profile_data(self, data):
        return {
            'social_id': data['sub'],
            'email': data['name']
        }

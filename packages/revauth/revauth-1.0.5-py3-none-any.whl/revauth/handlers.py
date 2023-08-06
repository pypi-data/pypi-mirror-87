from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from revauth import exceptions
from rest_framework import response
from revauth.settings import api_settings
from revauth.jwt import JWTCryptor
from revauth.serializers import ProfileJWTSerializer
from django.db.utils import IntegrityError
import requests
from django.conf import settings
from jwt import decode, get_unverified_header


class BaseHandler:
    jwt_serializer_class = ProfileJWTSerializer
    profile_class = api_settings.DEFAULT_PROFILE_CLASS
    identity_type = api_settings.DEFAULT_IDENTITY
    issuer = api_settings.DEFAULT_VALIDATION_ISSUER
    DEBUG = settings.DEBUG
    auth_version = api_settings.AUTH_VERSION

    @property
    def auth_host(self):
        if self.DEBUG:
            return f'https://auth-stg.revtel-api.com/{self.auth_version}/validation/request?issuer={self.issuer}&client_id={settings.CLIENT_ID}'
        return f'https://auth.revtel-api.com/{self.auth_version}/validation/request?issuer={self.issuer}&client_id={settings.CLIENT_ID}'

    def send_validation(self, identity):
        resp = requests.post(self.auth_host, json={'identity': identity})
        resp_json = resp.json()
        resp.raise_for_status()
        return resp_json

    def validate(self, identity):
        user = User.objects.filter(username=identity)
        if user:
            raise exceptions.UserExistsError
        return self.send_validation(identity)

    def on_register(self, **kwargs):
        raise NotImplementedError('on_register')

    def on_login_success(self, profile):
        raise NotImplementedError('on_profile_create')

    def perform_register(self, **kwargs):
        try:
            token = kwargs['access_token']
            unverified = decode(token, verify=False)
            headers = get_unverified_header(token)
            decoded = JWTCryptor(headers, unverified).decode_register(token)
        except:
            raise exceptions.JWTDecodeError

        profile = self.on_register(decoded=decoded, **kwargs)
        resp = self.on_login_success(profile)
        return response.Response(resp, 200)

    def login(self, identity, password):
        user = authenticate(username=identity, password=password)
        if not user:
            raise exceptions.UserNotFoundError
        profile = user.profile
        result = self.on_login_success(profile)
        return result


class DefaultHandler(BaseHandler):
    def on_register(self, decoded, password, **kwargs):
        try:
            iss, version = decoded['iss'].split('/')
            if version not in ['v1', 'v2']:
                identity = decoded['sub']
            else:
                identity = decoded['idy']
            user = User.objects.create_user(username=identity, password=password)
        except IntegrityError:
            raise exceptions.UserExistsError
        except KeyError:
            raise exceptions.JWTDecodeError

        data = {self.identity_type: identity}
        try:
            profile = user.profile
        except:
            profile = self.profile_class.objects.create(user=user)

        for key, value in data.items():
            setattr(profile, key, value)

        profile.save()

        return profile

    def on_login_success(self, profile):
        serialized = self.jwt_serializer_class(profile).data
        tokens = JWTCryptor().encode(serialized)
        return {**tokens, **serialized}

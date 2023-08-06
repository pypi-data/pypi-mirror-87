from rest_framework import views, response, permissions, generics
from revauth.settings import api_settings
from .serializers import SocialSerializer, ValidationSerializer, ProfileJWTSerializer, LoginSerializer
from revauth import exceptions
from revauth.socials import SocialSDK
from rest_framework import views
from django.conf import settings


class ValidationView(views.APIView):
    permission_classes = ()
    serializer_class = ValidationSerializer
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']
        handler = self.handler_class()
        result = handler.validate(identity)
        return response.Response(result, 200)


class UserLogin(views.APIView):
    permission_classes = ()
    serializer_class = LoginSerializer
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        handler = self.handler_class()
        result = handler.login(identity=data['identity'], password=data['password'])
        return response.Response(result, 200)


class UserRegister(views.APIView):
    profile_class = api_settings.DEFAULT_PROFILE_CLASS
    permission_classes = ()
    serializer_class = api_settings.DEFAULT_REGISTER_SERIALIZER
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise exceptions.SerializerError

        handler = self.handler_class()
        return handler.perform_register(**serializer.validated_data)


class BaseSocialView(views.APIView):
    permission_classes = ()
    provider = None
    serializer_class = SocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = SocialSDK(social_type=self.provider)
        return client.login(serializer.validated_data['token'])


class FacebookLogin(BaseSocialView):
    provider = 'facebook'


class GoogleLogin(BaseSocialView):
    provider = 'google'


class AppleLogin(BaseSocialView):
    provider = 'apple'


class RefreshProfile(views.APIView):
    serializer_class = ProfileJWTSerializer
    permission_classes = ()
    profile_class = api_settings.DEFAULT_PROFILE_CLASS

    def post(self, request):
        profile_id = self.request.data.get('user')
        key = request.query_params.get('api_key')
        if key != settings.CLIENT_SECRET:
            raise exceptions.APIKeyError

        try:
            profile = self.profile_class.objects.get(id=profile_id)
        except:
            raise exceptions.UserNotFoundError

        serializer = self.serializer_class(profile)
        resp = serializer.data
        return response.Response(resp, 200)

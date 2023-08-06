from django.conf import settings
from django.http import HttpResponse
from api.models.redirect_state import RedirectState
from django.shortcuts import get_object_or_404, redirect
from authorization.models.user_profile import UserProfile
from django.contrib.auth.models import User
import json
from ..utils.getUniIdentifier import getUniIdentifier
from ..utils.url import add_url_query
from django.conf import settings


class SignInSDK:
    social_type = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_provider_class(self):
        from .providers import FacebookProvider, GoogleProvider
        if self.social_type == 'facebook':
            return FacebookProvider
        elif self.social_type == 'google':
            return GoogleProvider

    def get_provider(self):
        provider_class = self.get_provider_class()
        return provider_class(API_KEY=settings.API_KEY)

    def get_callback_url(self, state):
        return '{}/auth/{}/callback?state={}'.format(settings.API_HOST, self.social_type, state)

    def request(self, req_redirect_url, is_mobile=False):
        provider = self.get_provider()
        state = RedirectState.objects.create(
            redirect_url=req_redirect_url,
            is_mobile=is_mobile
        )
        callback_url = self.get_callback_url(state=state.state)
        url = provider.request(state=state, callback_url=callback_url)
        return redirect(url)

    def callback(self, request):
        provider = self.get_provider()
        state = request.query_params.get('state')
        state = get_object_or_404(RedirectState, state=state)
        access_token = request.query_params.get('token')
        error = request.query_params.get('error')
        if error:
            return self.error_resp()

        meta = provider.get_profile(access_token)
        meta['social_type'] = meta.get('provider')

        token = self.on_login_success(
            social_type=self.social_type,
            social_id=meta.get('social_id'),
            meta=meta
        )

        if state.is_mobile:
            return self.static_result_view(token)

        result_url = self.get_result_url(state, token)
        return redirect(result_url)

    def on_login_success(self, social_id, meta: dict):
        profile = UserProfile.objects.filter(social_id=social_id,
                                             social_type=self.social_type).first()
        if not profile:
            user = User.objects.create_user(username=getUniIdentifier(User.objects, field_name='username'))
            profile = user.profile
        for k, v in meta.items():
            if k == 'id':
                continue
            if hasattr(profile, k):
                setattr(profile, k, v)
        profile.save()
        return profile.user.auth_token.key

    def error_resp(self, is_mobile=False):
        if is_mobile:
            return self.static_failure_view()
        return redirect(settings.WEB_HOST + '?error=failed')

    def random_string_digits(self, string_length=12):
        import string
        import random
        """Generate a random string of letters and digits """
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(string_length))

    def static_result_view(self, token):
        html = '''
            <html>
            <head>
            </head>
            <body style="display: flex; flex-direction: column; align-items: center;">
              <img src="{}/static/telu-logo.png" width="250px" style="display: block; margin: 60px auto 10px;"/>
                <h1 style="text-align: center; color: #0069AB; font-size: 50px;">登入成功</h1>
            <img src="{}/static/telu-icon.png" width="250px" style="display: block; margin: 60px auto 10px;"/>
            <p style="font-size: 40px;text-align: center; color: #0069AB; letter-spacing: 20px;margin-bottom: 300px;">在此開啟您的全球漫遊服務</p>

              <a href="{}://social-signin?token={}"
                style="font-size: 40px; width: 200px; border-radius: 40px;color: #ffffff; background-color:#0069AB; padding: 20px 80px; text-decoration: none; text-align: center;" >
                開啟App
              </a>
            </body>
            </html>



            '''.format(settings.API_HOST,
                       settings.API_HOST,
                       settings.IOS_BUNDLE_ID, token)
        return HttpResponse(html)

    def static_failure_view(self, **kwargs):
        html = '''
                <html>
                <head>
                </head>
                <body style="display: flex; flex-direction: column; align-items: center;">
                  <img src="{}/static/telu-logo.png" width="250px" style="display: block; margin: 60px auto 10px;"/>
                    <h1 style="text-align: center; color: red; font-size: 50px;">登入失敗</h1>
                <img src="{}/static/telu-icon.png" width="250px" style="display: block; margin: 60px auto 10px;"/>
                <p style="font-size: 40px;text-align: center; color: #0069AB; letter-spacing: 20px;margin-bottom: 300px;">在此開啟您的全球漫遊服務</p>
                <a href="{}://social-signin"
                style="font-size: 40px; width: 200px; border-radius: 40px;color: #ffffff; background-color:#0069AB; padding: 20px 80px; text-decoration: none; text-align: center;" >
                開啟App
              </a>
                </body>
                </html>
            '''.format(settings.API_HOST,
                       settings.API_HOST,
                       settings.IOS_BUNDLE_ID)
        return HttpResponse(html)

    def get_result_url(self, state, token, **kwargs):
        result_url = add_url_query(url=state.redirect_url,
                                   token=token
                                   )
        return result_url

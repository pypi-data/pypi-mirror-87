from django.urls import path
from revauth import views

urlpatterns = [
    path('google', views.GoogleLogin.as_view(), name='auth-google'),
    path('facebook', views.FacebookLogin.as_view(), name='auth-facebook'),
    path('apple', views.AppleLogin.as_view(), name='auth-apple'),
    path('validation/request', views.ValidationView.as_view(), name='auth-validation'),
    path('user/register', views.UserRegister.as_view(), name='auth-register'),
    path('user/login', views.UserLogin.as_view(), name='auth-login'),
    path('user/refresh', views.RefreshProfile.as_view(), name='auth-refresh'),
]

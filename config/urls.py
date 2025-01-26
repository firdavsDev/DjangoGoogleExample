from django.contrib import admin
from django.urls import include, path

from google_custom_aut.views import oauth_callback

from .views import auth_receiver, index, login, signup

urlpatterns = [
    path("", index, name="index"),
    path("drive/", include("google_custom_aut.urls")),
    path("admin/", admin.site.urls),
    path("accounts/signup/", signup, name="account_signup"),
    path("accounts/login/", login, name="account_login"),
    path("accounts/google/login/callback/", oauth_callback, name="auth_receiver"),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth.socialaccount.urls")),
]

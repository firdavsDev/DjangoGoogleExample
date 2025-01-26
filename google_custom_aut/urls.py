from django.urls import path

from .views import google_auth, oauth_callback, upload_file, upload_to_drive

urlpatterns = [
    path("upload/", upload_file, name="upload_file"),
    path("google-auth/", google_auth, name="google_auth"),
    path("oauth/callback/", oauth_callback, name="oauth_callback"),
    path("upload-to-drive/", upload_to_drive, name="upload_to_drive"),
]

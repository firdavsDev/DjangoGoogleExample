import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.settings import client_secrets_file


# Create your views here.
def upload_file(request):
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        request.session["uploaded_file_path"] = os.path.join(
            settings.MEDIA_ROOT, filename
        )
        return redirect("google_auth")
    return render(request, "upload.html")


def google_auth(request):
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=["https://www.googleapis.com/auth/drive.file"],
        redirect_uri=settings.REDIRECT_URI,
    )
    auth_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    request.session["state"] = state
    return redirect(auth_url)


def oauth_callback(request):
    state = request.session.get("state")
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=["https://www.googleapis.com/auth/drive.file"],
        state=state,
        redirect_uri=settings.REDIRECT_URI,
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect("upload_to_drive")


def upload_to_drive(request):
    credentials = request.session.get("credentials")
    if not credentials:
        return redirect("google_auth")

    creds = Credentials(**credentials)
    service = build("drive", "v3", credentials=creds)

    file_path = request.session.get("uploaded_file_path")
    if not file_path:
        return JsonResponse({"status": "No file found to upload!"})

    file_metadata = {"name": os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype="application/pdf")
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return JsonResponse(
        {"status": "File uploaded successfully!", "file_id": file.get("id")}
    )

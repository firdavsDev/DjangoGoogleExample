# django login form
import requests
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport import requests
from google.oauth2 import id_token

from .settings import SOCIALACCOUNT_PROVIDERS


def index(request):
    return render(request, "index.html")


def signup(request):
    context = {
        "form": UserCreationForm(),
    }
    return render(request, "signup.html", context)


def login(request):
    context = {
        "form": AuthenticationForm(),
    }
    return render(request, "login.html", context)


@csrf_exempt  # csrf_exempt decorator is used to disable csrf token for this view. csrt token is used to prevent cross site request forgery attacks.
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print("Inside")
    print(request.POST)
    token = request.POST["credential"]

    try:
        user_data = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"],
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    # auth.login(request, user)
    request.session["user_data"] = user_data

    return redirect("index")

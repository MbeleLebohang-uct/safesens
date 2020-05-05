from django.http import HttpResponse
from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator

from .models import User

def account_confirm_view(request):
    email = request.GET.get("email", None)
    token = request.GET.get("token", None)

    if email == None or token == None:
        return HttpResponse("<h1>Somethis went wrong. Contact the admin. Email or token could not be found.</h1>")

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("<h1>User with this email doesn't exist.</h1>")
        
    if not default_token_generator.check_token(user, token):
        return HttpResponse("<h1>Invalid or expired token.</h1>")

    user.is_active = True
    user.save(update_fields=["is_active"])

    return HttpResponse("<h1>You account is now active</h1>")
from django.conf import settings
from django.shortcuts import render, redirect

from rest_framework import status

from . import request_handler
from .utils import redirect_to_landing, redirect_to_login

from users.models import User


def index(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    user.load_examinations()
    locations = user.get_permitted_locations()


    context = {
        'session_user': user,
        'filter_locations': locations,
    }
    return render(request, 'home/index.html', context)


def login_callback(request):
    token_response = request_handler.create_session(request.GET.get('code'))
    response = redirect_to_landing()
    id_token = token_response.json().get('id_token')
    auth_token = token_response.json().get('access_token')
    response.set_cookie(settings.AUTH_TOKEN_NAME, auth_token)
    response.set_cookie(settings.ID_TOKEN_NAME, id_token)
    return response


def login(request):
    context = {
        'page_heading': 'Welcome to the Medical Examiners Service',
        'base_uri': settings.OP_DOMAIN,
        'client_id': settings.OP_ID,
        'cms_url': settings.CMS_URL,
        'issuer': settings.OP_ISSUER
    }
    status_code = status.HTTP_200_OK

    user = User.initialise_with_token(request)
    if user.check_logged_in():
        return redirect_to_landing()

    return render(request, 'home/login.html', context, status=status_code)


def logout(request):
    user = User.initialise_with_token(request)
    user.logout()

    response = redirect_to_login()
    response.delete_cookie(settings.AUTH_TOKEN_NAME)
    response.delete_cookie(settings.ID_TOKEN_NAME)
    return response


def settings_index(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    context = {
        'session_user': user,
        'page_heading': 'Settings',
        'sub_heading': 'Overview',
    }
    return render(request, 'home/settings_index.html', context)

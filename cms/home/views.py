from django.conf import settings
from django.shortcuts import render, redirect

from rest_framework import status

from home.forms import IndexFilterForm
from locations.models import Location
from . import request_handler
from .utils import redirect_to_landing, redirect_to_login

from users.models import User


def index(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    people = False

    if request.method == 'GET':
        user.load_examinations()
        form = IndexFilterForm()
    elif request.method == 'POST':
        form = IndexFilterForm(request.POST)
        user.load_examinations(location=form.location, person=form.person)
        filter_location = Location.initialise_with_id(request.POST.get('location'))
        people = filter_location.load_permitted_users(user.auth_token)
    locations = user.get_permitted_locations()

    context = {
        'page_header': '%s Dashboard' % user.role_type,
        'session_user': user,
        'filter_locations': locations,
        'filter_people': people,
        'form': form
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

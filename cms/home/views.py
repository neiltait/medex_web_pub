from django.conf import settings
from django.shortcuts import render, redirect

from rest_framework import status

from errors.utils import log_unexpected_method
from errors.views import __handle_method_not_allowed_error, __handle_not_permitted_error
from home.forms import IndexFilterForm
from . import request_handler
from .utils import redirect_to_landing, redirect_to_login

from users.models import User


def index(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'GET':
        template, context, status_code = __get_index(user)

    elif request.method == 'POST':
        template, context, status_code = __post_index(user, request.POST)

    else:
        log_unexpected_method(request.method, 'case index')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_index(user):
    template = 'home/index.html'
    status_code = status.HTTP_200_OK
    page_size = 20
    page_number = 1

    form = IndexFilterForm(user.default_filter_options())
    user.load_examinations(page_size, page_number)

    context = __set_index_context(user, form)

    return template, context, status_code


def __post_index(user, post_body):
    template = 'home/index.html'
    status_code = status.HTTP_200_OK
    page_size = 20
    page_number = 1

    form = IndexFilterForm(post_body)
    user.load_examinations(page_size, page_number, location=form.location, person=form.person)

    context = __set_index_context(user, form)

    return template, context, status_code


def __set_index_context(user, form):
    return {
        'page_header': '%s Dashboard' % user.role,
        'session_user': user,
        'form': form,
    }


def login_callback(request):
    token_response = request_handler.create_session(request.GET.get('code'))
    response = redirect_to_landing()
    id_token = token_response.json().get('id_token')
    auth_token = token_response.json().get('access_token')
    response.set_cookie(settings.AUTH_TOKEN_NAME, auth_token)
    response.set_cookie(settings.ID_TOKEN_NAME, id_token)
    return response


def login(request):
    user = User.initialise_with_token(request)
    if user.check_logged_in():
        return redirect_to_landing()

    if request.method == "GET":
        template = 'home/login.html'
        status_code = status.HTTP_200_OK
        context = {
            'page_heading': 'Welcome to the Medical Examiners Service',
            'base_uri': settings.OP_DOMAIN,
            'client_id': settings.OP_ID,
            'cms_url': settings.CMS_URL,
            'issuer': settings.OP_ISSUER,
        }
    else:
        log_unexpected_method(request.method, 'login')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


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
    if not user.permitted_actions.can_access_settings_index():
        template, context, status_code = __handle_not_permitted_error(user)

    elif request.method == 'GET':
        template = 'home/settings_index.html'
        status_code = status.HTTP_200_OK
        context = {
            'session_user': user,
            'page_heading': 'Settings',
            'sub_heading': 'Overview',
        }
    else:
        log_unexpected_method(request.method, 'settings index')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)

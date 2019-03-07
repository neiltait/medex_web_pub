from django.conf import settings
from django.shortcuts import render, redirect

from rest_framework import status

import json

from alerts import messages
from alerts.utils import generate_error_alert, generate_success_alert, generate_info_alert

from . import request_handler
from .forms import ForgottenPasswordForm
from .utils import redirect_to_landing, redirect_to_login

from users.models import User


def index(request):
  user = User.initialise_with_token(request)
  if not user.check_logged_in():
    return redirect_to_login()
    
  context = {
      'session_user': user,
      'case_list': 'All your current open cases',
  }
  return render(request, 'home/index.html', context)


def login_callback(request):
  token_response = request_handler.create_session(request.GET.get('code'))
  response = redirect_to_landing()
  response.set_cookie(settings.AUTH_TOKEN_NAME, json.dumps(token_response.json()))
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
  return response


def forgotten_password(request):
  context = {
    'page_heading': 'Welcome to the Medical Examiners Service'
  }
  alerts = []
  status_code = status.HTTP_200_OK

  if(request.POST):
    form = ForgottenPasswordForm(request.POST)
    if form.is_valid():
      return redirect('/reset-sent')
    else:
      alerts.append(generate_error_alert(messages.MISSING_EMAIL))
      status_code = status.HTTP_400_BAD_REQUEST
      context['invalid'] = True

  context['alerts'] = alerts
  return render(request, 'home/forgotten-password.html', context, status=status_code)


def reset_sent(request):
  context = {
    'page_heading': 'Welcome to the Medical Examiners Service',
    'content': messages.FORGOTTEN_PASSWORD_SENT
  }
  return render(request, 'home/reset-sent.html', context)


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

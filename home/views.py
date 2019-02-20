from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert, generate_success_alert, generate_info_alert

from .forms import LoginForm, ForgottenPasswordForm
from .utils import check_logged_in, redirect_to_landing, redirect_to_login

def index(request):
  if not check_logged_in(request):
    return redirect_to_login()
    
  context = {
      'session_user': {
        'name': 'Andrea Smith',
        'role': 'MEO'
      },
      'case_list': 'All your current open cases',
  }
  return render(request, 'home/index.html', context)


def login(request):
  context = {
    'page_heading': 'Welcome to the Medical Examiners Service'
  }
  alerts = []
  status_code = status.HTTP_200_OK
  if check_logged_in(request):
    return redirect_to_landing()

  if (request.POST):
    form = LoginForm(request.POST)
    context['email_address'] = form.email_address
    if form.is_valid():
      if form.is_authorised():

        response = redirect_to_landing()
        response.set_cookie(settings.AUTH_TOKEN_NAME, form.auth_token)
        # ## TODO implement user 'Remember me' when better defined and connect to API
        # # if form.persist_user:
        return response
      else:
        alerts.append(generate_error_alert(messages.INVALID_CREDENTIALS))
        status_code = status.HTTP_401_UNAUTHORIZED
    else:
      alerts.append(generate_error_alert(messages.MISSING_CREDENTIALS))
      status_code = status.HTTP_401_UNAUTHORIZED

    context['invalid'] = True

  context['alerts'] = alerts
  return render(request, 'home/login.html', context, status=status_code)


def logout(request):
  #TODO submit logout request to OCTA

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
      alerts.append(generate_info_alert(messages.FORGOTTEN_PASSWORD_SENT))
    else:
      alerts.append(generate_error_alert(messages.MISSING_EMAIL))
      status_code = status.HTTP_400_BAD_REQUEST

  context['alerts'] = alerts
  return render(request, 'home/forgotten-password.html', context, status=status_code)


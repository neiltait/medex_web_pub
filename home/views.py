from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert, generate_success_alert, generate_info_alert

from .forms import LoginForm, ForgottenPasswordForm, ForgottenUserIdForm

def index(request):
  context = {
      'session_user': {
        'name': 'Andrea Smith',
        'role': 'MEO'
      },
      'case_list': 'All your current open cases',
  }
  return render(request, 'home/index.html', context)


def login(request):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK

  if (request.POST):
    form = LoginForm(request.POST)
    context['user_id'] = form.user_id
    if form.is_valid():
      if form.is_authorised():
        return redirect('/')
      else:
        alerts.append(generate_error_alert(messages.INVALID_CREDENTIALS))
        status_code = status.HTTP_401_UNAUTHORIZED
    else:
      alerts.append(generate_error_alert(messages.MISSING_CREDENTIALS))
      status_code = status.HTTP_401_UNAUTHORIZED

  context['alerts'] = alerts
  return render(request, 'home/login.html', context, status=status_code)


def logout(request):
  #TODO submit logout request to OCTA

  return redirect('/login')


def forgotten_password(request):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK

  if(request.POST):
    form = ForgottenPasswordForm(request.POST)
    if form.is_valid():
      alerts.append(generate_info_alert(messages.FORGOTTEN_PASSWORD_SENT))
    else:
      alerts.append(generate_error_alert(messages.MISSING_USER_ID))
      status_code = status.HTTP_400_BAD_REQUEST

  context['alerts'] = alerts
  return render(request, 'home/forgotten-password.html', context, status=status_code)

def forgotten_userid(request):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK

  if(request.POST):
    form = ForgottenUserIdForm(request.POST)
    if form.is_valid():
      alerts.append(generate_info_alert(messages.FORGOTTEN_ID_SENT))
    else:
      alerts.append(generate_error_alert(messages.MISSING_EMAIL))
      status_code = status.HTTP_400_BAD_REQUEST

  context['alerts'] = alerts
  return render(request, 'home/forgotten-userid.html', context, status=status_code)

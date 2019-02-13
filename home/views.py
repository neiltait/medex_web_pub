from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from rest_framework import status

from alerts import messages

from .forms import LoginForm

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
  errors = []
  status_code = status.HTTP_200_OK

  if (request.POST):
    form = LoginForm(request.POST)
    context['user_id'] = form.user_id
    if form.is_valid():
      if form.is_authorised():
        return redirect('/')
      else:
        errors.append(messages.INVALID_CREDENTIALS)
        status_code = status.HTTP_401_UNAUTHORIZED
    else:
      errors.append(messages.MISSING_CREDENTIALS)
      status_code = status.HTTP_401_UNAUTHORIZED

  context['errors'] = errors
  return render(request, 'home/login.html', context, status=status_code)


def logout(request):
  #TODO submit logout request to OCTA

  return redirect('/login')


def forgotten_password(request):
  context = {}
  return render(request, 'home/forgotten-password.html', context)

def forgotten_userid(request):
  context = {}
  return render(request, 'home/forgotten-userid.html', context)

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from errors import messages, status

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
  status_code = status.success()

  if (request.POST):
    form = LoginForm(request.POST)
    context['user_id'] = form.user_id
    if form.is_valid():
      if form.is_authorised():
        return redirect('/')
      else:
        errors.append(messages.invalid_credentials())
        status_code = status.unauthorised()
    else:
      errors.append(messages.missing_credentials())
      status_code = status.unauthorised()

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

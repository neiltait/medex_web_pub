from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from django.conf import settings


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

  if (request.POST):
    user_id = request.POST.get('user_id')
    password = request.POST.get('password')
    context['user_id'] = user_id
    details_present = True if user_id and password else False
    if details_present:
      # TODO submit details to OCTA
      # Temporary auth check until we have OCTA integrated
      # may need to add in an attempt check if OCTA doesn't have one.
      if user_id == 'Matt' and password == 'Password':
        return redirect('/')
      else:
        errors.append('Invalid User ID and/or Password entered')
    else:
      errors.append('Please enter a User ID and Password')

  context['errors'] = errors
  return render(request, 'home/login.html', context)


def logout(request):
  #TODO submit logout request to OCTA

  return redirect('/login')

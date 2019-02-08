from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from django.conf import settings


def index(request):
  context = {
      'user': {
        'name': 'Andrea Smith',
        'role': 'MEO'
      },
      'case_list': 'All your current open cases',
  }
  return render(request, 'home/index.html', context)


def login(request):
  return HttpResponse('Login to access your cases')

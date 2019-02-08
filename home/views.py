from django.http import HttpResponse
from django.shortcuts import render
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
  return render(request, 'home/login.html', context)

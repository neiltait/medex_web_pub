from django.conf import settings
from django.shortcuts import redirect


def redirect_to_landing():
  return redirect('/')

def redirect_to_login():
  return redirect('/login')

from django.shortcuts import render, redirect

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from locations.request_handler import load_trusts_list

from home.utils import redirect_to_login

from .models import User


def create_user(request):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  trust_list = load_trusts_list()

  context = {
    'session_user': user,
    'page_heading': 'Add a user',
    'trusts': trust_list
  }
  alerts = []
  status_code = status.HTTP_200_OK

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)

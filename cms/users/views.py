from django.shortcuts import render, redirect

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from home.utils import redirect_to_login

from .models import User


def create_user(request):
  context = {}
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  alerts = []
  status_code = status.HTTP_200_OK

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)

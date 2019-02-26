from django.shortcuts import render, redirect

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from .models import User


def create_user(request):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)

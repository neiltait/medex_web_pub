from django.shortcuts import render, redirect

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from .forms import UserLookupForm
from .models import User

def user_lookup(request):
  context = {
    'session_user': {
      'name': 'Andrea Smith',
      'role': 'MEO'
    },
  }
  alerts = []
  status_code = status.HTTP_200_OK

  if (request.POST):
    form = UserLookupForm(request.POST)
    if (form.is_valid()):
      loaded_user = User.load_by_email(form.email_address)
      if (loaded_user):
        return redirect('/users/manage/' + loaded_user.user_id)
      else:
        return redirect('/users/new')
    else:
      alerts.append(generate_error_alert(messages.MISSING_EMAIL))
      status_code = status.HTTP_400_BAD_REQUEST

  context['alerts'] = alerts
  return render(request, 'users/lookup.html', context, status=status_code)

def manage_user(request, user_id):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK
  managed_user = User.load_by_user_id(user_id)

  if not managed_user:
    alerts.append(generate_error_alert(messages.OBJECT_NOT_FOUND % 'user'))
    status_code = status.HTTP_404_NOT_FOUND

  context['alerts'] = alerts
  context['managed_user'] = managed_user
  return render(request, 'users/manage.html', context, status=status_code)

def create_user(request):
  context = {}
  alerts = []
  status_code = status.HTTP_200_OK

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)

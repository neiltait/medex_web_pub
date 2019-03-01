from django.shortcuts import render, redirect

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from locations.request_handler import load_trusts_list

from home.utils import redirect_to_landing, redirect_to_login

from . import request_handler
from .forms import CreateUserForm
from .models import User


def create_user(request):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  trust_list = load_trusts_list()

  context = {
    'session_user': user,
    'page_heading': 'Add a user',
    'trusts': trust_list,
    'form': CreateUserForm()
  }
  alerts = []
  status_code = status.HTTP_200_OK

  if request.POST:
    form = CreateUserForm(request.POST)

    if form.validate():
      response = request_handler.create_user({'email': form.email_address})

      if response.status_code == status.HTTP_200_OK:
        return redirect_to_landing()
      else:
        alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
        status_code = response.status_code
    else:
      alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
      status_code = status.HTTP_400_BAD_REQUEST

    context['form'] = form
    context['invalid'] = True

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)

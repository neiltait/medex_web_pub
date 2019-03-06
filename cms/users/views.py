from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert

from locations import request_handler as locations_request_handler

from home.utils import redirect_to_landing, redirect_to_login

from . import request_handler
from .forms import CreateUserForm, PermissionBuilderForm
from .models import User


def create_user(request):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  context = {
    'session_user': user,
    'page_heading': 'Add a user',
    'form': CreateUserForm()
  }
  alerts = []
  status_code = status.HTTP_200_OK

  if request.POST:
    form = CreateUserForm(request.POST)

    if form.validate():

      if form.check_is_in_okta():
        response = request_handler.create_user({'email': form.email_address})

        if response.status_code == status.HTTP_200_OK:
          return redirect('/users/%s/add_permission' % response.json()['id'])
        else:
          alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
          status_code = response.status_code
      else:
        alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
        status_code = status.HTTP_404_NOT_FOUND
    else:
      alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
      status_code = status.HTTP_400_BAD_REQUEST

    context['form'] = form
    context['invalid'] = True

  context['alerts'] = alerts
  return render(request, 'users/new.html', context, status=status_code)


def add_permission(request, user_id):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  context = {
    'session_user': user,
    'sub_heading': 'Add role and permission level',
    'form': PermissionBuilderForm(),
    'submit_path': 'add_permission'
  }
  alerts = []
  status_code = status.HTTP_200_OK

  if request.POST:
    form = PermissionBuilderForm(request.POST)
    add_another = True if request.POST.get('add_another') == "true" else False
  
    if form.is_valid(): 
      response = request_handler.create_permission(form.to_dict(), user_id)

      if response.status_code == status.HTTP_200_OK:
        if add_another:
          return redirect('add_permission', user_id=user_id)
        else:
          return redirect('/settings')
      else:
        alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
        status_code = response.status_code

    else: 
      alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
      status_code = status.HTTP_400_BAD_REQUEST

    context['form'] = form
    context['invalid'] = True


  managed_user = User.load_by_id(user_id)
  context['managed_user'] = managed_user
    
  if managed_user == None:
    alerts.append(generate_error_alert(messages.OBJECT_NOT_FOUND % 'user'))
  else:
    context['trusts'] = locations_request_handler.load_trusts_list()
    context['regions'] = locations_request_handler.load_region_list()

  context['alerts'] = alerts
  return render(request, 'users/permission_builder.html', context, status=status_code)

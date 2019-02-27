from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

USERS = [
  {
    'session_key': 'd4ba0bbb-efd2-4fe3-8dcf-641cd2f7923d',
    'password': 'Password',
    'user_object': {
      'user_id': '1',
      'first_name': 'Matt',
      'last_name': 'Nicks',
      'email_address': 'matt.nicks@nhs.uk',
      'permissions': []
    }
  },
  {
    'session_key': '506b344b-939c-4ba1-bd26-ee5f28af607a',
    'password': 'Password',
    'user_object': { 
      'user_id': '2',
      'first_name': 'Test',
      'last_name': 'User',
      'email_address': 'tom.ridd@nhs.uk',
      'permissions': []
    }
  },
  {
    'session_key': 'e458292a-a97d-4864-9445-db40a3cd2565',
    'password': 'Password',
    'user_object': {
      'user_id': '3',
      'first_name': 'Alan',
      'last_name': 'Fletcher',
      'email_address': 'alan.fletcher@nhs.uk',
      'permissions': []
    }
  }
]


@csrf_exempt
@require_POST
def create_session(request):
  email_address = request.POST.get('email_address')
  password = request.POST.get('password')
  auth_token = None
  for user in USERS:
    if user['user_object']['email_address'] == email_address and user['password'] == password:
      auth_token = user['session_key']
  status_code = 200 if auth_token else 401
  return HttpResponse(json.dumps({'auth_token': auth_token}), content_type="application/json")


@csrf_exempt
@require_POST
def validate_session(request):
  auth_token = request.POST.get('auth_token')
  session_user = None
  for user in USERS:
    if user['session_key'] == auth_token:
      session_user = user['user_object']
  status_code = 200 if session_user else 401
  return HttpResponse(json.dumps(session_user), content_type="application/json", status=status_code)

@csrf_exempt
def users(request):
  if request.POST:
    email = request.POST.get('email')
    status_code =  200 if email != '' and email != None else 400
    return HttpResponse(json.dumps({'id': 1}), content_type="application/json", status=status_code)
  else:
    return HttpResponse('', content_type="application/json", status=404)


@csrf_exempt
@require_POST
def load_by_email(request):
  user = {
    'user_id': '1',
    'first_name': 'Test',
    'last_name': 'User',
    'email_address': 'test.user@email.com',
    'role': 'MEO',
    'permissions': [],
  }
  return HttpResponse(json.dumps(user), content_type="application/json")

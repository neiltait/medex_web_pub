from django.conf import settings

from requests.models import Response

from rest_framework import status

import json

import requests

def validate_session(cookie):
  headers = {
    'authorization' : 'bearer ' + cookie
  }
  return requests.post('%s/auth/validate-session' % settings.API_URL, headers=headers)

def create_user(user_object):
  return requests.post('%s/users' % settings.API_URL, data = user_object)

def load_by_id(user_id):
  return requests.get('%s/users/%s' % (settings.API_URL, user_id))

def create_permission(permission, user_id):
  return requests.post('%s/users/%s/permissions' % (settings.API_URL, user_id), data = permission)

def check_email_in_okta(email_address):
  ## TODO integrate with OKTA
  response = Response()
  response.status_code = status.HTTP_200_OK
  response._content = json.dumps(None).encode('utf-8')
  return response

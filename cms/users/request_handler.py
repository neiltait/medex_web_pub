from django.conf import settings

import requests

def validate_session(cookie):
  return requests.post('%s/users/validate-session' % settings.API_URL, data = {'auth_token': cookie})

def create_user(user_object):
  return requests.post('%s/users' % settings.API_URL, data = user_object)

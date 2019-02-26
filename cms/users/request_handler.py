from django.conf import settings

import requests

def validate_session(cookie):
  return requests.post('%s/users/validate-session' % settings.API_URL, data = {'auth_token': cookie})

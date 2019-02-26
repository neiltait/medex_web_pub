from django.conf import settings

import requests

def create_session(email_address, password):
  return requests.post('%s/create-session' % settings.API_URL, data = {'email_address': email_address, 'password': password})

from django.conf import settings

import requests

from rest_framework import status

import uuid

from . import request_handler

class LoginForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()
    self.password = request.get('password')
    self.persist_user = request.get('persist')

  def is_valid(self):
    return True if self.email_address and self.password else False

  def is_authorised(self):
    ## TODO submit details to OCTA

    response = request_handler.create_session(self.email_address, self.password)
    authenticated = response.status_code == status.HTTP_200_OK
    if authenticated:
      self.auth_token = response.json()['auth_token']
    
    return authenticated


class ForgottenPasswordForm():

  def __init__(self, request):
    self.email_address = request.get('email_address')


  def is_valid(self):
    return True if self.email_address else False

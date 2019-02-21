import requests
from rest_framework import status
import uuid

class LoginForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()
    self.password = request.get('password')
    self.persist_user = request.get('persist')

  def is_valid(self):
    return True if self.email_address and self.password else False

  def is_authorised(self):
    ## TODO submit details to OCTA

    # response = requests.post(settings.API_URL + '/create-session', data = {'email_address': self.email_address, 'password': self.password})
    # authenticated = response.status_code == status.HTTP_200_OK
    # if authenticated:
    #   self.auth_token = response.json['auth_token']
    
    ## Temporary auth check until we have OCTA integrated
    ## may need to add in an attempt check if OCTA doesn't have one.
    authenticated = self.email_address == 'matt' and self.password == 'Password'
    if authenticated:
      self.auth_token = uuid.uuid4()
    
    return authenticated


class ForgottenPasswordForm():

  def __init__(self, request):
    self.user_id = request.get('user_id')


  def is_valid(self):
    return True if self.user_id else False


class ForgottenUserIdForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()


  def is_valid(self):
    return True if self.email_address else False

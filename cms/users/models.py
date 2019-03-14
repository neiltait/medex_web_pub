from django.conf import settings

from rest_framework import status

from home import request_handler as home_request_handler

from . import request_handler

import json


class User():

  def __init__(self, obj_dict=None):
    if obj_dict:
      self.user_id = obj_dict['user_id']
      self.first_name = obj_dict['first_name']
      self.last_name = obj_dict['last_name']
      self.email_address = obj_dict['email_address']


  @classmethod
  def initialise_with_token(cls, request):
    user = User()

    try:
      user.auth_token = request.COOKIES[settings.AUTH_TOKEN_NAME]
    except KeyError:
      user.auth_token = None

    return user

  def __str__(self):
    return self.full_name()

  def full_name(self):
    return self.first_name + ' ' + self.last_name

  def check_logged_in(self):
    if self.auth_token:
      response = request_handler.validate_session(self.auth_token)

      authenticated = response.status_code == status.HTTP_200_OK

      if authenticated:
        response_data = response.json()
        self.user_id = response_data['user_id']
        self.first_name = response_data['first_name']
        self.last_name = response_data['last_name']
        self.email_address = response_data['email_address']
        
      return authenticated
    else:
      return False


  def logout(self):
    if self.auth_token:
      home_request_handler.end_session(json.loads(self.auth_token))


  @classmethod
  def load_by_email(cls, email_address):
    # r = requests.post(settings.API_URL + '/users/find_by_email', data = {'email_address': email_address})
    # TODO need to tie into the api when possible
    if email_address == 'test.user@email.com':
      return User({
        'user_id': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email_address': 'test.user@email.com',
        'permissions': [],
      })
    else:
      return None


  @classmethod
  def load_by_id(cls, user_id):
    response = request_handler.load_by_id(user_id)

    authenticated = response.status_code == status.HTTP_200_OK

    if authenticated:
      return User(response.json())
    else:
      return None

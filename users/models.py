from django.conf import settings
from django.db import models


class User():

  def __init__(self, obj_dict):
    self.user_id = obj_dict['user_id']
    self.first_name = obj_dict['first_name']
    self.last_name = obj_dict['last_name']
    self.email_address = obj_dict['email_address']
    self.permissions = obj_dict['permissions']

  @classmethod
  def initialise_with_token(cls, request):
    user = User({
      'user_id': None,
      'first_name': None,
      'last_name': None,
      'email_address': None,
      'permissions': None
    })

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
      # response = requests.post(settings.API_URL + '/validate-session', data = {'auth_token': cookie})
      # authenticated = response.status_code == status.HTTP_200_OK
      authenticated = True
      return authenticated
    else:
      return False

  @classmethod
  def load_by_email(cls, email_address):
    # TODO need to tie into the api when possible
    if email_address == 'test.user@email.com':
      return User({
        'user_id': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email_address': 'test.user@email.com',
        'role': 'MEO',
        'permissions': [],
      })
    else:
      return None

  @classmethod
  def load_by_user_id(cls, user_id):
    # TODO need to tie into the api when possible
    if user_id == 'TestUser':
      return User({
        'user_id': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email_address': 'test.user@email.com',
        'role': 'MEO',
        'permissions': [],
      })
    else:
      return None

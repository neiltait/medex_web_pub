from django.conf import settings
from django.db import models

import requests

class User():

  def __init__(self, obj_dict):
    self.user_id = obj_dict['user_id']
    self.first_name = obj_dict['first_name']
    self.last_name = obj_dict['last_name']
    self.email_address = obj_dict['email_address']
    self.role = obj_dict['role']
    self.permissions = obj_dict['permissions']

  def __str__(self):
    return self.full_name()

  def full_name(self):
    return self.first_name + ' ' + self.last_name

  @classmethod
  def load_by_email(cls, email_address):
    NO_PROXY = {
      'no': 'pass',
    }
    print(settings.API_URL)
    # r = requests.get('https://62b2f542-43c1-4bd3-a312-44551e14f029.mock.pstmn.io')
    r = requests.post(settings.API_URL + '/users/find_by_email', data = {'email_address': email_address})
    print(r.text)
    # TODO need to tie into the api when possible
    if email_address == 'test.user@email.com':
      return User({
        "user_id": "TestUser",
        "first_name": "Test",
        "last_name": "User",
        "email_address": "test.user@email.com",
        "role": "MEO",
        "permissions": [],
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

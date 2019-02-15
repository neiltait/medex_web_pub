from django.db import models

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

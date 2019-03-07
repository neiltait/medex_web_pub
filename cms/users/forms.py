from alerts import messages

from . import request_handler

class CreateUserForm():
  submit_btn_text = 'Save and add role/permission'

  def __init__(self, request=None):
    if request:
      self.email_address = request.get('email_address')
    else:
      self.email_address = ''


  def validate(self):
    self.email_error = None

    if self.email_address == '' or self.email_address is None:
      self.email_error = messages.MISSING_EMAIL
    elif not self.check_is_nhs_email():
      self.email_error = messages.INVALID_EMAIL_DOMAIN
    
    return False if self.email_error else True


  def check_is_nhs_email(self):
    return '@nhs.uk' in self.email_address

  def check_is_in_okta(self):
    ## TODO call out to OKTA to check email in system
    response = request_handler.check_email_in_okta(self.email_address)
    exists = response.status_code == 200
    if not exists:
      self.email_error = messages.NOT_IN_OKTA
    return exists


class PermissionBuilderForm():
  submit_btn_text = 'Save'

  def __init__(self, request=None):
    if request:
      self.role = request.get('role')
      self.permission_level = request.get('permission_level')
      self.region = request.get('region')
      self.trust = request.get('trust')
    else:
      self.role = None
      self.permission_level = None
      self.region = None
      self.trust = None

  def is_valid(self):
    self.role_error = None
    self.permission_level_error = None
    self.trust_error = None
    self.region_error = None


    if self.role is None or self.role is '':
      self.role_error = messages.FIELD_MISSING % "a role"

    if self.permission_level is None or self.permission_level is '':
      self.permission_level_error = messages.FIELD_MISSING % "a level"

    if self.permission_level == 'trust' and (self.trust is None or self.trust is ''):
      self.trust_error = messages.FIELD_MISSING % "a trust"

    if self.permission_level == 'regional' and (self.region is None or self.region is ''):
      self.region_error = messages.FIELD_MISSING % "a region"

    return False if self.role_error or self.permission_level_error or self.trust_error or self.region_error else True

  def to_dict(self):
    return {
      'role': self.role,
      'permission_level': self.permission_level,
      'region': self.region,
      'trust': self.trust
    }

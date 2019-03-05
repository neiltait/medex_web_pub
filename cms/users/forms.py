from alerts import messages

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


class PermissionBuilderForm():
  submit_btn_text = 'Save'

  def __init__(self, request=None):
    if request:
      self.role = request.get('role')
      self.permission_level = request.get('permission_level')
      self.region = request.get('region')
      self.trust = request.get('trust')
    else:
      self.role = ''
      self.permission_level = ''
      self.region = ''
      self.trust = ''

  def is_valid(self):
    self.role_error = None
    self.permission_level_error = None
    self.trust_error = None
    self.region_error = None

    if self.role is None:
      self.role_error = "Missing role"
      print('role error')
    if self.permission_level is None:
      self.permission_level_error = "Missing level"
      print('level error')
    if self.permission_level == 'trust' and self.trust is None:
      print('trust error')
      self.trust_error = "Missing trust"
    if self.permission_level == 'regional' and self.region is None:
      self.region_error = "Missing region"
      print('region error')

    return False if self.role_error or self.permission_level_error or self.trust_error or self.region_error else True

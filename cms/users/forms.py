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
      self.location = request.get('location')
    else:
      self.role = ''
      self.permission_level = ''
      self.location = ''

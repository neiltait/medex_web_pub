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
    elif '@nhs.uk' not in self.email_address:
      self.email_error = messages.INVALID_EMAIL_DOMAIN
    
    return False if self.email_error else True

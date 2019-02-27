from alerts import messages

class CreateUserForm():

  def __init__(self, request=None):
    if request:
      self.email_address = request.get('email_address')
      self.locations = request.get('locations')
      self.role = request.get('role')
    else:
      self.email_address = ''
      self.locations = ''
      self.role = ''


  def validate(self):
    self.email_error = None
    self.locations_error = None
    self.role_error = None

    if self.email_address == '' or self.email_address is None:
      self.email_error = messages.MISSING_EMAIL
    elif '@nhs.uk' not in self.email_address:
      self.email_error = messages.INVALID_EMAIL_DOMAIN

    if self.locations == '' or self.locations is None:
      self.locations_error = messages.MISSING_LOCATIONS

    if self.role == '' or self.role is None:
      self.role_error = messages.MISSING_ROLE
    
    return False if self.email_error or self.locations_error or self.role_error else True

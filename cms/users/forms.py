
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


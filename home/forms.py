
class LoginForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()
    self.password = request.get('password')

  def is_valid(self):
    return True if self.email_address and self.password else False

  def is_authorised(self):
    # TODO submit details to OCTA
    # Temporary auth check until we have OCTA integrated
    # may need to add in an attempt check if OCTA doesn't have one.
    return self.email_address == 'matt' and self.password == 'Password'


class ForgottenPasswordForm():

  def __init__(self, request):
    self.user_id = request.get('user_id')


  def is_valid(self):
    return True if self.user_id else False


class ForgottenUserIdForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()


  def is_valid(self):
    return True if self.email_address else False


class ForgottenPasswordForm():

  def __init__(self, request):
    self.email_address = request.get('email_address')


  def is_valid(self):
    return True if self.email_address else False

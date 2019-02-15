
class UserLookupForm():

  def __init__(self, request):
    self.email_address = request.get('email_address').lower()

  def is_valid(self):
    return True if self.email_address else False

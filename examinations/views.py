from django.shortcuts import render

from home.utils import redirect_to_login
from users.models import User

def create_examination(request):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()


  context = {}
  alerts = []

  return render(request, 'examinations/create.html', context)

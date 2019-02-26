from django.conf import settings
from django.shortcuts import redirect

def check_logged_in(request):
  try:
    cookie = request.COOKIES[settings.AUTH_TOKEN_NAME]
    # response = requests.post(settings.API_URL + '/validate-session', data = {'auth_token': cookie})
    # authenticated = response.status_code == status.HTTP_200_OK
    authenticated = True
    return authenticated
  except KeyError:
    return False



def redirect_to_landing():
  return redirect('/')

def redirect_to_login():
  return redirect('/login')

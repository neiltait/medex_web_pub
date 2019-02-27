from django.shortcuts import render

from home.utils import redirect_to_login

from users.models import User

from .request_handler import get_locations_list, get_me_offices_list
from .forms import PrimaryExaminationInformationForm

def create_examination(request):
  user = User.initialise_with_token(request)

  if not user.check_logged_in():
    return redirect_to_login()

  locations = get_locations_list()
  me_offices = get_me_offices_list()

  context = {
    'session_user': user,
    'page_heading': 'Add a new case',
    'sub_heading': 'Primary information',
    'locations': locations,
    'me_offices': me_offices,
    'form': PrimaryExaminationInformationForm()
  }
  alerts = []

  return render(request, 'examinations/create.html', context)

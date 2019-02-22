from django.shortcuts import render

from home.utils import check_logged_in, redirect_to_login

def create_examination(request):
  if not check_logged_in(request):
    return redirect_to_login()

  context = {}
  alerts = []

  return render(request, 'examinations/create.html', context)

from django.shortcuts import render

def user_lookup(request):
  context = {
    'session_user': {
      'name': 'Andrea Smith',
      'role': 'MEO'
    },
  }
  alerts = []

  context['alerts'] = alerts
  return render(request, 'users/lookup.html', context)

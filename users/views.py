from django.shortcuts import render

def user_lookup(request):
  context = {}
  alerts = []

  context['alerts'] = alerts
  return render(request, 'users/lookup.html', context)

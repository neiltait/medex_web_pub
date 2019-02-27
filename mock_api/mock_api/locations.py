from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

def get_locations_list(request):
  locations = [{
    'id': '1',
    'name': 'Barnet Hospital',
  }, {
    'id': '2',
    'name': 'Sheffield Hospital',
  }, {
    'id': '3',
    'name': 'Gloucester Hospital',
  }]
  return HttpResponse(json.dumps(locations), content_type="application/json")

from django.http import HttpResponse
from django.views.decorators.http import require_GET

import json

@require_GET
def load_trust_list(request):
  trust_list = [
    {
      'id': 1,
      'name': 'Gloucester NHS Trust',
    },
    {
      'id': 2,
      'name': 'Sheffield NHS Trust',
    },
    {
      'id': 3,
      'name': 'Barts NHS Trust',
    }
  ]
  return HttpResponse(json.dumps(trust_list), content_type="application/json")

@require_GET
def load_regions_list(request):
  region_list = [
    {
      'id': 1,
      'name': 'North',
    },
    {
      'id': 2,
      'name': 'South',
    },
    {
      'id': 3,
      'name': 'East',
    },
    {
      'id': 4,
      'name': 'West',
    }
  ]
  return HttpResponse(json.dumps(region_list), content_type="application/json")

@require_GET
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
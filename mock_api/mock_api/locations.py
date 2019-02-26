from django.http import HttpResponse

import json

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
      'id': 1,
      'name': 'Barts NHS Trust',
    }
  ]
  return HttpResponse(json.dumps(trust_list), content_type="application/json")

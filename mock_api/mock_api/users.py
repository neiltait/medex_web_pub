from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

@csrf_exempt
@require_POST
def load_by_email(request):
  user = {
    'user_id': 'TestUser',
    'first_name': 'Test',
    'last_name': 'User',
    'email_address': 'test.user@email.com',
    'role': 'MEO',
    'permissions': [],
  }
  return HttpResponse(json.dumps(user), content_type="application/json")

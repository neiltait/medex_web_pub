
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def create_case(request):
    response = {
        "example": "response"
    }
    return HttpResponse(json.dumps(response), status=200, content_type="application/json")

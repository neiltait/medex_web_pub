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


def load_examination_by_id(request, case_id):
    examination = {"examination_id": 1}

    status_code = 200 if case_id == '1' else 404
    return HttpResponse(json.dumps(examination), content_type="application/json", status=status_code)

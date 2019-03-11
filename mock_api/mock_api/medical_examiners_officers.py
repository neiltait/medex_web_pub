
import json

from django.http import HttpResponse


def get_medical_examiners_officers_list(request):
    officers = [{
        'id': '1',
        'name': 'Andrew Peters',
    }, {
        'id': '2',
        'name': 'Caspar Melancuk',
    }, {
        'id': '3',
        'name': 'Ella Marx',
    }, {
        'id': '4',
        'name': 'Tom Lesirge',
    }, {
        'id': '5',
        'name': 'Aisling Quinn',
    }]
    return HttpResponse(json.dumps(officers), content_type="application/json")


import json

from django.http import HttpResponse


def get_medical_examiners_list(request):
    examiners = [{
        'id': '1',
        'name': 'Dr Alicia Anders',
    }, {
        'id': '2',
        'name': 'Dr Brandon Weatherby',
    }, {
        'id': '3',
        'name': 'Dr Charles Lighterman',
    }, {
        'id': '4',
        'name': 'Dr Subhashine Sanapala',
    }, {
        'id': '5',
        'name': 'Dr Ore Thompson',
    }]
    return HttpResponse(json.dumps(examiners), content_type="application/json")

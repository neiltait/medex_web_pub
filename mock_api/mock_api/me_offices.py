
import json

from django.http import HttpResponse


def get_me_offices_list(request):
    offices = [{
        'id': '1',
        'name': 'Barnet Hospital ME Office',
    }, {
        'id': '2',
        'name': 'Sheffield Hospital ME Office',
    }, {
        'id': '3',
        'name': 'Gloucester Hospital ME Office',
    }]
    return HttpResponse(json.dumps(offices), content_type="application/json")

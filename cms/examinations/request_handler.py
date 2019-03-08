import json

import requests
from django.conf import settings

from examinations.forms import PrimaryExaminationInformationForm


def get_coroner_statuses_list():
    # return requests.get(settings.API_URL + '/datatype/coroner_status')

    return [{'status': 'blocked'}]

def post_new_examination(examination_object):
    return requests.post('%s/cases/create' % settings.API_URL, data=json.dumps(examination_object))
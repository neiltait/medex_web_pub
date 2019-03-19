import json

from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_coroner_statuses_list():
    return [{'status': 'blocked'}]


def post_new_examination(examination_object, auth_token):
    return MedexRequest.post(auth_token, '%s/cases/create' % settings.API_URL, json.dumps(examination_object))


def load_by_id(examination_id, auth_token):
    # return MedexRequest.get(auth_token, '%s/examinations/%s' % (settings.API_URL, examination_id))
    return mocks.SUCCESSFUL_CASE_LOAD


def load_users_examinations(user_id, auth_token):
    return MedexRequest.get(auth_token, '%s/examinations' % settings.API_URL)

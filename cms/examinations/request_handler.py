import json

from django.conf import settings

from medexCms.models import MedexRequest


def get_coroner_statuses_list():
    return [{'status': 'blocked'}]


def post_new_examination(examination_object, auth_token):
    return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, json.dumps(examination_object))


def load_by_id(examination_id, auth_token):
    return MedexRequest.get(auth_token, '%s/examinations/%s' % (settings.API_URL, examination_id))


def load_examinations_index(params, auth_token):
    return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, params)

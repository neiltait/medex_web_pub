import json

from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_coroner_statuses_list():
    return [{'status': 'blocked'}]


def post_new_examination(examination_object, auth_token):

    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_CREATE
    else:
        return MedexRequest.post(auth_token, '%s/cases/create' % settings.API_URL, json.dumps(examination_object))


def load_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s' % (settings.API_URL, examination_id))


def load_examinations_index(params, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_INDEX
    else:
        return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, params)


def load_patient_details_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_PATIENT_DETAILS_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/patient_details' % (settings.API_URL, examination_id))


def update_patient_details(examination_id, submission, auth_token):
    return MedexRequest.put(auth_token, '%s/examinations/%s/patient_details' % (settings.API_URL, examination_id),
                            submission)


def load_medical_team_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_TEAM_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/medical_team' % (settings.API_URL, examination_id))


def update_medical_team(examination_id, submission, auth_token):
    return MedexRequest.put(auth_token, '%s/examinations/%s/medical_team' % (settings.API_URL, examination_id),
                            submission)


def load_modes_of_disposal(auth_token):
    if settings.LOCAL:
        return mocks.LOAD_MODES_OF_DISPOSAL
    else:
        return MedexRequest.get(auth_token, '%s/data_types/mode_of_disposal' % settings.API_URL).json()


def load_case_breakdown_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_LOAD_CASE_BREAKDOWN
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/case_breakdown' % (settings.API_URL, examination_id))

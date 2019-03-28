from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_medical_examiners_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_EXAMINERS
    else:
        response_users = MedexRequest.get(auth_token, "%s/users/medical_examiners" % settings.API_URL).json()['users']
        return [convert_user(response_user) for response_user in response_users]


def get_medical_examiners_officers_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS
    else:
        response_users = MedexRequest.get(auth_token, "%s/users/medical_examiner_officers" % settings.API_URL).json()['users']
        return [convert_user(response_user) for response_user in response_users]


def convert_user(response_user):
    return {
        "first_name": response_user['firstName'],
        "last_name": response_user['lastName'],
        "user_id": response_user['userId']
    }

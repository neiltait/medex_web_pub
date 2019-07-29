from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import UserMocks


def get_medical_examiners_list(auth_token):
    if settings.LOCAL:
        return [convert_user(user) for user in UserMocks.get_me_user_list()]
    else:
        response_users = MedexRequest.get(auth_token, "%s/users/medical_examiners" % settings.API_URL).json()['users']
        return [convert_user(response_user) for response_user in response_users]


def get_medical_examiners_officers_list(auth_token):
    if settings.LOCAL:
        return [convert_user(user) for user in UserMocks.get_meo_user_list()]
    else:
        response_users = MedexRequest.get(auth_token, "%s/users/medical_examiner_officers" % settings.API_URL).json()[
            'users']
        return [convert_user(response_user) for response_user in response_users]


def get_medical_examiners_list_for_examination(auth_token, examination_id):
    if settings.LOCAL:
        return [convert_user(user) for user in UserMocks.get_me_user_list()]
    else:
        response_users = MedexRequest.get(auth_token, "%s/examination/%s/users/role/medical_examiner" % (
            settings.API_URL, examination_id)).json()['users']
        return [convert_user(response_user) for response_user in response_users]


def get_medical_examiners_officers_list_for_examination(auth_token, examination_id):
    if settings.LOCAL:
        return [convert_user(user) for user in UserMocks.get_meo_user_list()]
    else:
        response_users = MedexRequest.get(auth_token, "%s/examination/%s/users/role/medical_examiner_officer" % (
            settings.API_URL, examination_id)).json()['users']
        return [convert_user(response_user) for response_user in response_users]


def convert_user(response_user):
    return {
        "first_name": response_user['firstName'],
        "last_name": response_user['lastName'],
        "user_id": response_user['userId']
    }

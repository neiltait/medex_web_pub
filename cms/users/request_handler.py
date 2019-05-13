from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import SessionMocks, UserMocks


def validate_session(auth_token):
    if settings.LOCAL:
        return SessionMocks.get_successful_validate_session_response()
    else:
        return MedexRequest.post(auth_token, '%s/auth/validate_session' % settings.API_URL)


def create_user(user_object, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_user_creation_response()
    else:
        return MedexRequest.post(auth_token, '%s/users' % settings.API_URL, user_object)


def load_by_id(user_id, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_single_user_load_response()
    else:
        return MedexRequest.get(auth_token, '%s/users/%s' % (settings.API_URL, user_id))


def get_permitted_users(auth_token, location_id):
    if settings.LOCAL:
        return UserMocks.get_medical_examiners_load_response_content()
    else:
        # TODO update to the right end point once we have it
        # return MedexRequest.get(auth_token, "%s/users/medical_examiners" % settings.API_URL).json()
        return UserMocks.get_medical_examiners_load_response_content()

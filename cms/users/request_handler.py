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


def update_user(user_object, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_user_update_response()
    else:
        return MedexRequest.put(auth_token, '%s/users' % settings.API_URL, user_object)


def update_current_user_profile(profile_object, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_user_update_profile_response()
    else:
        return MedexRequest.put(auth_token, '%s/profile' % settings.API_URL, profile_object)


def update_user_profile(user_id, profile_object, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_user_update_profile_response()
    else:
        return MedexRequest.put(auth_token, '%s/users/%s/profile' % (settings.API_URL, user_id), profile_object)


def load_by_id(user_id, auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_single_user_load_response()
    else:
        return MedexRequest.get(auth_token, '%s/users/%s' % (settings.API_URL, user_id))


def load_all_users(auth_token):
    if settings.LOCAL:
        return UserMocks.get_successful_users_load_response()
    else:
        return MedexRequest.get(auth_token, "%s/users" % settings.API_URL)

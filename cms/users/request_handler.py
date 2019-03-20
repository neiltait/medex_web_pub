from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def validate_session(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_LOAD_USER
    else:
        return MedexRequest.post(auth_token, '%s/auth/validate-session' % settings.API_URL)


def create_user(user_object, auth_token):
    return MedexRequest.post(auth_token, '%s/users' % settings.API_URL, user_object)


def load_by_id(user_id, auth_token):
    return MedexRequest.get(auth_token, '%s/users/%s' % (settings.API_URL, user_id))


def create_permission(permission, user_id, auth_token):
    return MedexRequest.post(auth_token, '%s/users/%s/permissions' % (settings.API_URL, user_id), permission)


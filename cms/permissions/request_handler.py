from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import PermissionMocks


def load_permissions_for_user(user_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_permission_load_response(PermissionMocks.MEO_TYPE)
    else:
        return MedexRequest.get(auth_token, '%s/users/%s/permissions' % (settings.API_URL, user_id))


def load_single_permission_for_user(user_id, permission_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_permission_load_response(PermissionMocks.MEO_TYPE)
    else:
        return MedexRequest.get(auth_token, '%s/users/%s/permissions/%s' % (settings.API_URL, user_id, permission_id))


def create_permission(permission, user_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_permission_creation_response()
    else:
        return MedexRequest.post(auth_token, '%s/users/%s/permissions' % (settings.API_URL, user_id), permission)


def delete_permission(permission_id, user_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_permission_delete_response()
    else:
        print("call the DELETE endpoint %s/users/%s/permissions/%s'" % (settings.API_URL, user_id, permission_id))


def update_permission(permission, user_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_permission_creation_response()
    else:
        return MedexRequest.put(auth_token,
                                '%s/users/%s/permissions/%s' % (settings.API_URL, user_id, permission.permission_id),
                                permission)

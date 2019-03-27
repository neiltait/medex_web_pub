from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def load_permissions_for_user(user_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_PERMISSION_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/users/%s/permissions' % (settings.API_URL, user_id))

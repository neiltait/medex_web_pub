from django.conf import settings

from medexCms.models import MedexRequest


def load_permissions_for_user(user_id, auth_token):
    return MedexRequest.get(auth_token, '%s/users/%s/permissions' % (settings.API_URL, user_id))

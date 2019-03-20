from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def load_trusts_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_TRUST_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def load_region_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_REGION_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def get_locations_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_TRUST_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def get_me_offices_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_ME_OFFICES_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()

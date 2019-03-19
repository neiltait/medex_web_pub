from django.conf import settings

from medexCms.models import MedexRequest


def load_trusts_list(auth_token):
    return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def load_region_list(auth_token):
    return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def get_locations_list(auth_token):
    return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()


def get_me_offices_list(auth_token):
    return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()

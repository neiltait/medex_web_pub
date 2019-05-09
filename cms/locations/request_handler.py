from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import LocationsMocks, UserMocks


def load_trusts_list(auth_token):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def load_region_list(auth_token):
    if settings.LOCAL:
        return LocationsMocks.get_region_location_list()
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_locations_list(auth_token):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_me_offices_list(auth_token, params):
    if settings.LOCAL:
        return LocationsMocks.get_me_office_location_list()
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL, params).json()['locations']


def get_permitted_locations_list(auth_token):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_permitted_users(auth_token, location_id):
    if settings.LOCAL:
        return UserMocks.get_medical_examiners_load_response_content()
    else:
        # TODO update to the right end point once we have it
        return MedexRequest.get(auth_token, "%s/users/medical_examiners" % settings.API_URL).json()

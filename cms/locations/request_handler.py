from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import LocationsMocks


def get_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        if limit_to_me_offices:
            return MedexRequest.get(auth_token, "%s/locations?OnlyMEOffices=true" % settings.API_URL).json()[
                'locations']
        else:
            return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_permitted_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        query_params = {
            "AccessOnly": True
        }
        if limit_to_me_offices:
            return \
            MedexRequest.get(auth_token,
                             "%s/locations?OnlyMEOffices=true" % settings.API_URL, query_params).json()['locations']
        else:
            return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL, query_params).json()['locations']

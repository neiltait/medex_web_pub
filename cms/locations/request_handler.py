from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import LocationsMocks


def get_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=False,
                                             limit_to_me_offices=limit_to_me_offices,
                                             create_examination_locations=False)


def get_permitted_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=True,
                                             limit_to_me_offices=limit_to_me_offices,
                                             create_examination_locations=False)


def get_create_examination_permitted_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=False,
                                             limit_to_me_offices=limit_to_me_offices,
                                             create_examination_locations=True)


def __get_filtered_locations_list(auth_token, permitted_locations_only, limit_to_me_offices,
                                  create_examination_locations):
    query_params = {
        "AccessOnly": permitted_locations_only,
        "OnlyMEOffices": limit_to_me_offices,
        "CreateExaminationOnly": create_examination_locations,
    }
    return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL, query_params).json()['locations']

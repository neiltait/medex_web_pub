from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import LocationsMocks

def load_by_id(auth_token, location_id):
    print(location_id)
    response = MedexRequest.get(auth_token, "%s/locations/%s" % (settings.API_URL, location_id))
    print(response)
    if response.status_code == 200:
        return response.json()
    
    return None

def get_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=False,
                                             limit_to_me_offices=limit_to_me_offices,
                                             parent_id=None)

def get_child_locations_list(auth_token, parent_id):
    if settings.LOCAL:
        # @TODO
        return None
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=False,
                                             limit_to_me_offices=False,
                                             parent_id=parent_id)


def get_permitted_locations_list(auth_token, limit_to_me_offices=True):
    if settings.LOCAL:
        return LocationsMocks.get_trust_location_list()
    else:
        return __get_filtered_locations_list(auth_token, permitted_locations_only=True,
                                             limit_to_me_offices=limit_to_me_offices,
                                             parent_id=None)


def __get_filtered_locations_list(auth_token, permitted_locations_only, limit_to_me_offices, parent_id):
    query_params = {
        "ParentId" : parent_id,
        "AccessOnly": permitted_locations_only,
        "OnlyMEOffices": limit_to_me_offices
    }
    print(query_params)
    response = MedexRequest.get(auth_token, "%s/locations" % settings.API_URL, query_params).json()['locations']
    print(response)

    return response

def update_location_me_office(is_me_office, location_id, auth_token):
    if settings.LOCAL:
        return PermissionMocks.get_successful_location_update_response()
    else:
        return MedexRequest.put(auth_token,
                                '%s/locations/%s/is_me_office' % (settings.API_URL, location_id),
                                is_me_office)

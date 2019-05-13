from people.models import DropdownPerson
from . import request_handler
from .utils import filter_trusts, filter_regions


class Location:

    NATIONAL_TYPE = 'National'
    REGIONAL_TYPE = 'Region'
    TRUST_TYPE = 'Trust'
    SITE_TYPE = 'Site'

    def __init__(self):
        self.location_id = ''
        self.name = ''
        self.parent_id = ''

    @classmethod
    def initialise_with_id(cls, location_id):
        location = Location()
        location.location_id = location_id
        return location

    def set_values(self, obj_dict):
        self.location_id = obj_dict.get('locationId')
        self.name = obj_dict.get('name')
        self.parent_id = obj_dict.get('parentId')
        return self

    def load_permitted_users(self, auth_token):
        users = []
        users_data = request_handler.get_permitted_users(auth_token, self.location_id)['users']
        for user in users_data:
            users.append(DropdownPerson(user))
        return users

    @classmethod
    def get_locations_list(cls, auth_token):
        return request_handler.get_locations_list(auth_token)

    @classmethod
    def get_permitted_locations_for_user(cls, auth_token):
        locations_data = request_handler.get_permitted_locations_list(auth_token)
        locations = []
        for location in locations_data:
            locations.append(Location().set_values(location))
        return locations

    @classmethod
    def load_trusts_list_for_user(cls, auth_token):
        locations = request_handler.get_permitted_locations_list(auth_token)
        trusts = filter_trusts(locations)
        return trusts

    @classmethod
    def load_region_list_for_user(cls, auth_token):
        locations = request_handler.get_permitted_locations_list(auth_token)
        regions = filter_regions(locations)
        return regions

    @classmethod
    def load_me_offices(cls, auth_token):
        return cls.get_permitted_locations_for_user(auth_token)

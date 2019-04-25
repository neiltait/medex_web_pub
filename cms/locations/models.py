from people.models import DropdownPerson
from . import request_handler


class Location:

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
    def get_me_offices_list(cls, auth_token):
        return request_handler.get_me_offices_list(auth_token)

    @classmethod
    def load_trusts_list(cls, auth_token):
        return request_handler.load_trusts_list(auth_token)

    @classmethod
    def load_region_list(cls, auth_token):
        return request_handler.load_region_list(auth_token)

    @classmethod
    def load_me_offices(cls, auth_token):
        return request_handler.get_me_offices_list(auth_token)

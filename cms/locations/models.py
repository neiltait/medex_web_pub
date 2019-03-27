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

    def load_permitted_users(self, auth_token):
        users = request_handler.get_permitted_users(auth_token, self.location_id)
        return users

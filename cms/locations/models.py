from . import request_handler
from .utils import filter_trusts, filter_regions, filter_sites, filter_national


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

    @classmethod
    def load_by_id(cls, location_id, auth_token):
        return request_handler.load_by_id(auth_token, location_id)
      
    @classmethod
    def get_locations_list(cls, auth_token):
        return request_handler.get_locations_list(auth_token)

    @classmethod
    def get_child_locations_list(cls, parent_id, auth_token):
          return request_handler.get_child_locations_list(auth_token, parent_id)
      
    @classmethod
    def get_permitted_locations_for_user(cls, auth_token):
        locations_data = request_handler.get_permitted_locations_list(auth_token)
        locations = []
        for location in locations_data:
            locations.append(Location().set_values(location))
        return locations

    @classmethod
    def load_site_list_for_user(cls, auth_token):
        locations = request_handler.get_permitted_locations_list(auth_token)
        sites = filter_sites(locations)
        return sites

    @classmethod
    def load_create_examination_site_list_for_user(cls, auth_token):
        locations = request_handler.get_create_examination_permitted_locations_list(auth_token)
        sites = filter_sites(locations)
        return sites

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
        return cls.load_site_list_for_user(auth_token)

    @classmethod
    def load_create_examination_me_offices(cls, auth_token):
        return cls.load_create_examination_site_list_for_user(auth_token)

    @classmethod
    def get_national_location_id(cls, auth_token):
        locations_data = cls.get_locations_list(auth_token)
        national = filter_national(locations_data)
        return national.location_id

    @classmethod
    def load_location_collection_for_user(cls, auth_token):
        locations = request_handler.get_permitted_locations_list(auth_token, limit_to_me_offices=False)
        return LocationCollection(locations)

    @classmethod
    def update_location_me_office(cls, location, location_id, auth_token):
        print('update_location_me_office')
        print(location)
        return request_handler.update_location_me_office(location['isMeOffice'], location_id, auth_token)


class LocationCollection:

    def __init__(self, location_list):
        self.all = location_list

    def all(self):
        return self.all

    @property
    def trusts(self):
        return filter_trusts(self.all)

    @property
    def sites(self):
        return filter_sites(self.all)

    @property
    def regions(self):
        return filter_regions(self.all)

    @property
    def national(self):
        if len([n for n in self.all if n.get('type') == 'National']) > 0:
            return filter_national(self.all)
        else:
            return None

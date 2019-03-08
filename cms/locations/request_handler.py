from django.conf import settings

import requests


def load_trusts_list():
    return requests.get("%s/locations/load_trusts_list" % settings.API_URL).json()


def load_region_list():
    return requests.get("%s/locations/load_regions_list" % settings.API_URL).json()


def get_locations_list():
    return requests.get("%s/locations/get_locations_list" % settings.API_URL).json()


def get_me_offices_list():
    return requests.get("%s/me_offices/get_me_offices_list" % settings.API_URL).json()

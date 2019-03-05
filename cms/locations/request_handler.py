from django.conf import settings

import requests

def load_trusts_list():
  return requests.get('%s/locations/load_trusts_list' % settings.API_URL).json()

def load_region_list():
  return requests.get('%s/locations/load_regions_list' % settings.API_URL).json()

import requests
from django.conf import settings


def get_coroner_statuses_list():

    # return requests.get(settings.API_URL + '/datatype/coroner_status')

    return [{'status':'blocked'}]
from django.conf import settings

import requests



def get_medical_examiners_list():
    return requests.get("%s/people/get_medical_examiners_list" % settings.API_URL).json()


def get_medical_examiners_officers_list():
    return requests.get("%s/people/get_medical_examiners_officers_list" % settings.API_URL).json()

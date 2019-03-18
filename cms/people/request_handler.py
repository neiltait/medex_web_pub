from django.conf import settings

from medexCms.models import MedexRequest


def get_medical_examiners_list(auth_token):
    return MedexRequest.get(auth_token, "%s/people/get_medical_examiners_list" % settings.API_URL).json()


def get_medical_examiners_officers_list(auth_token):
    return MedexRequest.get(auth_token, "%s/people/get_medical_examiners_officers_list" % settings.API_URL).json()

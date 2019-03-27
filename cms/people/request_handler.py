from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_medical_examiners_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_EXAMINERS
    else:
        return MedexRequest.get(auth_token, "%s/MedicalExaminers" % settings.API_URL).json()


def get_medical_examiners_officers_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS
    else:
        return MedexRequest.get(auth_token, "%s/MedicalExaminerOfficers" % settings.API_URL).json()

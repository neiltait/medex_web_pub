from rest_framework import status

from errors.utils import log_api_error
from examinations import request_handler

from medexCms.utils import fallback_to


class MedicalTeam:

    def __init__(self, obj_dict, examination_id):
        from examinations.models.core import PatientHeader

        self.examination_id = examination_id
        self.case_header = PatientHeader(obj_dict.get("header"))
        self.consultant_responsible = MedicalTeamMember.from_dict(
            obj_dict['consultantResponsible']) if obj_dict['consultantResponsible'] else None
        self.qap = MedicalTeamMember.from_dict(obj_dict['qap']) if obj_dict['qap'] else None
        self.general_practitioner = MedicalTeamMember.from_dict(
            obj_dict['generalPractitioner']) if obj_dict['generalPractitioner'] else None

        if "consultantsOther" in obj_dict and obj_dict["consultantsOther"] is not None:
            self.consultants_other = [MedicalTeamMember.from_dict(consultant) for consultant in
                                      obj_dict['consultantsOther']]
        else:
            self.consultants_other = []

        self.nursing_team_information = obj_dict[
            'nursingTeamInformation'] if 'nursingTeamInformation' in obj_dict else ''

        self.medical_examiner_id = obj_dict['medicalExaminerUserId'] if 'medicalExaminerUserId' in obj_dict else ''
        self.medical_examiners_officer_id = obj_dict[
            'medicalExaminerOfficerUserId'] if 'medicalExaminerOfficerUserId' in obj_dict else ''

        if 'lookups' in obj_dict:
            lookups = obj_dict['lookups']
            self.medical_examiner_lookup = self.get_lookup(
                lookups['medicalExaminers']) if 'medicalExaminers' in lookups else []
            self.medical_examiner_officer_lookup = self.get_lookup(
                lookups['medicalExaminerOfficers']) if 'medicalExaminerOfficers' in lookups else []
        else:
            self.medical_examiner_lookup = []
            self.medical_examiner_officer_lookup = []

    @classmethod
    def get_lookup(cls, user_list):
        return [{'display_name': user['fullName'], 'user_id': user['userId']} for user in user_list]

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_medical_team_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return MedicalTeam(response.json(), examination_id)
        else:
            log_api_error('medical team load', response.text)
            return None

    def update(self, submission, auth_token):
        return request_handler.update_medical_team(self.examination_id, submission, auth_token)


class MedicalTeamMember:

    def __init__(self, name='', role='', organisation='', phone_number='', notes='', gmc_number=''):
        self.name = name.strip() if name else ''
        self.role = role
        self.organisation = organisation
        self.phone_number = phone_number
        self.notes = notes
        self.gmc_number = gmc_number

    @staticmethod
    def from_dict(obj_dict):
        if obj_dict is None:
            return None

        name = fallback_to(obj_dict.get('name'), '')
        role = fallback_to(obj_dict.get('role'), '')
        organisation = fallback_to(obj_dict.get('organisation'), '')
        phone_number = fallback_to(obj_dict.get('phone'), '')
        notes = fallback_to(obj_dict.get('notes'), '')
        gmc_number = fallback_to(obj_dict.get('gmcNumber'), '')
        return MedicalTeamMember(name=name, role=role, organisation=organisation, phone_number=phone_number,
                                 notes=notes, gmc_number=gmc_number)

    def has_name(self):
        return self.name and len(self.name.strip()) > 0

    def has_valid_name(self):
        return len(self.name.strip()) < 250

    def has_name_if_needed(self):
        from examinations.utils import text_field_is_not_null

        if text_field_is_not_null(self.role) or text_field_is_not_null(self.organisation) or text_field_is_not_null(
                self.phone_number):
            return text_field_is_not_null(self.name)
        else:
            return True

    def to_object(self):
        return {
            "name": self.name,
            "role": self.role,
            "organisation": self.organisation,
            "phone": self.phone_number,
            "notes": self.notes,
            "gmcNumber": self.gmc_number
        }



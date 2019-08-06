from alerts.messages import ErrorFieldTooLong, ErrorFieldRequiredMessage
from examinations.models.medical_team import MedicalTeamMember
from medexCms.utils import fallback_to, pop_if_falsey


class MedicalTeamMembersForm:
    consultant_1 = MedicalTeamMember(name='', role='', organisation='', phone_number='', gmc_number='')
    consultant_2 = MedicalTeamMember(name='', role='', organisation='', phone_number='', gmc_number='')
    consultant_3 = MedicalTeamMember(name='', role='', organisation='', phone_number='', gmc_number='')
    qap = MedicalTeamMember(name='', role='', organisation='', phone_number='', gmc_number='')
    gp = MedicalTeamMember(name='', role='', organisation='', phone_number='', gmc_number='')
    nursing_team_information = ''
    medical_examiner = ''
    medical_examiners_officer = ''
    consultant_count = 0

    def __init__(self, request=None, medical_team=None):
        self.initialise_errors()
        if request:
            self.initialise_form_from_data(request=request)
        elif medical_team:
            self.initialise_form_from_medical_team(medical_team=medical_team)

    def initialise_form_from_data(self, request):
        self.consultant_1 = MedicalTeamMember(name=request.get('consultant_name_1'),
                                              role=request.get('consultant_role_1'),
                                              organisation=request.get('consultant_organisation_1'),
                                              phone_number=request.get('consultant_phone_number_1'),
                                              notes=request.get('consultant_note_1'),
                                              gmc_number=request.get('gmc_number_consultant_1'))
        self.consultant_2 = MedicalTeamMember(name=request.get('consultant_name_2'),
                                              role=request.get('consultant_role_2'),
                                              organisation=request.get('consultant_organisation_2'),
                                              phone_number=request.get('consultant_phone_number_2'),
                                              notes=request.get('consultant_note_2'),
                                              gmc_number=request.get('gmc_number_consultant_2'))
        self.consultant_3 = MedicalTeamMember(name=request.get('consultant_name_3'),
                                              role=request.get('consultant_role_3'),
                                              organisation=request.get('consultant_organisation_3'),
                                              phone_number=request.get('consultant_phone_number_3'),
                                              notes=request.get('consultant_note_3'),
                                              gmc_number=request.get('gmc_number_consultant_3'))
        self.qap = MedicalTeamMember(name=request.get('qap_name'),
                                     role=request.get('qap_role'),
                                     organisation=request.get('qap_organisation'),
                                     phone_number=request.get('qap_phone_number'),
                                     notes=request.get('qap_note_1'),
                                     gmc_number=request.get('gmc_number_qap'))
        self.gp = MedicalTeamMember(name=request.get('gp_name'),
                                    role=request.get('gp_role'),
                                    organisation=request.get('gp_organisation'),
                                    phone_number=request.get('gp_phone_number'),
                                    notes=request.get('gp_note_1'),
                                    gmc_number=request.get('gmc_number_gp'))
        self.nursing_team_information = request.get('nursing_team_information')
        self.medical_examiner = request.get('medical_examiner') if request.get('medical_examiner') else ''
        self.medical_examiners_officer = request.get('medical_examiners_officer') if request.get(
            'medical_examiners_officer') else ''
        self.consultant_count = self.get_consultant_count()

    def initialise_form_from_medical_team(self, medical_team):
        self.consultant_1 = medical_team.consultant_responsible
        self.consultant_2 = medical_team.consultants_other[0] if len(
            medical_team.consultants_other) > 0 else MedicalTeamMember()
        self.consultant_3 = medical_team.consultants_other[1] if len(
            medical_team.consultants_other) > 1 else MedicalTeamMember()
        self.gp = medical_team.general_practitioner
        self.qap = medical_team.qap
        self.nursing_team_information = medical_team.nursing_team_information
        self.medical_examiner = medical_team.medical_examiner_id
        self.medical_examiners_officer = medical_team.medical_examiners_officer_id
        self.consultant_count = self.get_consultant_count()

    def get_consultant_count(self):
        if self.consultant_3 is not None and self.consultant_3.has_name():
            return 3
        elif self.consultant_2 is not None and self.consultant_2.has_name():
            return 2
        elif self.consultant_1 is not None and self.consultant_1.has_name():
            return 1
        else:
            return 0

    def is_valid(self):
        if not self.consultant_1.has_valid_name():
            self.errors["consultant_1"] = ErrorFieldTooLong(250)
            self.errors["count"] += 1

        if not self.consultant_1.has_name():
            self.errors["consultant_1"] = ErrorFieldRequiredMessage("name")
            self.errors["count"] += 1

        if not self.consultant_2.has_valid_name():
            self.errors["consultant_2"] = ErrorFieldTooLong(250)
            self.errors["count"] += 1

        if not self.consultant_2.has_name_if_needed():
            self.errors["consultant_2"] = ErrorFieldRequiredMessage("name")
            self.errors["count"] += 1

        if not self.consultant_3.has_valid_name():
            self.errors["consultant_3"] = ErrorFieldTooLong(250)
            self.errors["count"] += 1

        if not self.consultant_3.has_name_if_needed():
            self.errors["consultant_3"] = ErrorFieldRequiredMessage("name")
            self.errors["count"] += 1

        if not self.qap.has_valid_name():
            self.errors["qap"] = ErrorFieldTooLong(250)
            self.errors["count"] += 1

        if not self.qap.has_name_if_needed():
            self.errors["qap"] = ErrorFieldRequiredMessage("name")
            self.errors["count"] += 1

        if not self.gp.has_valid_name():
            self.errors["gp"] = ErrorFieldTooLong(250)
            self.errors["count"] += 1

        if not self.gp.has_name_if_needed():
            self.errors["gp"] = ErrorFieldRequiredMessage("name")
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def initialise_errors(self):
        self.errors = {"count": 0}

    @property
    def error_count(self):
        return self.errors['count']

    def to_object(self):
        consultants_other = []
        if self.consultant_2.has_name():
            consultants_other.append(self.consultant_2.to_object())
        if self.consultant_3.has_name():
            consultants_other.append(self.consultant_3.to_object())

        obj = {
            "consultantResponsible": self.consultant_1.to_object(),
            "consultantsOther": consultants_other,
            "nursingTeamInformation": fallback_to(self.nursing_team_information, ''),
            "medicalExaminerUserId": self.medical_examiner,
            "medicalExaminerOfficerUserId": self.medical_examiners_officer,
        }

        pop_if_falsey("medicalExaminerUserId", obj)
        pop_if_falsey("medicalExaminerOfficerUserId", obj)

        if self.qap.has_name():
            obj['qap'] = self.qap.to_object()

        if self.gp.has_name():
            obj['generalPractitioner'] = self.gp.to_object()

        return obj

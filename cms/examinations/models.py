from rest_framework import status

from medexCms.utils import parse_datetime, is_empty_date

from . import request_handler


class Examination:

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.id = obj_dict.get("id")
            self.time_of_death = obj_dict.get("timeOfDeath")
            self.given_names = obj_dict.get("givenNames")
            self.surname = obj_dict.get("surname")
            self.nhs_number = obj_dict.get("nhsNumber")
            self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
            self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
            self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
            self.gender = obj_dict.get("gender")
            self.gender_details = obj_dict.get("genderDetails")
            self.house_name_number = obj_dict.get("houseNameNumber")
            self.street = obj_dict.get("street")
            self.town = obj_dict.get("town")
            self.county = obj_dict.get("county")
            self.postcode = obj_dict.get("postcode")
            self.country = obj_dict.get("country")
            self.last_occupation = obj_dict.get("lastOccupation")
            self.organisation_care_before_death_locationId = obj_dict.get("organisationCareBeforeDeathLocationId")
            self.death_occurred_location_id = obj_dict.get("deathOccuredLocationId")
            self.mode_of_disposal = obj_dict.get("modeOfDisposal")
            self.funeral_directors = obj_dict.get("funeralDirectors")
            self.personal_affects_collected = obj_dict.get("personalAffectsCollected")
            self.personal_affects_details = obj_dict.get("personalAffectsDetails")
            self.date_of_birth = obj_dict.get("dateOfBirth")
            self.date_of_death = obj_dict.get("dateOfDeath")
            self.faith_priority = obj_dict.get("faithPriority")
            self.child_priority = obj_dict.get("childPriority")
            self.coroner_priority = obj_dict.get("coronerPriority")
            self.cultural_priority = obj_dict.get("culturalPriority")
            self.other_priority = obj_dict.get("otherPriority")
            self.priority_details = obj_dict.get("priorityDetails")
            self.completed = obj_dict.get("completed")
            self.coroner_status = obj_dict.get("coronerStatus")
            self.representatives = obj_dict.get("representatives")
            self.out_of_hours = obj_dict.get('outOfHours')

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return Examination(response.json())
        else:
            return None


class ExaminationOverview:
    date_format = '%d.%m.%Y'

    def __init__(self, obj_dict):
        self.urgency_score = obj_dict.get("urgencyScore")
        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.id = obj_dict.get("id")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.appointment_date = obj_dict.get("appointmentDate")
        self.appointment_time = obj_dict.get("appointmentTime")
        self.last_admission = obj_dict.get("lastAdmission")
        self.case_created_date = obj_dict.get("caseCreatedDate")

    def display_dod(self):
        return self.date_of_death.strftime(self.date_format) if self.date_of_death else 'D.O.D unknown'

    def display_dob(self):
        return self.date_of_birth.strftime(self.date_format) if self.date_of_birth else 'D.O.B unknown'

    def urgent(self):
        return True if self.urgency_score and self.urgency_score > 0 else False


class PatientDetails:

    def __init__(self, obj_dict):
        self.id = obj_dict.get("id")
        self.cultural_priority = obj_dict.get("culturalPriority")
        self.faith_priority = obj_dict.get("faithPriority")
        self.child_priority = obj_dict.get("childPriority")
        self.coroner_priority = obj_dict.get("coronerPriority")
        self.other_priority = obj_dict.get("otherPriority")
        self.priority_details = obj_dict.get("priorityDetails")
        self.completed = obj_dict.get("completed")
        self.coroner_status = obj_dict.get("coronerStatus")
        self.gender = obj_dict.get("gender").lower()
        self.gender_details = obj_dict.get("genderDetails")
        self.death_occurred_location_id = obj_dict.get("placeDeathOccured")
        self.medical_examiner_office_responsible = obj_dict.get("medicalExaminerOfficeResponsible")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
        self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
        self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.out_of_hours = obj_dict.get("outOfHours")
        self.postcode = obj_dict.get("postCode")
        self.house_name_number = obj_dict.get("houseNameNumber")
        self.street = obj_dict.get("street")
        self.town = obj_dict.get("town")
        self.county = obj_dict.get("county")
        self.country = obj_dict.get("country")
        self.last_occupation = obj_dict.get("lastOccupation")
        self.organisation_care_before_death_location_id = obj_dict.get("organisationCareBeforeDeathLocationId")
        self.mode_of_disposal = obj_dict.get("modeOfDisposal")
        self.any_implants = obj_dict.get("anyImplants")
        self.implant_details = obj_dict.get("implantDetails")
        self.funeral_directors = obj_dict.get("funeralDirectors")
        self.any_personal_effects = obj_dict.get("anyPersonalEffects")
        self.personal_affects_details = obj_dict.get("personalEffectDetails")
        self.representatives = obj_dict.get("representatives")

        if not is_empty_date(obj_dict.get("dateOfBirth")):
            self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
            self.day_of_birth = self.date_of_birth.day
            self.month_of_birth = self.date_of_birth.month
            self.year_of_birth = self.date_of_birth.year
        else:
            self.date_of_birth = None
            self.day_of_birth = None
            self.month_of_birth = None
            self.year_of_birth = None

        if not is_empty_date(obj_dict.get("dateOfDeath")):
            self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
            self.day_of_death = self.date_of_death.day
            self.month_of_death = self.date_of_death.month
            self.year_of_death = self.date_of_death.year
        else:
            self.date_of_death = None
            self.day_of_death = None
            self.month_of_death = None
            self.year_of_death = None

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_patient_details_by_id(examination_id, auth_token)
        print(response.__dict__)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return PatientDetails(response.json())
        else:
            return None

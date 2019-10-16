from errors.utils import log_api_error, handle_error
from examinations import request_handler
from examinations.models.case_breakdown import CaseStatus
from examinations.presenters.core import PatientHeader
from medexCms.utils import fallback_to, bool_to_string, is_empty_time, is_empty_date, parse_datetime
from people.models import BereavedRepresentative


class PatientDetails:

    def __init__(self, obj_dict={}, modes_of_disposal={}, examination_id=None):

        self.modes_of_disposal = modes_of_disposal

        self.id = examination_id if examination_id else obj_dict.get("id")
        self.case_header = PatientHeader(obj_dict.get("header"))

        self.completed = obj_dict.get("completed")
        self.coroner_status = obj_dict.get("coronerStatus")

        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.gender = obj_dict.get("gender")
        self.gender_details = obj_dict.get("genderDetails")
        self.nhs_number = self.remove_whitespace(obj_dict.get("nhsNumber"))
        self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
        self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
        self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
        self.death_occurred_location_id = obj_dict.get("placeDeathOccured")
        self.medical_examiner_office_responsible = obj_dict.get("medicalExaminerOfficeResponsible")
        self.out_of_hours = obj_dict.get("outOfHours")

        self.house_name_number = fallback_to(obj_dict.get("houseNameNumber"), '')
        self.street = fallback_to(obj_dict.get("street"), '')
        self.town = fallback_to(obj_dict.get("town"), '')
        self.county = fallback_to(obj_dict.get("county"), '')
        self.country = fallback_to(obj_dict.get("country"), '')
        self.postcode = fallback_to(obj_dict.get("postCode"), '')
        self.last_occupation = fallback_to(obj_dict.get("lastOccupation"), '')
        self.organisation_care_before_death_location_id = fallback_to(
            obj_dict.get("organisationCareBeforeDeathLocationId"), '')
        self.any_implants = 'true' if obj_dict.get("anyImplants") else 'false'
        self.implant_details = fallback_to(obj_dict.get("implantDetails"), '')
        self.funeral_directors = fallback_to(obj_dict.get("funeralDirectors"), '')
        self.any_personal_effects = 'true' if obj_dict.get("anyPersonalEffects") else 'false'
        self.personal_affects_details = fallback_to(obj_dict.get("personalEffectDetails"), '')

        self.cultural_priority = bool_to_string(obj_dict.get("culturalPriority"))
        self.faith_priority = bool_to_string(obj_dict.get("faithPriority"))
        self.child_priority = bool_to_string(obj_dict.get("childPriority"))
        self.coroner_priority = bool_to_string(obj_dict.get("coronerPriority"))
        self.other_priority = bool_to_string(obj_dict.get("otherPriority"))
        self.priority_details = fallback_to(obj_dict.get("priorityDetails"), '')

        if is_empty_time(obj_dict.get("timeOfDeath")):
            self.time_of_death = None
        else:
            self.time_of_death = obj_dict.get("timeOfDeath")

        if not (is_empty_date(obj_dict.get("dateOfBirth")) or obj_dict.get("dateOfBirth") is None):
            self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
            self.day_of_birth = self.date_of_birth.day
            self.month_of_birth = self.date_of_birth.month
            self.year_of_birth = self.date_of_birth.year
        else:
            self.date_of_birth = None
            self.day_of_birth = None
            self.month_of_birth = None
            self.year_of_birth = None

        if not (is_empty_date(obj_dict.get("dateOfDeath")) or obj_dict.get("dateOfDeath") is None):
            self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
            self.day_of_death = self.date_of_death.day
            self.month_of_death = self.date_of_death.month
            self.year_of_death = self.date_of_death.year
        else:
            self.date_of_death = None
            self.day_of_death = None
            self.month_of_death = None
            self.year_of_death = None

        self.mode_of_disposal = ''
        for key, value in self.modes_of_disposal.items():
            if key == obj_dict.get("modeOfDisposal"):
                self.mode_of_disposal = key

        self.representatives = []
        if obj_dict.get('representatives'):
            for representative in obj_dict.get("representatives"):
                self.representatives.append(BereavedRepresentative(representative))

    def set_values_from_forms(self, primary_form, secondary_form, bereaved_form, urgency_form):
        self.set_primary_info_values(primary_form) \
            .set_secondary_info_values(secondary_form) \
            .set_bereaved_info_values(bereaved_form) \
            .set_urgency_info_values(urgency_form)

    def set_primary_info_values(self, form):
        self.given_names = form.first_name
        self.surname = form.last_name
        self.gender = form.gender
        self.gender_details = form.gender_details
        self.nhs_number = self.remove_whitespace(form.nhs_number)
        self.hospital_number_1 = form.hospital_number_1
        self.hospital_number_2 = form.hospital_number_2
        self.hospital_number_3 = form.hospital_number_3
        self.day_of_birth = form.day_of_birth
        self.month_of_birth = form.month_of_birth
        self.year_of_birth = form.year_of_birth
        self.day_of_death = form.day_of_death
        self.month_of_death = form.month_of_death
        self.year_of_death = form.year_of_death
        self.time_of_death = form.time_of_death
        self.death_occurred_location_id = form.place_of_death
        return self

    @staticmethod
    def remove_whitespace(string):
        return string.replace(' ', '')

    def set_secondary_info_values(self, form):
        self.house_name_number = form.address_line_1
        self.street = form.address_line_2
        self.town = form.address_town
        self.county = form.address_county
        self.country = form.address_country
        self.postcode = form.address_postcode
        self.last_occupation = form.relevant_occupation
        self.organisation_care_before_death_location_id = form.care_organisation
        self.mode_of_disposal = form.funeral_arrangements
        self.any_implants = form.implanted_devices
        self.implant_details = form.implanted_devices_details
        self.funeral_directors = form.funeral_directors
        self.any_personal_effects = form.personal_effects
        self.personal_affects_details = form.personal_effects_details
        return self

    def set_bereaved_info_values(self, form):
        self.representatives = []
        representative1 = {
            'bereaved_name': form.bereaved_name_1,
            'relationship': form.relationship_1,
            'phone_number': form.phone_number_1,
            'day_of_appointment': form.day_of_appointment_1,
            'month_of_appointment': form.month_of_appointment_1,
            'year_of_appointment': form.year_of_appointment_1,
            'time_of_appointment': form.time_of_appointment_1,
            'appointment_notes': form.appointment_additional_details_1,
        }
        representative2 = {
            'bereaved_name': form.bereaved_name_2,
            'relationship': form.relationship_2,
            'phone_number': form.phone_number_2,
            'day_of_appointment': form.day_of_appointment_2,
            'month_of_appointment': form.month_of_appointment_2,
            'year_of_appointment': form.year_of_appointment_2,
            'time_of_appointment': form.time_of_appointment_2,
            'appointment_notes': form.appointment_additional_details_2,
        }
        self.representatives.append(BereavedRepresentative().set_values_from_form(representative1))
        self.representatives.append(BereavedRepresentative().set_values_from_form(representative2))
        return self

    def set_urgency_info_values(self, form):
        self.faith_priority = form.faith_death
        self.coroner_priority = form.coroner_case
        self.child_priority = form.child_death
        self.cultural_priority = form.cultural_death
        self.other_priority = form.other
        self.priority_details = form.urgency_additional_details
        return self

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_patient_details_by_id(examination_id, auth_token)
        patient_details = None
        error = None
        case_status = None

        if response.ok:
            case_status = CaseStatus(response.json())
            modes_of_disposal_response = request_handler.load_modes_of_disposal(auth_token)
            if modes_of_disposal_response.ok:
                patient_details = PatientDetails(response.json(), modes_of_disposal_response.json(), examination_id)
            else:
                log_api_error('modes of disposal load', '')
                error = handle_error(modes_of_disposal_response, {"action": "loading", "type": "modes of disposal"})
        else:
            log_api_error('patient details load', response.text)
            error = handle_error(response, {"action": "loading", "type": "patient details"})
        return patient_details, case_status, error

    def update(self, submission, auth_token):
        return request_handler.update_patient_details(self.id, submission, auth_token)

    def full_name(self):
        return "%s %s" % (self.given_names, self.surname)

    def get_nhs_number(self):
        return self.nhs_number if self.nhs_number else 'Unknown'

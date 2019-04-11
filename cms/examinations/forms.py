from datetime import datetime

from alerts import messages
from alerts.messages import ErrorFieldRequiredMessage, INVALID_DATE, DEATH_IS_NOT_AFTER_BIRTH, ErrorFieldTooLong
from examinations.models import MedicalTeamMember, MedicalTeam
from medexCms.utils import validate_date, parse_datetime, API_DATE_FORMAT, NONE_DATE, build_date, fallback_to


class PrimaryExaminationInformationForm:

    def __init__(self, request=None):
        self.initialiseErrors()
        if request:
            self.initialise_form_from_data(request)
        else:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.first_name = ""
        self.last_name = ""
        self.gender = ""
        self.gender_details = ""
        self.nhs_number = ""
        self.nhs_number_not_known = ""
        self.hospital_number_1 = ""
        self.hospital_number_2 = ""
        self.hospital_number_3 = ""
        self.date_of_birth = ""
        self.date_of_birth_not_known = ""
        self.date_of_death = ""
        self.date_of_death_not_known = ""
        self.time_of_death = ""
        self.time_of_death_not_known = ""
        self.place_of_death = ""
        self.out_of_hours = ""

    def initialise_form_from_data(self, request):
        self.last_name = request.get("last_name")
        self.first_name = request.get("first_name")
        self.gender = request.get("gender")
        self.gender_details = request.get("gender_details")
        self.nhs_number = request.get("nhs_number")
        self.nhs_number_not_known = True if "nhs_number_not_known" in request else False

        self.set_hospital_numbers(request)

        self.day_of_birth = request.get("day_of_birth")
        self.month_of_birth = request.get("month_of_birth")
        self.year_of_birth = request.get("year_of_birth")
        self.date_of_birth_not_known = (
            True if "date_of_birth_not_known" in request else False
        )
        self.day_of_death = request.get("day_of_death")
        self.month_of_death = request.get("month_of_death")
        self.year_of_death = request.get("year_of_death")
        self.date_of_death_not_known = (
            True if "date_of_death_not_known" in request else False
        )
        self.time_of_death = request.get("time_of_death")
        self.time_of_death_not_known = (
            True if "time_of_death_not_known" in request else False
        )
        self.place_of_death = request.get("place_of_death")
        self.me_office = request.get("me_office")
        self.out_of_hours = True if "out_of_hours" in request else False

    def set_values_from_instance(self, examination):
        self.first_name = examination.given_names
        self.last_name = examination.surname
        self.gender = examination.gender
        self.gender_details = examination.gender_details
        self.nhs_number = examination.nhs_number
        self.nhs_number_not_known = True if not examination.nhs_number else False
        self.hospital_number_1 = examination.hospital_number_1
        self.hospital_number_2 = examination.hospital_number_2
        self.hospital_number_3 = examination.hospital_number_3
        self.day_of_birth = examination.day_of_birth
        self.month_of_birth = examination.month_of_birth
        self.year_of_birth = examination.year_of_birth
        self.date_of_birth_not_known = True if not examination.date_of_birth else False
        self.day_of_death = examination.day_of_death
        self.month_of_death = examination.month_of_death
        self.year_of_death = examination.year_of_death
        self.date_of_death_not_known = True if not examination.date_of_death else False
        self.time_of_death = examination.time_of_death
        self.time_of_death_not_known = True if not examination.time_of_death else False
        self.place_of_death = examination.death_occurred_location_id
        self.out_of_hours = examination.out_of_hours
        self.me_office = examination.medical_examiner_office_responsible
        return self

    def set_hospital_numbers(self, request):
        # get numbers
        self.hospital_number_1 = request.get("hospital_number_1")
        self.hospital_number_2 = request.get("hospital_number_2")
        self.hospital_number_3 = request.get("hospital_number_3")

        # fill an array
        hospital_numbers = [
            self.hospital_number_1,
            self.hospital_number_2,
            self.hospital_number_3,
        ]

        # filter the array
        filled_numbers = self.filter_to_not_blank_values(hospital_numbers)
        filled_numbers = filled_numbers + ["", "", ""]

        # display results
        self.hospital_number_1 = filled_numbers[0]
        self.hospital_number_2 = filled_numbers[1]
        self.hospital_number_3 = filled_numbers[2]

    def filter_to_not_blank_values(self, a_list):
        not_empty = []
        for item in a_list:
            if item != '':
                not_empty.append(item)
        return not_empty

    def initialiseErrors(self):
        self.errors = {"count": 0}

    def is_valid(self):
        self.errors["count"] = 0

        if self.first_name is None or len(self.first_name.strip()) == 0:
            self.errors["first_name"] = ErrorFieldRequiredMessage("first name")
            self.errors["count"] += 1

        if self.first_name and len(self.first_name) > 150:
            self.errors["first_name"] = ErrorFieldTooLong(150)
            self.errors["count"] += 1

        if self.last_name is None or len(self.last_name.strip()) == 0:
            self.errors["last_name"] = ErrorFieldRequiredMessage("last name")
            self.errors["count"] += 1

        if self.last_name and len(self.last_name) > 150:
            self.errors["last_name"] = ErrorFieldTooLong(150)
            self.errors["count"] += 1

        if self.gender is None:
            self.errors["gender"] = ErrorFieldRequiredMessage("gender")
            self.errors["count"] += 1

        if self.gender == 'other' and (self.gender_details is None or len(self.gender_details.strip()) == 0):
            self.errors["gender"] = ErrorFieldRequiredMessage("other gender details")
            self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.nhs_number], self.nhs_number_not_known
        ):
            self.errors["nhs_number"] = ErrorFieldRequiredMessage("NHS number")
            self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.time_of_death], self.time_of_death_not_known
        ):
            self.errors["time_of_death"] = ErrorFieldRequiredMessage("time of death")
            self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.day_of_birth, self.month_of_birth, self.year_of_birth],
                self.date_of_birth_not_known,
        ):
            self.errors["date_of_birth"] = ErrorFieldRequiredMessage("date of birth")
            self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.day_of_death, self.month_of_death, self.year_of_death],
                self.date_of_death_not_known,
        ):
            self.errors["date_of_death"] = ErrorFieldRequiredMessage("date of death")
            self.errors["count"] += 1

        if not self.text_group_is_blank_or_contains_valid_date(self.day_of_death, self.month_of_death,
                                                               self.year_of_death):
            self.errors["date_of_death"] = INVALID_DATE
            self.errors["count"] += 1

        if not self.text_group_is_blank_or_contains_valid_date(self.day_of_birth, self.month_of_birth,
                                                               self.year_of_birth):
            self.errors["date_of_birth"] = INVALID_DATE
            self.errors["count"] += 1

        if not self.dates_are_blank_or_death_is_after_birth_date():
            self.errors["date_of_birth"] = DEATH_IS_NOT_AFTER_BIRTH
            self.errors["date_of_death"] = DEATH_IS_NOT_AFTER_BIRTH
            self.errors["count"] += 1

        if self.place_of_death is None:
            self.errors["place_of_death"] = ErrorFieldRequiredMessage("place of death")
            self.errors["count"] += 1

        if self.me_office is None:
            self.errors["me_office"] = ErrorFieldRequiredMessage("ME office")
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def to_object(self):
        dob = NONE_DATE
        dod = NONE_DATE

        if not self.date_of_birth_not_known:
            dob = build_date(self.year_of_birth, self.month_of_birth, self.day_of_birth).strftime(API_DATE_FORMAT)

        if not self.date_of_death_not_known:
            dod = build_date(self.year_of_death, self.month_of_death, self.day_of_death).strftime(API_DATE_FORMAT)
        return {
            "givenNames": self.first_name,
            "surname": self.last_name,
            "gender": self.gender,
            "genderDetails": self.gender_details,
            "placeDeathOccured": self.place_of_death,
            "medicalExaminerOfficeResponsible": self.me_office,
            "nhsNumber": self.nhs_number,
            "hospitalNumber_1": self.hospital_number_1,
            "hospitalNumber_2": self.hospital_number_2,
            "hospitalNumber_3": self.hospital_number_3,
            "dateOfBirth": dob,
            "dateOfDeath": dod,
            "timeOfDeath": '00:00' if self.time_of_death_not_known else self.time_of_death,
            "outOfHours": 'true' if self.out_of_hours else 'false',
        }

    def text_and_checkbox_group_is_valid(self, textboxes, checkbox):
        if checkbox is None or checkbox is False:
            for textbox in textboxes:
                if textbox is None or len(textbox.strip()) == 0:
                    return False
        return True

    def text_group_is_blank_or_contains_valid_date(self, day, month, year):
        if day and month and year:
            return validate_date(year, month, day)
        else:
            return True

    def dates_are_blank_or_death_is_after_birth_date(self):
        valid_date_of_death = validate_date(self.year_of_death, self.month_of_death, self.day_of_death)
        valid_date_of_birth = validate_date(self.year_of_birth, self.month_of_birth, self.day_of_birth)
        if valid_date_of_death and valid_date_of_birth:
            date_of_death = build_date(self.year_of_death, self.month_of_death, self.day_of_death)
            date_of_birth = build_date(self.year_of_birth, self.month_of_birth, self.day_of_birth)
            if date_of_death >= date_of_birth:
                return True
            else:
                return False
        else:
            return True


class SecondaryExaminationInformationForm:

    def __init__(self, request=None):
        self.errors = {'count': 0}
        if request:
            self.address_line_1 = fallback_to(request.get('address_line_1'), '')
            self.address_line_2 = fallback_to(request.get('address_line_2'), '')
            self.address_town = fallback_to(request.get('address_town'), '')
            self.address_county = fallback_to(request.get('address_county'), '')
            self.address_country = fallback_to(request.get('address_country'), '')
            self.address_postcode = fallback_to(request.get('address_postcode'), '')
            self.relevant_occupation = fallback_to(request.get('relevant_occupation'), '')
            self.care_organisation = fallback_to(request.get('care_organisation'), '')
            self.funeral_arrangements = fallback_to(request.get('funeral_arrangements'), '')
            self.implanted_devices = fallback_to(request.get('implanted_devices'), '')
            self.implanted_devices_details = fallback_to(request.get('implanted_devices_details'), '')
            self.funeral_directors = fallback_to(request.get('funeral_directors'), '')
            self.personal_effects = fallback_to(request.get('personal_effects'), '')
            self.personal_effects_details = fallback_to(request.get('personal_effects_details'), '')
        else:
            self.address_line_1 = ''
            self.address_line_2 = ''
            self.address_town = ''
            self.address_county = ''
            self.address_country = ''
            self.address_postcode = ''
            self.relevant_occupation = ''
            self.care_organisation = ''
            self.funeral_arrangements = ''
            self.implanted_devices = ''
            self.implanted_devices_details = ''
            self.funeral_directors = ''
            self.personal_effects = ''
            self.personal_effects_details = ''

    def set_values_from_instance(self, examination):
        self.address_line_1 = examination.house_name_number
        self.address_line_2 = examination.street
        self.address_town = examination.town
        self.address_county = examination.county
        self.address_country = examination.country
        self.address_postcode = examination.postcode
        self.relevant_occupation = examination.last_occupation
        self.care_organisation = examination.organisation_care_before_death_location_id
        self.funeral_arrangements = examination.mode_of_disposal
        self.implanted_devices = examination.any_implants
        self.implanted_devices_details = examination.implant_details
        self.funeral_directors = examination.funeral_directors
        self.personal_effects = examination.any_personal_effects
        self.personal_effects_details = examination.personal_affects_details
        return self

    def is_valid(self):
        return True

    def for_request(self):
        return {
            'houseNameNumber': self.address_line_1,
            'street': self.address_line_2,
            'town': self.address_town,
            'county': self.address_county,
            'country': self.address_country,
            'postCode': self.address_postcode,
            'lastOccupation': self.relevant_occupation,
            'organisationCareBeforeDeathLocationId': self.care_organisation,
            'modeOfDisposal': self.funeral_arrangements,
            'anyImplants': self.implanted_devices,
            'implantDetails': self.implanted_devices_details,
            'funeralDirectors': self.funeral_directors,
            'anyPersonalEffects': self.personal_effects,
            'personalEffectDetails': self.personal_effects_details,
        }


class BereavedInformationForm:

    def __init__(self, request=None):
        self.errors = {'count': 0}
        if request:
            self.bereaved_name_1 = request.get('bereaved_name_1')
            self.relationship_1 = request.get('relationship_1')
            self.present_death_1 = request.get('present_death_1')
            self.phone_number_1 = request.get('phone_number_1')
            self.informed_1 = request.get('informed_1')
            self.day_of_appointment_1 = request.get('day_of_appointment_1')
            self.month_of_appointment_1 = request.get('month_of_appointment_1')
            self.year_of_appointment_1 = request.get('year_of_appointment_1')
            self.time_of_appointment_1 = request.get('time_of_appointment_1')
            self.bereaved_name_2 = request.get('bereaved_name_2')
            self.relationship_2 = request.get('relationship_2')
            self.present_death_2 = request.get('present_death_2')
            self.phone_number_2 = request.get('phone_number_2')
            self.informed_2 = request.get('informed_2')
            self.day_of_appointment_2 = request.get('day_of_appointment_2')
            self.month_of_appointment_2 = request.get('month_of_appointment_2')
            self.year_of_appointment_2 = request.get('year_of_appointment_2')
            self.time_of_appointment_2 = request.get('time_of_appointment_2')
            self.appointment_additional_details = request.get('appointment_additional_details')
        else:
            self.bereaved_name_1 = ''
            self.relationship_1 = ''
            self.present_death_1 = ''
            self.phone_number_1 = ''
            self.informed_1 = ''
            self.day_of_appointment_1 = ''
            self.month_of_appointment_1 = ''
            self.year_of_appointment_1 = ''
            self.time_of_appointment_1 = ''
            self.bereaved_name_2 = ''
            self.relationship_2 = ''
            self.present_death_2 = ''
            self.phone_number_2 = ''
            self.informed_2 = ''
            self.day_of_appointment_2 = ''
            self.month_of_appointment_2 = ''
            self.year_of_appointment_2 = ''
            self.time_of_appointment_2 = ''
            self.appointment_additional_details = ''

    def set_values_from_instance(self, examination):
        count = 1
        for representative in examination.representatives:
            setattr(self, 'bereaved_name_%s' % count, representative.full_name)
            setattr(self, 'relationship_%s' % count, representative.relationship)
            setattr(self, 'phone_number_%s' % count, representative.phone_number)
            setattr(self, 'present_death_%s' % count, representative.present_at_death)
            setattr(self, 'informed_%s' % count, representative.informed)
            setattr(self, 'day_of_appointment_%s' % count, representative.appointment_day)
            setattr(self, 'month_of_appointment_%s' % count, representative.appointment_month)
            setattr(self, 'year_of_appointment_%s' % count, representative.appointment_year)
            setattr(self, 'time_of_appointment_%s' % count, representative.appointment_time)
            count += 1
        # TODO: appointment_additional_details is not currently in the examinations model
        self.appointment_additional_details = ''
        return self

    def is_valid(self):
        valid_date_1 = True
        valid_date_2 = True

        if all(v is not '' for v in [self.year_of_appointment_1, self.month_of_appointment_1,
                                     self.day_of_appointment_1, self.time_of_appointment_1]):
            hours = self.time_of_appointment_1.split(':')[0]
            mins = self.time_of_appointment_1.split(':')[1]
            valid_date_1 = validate_date(self.year_of_appointment_1, self.month_of_appointment_1,
                                         self.day_of_appointment_1, hours, mins)

        elif any(v is not '' for v in [self.year_of_appointment_1, self.month_of_appointment_1,
                                       self.day_of_appointment_1, self.time_of_appointment_1]):
            valid_date_1 = False

        if not valid_date_1:
            self.errors['count'] += 1
            self.errors['date_of_appointment_1'] = messages.INVALID_DATE

        if all(v is not '' for v in [self.year_of_appointment_2, self.month_of_appointment_2,
                                     self.day_of_appointment_2, self.time_of_appointment_2]):
            hours = self.time_of_appointment_2.split(':')[0]
            mins = self.time_of_appointment_2.split(':')[1]
            valid_date_2 = validate_date(self.year_of_appointment_2, self.month_of_appointment_2,
                                         self.day_of_appointment_2, hours, mins)

        elif any(v is not '' for v in [self.year_of_appointment_2, self.month_of_appointment_2,
                                       self.day_of_appointment_2, self.time_of_appointment_1]):
            valid_date_2 = False

        if not valid_date_2:
            self.errors['count'] += 1
            self.errors['date_of_appointment_1'] = messages.INVALID_DATE

        return True if valid_date_1 and valid_date_2 else False

    def for_request(self):
        representatives = []
        if self.bereaved_name_1:
            appointment_1_date = None
            if self.day_of_appointment_1 and self.month_of_appointment_1 and self.year_of_appointment_1:
                appointment_1_date = build_date(self.year_of_appointment_1, self.month_of_appointment_1,
                                                self.day_of_appointment_1).strftime(API_DATE_FORMAT)
            representatives.append({
                "fullName": self.bereaved_name_1,
                "relationship": self.relationship_1,
                "phoneNumber": self.phone_number_1,
                "presentAtDeath": self.present_death_1,
                "informed": self.informed_1,
                "appointmentDate": appointment_1_date,
                "appointmentTime": self.time_of_appointment_1
            })
        if self.bereaved_name_2:
            appointment_2_date = None
            if self.day_of_appointment_2 and self.month_of_appointment_2 and self.year_of_appointment_2:
                appointment_2_date = build_date(self.year_of_appointment_2, self.month_of_appointment_2,
                                                self.day_of_appointment_2).strftime(API_DATE_FORMAT)
            representatives.append({
                "fullName": self.bereaved_name_2,
                "relationship": self.relationship_2,
                "phoneNumber": self.present_death_2,
                "presentAtDeath": self.phone_number_2,
                "informed": self.informed_2,
                "appointmentDate": appointment_2_date,
                "appointmentTime": self.time_of_appointment_2
            })
        return {
            'representatives': representatives,
        }


class UrgencyInformationForm:

    def __init__(self, request=None):
        self.errors = {'count': 0}
        if request:
            self.faith_death = request.get('faith_death')
            self.coroner_case = request.get('coroner_case')
            self.child_death = request.get('child_death')
            self.cultural_death = request.get('cultural_death')
            self.other = request.get('other')
            self.urgency_additional_details = request.get('urgency_additional_details')
        else:
            self.faith_death = ''
            self.coroner_case = ''
            self.child_death = ''
            self.cultural_death = ''
            self.other = ''
            self.urgency_additional_details = ''

    def set_values_from_instance(self, examination):
        self.faith_death = examination.faith_priority
        self.coroner_case = examination.coroner_priority
        self.child_death = examination.child_priority
        self.cultural_death = examination.cultural_priority
        self.other = examination.other_priority
        self.urgency_additional_details = examination.priority_details
        return self

    def is_valid(self):
        return True

    def for_request(self):
        return {
            'faithPriority': 'true' if self.faith_death else 'false',
            'coronerPriority': 'true' if self.coroner_case else 'false',
            'childPriority': 'true' if self.child_death else 'false',
            'culturalPriority': 'true' if self.cultural_death else 'false',
            'otherPriority': 'true' if self.other else 'false',
            'priorityDetails': self.urgency_additional_details,
        }


class MedicalTeamMembersForm:
    consultant_1 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
    consultant_2 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
    consultant_3 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
    qap = MedicalTeamMember(name='', role='', organisation='', phone_number='')
    gp = MedicalTeamMember(name='', role='', organisation='', phone_number='')
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
                                              notes=request.get('consultant_note_1'))
        self.consultant_2 = MedicalTeamMember(name=request.get('consultant_name_2'),
                                              role=request.get('consultant_role_2'),
                                              organisation=request.get('consultant_organisation_2'),
                                              phone_number=request.get('consultant_phone_number_2'),
                                              notes=request.get('consultant_note_2'))
        self.consultant_3 = MedicalTeamMember(name=request.get('consultant_name_3'),
                                              role=request.get('consultant_role_3'),
                                              organisation=request.get('consultant_organisation_3'),
                                              phone_number=request.get('consultant_phone_number_3'),
                                              notes=request.get('consultant_note_3'))
        self.qap = MedicalTeamMember(name=request.get('qap_name'),
                                     role=request.get('qap_role'),
                                     organisation=request.get('qap_organisation'),
                                     phone_number=request.get('qap_phone_number'),
                                     notes=request.get('qap_note_1'))
        self.gp = MedicalTeamMember(name=request.get('gp_name'),
                                    role=request.get('gp_role'),
                                    organisation=request.get('gp_organisation'),
                                    phone_number=request.get('gp_phone_number'),
                                    notes=request.get('gp_note_1'))
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

    def to_object(self):
        consultants_other = []
        if self.consultant_2.has_name():
            consultants_other.append(self.consultant_2.to_object())
        if self.consultant_3.has_name():
            consultants_other.append(self.consultant_3.to_object())

        obj = {
            "consultantResponsible": self.consultant_1.to_object(),
            "consultantsOther": consultants_other,
            "nursingTeamInformation": self.nursing_team_information,
            "medicalExaminerUserId": self.medical_examiner,
            "medicalExaminerOfficerUserId": self.medical_examiners_officer,
        }

        if self.qap.has_name():
            obj['qap'] = self.qap.to_object()

        if self.gp.has_name():
            obj['generalPractitioner'] = self.gp.to_object()

        return obj


class PreScrutinyEventForm:

    def __init__(self, form_data):
        self.me_thoughts = form_data.get('me-thoughts')
        self.circumstances_of_death = form_data.get('cod')
        self.possible_cod_1a = form_data.get('possible-cod-1a')
        self.possible_cod_1b = form_data.get('possible-cod-1b')
        self.possible_cod_1c = form_data.get('possible-cod-1c')
        self.possible_cod_2 = form_data.get('possible-cod-2')
        self.overall_outcome = form_data.get('ops')
        self.governance_review = form_data.get('gr')
        self.governance_review_text = form_data.get('grt')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def is_valid(self):
        return True

    def for_request(self):
        return {
          "medicalExaminerThoughts": self.me_thoughts,
          "isFinal": self.is_final,
          "circumstancesOfDeath": self.circumstances_of_death,
          "causeOfDeath1a": self.possible_cod_1a,
          "causeOfDeath1b": self.possible_cod_1b,
          "causeOfDeath1c": self.possible_cod_1c,
          "causeOfDeath2": self.possible_cod_2,
          "outcomeOfPreScrutiny": self.overall_outcome,
          "clinicalGovernanceReview": self.governance_review,
          "clinicalGovernanceReviewText": self.governance_review_text
        }


class OtherEventForm:

    def __init__(self, form_data):
        self.more_detail = form_data.get('more-detail')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def is_valid(self):
        return True

    def for_request(self):
        return {
          "text": self.more_detail,
          "isFinal": self.is_final
        }


class AdmissionNotesEventForm:
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, form_data):
        self.admission_day = form_data.get('day_of_last_admission')
        self.admission_month = form_data.get('month_of_last_admission')
        self.admission_year = form_data.get('year_of_last_admission')
        self.admission_date_unknown = form_data.get('date_of_last_admission_not_known')
        self.admission_time = form_data.get('time_of_last_admission')
        self.admission_time_unknown = form_data.get('time_of_last_admission_not_known')
        self.admission_notes = form_data.get('latest_admission_notes')
        self.coroner_referral = form_data.get('latest-admission-suspect-referral')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def is_valid(self):
        return True

    def admission_date(self):
        if self.admission_date_unknown:
            return None
        else:
            return build_date(self.admission_year, self.admission_month, self.admission_day).strftime(self.date_format)

    def get_immediate_coroner_referral(self):
        return True if self.coroner_referral == 'yes' else False

    def for_request(self):
        return {
          "notes": self.admission_notes,
          "isFinal": self.is_final,
          "admittedDate": self.admission_date(),
          "admittedTime": None if self.admission_time_unknown else self.admission_time,
          "immediateCoronerReferral": self.get_immediate_coroner_referral()
        }

from datetime import datetime

from alerts import messages
from alerts.messages import ErrorFieldRequiredMessage, INVALID_DATE, DEATH_IS_NOT_AFTER_BIRTH, ErrorFieldTooLong
from medexCms.utils import validate_date, parse_datetime, API_DATE_FORMAT, NONE_DATE


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
            dob = datetime(self.year_of_birth, self.month_of_birth, self.day_of_birth).strftime(API_DATE_FORMAT)

        if not self.date_of_death_not_known:
            dod = datetime(self.year_of_death, self.month_of_death, self.day_of_death).strftime(API_DATE_FORMAT)
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
            date_of_death = datetime(int(self.year_of_death), int(self.month_of_death), int(self.day_of_death), 0, 0)
            date_of_birth = datetime(int(self.year_of_birth), int(self.month_of_birth), int(self.day_of_birth), 0, 0)
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
            self.address_line_1 = request.get('address_line_1')
            self.address_line_2 = request.get('address_line_2')
            self.address_town = request.get('address_town')
            self.address_county = request.get('address_county')
            self.address_postcode = request.get('address_postcode')
            self.relevant_occupation = request.get('relevant_occupation')
            self.care_organisation = request.get('care_organisation')
            self.funeral_arrangements = request.get('funeral_arrangements')
            self.implanted_devices = request.get('implanted_devices')
            self.implanted_devices_details = request.get('implanted_devices_details')
            self.funeral_directors = request.get('funeral_directors')
            self.personal_effects = request.get('personal_effects')
            self.personal_effects_details = request.get('personal_effects_details')
        else:
            self.address_line_1 = ''
            self.address_line_2 = ''
            self.address_town = ''
            self.address_county = ''
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
        self.address_postcode = examination.postcode
        self.relevant_occupation = examination.last_occupation
        self.care_organisation = examination.organisation_care_before_death_location_id
        self.funeral_arrangements = examination.mode_of_disposal
        self.implanted_devices = examination.any_implants
        self.implanted_devices_details = examination.implant_details
        self.funeral_directors = examination.funeral_directors
        self.personal_effects = examination.any_personal_effects
        self.personal_effects_details = examination.personal_affects_details

    def is_valid(self):
        return True

    def for_request(self):
        return {
            'houseNameNumber': self.address_line_1,
            'street': self.address_line_2,
            'town': self.address_town,
            'county': self.address_county,
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
            setattr(self, 'bereaved_name_%s' % count, representative['full_name'])
            setattr(self, 'relationship_%s' % count, representative['relationship'])
            setattr(self, 'phone_number_%s' % count, representative['phone_number'])
            setattr(self, 'present_death_%s' % count, representative['present_at_death'].lower())
            setattr(self, 'informed_%s' % count, representative['informed'].lower())
            appointment_date = parse_datetime(representative['appointment_date'])
            setattr(self, 'day_of_appointment_%s' % count, appointment_date.day)
            setattr(self, 'month_of_appointment_%s' % count, appointment_date.month)
            setattr(self, 'year_of_appointment_%s' % count, appointment_date.year)
            setattr(self, 'time_of_appointment_%s' % count, representative['appointment_time'])
            count += 1
        # TODO: appointment_additional_details is not currently in the examinations model
        self.appointment_additional_details = ''

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
        return {
            'representatives': [],
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

    def __init__(self, request=None):
        self.initialiseErrors()
        if request:
            self.initialise_form_from_data(request)
        else:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.consultant_1 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
        self.consultant_2 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
        self.consultant_3 = MedicalTeamMember(name='', role='', organisation='', phone_number='')
        self.qap = MedicalTeamMember(name='', role='', organisation='', phone_number='')
        self.gp = MedicalTeamMember(name='', role='', organisation='', phone_number='')

    def initialise_form_from_data(self, request):
        self.consultant_1 = MedicalTeamMember(name=request.get('consultant_name_1'),
                                              role=request.get('consultant_role_1'),
                                              organisation=request.get('consultant_organisation_1'),
                                              phone_number=request.get('consultant_phone_number_1'))
        self.consultant_2 = MedicalTeamMember(name=request.get('consultant_name_2'),
                                              role=request.get('consultant_role_2'),
                                              organisation=request.get('consultant_organisation_2'),
                                              phone_number=request.get('consultant_phone_number_2'))
        self.consultant_3 = MedicalTeamMember(name=request.get('consultant_name_3'),
                                              role=request.get('consultant_role_3'),
                                              organisation=request.get('consultant_organisation_3'),
                                              phone_number=request.get('consultant_phone_number_3'))
        self.qap = MedicalTeamMember(name=request.get('qap_name'),
                                     role=request.get('qap_role'),
                                     organisation=request.get('qap_organisation'),
                                     phone_number=request.get('qap_phone_number'))
        self.gp = MedicalTeamMember(name=request.get('gp_name'),
                                    role=request.get('gp_role'),
                                    organisation=request.get('gp_organisation'),
                                    phone_number=request.get('gp_phone_number'))
        self.nursing_team = request.get('nursing_team')

    def is_valid(self):
        return True

    def initialiseErrors(self):
        self.errors = {"count": 0}


class MedicalTeamMember:

    def __init__(self, name='', role='', organisation='', phone_number=''):
        self.name = name.strip() if name else ''
        self.role = role
        self.organisation = organisation
        self.phone_number = phone_number

    def has_name(self):
        return self.name and len(self.name.strip()) > 0

    def has_valid_name(self):
        return len(self.name.strip()) < 250


class MedicalTeamAssignedTeamForm:

    def __init__(self, request=None):
        self.initialiseErrors()
        if request:
            self.initialise_form_from_data(request)
        else:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.medical_examiner = ''
        self.medical_examiners_officer = ''

    def initialise_form_from_data(self, request):
        self.medical_examiner = request.get('medical_examiner')
        self.medical_examiners_officer = request.get('medical_examiners_officer')

    def is_valid(self):
        return True

    def initialiseErrors(self):
        self.errors = {"count": 0}

from alerts.messages import ErrorFieldRequiredMessage, ErrorFieldTooLong, NHS_NUMBER_ERROR, INVALID_DATE, \
    DEATH_IS_NOT_AFTER_BIRTH, api_error_messages, DEATH_DATE_MISSING_WHEN_TIME_GIVEN, NO_GENDER, DOB_IN_FUTURE
from medexCms.api import enums
from medexCms.utils import NONE_DATE, build_date, validate_date, API_DATE_FORMAT, fallback_to, validate_date_time_field
from datetime import datetime


class PrimaryExaminationInformationForm:
    CREATE_AND_CONTINUE_FLAG = 'create-and-continue'
    NHS_MIN_LENGTH = 10
    NHS_MAX_LENGTH = 17

    def __init__(self, request=None):
        self.initialise_errors()
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

    def initialise_errors(self):
        self.errors = {"count": 0}

    @property
    def error_count(self):
        return self.errors['count']

    def is_valid(self):
        self.errors["count"] = 0

        if self.first_name is None or len(self.first_name.strip()) == 0:
            self.errors["first_name"] = ErrorFieldRequiredMessage("a given name")
            self.errors["count"] += 1

        if self.first_name and len(self.first_name) > 150:
            self.errors["first_name"] = ErrorFieldTooLong(150)
            self.errors["count"] += 1

        if self.last_name is None or len(self.last_name.strip()) == 0:
            self.errors["last_name"] = ErrorFieldRequiredMessage("a surname")
            self.errors["count"] += 1

        if self.last_name and len(self.last_name) > 150:
            self.errors["last_name"] = ErrorFieldTooLong(150)
            self.errors["count"] += 1

        if self.gender is None:
            self.errors["gender"] = NO_GENDER
            self.errors["count"] += 1

        if self.gender == enums.gender.OTHER and (self.gender_details is None or len(self.gender_details.strip()) == 0):
            self.errors["gender"] = ErrorFieldRequiredMessage("some more information for gender")
            self.errors["count"] += 1

        # check if nhs number group has content
        if not self.text_and_checkbox_group_is_valid(
                [self.nhs_number], self.nhs_number_not_known
        ):
            self.errors["nhs_number"] = ErrorFieldRequiredMessage("an NHS number")
            self.errors["count"] += 1

        elif not self.nhs_number_not_known:
            # case - nhs number is entered
            if self.nhs_number and self.NHS_MIN_LENGTH <= len(self.nhs_number) <= self.NHS_MAX_LENGTH:
                pass
            else:
                self.errors["nhs_number"] = NHS_NUMBER_ERROR
                self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.time_of_death], self.time_of_death_not_known
        ):
            self.errors["time_of_death"] = ErrorFieldRequiredMessage("a time of death")
            self.errors["count"] += 1

        if not self.text_and_checkbox_group_is_valid(
                [self.day_of_birth, self.month_of_birth, self.year_of_birth],
                self.date_of_birth_not_known,
        ):
            self.errors["date_of_birth"] = ErrorFieldRequiredMessage("a date of birth")
            self.errors["count"] += 1

        if self.date_of_birth_in_future():
            self.errors["date_of_birth"] = DOB_IN_FUTURE

        if not self.text_and_checkbox_group_is_valid(
                [self.day_of_death, self.month_of_death, self.year_of_death],
                self.date_of_death_not_known,
        ):
            self.errors["date_of_death"] = ErrorFieldRequiredMessage("a date of death")
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

        if self.death_time_present_but_date_unknown():
            self.errors["date_of_death"] = DEATH_DATE_MISSING_WHEN_TIME_GIVEN
            self.errors["time_of_death"] = DEATH_DATE_MISSING_WHEN_TIME_GIVEN
            self.errors["count"] += 1

        if self.place_of_death is None or len(self.place_of_death.strip()) == 0:
            self.errors["place_of_death"] = ErrorFieldRequiredMessage("a place of death")
            self.errors["count"] += 1

        if self.me_office is None:
            self.errors["me_office"] = ErrorFieldRequiredMessage("an ME office")
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def register_known_api_errors(self, api_errors):
        known_errors = []
        nhs_number_errors = self.__get_nhs_number_errors(api_errors)

        if "NhsNumber" in api_errors:
            if enums.errors.CONTAINS_WHITESPACE in nhs_number_errors:
                self.errors["nhs_number"] = api_error_messages.nhs_numbers.CONTAINS_WHITESPACE
                self.errors["count"] += 1
                known_errors = known_errors + [{'field': 'NhsNumber', 'error_code': enums.errors.CONTAINS_WHITESPACE}]

            if enums.errors.CONTAINS_INVALID_CHARACTERS in nhs_number_errors:
                self.errors["nhs_number"] = api_error_messages.nhs_numbers.CONTAINS_INVALID_CHARACTERS
                self.errors["count"] += 1
                known_errors = known_errors + [
                    {'field': 'NhsNumber', 'error_code': enums.errors.CONTAINS_INVALID_CHARACTERS}]

            if enums.errors.INVALID in nhs_number_errors:
                self.errors["nhs_number"] = api_error_messages.nhs_numbers.INVALID
                self.errors["count"] += 1
                known_errors = known_errors + [{'field': 'NhsNumber', 'error_code': enums.errors.INVALID}]

            if enums.errors.DUPLICATE in nhs_number_errors:
                self.errors["nhs_number"] = api_error_messages.nhs_numbers.DUPLICATE
                self.errors["count"] += 1
                known_errors = known_errors + [{'field': 'NhsNumber', 'error_code': enums.errors.DUPLICATE}]

        if "DateOfBirth" in api_errors:
            dob_errors = api_errors["DateOfBirth"]
            if enums.errors.END_DATE_BEFORE_START_DATE in dob_errors:
                self.errors["date_of_birth"] = api_error_messages.date_of_birth.DATE_OF_BIRTH_AFTER_DATE_OF_DEATH
                self.errors["count"] += 1

        return known_errors

    def register_unknown_api_errors(self, api_errors):
        KNOWN_API_ERROR_LIST = [enums.errors.CONTAINS_WHITESPACE, enums.errors.CONTAINS_INVALID_CHARACTERS,
                                enums.errors.INVALID, enums.errors.DUPLICATE]
        nhs_number_errors = self.__get_nhs_number_errors(api_errors)
        if nhs_number_errors:
            for error in nhs_number_errors:
                if not error in KNOWN_API_ERROR_LIST:
                    self.errors["nhs_number"] = api_error_messages.nhs_numbers.UNKNOWN
                    self.errors["count"] += 1
                    return [{'field': 'NhsNumber', 'error_code': enums.errors.UNKNOWN}]
        return []

    def register_form_errors(self, api_errors):
        if 'message' in api_errors:
            self.errors['count'] += 1
            self.errors['form'] = api_errors['message']
        return [{'field': 'MedicalTeamForm', 'error_code': 500}]

    def __get_nhs_number_errors(self, api_errors):
        nhs_errors = None
        if "NhsNumber" in api_errors:
            nhs_errors = api_errors["NhsNumber"]
        elif "examinationId.NhsNumber" in api_errors:
            nhs_errors = api_errors["examinationId.NhsNumber"]
        return nhs_errors

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

    def date_of_birth_in_future(self):
        valid_date_of_birth = validate_date(self.year_of_birth, self.month_of_birth, self.day_of_birth)
        if valid_date_of_birth:
            date_of_birth = build_date(self.year_of_birth, self.month_of_birth, self.day_of_birth)
            current_date = datetime.today()
            if date_of_birth > current_date:
                return True
        else:
            return False

    def death_time_present_but_date_unknown(self):
        if self.date_of_death_not_known and not self.time_of_death_not_known:
            return True
        else:
            return False

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


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

    @property
    def error_count(self):
        return self.errors['count']

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
            self.appointment_additional_details_1 = request.get('appointment_additional_details_1')
            self.bereaved_name_2 = request.get('bereaved_name_2')
            self.relationship_2 = request.get('relationship_2')
            self.present_death_2 = request.get('present_death_2')
            self.phone_number_2 = request.get('phone_number_2')
            self.informed_2 = request.get('informed_2')
            self.day_of_appointment_2 = request.get('day_of_appointment_2')
            self.month_of_appointment_2 = request.get('month_of_appointment_2')
            self.year_of_appointment_2 = request.get('year_of_appointment_2')
            self.time_of_appointment_2 = request.get('time_of_appointment_2')
            self.appointment_additional_details_2 = request.get('appointment_additional_details_2')
        else:
            self.bereaved_name_1 = ''
            self.relationship_1 = ''
            self.present_death_1 = enums.yes_no.UNKNOWN
            self.phone_number_1 = ''
            self.informed_1 = enums.yes_no.UNKNOWN
            self.day_of_appointment_1 = ''
            self.month_of_appointment_1 = ''
            self.year_of_appointment_1 = ''
            self.time_of_appointment_1 = ''
            self.appointment_additional_details_1 = ''
            self.bereaved_name_2 = ''
            self.relationship_2 = ''
            self.present_death_2 = enums.yes_no.UNKNOWN
            self.phone_number_2 = ''
            self.informed_2 = enums.yes_no.UNKNOWN
            self.day_of_appointment_2 = ''
            self.month_of_appointment_2 = ''
            self.year_of_appointment_2 = ''
            self.time_of_appointment_2 = ''
            self.appointment_additional_details_2 = ''

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
            setattr(self, 'appointment_additional_details_%s' % count, representative.appointment_notes)
            count += 1
        return self

    def is_valid(self):
        valid_date_1 = validate_date_time_field('date_of_appointment_1', self.errors, self.year_of_appointment_1,
                                                self.month_of_appointment_1, self.day_of_appointment_1,
                                                self.time_of_appointment_1)
        valid_date_2 = validate_date_time_field('date_of_appointment_2', self.errors, self.year_of_appointment_2,
                                                self.month_of_appointment_2, self.day_of_appointment_2,
                                                self.time_of_appointment_2)
        return True if valid_date_1 and valid_date_2 else False

    @property
    def error_count(self):
        return self.errors['count']

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
                "appointmentTime": self.time_of_appointment_1,
                "notes": self.appointment_additional_details_1
            })
        if self.bereaved_name_2:
            appointment_2_date = None
            if self.day_of_appointment_2 and self.month_of_appointment_2 and self.year_of_appointment_2:
                appointment_2_date = build_date(self.year_of_appointment_2, self.month_of_appointment_2,
                                                self.day_of_appointment_2).strftime(API_DATE_FORMAT)
            representatives.append({
                "fullName": self.bereaved_name_2,
                "relationship": self.relationship_2,
                "phoneNumber": self.phone_number_2,
                "presentAtDeath": self.present_death_2,
                "informed": self.informed_2,
                "appointmentDate": appointment_2_date,
                "appointmentTime": self.time_of_appointment_2,
                "notes": self.appointment_additional_details_2
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

    @property
    def error_count(self):
        return self.errors['count']

    def for_request(self):
        return {
            'faithPriority': 'true' if self.faith_death else 'false',
            'coronerPriority': 'true' if self.coroner_case else 'false',
            'childPriority': 'true' if self.child_death else 'false',
            'culturalPriority': 'true' if self.cultural_death else 'false',
            'otherPriority': 'true' if self.other else 'false',
            'priorityDetails': self.urgency_additional_details,
        }

from alerts import messages
from alerts.messages import ErrorFieldRequiredMessage, INVALID_DATE, DEATH_IS_NOT_AFTER_BIRTH, ErrorFieldTooLong
from examinations.models import MedicalTeamMember, CauseOfDeathProposal, CaseQapDiscussionEvent
from medexCms.utils import validate_date, API_DATE_FORMAT, NONE_DATE, build_date, fallback_to
from people.models import BereavedRepresentative


class PrimaryExaminationInformationForm:
    CREATE_AND_CONTINUE_FLAG = 'create-and-continue'

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

    def initialise_errors(self):
        self.errors = {"count": 0}

    @property
    def error_count(self):
        return self.errors['count']

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
                                       self.day_of_appointment_2, self.time_of_appointment_2]):
            valid_date_2 = False

        if not valid_date_2:
            self.errors['count'] += 1
            self.errors['date_of_appointment_2'] = messages.INVALID_DATE

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
    active = False

    def __init__(self, form_data={}):
        self.event_id = form_data.get('pre_scrutiny_id')
        self.me_thoughts = fallback_to(form_data.get('me-thoughts'), '')
        self.circumstances_of_death = form_data.get('cod')
        self.possible_cod_1a = fallback_to(form_data.get('possible-cod-1a'), '')
        self.possible_cod_1b = fallback_to(form_data.get('possible-cod-1b'), '')
        self.possible_cod_1c = fallback_to(form_data.get('possible-cod-1c'), '')
        self.possible_cod_2 = fallback_to(form_data.get('possible-cod-2'), '')
        self.overall_outcome = form_data.get('ops')
        self.governance_review = form_data.get('gr')
        self.governance_review_text = fallback_to(form_data.get('grt'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        return True

    def for_request(self):
        return {
            "eventId": self.event_id,
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

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.me_thoughts = draft.body
        self.circumstances_of_death = draft.circumstances_of_death
        self.possible_cod_1a = draft.cause_of_death_1a
        self.possible_cod_1b = draft.cause_of_death_1b
        self.possible_cod_1c = draft.cause_of_death_1c
        self.possible_cod_2 = draft.cause_of_death_2
        self.overall_outcome = draft.outcome_of_pre_scrutiny
        self.governance_review = draft.clinical_governance_review
        self.governance_review_text = draft.clinical_governance_review_text
        return self


class MeoSummaryEventForm:
    active = False
    errors = {'count': 0}

    def __init__(self, form_data={}):
        self.event_id = form_data.get('meo_summary_id')
        self.meo_summary_notes = fallback_to(form_data.get('meo_summary_notes'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        if self.is_final and self.meo_summary_notes.strip() == '':
            self.errors['count'] += 1
            self.errors['meo_summary_notes'] = messages.ErrorFieldRequiredMessage('summary notes')
            return False
        else:
            return True

    def for_request(self):
        return {
            "eventId": self.event_id,
            "isFinal": self.is_final,
            "summaryDetails": self.meo_summary_notes
        }

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.meo_summary_notes = draft.body
        return self


class OtherEventForm:
    active = False

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('other_notes_id'), '')
        self.more_detail = fallback_to(form_data.get('other-text'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        return True

    def for_request(self):
        return {
            "eventId": self.event_id,
            "text": self.more_detail,
            "isFinal": self.is_final
        }

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.more_detail = draft.body
        return self


class MedicalHistoryEventForm:
    active = False

    def __init__(self, form_data={}):
        self.event_id = form_data.get('history_notes_id')
        self.medical_history_details = fallback_to(form_data.get('medical-history-details'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        return True

    def for_request(self):
        return {
            "eventId": self.event_id,
            "text": self.medical_history_details,
            "isFinal": self.is_final
        }

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.medical_history_details = draft.body
        return self


class QapDiscussionEventForm:
    active = False
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def make_active(self):
        self.active = True
        return self

    def __init__(self, form_data={}):

        self.event_id = form_data.get('qap_discussion_id')

        self.discussion_participant_type = fallback_to(form_data.get('qap-discussion-doctor'), '')

        self.qap_default_qap_name = fallback_to(form_data.get('qap-default__full-name'), '')
        self.qap_default_qap_role = fallback_to(form_data.get('qap-default__role'), '')
        self.qap_default_qap_organisation = fallback_to(form_data.get('qap-default__organisation'), '')
        self.qap_default_qap_phone_number = fallback_to(form_data.get('qap-default__phone-number'), '')

        self.qap_discussion_name = fallback_to(form_data.get('qap-other__full-name'), '')
        self.qap_discussion_role = fallback_to(form_data.get('qap-other__role'), '')
        self.qap_discussion_organisation = fallback_to(form_data.get('qap-other__organisation'), '')
        self.qap_discussion_phone_number = fallback_to(form_data.get('qap-other__phone-number'), '')

        self.cause_of_death = CauseOfDeathProposal()
        self.cause_of_death.section_1a = fallback_to(form_data.get('qap_discussion_revised_1a'), '')
        self.cause_of_death.section_1b = fallback_to(form_data.get('qap_discussion_revised_1b'), '')
        self.cause_of_death.section_1c = fallback_to(form_data.get('qap_discussion_revised_1c'), '')
        self.cause_of_death.section_2 = fallback_to(form_data.get('qap_discussion_revised_2'), '')

        self.discussion_details = fallback_to(form_data.get('qap_discussion_details'), '')

        self.outcome = fallback_to(form_data.get('qap-discussion-outcome'), '')
        self.outcome_decision = fallback_to(form_data.get('qap-discussion-outcome-decision'), '')

        self.day_of_conversation = fallback_to(form_data.get('qap_day_of_conversation'), '')
        self.month_of_conversation = fallback_to(form_data.get('qap_month_of_conversation'), '')
        self.year_of_conversation = fallback_to(form_data.get('qap_year_of_conversation'), '')
        self.time_of_conversation = fallback_to(form_data.get('qap_time_of_conversation'), '')

        self.is_final = True if form_data.get('add-event-to-timeline') else False

    @staticmethod
    def __draft_participant_is_default_qap(draft, default_qap):
        return default_qap is not None and \
               default_qap.name == draft.participant_name and \
               default_qap.phone_number == draft.participant_phone_number and \
               default_qap.organisation == draft.participant_organisation and \
               default_qap.role == draft.participant_role

    def fill_from_draft(self, draft, default_qap):
        # simple values
        self.event_id = fallback_to(draft.event_id, '')

        # in this refactor we make calculations with default qap details at the fill stage
        self.__calculate_discussion_participant_alternatives(default_qap, draft)

        self.__fill_default_qap_from_draft(default_qap)

        self.__calculate_time_values(draft)

        self.discussion_details = draft.discussion_details

        self.__calculate_discussion_outcome_radio_button_combination(draft)

        # fill alternate cause of death boxes
        self.__fill_cause_of_death_from_draft(draft)

        return self

    def __fill_cause_of_death_from_draft(self, draft):
        self.cause_of_death = CauseOfDeathProposal()
        self.cause_of_death.section_1a = draft.cause_of_death_1a
        self.cause_of_death.section_1b = draft.cause_of_death_1b
        self.cause_of_death.section_1c = draft.cause_of_death_1c
        self.cause_of_death.section_2 = draft.cause_of_death_2

    def __calculate_discussion_participant_alternatives(self, default_qap, draft):
        if self.__draft_participant_is_default_qap(draft, default_qap):
            self.discussion_participant_type = "qap"
        elif default_qap and (draft is None or draft.participant_name is None):
            self.discussion_participant_type = "qap"
        else:
            self.discussion_participant_type = "other"
            self.qap_discussion_name = draft.participant_name
            self.qap_discussion_role = draft.participant_role
            self.qap_discussion_organisation = draft.participant_organisation
            self.qap_discussion_phone_number = draft.participant_phone_number

    def __fill_default_qap_from_draft(self, default_qap):
        if default_qap:
            self.qap_default_qap_name = default_qap.name
            self.qap_default_qap_role = default_qap.role
            self.qap_default_qap_organisation = default_qap.organisation
            self.qap_default_qap_phone_number = default_qap.phone_number

    def __calculate_discussion_outcome_radio_button_combination(self, draft):
        api_outcome = draft.qap_discussion_outcome
        if api_outcome == CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_FROM_QAP:
            self.outcome = "mccd"
            self.outcome_decision = "outcome-decision-1"
        elif api_outcome == CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_FROM_ME:
            self.outcome = "mccd"
            self.outcome_decision = "outcome-decision-2"
        elif api_outcome == CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_AGREED_UPDATE:
            self.outcome = "mccd"
            self.outcome_decision = "outcome-decision-3"
        elif api_outcome == CaseQapDiscussionEvent.DISCUSSION_OUTCOME_CORONER:
            self.outcome = "coroner"
            self.outcome_decision = ""

    def __calculate_time_values(self, draft):
        date_of_conversation = draft.date_of_conversation
        if date_of_conversation is not None:
            # Individual day, month, year values
            self.day_of_conversation = date_of_conversation.day
            self.month_of_conversation = date_of_conversation.month
            self.year_of_conversation = date_of_conversation.year

            # Time as a string
            hr_str = ("0%s" % date_of_conversation.hour)[-2:]
            min_str = ("0%s" % date_of_conversation.minute)[-2:]
            self.time_of_conversation = "%s:%s" % (hr_str, min_str)
        else:
            self.day_of_conversation = ''
            self.month_of_conversation = ''
            self.year_of_conversation = ''
            self.time_of_conversation = ''

    def is_valid(self):
        return True

    def for_request(self):
        name, role, organisation, phone_number = self.__participant_for_request()

        date_of_conversation = self.__calculate_full_date_of_conversation()

        outcome = self.__calculate_discussion_outcome()

        return {
            "eventId": self.event_id,
            "isFinal": self.is_final,
            "participantRoll": role,
            "participantOrganisation": organisation,
            "participantPhoneNumber": phone_number,
            "discussionUnableHappen": False,
            "discussionDetails": self.discussion_details,
            "qapDiscussionOutcome": outcome,
            "participantName": name,
            "causeOfDeath1a": self.cause_of_death.section_1a,
            "causeOfDeath1b": self.cause_of_death.section_1b,
            "causeOfDeath1c": self.cause_of_death.section_1c,
            "causeOfDeath2": self.cause_of_death.section_2,
            "dateOfConversation": date_of_conversation.strftime(API_DATE_FORMAT)
        }

    def __participant_for_request(self):
        if self.discussion_participant_type == 'other':
            name = self.qap_discussion_name
            role = self.qap_discussion_role
            organisation = self.qap_discussion_organisation
            phone_number = self.qap_discussion_phone_number
        else:
            name = self.qap_default_qap_name
            role = self.qap_default_qap_role
            organisation = self.qap_default_qap_organisation
            phone_number = self.qap_default_qap_phone_number
        return name, role, organisation, phone_number

    def __calculate_discussion_outcome(self):
        if self.outcome == 'mccd':
            if self.outcome_decision == 'outcome-decision-1':
                return CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_FROM_QAP
            elif self.outcome_decision == 'outcome-decision-2':
                return CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_FROM_ME
            elif self.outcome_decision == 'outcome-decision-3':
                return CaseQapDiscussionEvent.DISCUSSION_OUTCOME_MCCD_AGREED_UPDATE
        elif self.outcome == 'coroner':
            return CaseQapDiscussionEvent.DISCUSSION_OUTCOME_CORONER

    def __calculate_full_date_of_conversation(self):
        if self.day_of_conversation != '' and self.month_of_conversation != '' and self.year_of_conversation != '':
            hr, minute = self.__calculate_hour_and_minute_of_conversation()
            return build_date(self.year_of_conversation, self.month_of_conversation,
                              self.day_of_conversation, hr, minute)
        else:
            return None

    def __calculate_hour_and_minute_of_conversation(self):
        hr = 0
        minute = 0
        time_components = self.time_of_conversation.split(":")
        if len(time_components) >= 2:
            hr = int(time_components[0])
            minute = int(time_components[1])
        return hr, minute


class AdmissionNotesEventForm:
    YES = 'yes'
    NO = 'no'

    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    active = False

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('admission_notes_id'), '')
        self.admission_day = fallback_to(form_data.get('day_of_last_admission'), '')
        self.admission_month = fallback_to(form_data.get('month_of_last_admission'), '')
        self.admission_year = fallback_to(form_data.get('year_of_last_admission'), '')
        self.admission_date_unknown = fallback_to(form_data.get('date_of_last_admission_not_known'), '')
        self.admission_time = fallback_to(form_data.get('time_of_last_admission'), '')
        self.admission_time_unknown = fallback_to(form_data.get('time_of_last_admission_not_known'), '')
        self.admission_notes = fallback_to(form_data.get('latest_admission_notes'), '')
        self.coroner_referral = fallback_to(form_data.get('latest_admission_immediate_referral'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

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
            "eventId": self.event_id,
            "notes": self.admission_notes,
            "isFinal": self.is_final,
            "admittedDate": self.admission_date(),
            "admittedTime": None if self.admission_time_unknown else self.admission_time,
            "immediateCoronerReferral": self.get_immediate_coroner_referral()
        }

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.admission_day = draft.admitted_date.day if draft.admitted_date else ''
        self.admission_month = draft.admitted_date.month if draft.admitted_date else ''
        self.admission_year = draft.admitted_date.year if draft.admitted_date else ''
        self.admission_date_unknown = False if draft.admitted_date else True
        self.admission_time = draft.admitted_time
        self.admission_time_unknown = False if draft.admitted_time else True
        self.admission_notes = draft.body
        self.coroner_referral = 'yes' if draft.immediate_coroner_referral else 'no'
        return self


class BereavedDiscussionEventForm:
    # constants
    REPRESENTATIVE_TYPE_EXISTING = 'existing-rep'
    REPRESENTATIVE_TYPE_ALTERNATE = 'alternate-rep'

    BEREAVED_OUTCOME_NO_CONCERNS = 'no concerns'
    BEREAVED_OUTCOME_CONCERNS = 'concerns'

    BEREAVED_CONCERNED_OUTCOME_CORONER = 'coroner'
    BEREAVED_CONCERNED_OUTCOME_100A = '100a'
    BEREAVED_CONCERNED_OUTCOME_ADDRESSED = 'addressed'

    BEREAVED_RADIO_YES = 'yes'
    BEREAVED_RADIO_NO = 'no'
    BEREAVED_RADIO_UNKNOWN = 'unknown'

    REQUEST_OUTCOME_NO_CONCERNS = "CauseOfDeathAccepted"
    REQUEST_OUTCOME_CORONER = "ConcernsCoronerInvestigation"
    REQUEST_OUTCOME_100A = "ConcernsRequires100a"
    REQUEST_OUTCOME_ADDRESSED = "ConcernsAddressedWithoutCoroner"

    # properties
    active = False
    event_id = ''
    use_existing_bereaved = False
    discussion_representative_type = ''
    existing_representative = None
    alternate_representative = None
    discussion_details = ''
    discussion_outcome = ''
    discussion_concerned_outcome = ''
    day_of_conversation = ''
    month_of_conversation = ''
    year_of_conversation = ''
    discussion_could_not_happen = False

    def make_active(self):
        self.active = True
        return self

    # init from form_data (used on POST request)
    def __init__(self, form_data={}, representatives=[]):

        self.event_id = fallback_to(form_data.get('bereaved_event_id'), '')

        if len(form_data) > 0:
            self.__init_representatives_from_draft(form_data)
        elif len(representatives) > 0:
            self.__init_representatives(representatives)

        self.__init_time_of_discussion(form_data)
        self.__init_discussion_details(form_data)

    def __init_representatives(self, representatives):
        self.existing_representative = representatives[0]
        self.discussion_representative_type = self.REPRESENTATIVE_TYPE_EXISTING
        self.use_existing_bereaved = True

    def __init_representatives_from_draft(self, form_data):
        self.__init_existing_representative(form_data)
        self.__init_alternate_representative(form_data)
        self.__init_type_of_representative(form_data)

    def __init_type_of_representative(self, form_data):
        self.discussion_representative_type = fallback_to(form_data.get('bereaved_rep_type'), '')
        self.__set_use_existing_bereaved()

    def __set_use_existing_bereaved(self):
        if self.discussion_representative_type == self.REPRESENTATIVE_TYPE_EXISTING:
            self.use_existing_bereaved = True
        elif self.discussion_representative_type == self.REPRESENTATIVE_TYPE_ALTERNATE:
            self.use_existing_bereaved = False
        elif self.existing_representative:
            self.use_existing_bereaved = True
        else:
            self.use_existing_bereaved = False

    def __init_alternate_representative(self, form_data):
        alternate_bereaved_data = {
            'fullName': fallback_to(form_data.get('bereaved_alternate_rep_name'), ''),
            'relationship': fallback_to(form_data.get('bereaved_alternate_rep_relationship'), ''),
            'phoneNumber': fallback_to(form_data.get('bereaved_alternate_rep_phone_number'), ''),
            'presentAtDeath': fallback_to(form_data.get('bereaved_alternate_rep_present_at_death'), ''),
            'informed': fallback_to(form_data.get('bereaved_alternate_rep_informed'), '')
        }
        self.alternate_representative = BereavedRepresentative(obj_dict=alternate_bereaved_data)

    def __init_existing_representative(self, form_data):
        self.existing_representative = None
        bereaved_existing_name = fallback_to(form_data.get('bereaved_existing_rep_name'), '')
        if len(bereaved_existing_name) > 0:
            existing_bereaved_data = {
                'fullName': bereaved_existing_name,
                'relationship': fallback_to(form_data.get('bereaved_existing_rep_relationship'), ''),
                'phoneNumber': fallback_to(form_data.get('bereaved_existing_rep_phone_number'), ''),
                'presentAtDeath': fallback_to(form_data.get('bereaved_existing_rep_present_at_death'), ''),
                'informed': fallback_to(form_data.get('bereaved_existing_rep_informed'), '')
            }
            self.existing_representative = BereavedRepresentative(obj_dict=existing_bereaved_data)

    def __init_discussion_details(self, form_data):
        self.discussion_details = fallback_to(form_data.get('bereaved_discussion_details'), '')
        self.discussion_outcome = fallback_to(form_data.get('bereaved_discussion_outcome'), '')
        self.discussion_concerned_outcome = fallback_to(form_data.get('bereaved_outcome_concerned_outcome'), '')

    def __init_time_of_discussion(self, form_data):
        self.day_of_conversation = fallback_to(form_data.get('bereaved_day_of_conversation'), '')
        self.month_of_conversation = fallback_to(form_data.get('bereaved_month_of_conversation'), '')
        self.year_of_conversation = fallback_to(form_data.get('bereaved_year_of_conversation'), '')
        self.time_of_conversation = fallback_to(form_data.get('bereaved_time_of_conversation'), '')
        self.discussion_could_not_happen = True if form_data.get(
            'bereaved_discussion_could_not_happen') == self.BEREAVED_RADIO_YES else False

    def is_valid(self):
        return True

    def fill_from_draft(self, draft, default_representatives):

        self.event_id = draft.event_id
        self.discussion_could_not_happen = draft.discussion_unable_happen
        self.discussion_details = draft.discussion_details

        self.__fill_representatives_from_draft(default_representatives, draft)

        self.__calculate_bereaved_outcomes(draft)

        self.__calculate_time_values(draft)

        return self

    def __calculate_bereaved_outcomes(self, draft):
        request_outcome = draft.bereaved_discussion_outcome
        if request_outcome == BereavedDiscussionEventForm.REQUEST_OUTCOME_NO_CONCERNS:
            self.discussion_outcome = BereavedDiscussionEventForm.BEREAVED_OUTCOME_NO_CONCERNS
        elif request_outcome == BereavedDiscussionEventForm.REQUEST_OUTCOME_CORONER:
            self.discussion_outcome = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
            self.discussion_concerned_outcome = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_CORONER
        elif request_outcome == BereavedDiscussionEventForm.REQUEST_OUTCOME_100A:
            self.discussion_outcome = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
            self.discussion_concerned_outcome = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_100A
        elif request_outcome == BereavedDiscussionEventForm.REQUEST_OUTCOME_ADDRESSED:
            self.discussion_outcome = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
            self.discussion_concerned_outcome = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_ADDRESSED

    def __calculate_time_values(self, draft):
        date_of_conversation = draft.date_of_conversation
        if date_of_conversation is not None:
            # Individual day, month, year values
            self.day_of_conversation = date_of_conversation.day
            self.month_of_conversation = date_of_conversation.month
            self.year_of_conversation = date_of_conversation.year

            # Time as a string
            hr_str = ("0%s" % date_of_conversation.hour)[-2:]
            min_str = ("0%s" % date_of_conversation.minute)[-2:]
            self.time_of_conversation = "%s:%s" % (hr_str, min_str)
        else:
            self.day_of_conversation = ''
            self.month_of_conversation = ''
            self.year_of_conversation = ''
            self.time_of_conversation = ''

    def __fill_representatives_from_draft(self, default_representatives, draft):

        self.existing_representative = None
        self.alternate_representative = None
        if default_representatives and len(default_representatives) > 0:
            self.existing_representative = default_representatives[0]
        draft_participant = None
        if len(draft.participant_full_name) > 0:
            draft_participant = BereavedRepresentative({
                "fullName": draft.participant_full_name,
                "relationship": draft.participant_relationship,
                'phoneNumber': draft.participant_phone_number,
                'presentAtDeath': draft.present_at_death,
                'informed': draft.informed_at_death,
            })
        if draft_participant is None:
            if self.existing_representative is not None:
                self.discussion_representative_type = BereavedDiscussionEventForm.REPRESENTATIVE_TYPE_EXISTING
            else:
                self.discussion_representative_type = BereavedDiscussionEventForm.REPRESENTATIVE_TYPE_ALTERNATE
        else:
            if draft_participant.equals(self.existing_representative):
                self.discussion_representative_type = BereavedDiscussionEventForm.REPRESENTATIVE_TYPE_EXISTING
            else:
                self.discussion_representative_type = BereavedDiscussionEventForm.REPRESENTATIVE_TYPE_ALTERNATE
                self.alternate_representative = draft_participant

        self.__set_use_existing_bereaved()

    def for_request(self):
        date_of_conversation = self.__calculate_full_date_of_conversation()

        participant = self.__participant_for_request()

        return {
            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
            "userId": "WERGT-243TRGS-WE4TG-WERGT",
            "isFinal": True,
            "eventType": "BereavedDiscussion",
            "created": "2019-03-13T10:30:43.019Z",
            "participantFullName": participant.full_name if participant else "",
            "participantRelationship": participant.relationship if participant else "",
            "participantPhoneNumber": participant.phone_number if participant else "",
            "presentAtDeath": participant.present_at_death if participant else "",
            "informedAtDeath": participant.informed if participant else "",
            "dateOfConversation": date_of_conversation.strftime(API_DATE_FORMAT) if date_of_conversation else '',
            "discussionUnableHappen": self.discussion_could_not_happen,
            "discussionDetails": self.discussion_details,
            "bereavedDiscussionOutcome": self.__calculate_combined_outcome()
        }

    def __calculate_combined_outcome(self):
        if self.discussion_outcome == BereavedDiscussionEventForm.BEREAVED_OUTCOME_NO_CONCERNS:
            return BereavedDiscussionEventForm.REQUEST_OUTCOME_NO_CONCERNS
        elif self.discussion_outcome == BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS:
            if self.discussion_concerned_outcome == BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_CORONER:
                return BereavedDiscussionEventForm.REQUEST_OUTCOME_CORONER
            elif self.discussion_concerned_outcome == BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_100A:
                return BereavedDiscussionEventForm.REQUEST_OUTCOME_100A
            elif self.discussion_concerned_outcome == BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_ADDRESSED:
                return BereavedDiscussionEventForm.REQUEST_OUTCOME_ADDRESSED

        return ''

    def __participant_for_request(self):
        if self.discussion_representative_type == BereavedDiscussionEventForm.REPRESENTATIVE_TYPE_EXISTING:
            return self.existing_representative
        else:
            return self.alternate_representative

    def __calculate_full_date_of_conversation(self):
        if self.day_of_conversation != '' and self.month_of_conversation != '' and self.year_of_conversation != '':
            hr, minute = self.__calculate_hour_and_minute_of_conversation()
            return build_date(self.year_of_conversation, self.month_of_conversation,
                              self.day_of_conversation, hr, minute)
        else:
            return None

    def __calculate_hour_and_minute_of_conversation(self):
        hr = 0
        minute = 0
        time_components = self.time_of_conversation.split(":")
        if len(time_components) >= 2:
            hr = int(time_components[0])
            minute = int(time_components[1])
        return hr, minute


class OutstandingItemsForm:

    def __init__(self, form_data):
        self.mccd_issued = form_data.get('mccd_issued')
        self.cremation_form = form_data.get('cremation_form')
        self.gp_notified = form_data.get('gp_notified')

    def for_request(self):
        return {
            "mccdIssed": True if self.mccd_issued == 'true' else False,
            "cremationFormStatus": self.cremation_form,
            "gpNotifedStatus": self.gp_notified
        }

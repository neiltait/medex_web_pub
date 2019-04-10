from rest_framework import status
from datetime import datetime, timedelta

from errors.utils import handle_error
from medexCms.utils import parse_datetime, is_empty_date, bool_to_string, API_DATE_FORMAT

from people.models import BereavedRepresentative
from users.utils import get_user_presenter

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
        self.id = obj_dict.get("examinationId")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.appointment_date = parse_datetime(obj_dict.get("appointmentDate"))
        self.appointment_time = obj_dict.get("appointmentTime")
        self.last_admission = parse_datetime(obj_dict.get("lastAdmission"))
        self.case_created_date = parse_datetime(obj_dict.get("caseCreatedDate"))

    def display_dod(self):
        return self.date_of_death.strftime(self.date_format) if self.date_of_death else 'D.O.D unknown'

    def display_dob(self):
        return self.date_of_birth.strftime(self.date_format) if self.date_of_birth else 'D.O.B unknown'

    def display_appointment_date(self):
        return self.appointment_date.strftime(self.date_format) if self.appointment_date else None

    def calc_age(self):
        if self.date_of_birth and self.date_of_death:
            return self.date_of_death.year - self.date_of_birth.year - (
                    (self.date_of_death.month, self.date_of_death.day) < (
                self.date_of_birth.month, self.date_of_birth.day))
        else:
            return 0

    def calc_last_admission_days_ago(self):
        if self.last_admission:
            delta = datetime.now() - self.last_admission
            return delta.days
        else:
            return 0

    def calc_created_days_ago(self):
        if self.case_created_date:
            delta = datetime.now() - self.case_created_date
            return delta.days
        else:
            return 0

    def urgent(self):
        return True if self.urgency_score and self.urgency_score > 0 else False


class PatientDetails:

    def __init__(self, obj_dict={}, modes_of_disposal={}):
        self.modes_of_disposal = modes_of_disposal

        self.id = obj_dict.get("id")

        self.completed = obj_dict.get("completed")
        self.coroner_status = obj_dict.get("coronerStatus")

        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.gender = obj_dict.get("gender")
        self.gender_details = obj_dict.get("genderDetails")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
        self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
        self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.death_occurred_location_id = obj_dict.get("placeDeathOccured")
        self.medical_examiner_office_responsible = obj_dict.get("medicalExaminerOfficeResponsible")
        self.out_of_hours = obj_dict.get("outOfHours")

        self.house_name_number = obj_dict.get("houseNameNumber")
        self.street = obj_dict.get("street")
        self.town = obj_dict.get("town")
        self.county = obj_dict.get("county")
        self.country = obj_dict.get("country")
        self.postcode = obj_dict.get("postCode")
        self.last_occupation = obj_dict.get("lastOccupation")
        self.organisation_care_before_death_location_id = obj_dict.get("organisationCareBeforeDeathLocationId")
        self.any_implants = 'true' if obj_dict.get("anyImplants") else 'false'
        self.implant_details = obj_dict.get("implantDetails")
        self.funeral_directors = obj_dict.get("funeralDirectors")
        self.any_personal_effects = 'true' if obj_dict.get("anyPersonalEffects") else 'false'
        self.personal_affects_details = obj_dict.get("personalEffectDetails")

        self.cultural_priority = bool_to_string(obj_dict.get("culturalPriority"))
        self.faith_priority = bool_to_string("faithPriority")
        self.child_priority = bool_to_string("childPriority")
        self.coroner_priority = bool_to_string("coronerPriority")
        self.other_priority = bool_to_string("otherPriority")
        self.priority_details = obj_dict.get("priorityDetails")

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
            if value == obj_dict.get("modeOfDisposal"):
                self.mode_of_disposal = key

        self.representatives = []
        if obj_dict.get('representatives'):
            for representative in obj_dict.get("representatives"):
                self.representatives.append(BereavedRepresentative(representative))

    def set_primary_info_values(self, form):
        self.given_names = form.first_name
        self.surname = form.last_name
        self.gender = form.gender
        self.gender_details = form.gender_details
        self.nhs_number = form.nhs_number
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
        self.out_of_hours = form.out_of_hours
        return self

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
            'present_death': form.present_death_1,
            'phone_number': form.phone_number_1,
            'informed': form.informed_1,
            'day_of_appointment': form.day_of_appointment_1,
            'month_of_appointment': form.month_of_appointment_1,
            'year_of_appointment': form.year_of_appointment_1,
            'time_of_appointment': form.time_of_appointment_1,
        }
        representative2 = {
            'bereaved_name': form.bereaved_name_2,
            'relationship': form.relationship_2,
            'present_death': form.present_death_2,
            'phone_number': form.phone_number_2,
            'informed': form.informed_2,
            'day_of_appointment': form.day_of_appointment_2,
            'month_of_appointment': form.month_of_appointment_2,
            'year_of_appointment': form.year_of_appointment_2,
            'time_of_appointment': form.time_of_appointment_2,
        }
        self.representatives.append(BereavedRepresentative().set_values_from_form(representative1))
        self.representatives.append(BereavedRepresentative().set_values_from_form(representative2))
        self.appointment_additional_details = form.appointment_additional_details
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

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            modes_of_disposal = request_handler.load_modes_of_disposal(auth_token)
            return PatientDetails(response.json(), modes_of_disposal)
        else:
            return None

    @classmethod
    def update(cls, examination_id, submission, auth_token):
        return request_handler.update_patient_details(examination_id, submission, auth_token)

    def full_name(self):
        return "%s %s" % (self.given_names, self.surname)

    def get_nhs_number(self):
        return self.nhs_number if self.nhs_number else 'Unknown'


class CaseBreakdown:

    def __init__(self, obj_dict, medical_team):

        self.patient_name = obj_dict.get("patientName")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.time_of_death = obj_dict.get("timeOfDeath")

        ## parse data
        self.event_list = ExaminationEventList(obj_dict.get('caseBreakdown'), self.date_of_death, self.patient_name,
                                               "MEO")
        # self.event_list.create_initial_event(self.patient_name, "TODO", "MEO", self.date_of_death, self.date_of_death,
        #                                      self.time_of_death)
        self.event_list.sort_events_oldest_to_newest()
        self.event_list.add_event_numbers()
        self.medical_team = medical_team

        ## build form objects
        self.__build_case_breakdown_forms()

    def __build_case_breakdown_forms(self):
        self.qap_discussion = CaseBreakdownQAPDiscussion.from_data(self.medical_team,
                                                                   self.event_list.get_latest_me_scrutiny_cause_of_death(),
                                                                   self.event_list.get_qap_discussion_draft())
        self.latest_admission = CaseBreakdownLatestAdmission.from_data(self.event_list.get_latest_admission_draft())

    @classmethod
    def load_by_id(cls, auth_token, examination_id):
        response = request_handler.load_case_breakdown_by_id(examination_id, auth_token)

        medical_team = MedicalTeam.load_by_id(examination_id, auth_token)

        if response.status_code == status.HTTP_200_OK:
            return CaseBreakdown(response.json(), medical_team)
        else:
            return handle_error(response, {'type': 'case', 'action': 'loading'})


class ExaminationEventList:

    def __init__(self, timeline_items, dod, patient_name, user_role):
        self.events = []
        self.drafts = {}
        self.qap_discussion_draft = None
        self.other_notes_draft = None
        self.latest_admission_draft = None
        self.meo_summary_draft = None
        self.medical_history_draft = None
        self.bereaved_discussion_draft = None
        self.me_scrutiny_draft = None
        self.dod = dod
        self.parse_events(timeline_items, patient_name, user_role)

    def parse_events(self, timeline_items, patient_name, user_role):
        for key, event_type in timeline_items.items():
            if key == CaseEvent().INITIAL_EVENT_TYPE and event_type:
                self.events.append(CaseInitialEvent(event_type, patient_name, user_role))
            elif key != CaseEvent().INITIAL_EVENT_TYPE:
                for event in event_type['history']:
                    if event['is_final']:
                        self.events.append(CaseEvent.parse_event(event, event_type['latest']['event_id'], self.dod))
                if event_type['usersDraft']:
                    self.drafts[key] = CaseEvent.parse_event(event_type['usersDraft'], event_type['latest']['event_id'],
                                                             None)

    def sort_events_oldest_to_newest(self):
        self.events.sort(key=lambda event: event.created_date, reverse=False)

    def add_event_numbers(self):
        count = 1
        for event in self.events:
            event.number = count
            count += 1

    def get_qap_discussion_draft(self):
        return self.drafts.get(CaseEvent().QAP_DISCUSSION_EVENT_TYPE)

    def get_other_notes_draft(self):
        return self.drafts.get(CaseEvent().OTHER_EVENT_TYPE)

    def get_latest_admission_draft(self):
        return self.drafts.get(CaseEvent().ADMISSION_NOTES_EVENT_TYPE)

    def get_meo_summary_draft(self):
        return self.drafts.get(CaseEvent().MEO_SUMMARY_EVENT_TYPE)

    def get_medical_history_draft(self):
        return self.drafts.get(CaseEvent().MEDICAL_HISTORY_EVENT_TYPE)

    def get_bereaved_discussion_draft(self):
        return self.drafts.get(CaseEvent().BEREAVED_DISCUSSION_EVENT_TYPE)

    def get_me_scrutiny_draft(self):
        return self.drafts.get(CaseEvent().PRE_SCRUTINY_EVENT_TYPE)

    def get_latest_me_scrutiny_cause_of_death(self):
        return None

    def get_latest_agreed_cause_of_death(self):
        return None


class CaseEvent:
    OTHER_EVENT_TYPE = 'Other'
    PRE_SCRUTINY_EVENT_TYPE = 'PreScrutiny'
    BEREAVED_DISCUSSION_EVENT_TYPE = 'BereavedDiscussion'
    MEO_SUMMARY_EVENT_TYPE = 'MeoSummary'
    QAP_DISCUSSION_EVENT_TYPE = 'QapDiscussion'
    MEDICAL_HISTORY_EVENT_TYPE = 'MedicalHistory'
    ADMISSION_NOTES_EVENT_TYPE = 'Admission'
    INITIAL_EVENT_TYPE = 'patientDeathEvent'

    date_format = '%d.%m.%Y'
    time_format = "%H:%M"

    @classmethod
    def parse_event(cls, event_data, latest_id, dod):
        if event_data.get('event_type') == cls.OTHER_EVENT_TYPE:
            return CaseOtherEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.PRE_SCRUTINY_EVENT_TYPE:
            return CasePreScrutinyEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.BEREAVED_DISCUSSION_EVENT_TYPE:
            return CaseBereavedDiscussionEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.MEO_SUMMARY_EVENT_TYPE:
            return CaseMeoSummaryEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.QAP_DISCUSSION_EVENT_TYPE:
            return CaseQapDiscussionEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.MEDICAL_HISTORY_EVENT_TYPE:
            return CaseMedicalHistoryEvent(event_data, latest_id)
        elif event_data.get('event_type') == cls.ADMISSION_NOTES_EVENT_TYPE:
            return CaseAdmissionNotesEvent(event_data, latest_id, dod)

    def display_date(self):
        if self.created_date:
            date = parse_datetime(self.created_date)
            if date.date() == datetime.today().date():
                return 'Today at %s' % date.strftime(self.time_format)
            elif date.date() == datetime.today().date() - timedelta(days=1):
                return 'Yesterday at %s' % date.strftime(self.time_format)
            else:
                time = date.strftime(self.time_format)
                date = date.strftime(self.date_format)
                return "%s at %s" % (date, time)
        else:
            return None


class CaseInitialEvent(CaseEvent):
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_initial_event_body.html'
    event_type = CaseEvent().INITIAL_EVENT_TYPE
    css_type = 'initial'

    def __init__(self, obj_dict, patient_name, user_role):
        self.number = None
        self.patient_name = patient_name
        self.user_id = obj_dict.get('userId')
        self.user_role = user_role
        self.created_date = obj_dict.get('created')
        self.dod = obj_dict.get('dateOfDeath')
        self.tod = obj_dict.get('timeOfDeath')
        self.is_latest = False  # Used to flag whether can be amend, for the patient died event this is always true

    @property
    def display_type(self):
        return '%s died' % self.patient_name


class CaseOtherEvent(CaseEvent):
    event_type = CaseEvent().OTHER_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_other_event_body.html'
    display_type = 'Other case info'
    css_type = 'other'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('other_event_text')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id


class CasePreScrutinyEvent(CaseEvent):
    event_type = CaseEvent().PRE_SCRUTINY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_pre_scrutiny_event_body.html'
    display_type = 'ME pre-scrutiny'
    css_type = 'pre-scrutiny'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('medical_examiner_thoughts')
        self.circumstances_of_death = obj_dict.get('circumstances_of_death')
        self.cause_of_death_1a = obj_dict.get('cause_of_death_1a')
        self.cause_of_death_1b = obj_dict.get('cause_of_death_1b')
        self.cause_of_death_1c = obj_dict.get('cause_of_death_1c')
        self.cause_of_death_2 = obj_dict.get('cause_of_death_2')
        self.outcome_of_pre_scrutiny = obj_dict.get('outcome_of_pre_scrutiny')
        self.clinical_governance_review = obj_dict.get('clinical_governance_review')
        self.clinical_governance_review_text = obj_dict.get('clinical_governance_review_text')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id


class CaseBereavedDiscussionEvent(CaseEvent):
    event_type = CaseEvent().BEREAVED_DISCUSSION_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_bereaved_discussion_event_body.html'
    display_type = 'Bereaved/representative discussion'
    css_type = 'bereaved-discussion'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.participant_full_name = obj_dict.get('participant_full_name')
        self.participant_relationship = obj_dict.get('participant_relationship')
        self.participant_phone_number = obj_dict.get('participant_phone_number')
        self.present_at_death = obj_dict.get('present_at_death')
        self.informed_at_death = obj_dict.get('informed_at_death')
        self.date_of_conversation = obj_dict.get('date_of_conversation')
        self.discussion_unable_happen = obj_dict.get('discussion_unable_happen')
        self.discussion_details = obj_dict.get('discussion_details')
        self.bereaved_discussion_outcome = obj_dict.get('bereaved_discussion_outcome')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id


class CaseMeoSummaryEvent(CaseEvent):
    event_type = CaseEvent().MEO_SUMMARY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_meo_summary_event_body.html'
    display_type = 'MEO summary'
    css_type = 'meo-summary'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('summary_details')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id


class CaseQapDiscussionEvent(CaseEvent):
    event_type = CaseEvent().QAP_DISCUSSION_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_qap_discussion_event_body.html'
    display_type = 'QAP discussion'
    css_type = 'qap-discussion'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.participant_role = obj_dict.get('participant_roll')
        self.participant_organisation = obj_dict.get('participant_organisation')
        self.participant_phone_number = obj_dict.get('participant_phone_number')
        self.date_of_conversation = parse_datetime(obj_dict.get('date_of_conversation'))
        self.discussion_unable_happen = obj_dict.get('discussion_unable_happen')
        self.discussion_details = obj_dict.get('discussion_details')
        self.qap_discussion_outcome = obj_dict.get('qap_discussion_outcome')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id

    def conversation_display_date(self):
        return self.date_of_conversation.strftime(self.date_format)

    def conversation_display_time(self):
        return self.date_of_conversation.strftime(self.time_format)


class CaseMedicalHistoryEvent(CaseEvent):
    event_type = CaseEvent().MEDICAL_HISTORY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_medical_history_event_body.html'
    display_type = 'Medical history'
    css_type = 'medical-history'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('medical_history_event_text')
        self.published = obj_dict.get('is_final')
        self.is_latest = self.event_id == latest_id


class CaseAdmissionNotesEvent(CaseEvent):
    event_type = CaseEvent().ADMISSION_NOTES_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_admission_notes_event_body.html'
    display_type = 'Admission notes'
    css_type = 'admission-notes'

    def __init__(self, obj_dict, latest_id, dod):
        self.number = None
        self.event_id = obj_dict.get('event_id')
        self.user_id = obj_dict.get('user_id')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('admission_event_notes')
        self.admitted_date = parse_datetime(obj_dict.get('admitted_date'))
        self.admitted_time = obj_dict.get('admitted_time')
        self.immediate_coroner_referral = obj_dict.get('immediate_coroner_referral')
        self.published = obj_dict.get('is_final')
        self.dod = dod
        self.is_latest = self.event_id == latest_id

    def admission_length(self):
        if self.dod and self.admitted_date:
            delta = self.dod - self.admitted_date
            return delta.days
        else:
            return 'Unknown'

    def display_coroner_referral(self):
        return 'Yes' if self.immediate_coroner_referral else 'No'


class CaseBreakdownLatestAdmission:

    def __init__(self):
        self.day_of_last_admission = ''
        self.month_of_last_admission = ''
        self.year_of_last_admission = ''
        self.date_of_last_admission_unknown = False

        self.time_of_last_admission = ''
        self.time_of_last_admission_unknown = False

        self.latest_admission_notes = ''
        self.suspect_referral = ''

    @classmethod
    def from_data(cls, draft=None):
        latest_admission = CaseBreakdownLatestAdmission()
        if draft is not None:
            try:
                latest_admission.day_of_last_admission = draft['day_of_last_admission']
                latest_admission.month_of_last_admission = draft['month_of_last_admission']
                latest_admission.year_of_last_admission = draft['year_of_last_admission']
                latest_admission.date_of_last_admission_unknown = draft['date_of_last_admission_unknown']
                latest_admission.time_of_last_admission = draft['time_of_last_admission']
                latest_admission.time_of_last_admission_unknown = draft['time_of_last_admission_unknown']
                latest_admission.latest_admission_notes = draft['latest_admission_notes']
                latest_admission.suspect_referral = draft['suspect_referral']

            except KeyError:
                print('Could not parse latest admission object')

        return latest_admission

    def to_object(self):
        return {
            'day_of_last_admission': self.day_of_last_admission,
            'month_of_last_admission': self.month_of_last_admission,
            'year_of_last_admission': self.year_of_last_admission,
            'date_of_last_admission_unknown': self.date_of_last_admission_unknown,
            'time_of_last_admission': self.time_of_last_admission,
            'time_of_last_admission_unknown': self.time_of_last_admission_unknown,
            'latest_admission_notes': self.latest_admission_notes,
            'suspect_referral': self.suspect_referral,
        }


class CaseBreakdownQAPDiscussion:

    def __init__(self):
        self.default_qap = None
        self.use_default_qap = False

        self.alternate_qap = MedicalTeamMember()
        self.cause_of_death = None

        self.day_of_conversation = ''
        self.month_of_conversation = ''
        self.year_of_conversation = ''
        self.time_of_conversation = ''

        self.details = ''
        self.outcome = ''

    @classmethod
    def from_data(cls, medical_team=None, cause_of_death=None, qap_draft=None):
        qap_discussion = CaseBreakdownQAPDiscussion()

        cls.__set_default_qap(medical_team, qap_discussion, qap_draft)

        qap_discussion.cause_of_death = cause_of_death

        cls.__load_qap_draft(qap_discussion, qap_draft)

        return qap_discussion

    @classmethod
    def __load_qap_draft(cls, qap_discussion, qap_draft):
        if qap_draft is not None:
            try:
                qap_discussion.use_default_qap = qap_draft['use_default_qap']
                qap_discussion.alternate_qap = MedicalTeamMember.from_dict(qap_draft['alternate_qap'])
                qap_discussion.day_of_conversation = qap_draft['day_of_conversation']
                qap_discussion.month_of_conversation = qap_draft['month_of_conversation']
                qap_discussion.year_of_conversation = qap_draft['year_of_conversation']
                qap_discussion.time_of_conversation = qap_draft['time_of_conversation']
                qap_discussion.details = qap_draft['details']
                qap_discussion.outcome = qap_draft['outcome']

            except KeyError:
                print('Could not parse qap draft object')

    @classmethod
    def __set_default_qap(cls, medical_team, qap_discussion, qap_draft):
        if medical_team is not None and medical_team.qap is not None and medical_team.qap.name != '':
            qap_discussion.default_qap = medical_team.qap

            if qap_draft is None:
                qap_discussion.use_default_qap = True

    def to_object(self):
        return {
            'default_qap': self.default_qap.to_object(),
            'alternate_qap': self.alternate_qap.to_object(),
            'cause_of_death': self.cause_of_death.to_object(),
            'day_of_conversation': self.day_of_conversation,
            'month_of_conversation': self.month_of_conversation,
            'year_of_conversation': self.year_of_conversation,
            'time_of_conversation': self.time_of_conversation,
            'details': self.details,
            'outcome': self.outcome
        }


class CauseOfDeathProposal:

    def __init__(self):
        from users.models import User

        self.medical_examiner = User()
        self.creation_date = ''
        self.section_1a = ''
        self.section_1b = ''
        self.section_1c = ''
        self.section_2 = ''

    def to_object(self):
        return {
            'medical_examiner': get_user_presenter(self.medical_examiner),
            'creation_date': self.creation_date,
            'section_1a': self.section_1a,
            'section_1b': self.section_1b,
            'section_1c': self.section_1c,
            'section_2': self.section_2
        }


class MedicalTeam:

    def __init__(self, obj_dict):

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

        self.medical_examiner_id = obj_dict['medicalExaminerId'] if 'medicalExaminerId' in obj_dict else ''
        self.medical_examiners_officer_id = obj_dict['medicalExaminerOfficer'] if 'medicalExaminerOfficer' in obj_dict else ''

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_medical_team_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return MedicalTeam(response.json())
        else:
            return None


class MedicalTeamMember:

    def __init__(self, name='', role='', organisation='', phone_number='', notes=''):
        self.name = name.strip() if name else ''
        self.role = role
        self.organisation = organisation
        self.phone_number = phone_number
        self.notes = notes

    @staticmethod
    def from_dict(obj_dict):
        if obj_dict is None:
            return None

        name = obj_dict['name'] if 'name' in obj_dict else ''
        role = obj_dict['role'] if 'role' in obj_dict else ''
        organisation = obj_dict['organisation'] if 'organisation' in obj_dict else ''
        phone_number = obj_dict['phone'] if 'phone' in obj_dict else ''
        notes = obj_dict['notes'] if 'notes' in obj_dict else ''
        return MedicalTeamMember(name=name, role=role, organisation=organisation, phone_number=phone_number,
                                 notes=notes)


    def has_name(self):
        return self.name and len(self.name.strip()) > 0

    def has_valid_name(self):
        return len(self.name.strip()) < 250

    def has_name_if_needed(self):
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
            "notes": self.notes
        }


def text_field_is_not_null(field):
    return field and len(field.strip()) > 0

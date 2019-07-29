from datetime import datetime, timedelta

from examinations.constants import get_display_short_user_role, get_display_outcome_summary, \
    get_display_circumstances_of_death, get_display_scrutiny_outcome, get_display_bereaved_outcome, \
    get_display_qap_high_outcome, get_display_qap_outcome

from medexCms.api import enums
from medexCms.utils import parse_datetime, NONE_DATE, NONE_TIME, fallback_to


class CaseEvent:
    EVENT_TYPES = {
        enums.timeline_event_keys.OTHER_EVENT_KEY: enums.timeline_event_types.OTHER_EVENT_TYPE,
        enums.timeline_event_keys.PRE_SCRUTINY_EVENT_KEY: enums.timeline_event_types.PRE_SCRUTINY_EVENT_TYPE,
        enums.timeline_event_keys.BEREAVED_DISCUSSION_EVENT_KEY:
            enums.timeline_event_types.BEREAVED_DISCUSSION_EVENT_TYPE,
        enums.timeline_event_keys.MEO_SUMMARY_EVENT_KEY: enums.timeline_event_types.MEO_SUMMARY_EVENT_TYPE,
        enums.timeline_event_keys.QAP_DISCUSSION_EVENT_KEY: enums.timeline_event_types.QAP_DISCUSSION_EVENT_TYPE,
        enums.timeline_event_keys.MEDICAL_HISTORY_EVENT_KEY: enums.timeline_event_types.MEDICAL_HISTORY_EVENT_TYPE,
        enums.timeline_event_keys.ADMISSION_NOTES_EVENT_KEY: enums.timeline_event_types.ADMISSION_NOTES_EVENT_TYPE,
        enums.timeline_event_keys.CASE_CLOSED_EVENT_KEY: enums.timeline_event_types.CASE_CLOSED_TYPE
    }

    date_format = '%d.%m.%Y'
    time_format = "%H:%M"

    @classmethod
    def parse_event(cls, event_data, latest_id, dod):
        if event_data.get('eventType') == enums.timeline_event_types.OTHER_EVENT_TYPE:
            return CaseOtherEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.PRE_SCRUTINY_EVENT_TYPE:
            return CasePreScrutinyEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.BEREAVED_DISCUSSION_EVENT_TYPE:
            return CaseBereavedDiscussionEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.MEO_SUMMARY_EVENT_TYPE:
            return CaseMeoSummaryEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.QAP_DISCUSSION_EVENT_TYPE:
            return CaseQapDiscussionEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.MEDICAL_HISTORY_EVENT_TYPE:
            return CaseMedicalHistoryEvent(event_data, latest_id)
        elif event_data.get('eventType') == enums.timeline_event_types.ADMISSION_NOTES_EVENT_TYPE:
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

    def user_display_role(self):
        return get_display_short_user_role(self.user_role)


class CaseInitialEvent(CaseEvent):
    date_format = '%d.%m.%Y'
    time_format = "%H:%M"
    UNKNOWN = 'Unknown'

    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_initial_event_body.html'
    event_type = enums.timeline_event_types.INITIAL_EVENT_TYPE
    css_type = 'initial'

    def __init__(self, obj_dict, patient_name, user_role):
        self.number = None
        self.patient_name = patient_name
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.user_role = user_role
        self.created_date = obj_dict.get('created')
        self.dod = obj_dict.get('dateOfDeath')
        self.tod = obj_dict.get('timeOfDeath')
        self.is_latest = False  # Used to flag whether can be amend, for the patient died event this is always true
        self.published = False

    @property
    def display_type(self):
        return '%s died' % self.patient_name

    def display_date(self):
        if self.dod == NONE_DATE:
            return self.UNKNOWN
        else:
            date = parse_datetime(self.dod)
            return date.strftime(self.date_format)

    def display_time(self):
        if self.tod == NONE_TIME:
            return self.UNKNOWN
        else:
            if len(self.tod) == 8:
                return self.tod[:-3]
            else:
                return self.tod


class CaseClosedEvent(CaseEvent):
    date_format = '%d.%m.%Y'
    time_format = "%H:%M"
    UNKNOWN = 'Unknown'

    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_case_closed_body.html'
    event_type = enums.timeline_event_types.CASE_CLOSED_TYPE
    css_type = 'case-closed'

    def __init__(self, obj_dict, patient_name, user_role):
        self.number = None
        self.patient_name = patient_name
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.date_case_closed = obj_dict.get('dateCaseClosed')
        self.is_latest = False  # Used to flag whether can be amend, for the patient died event this is always true
        self.published = False
        self.case_outcome = obj_dict.get('caseOutcome')

    @property
    def display_type(self):
        return 'Case closed'

    def display_date_case_closed(self):
        if self.date_case_closed == NONE_DATE:
            return self.UNKNOWN
        else:
            date = parse_datetime(self.date_case_closed)
            return date.strftime(self.date_format)

    @property
    def display_case_outcome(self):
        return get_display_outcome_summary(self.case_outcome)


class CaseOtherEvent(CaseEvent):
    form_type = 'OtherEventForm'
    event_type = enums.timeline_event_types.OTHER_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_other_event_body.html'
    display_type = 'Other case info'
    css_type = 'other'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('text')
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import OtherEventForm
        form = OtherEventForm().fill_from_draft(self)
        form.event_id = None
        return form


class CasePreScrutinyEvent(CaseEvent):
    form_type = 'PreScrutinyEventForm'
    event_type = enums.timeline_event_types.PRE_SCRUTINY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_pre_scrutiny_event_body.html'
    display_type = 'ME review of records'
    css_type = 'pre-scrutiny'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('medicalExaminerThoughts')
        self.circumstances_of_death = obj_dict.get('circumstancesOfDeath')
        self.cause_of_death_1a = obj_dict.get('causeOfDeath1a')
        self.cause_of_death_1b = obj_dict.get('causeOfDeath1b')
        self.cause_of_death_1c = obj_dict.get('causeOfDeath1c')
        self.cause_of_death_2 = obj_dict.get('causeOfDeath2')
        self.outcome_of_pre_scrutiny = obj_dict.get('outcomeOfPreScrutiny')
        self.clinical_governance_review = obj_dict.get('clinicalGovernanceReview')
        self.clinical_governance_review_text = obj_dict.get('clinicalGovernanceReviewText')
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import PreScrutinyEventForm
        form = PreScrutinyEventForm().fill_from_draft(self)
        form.event_id = None
        return form

    def display_circumstances_of_death(self):
        return get_display_circumstances_of_death(self.circumstances_of_death)

    def display_scrutiny_outcome(self):
        return get_display_scrutiny_outcome(self.outcome_of_pre_scrutiny)


class CaseBereavedDiscussionEvent(CaseEvent):
    form_type = 'BereavedDiscussionEventForm'
    event_type = enums.timeline_event_types.BEREAVED_DISCUSSION_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_bereaved_discussion_event_body.html'
    display_type = 'Bereaved/representative discussion'
    css_type = 'bereaved-discussion'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.participant_full_name = fallback_to(obj_dict.get('participantFullName'), '')
        self.participant_relationship = fallback_to(obj_dict.get('participantRelationship'), '')
        self.participant_phone_number = fallback_to(obj_dict.get('participantPhoneNumber'), '')
        self.present_at_death = obj_dict.get('presentAtDeath')
        self.informed_at_death = obj_dict.get('informedAtDeath')
        self.date_of_conversation = parse_datetime(obj_dict.get('dateOfConversation'))
        self.discussion_unable_happen = enums.true_false.TRUE if obj_dict.get(
            'discussionUnableHappen') else enums.true_false.FALSE
        self.discussion_details = fallback_to(obj_dict.get('discussionDetails'), '')
        self.bereaved_discussion_outcome = obj_dict.get('bereavedDiscussionOutcome')
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import BereavedDiscussionEventForm
        form = BereavedDiscussionEventForm().fill_from_draft(self, default_representatives=representatives)
        form.event_id = None
        return form

    def display_bereaved_discussion_outcome(self):
        return get_display_bereaved_outcome(self.bereaved_discussion_outcome)


class CaseMeoSummaryEvent(CaseEvent):
    form_type = 'MeoSummaryEventForm'
    event_type = enums.timeline_event_types.MEO_SUMMARY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_meo_summary_event_body.html'
    display_type = 'MEO summary'
    css_type = 'meo-summary'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('summaryDetails')
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import MeoSummaryEventForm
        form = MeoSummaryEventForm().fill_from_draft(self)
        form.event_id = None
        return form


class CaseQapDiscussionEvent(CaseEvent):
    form_type = 'QapDiscussionEventForm'

    event_type = enums.timeline_event_types.QAP_DISCUSSION_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_qap_discussion_event_body.html'
    display_type = 'QAP discussion'
    css_type = 'qap-discussion'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.participant_full_name = obj_dict.get('participantName')
        self.participant_role = obj_dict.get('participantRole')
        self.participant_organisation = obj_dict.get('participantOrganisation')
        self.participant_phone_number = obj_dict.get('participantPhoneNumber')
        self.date_of_conversation = parse_datetime(obj_dict.get('dateOfConversation'))
        self.discussion_unable_happen = obj_dict.get('discussionUnableHappen')
        self.discussion_details = obj_dict.get('discussionDetails')
        self.qap_discussion_outcome = obj_dict.get('qapDiscussionOutcome')
        self.participant_name = obj_dict.get("participantName")
        self.cause_of_death_1a = obj_dict.get("causeOfDeath1a")
        self.cause_of_death_1b = obj_dict.get("causeOfDeath1b")
        self.cause_of_death_1c = obj_dict.get("causeOfDeath1c")
        self.cause_of_death_2 = obj_dict.get("causeOfDeath2")
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def conversation_display_date(self):
        return self.date_of_conversation.strftime(self.date_format) if self.date_of_conversation else ''

    def conversation_display_time(self):
        return self.date_of_conversation.strftime(self.time_format) if self.date_of_conversation else ''

    def as_amendment_form(self, default_qap, representatives):
        from examinations.forms.timeline_events import QapDiscussionEventForm
        form = QapDiscussionEventForm().fill_from_draft(self, default_qap=default_qap)
        form.event_id = None
        return form

    def display_qap_discussion_high_outcome(self):
        return get_display_qap_high_outcome(self.qap_discussion_outcome)

    def display_qap_discussion_mccd_outcome(self):
        return get_display_qap_outcome(self.qap_discussion_outcome)

    def hide_mccd_section(self):
        return self.qap_discussion_outcome in [enums.outcomes.CORONER_100A, enums.outcomes.CORONER_INVESTIGATION]

    def hide_new_cause_of_death_section(self):
        return self.qap_discussion_outcome in [enums.outcomes.MCCD_FROM_ME, enums.outcomes.CORONER_100A,
                                               enums.outcomes.CORONER_INVESTIGATION]


class CaseMedicalHistoryEvent(CaseEvent):
    form_type = 'MedicalHistoryEventForm'
    event_type = enums.timeline_event_types.MEDICAL_HISTORY_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_medical_history_event_body.html'
    display_type = 'Medical and social history'
    css_type = 'medical-history'

    def __init__(self, obj_dict, latest_id):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('text')
        self.published = obj_dict.get('isFinal')
        self.is_latest = self.event_id == latest_id

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import MedicalHistoryEventForm
        form = MedicalHistoryEventForm().fill_from_draft(self)
        form.event_id = None
        return form


class CaseAdmissionNotesEvent(CaseEvent):
    form_type = 'AdmissionNotesEventForm'
    event_type = enums.timeline_event_types.ADMISSION_NOTES_EVENT_TYPE
    type_template = 'examinations/partials/case_breakdown/event_card_bodies/_admission_notes_event_body.html'
    display_type = 'Admission notes'
    css_type = 'admission-notes'

    def __init__(self, obj_dict, latest_id, dod):
        self.number = None
        self.event_id = obj_dict.get('eventId')
        self.user_id = obj_dict.get('userId')
        self.user_full_name = obj_dict.get('userFullName')
        self.user_role = obj_dict.get('usersRole')
        self.created_date = obj_dict.get('created')
        self.body = obj_dict.get('notes')
        self.admitted_date = parse_datetime(obj_dict.get('admittedDate'))
        self.admitted_date_unknown = obj_dict.get('admittedDateUnknown')
        self.admitted_time = obj_dict.get('admittedTime')
        self.admitted_time_unknown = obj_dict.get('admittedTimeUnknown')
        self.immediate_coroner_referral = obj_dict.get('immediateCoronerReferral')
        self.published = obj_dict.get('isFinal')
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

    def as_amendment_form(self, qap, representatives):
        from examinations.forms.timeline_events import AdmissionNotesEventForm
        form = AdmissionNotesEventForm().fill_from_draft(self)
        form.event_id = None
        return form

from alerts import messages
from examinations.models.core import CauseOfDeath
from medexCms.api import enums
from medexCms.utils import fallback_to, validate_date_time_field, API_DATE_FORMAT, pop_if_falsey, build_date, \
    validate_date, date_is_valid_or_empty, validate_is_not_blank
from people.models import BereavedRepresentative


class PreScrutinyEventForm:
    active = False

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('pre_scrutiny_id'), '')
        self.me_thoughts = fallback_to(form_data.get('me-thoughts'), '')
        self.circumstances_of_death = form_data.get('cod')
        self.possible_cod_1a = fallback_to(form_data.get('possible-cod-1a'), '')
        self.possible_cod_1b = fallback_to(form_data.get('possible-cod-1b'), '')
        self.possible_cod_1c = fallback_to(form_data.get('possible-cod-1c'), '')
        self.possible_cod_2 = fallback_to(form_data.get('possible-cod-2'), '')
        self.overall_outcome = form_data.get('ops')
        self.coroner_outcome = form_data.get('coroner-outcome')
        self.governance_review = form_data.get('gr')
        self.governance_review_text = fallback_to(form_data.get('grt'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

        self.errors = {'count': 0}

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        self.errors = {'count': 0}
        if self.is_final:
            if self.me_thoughts.strip() == '':
                self.errors['count'] += 1
                self.errors['me_thoughts'] = messages.ErrorFieldRequiredMessage('notes')

            if self.circumstances_of_death == '' or self.circumstances_of_death is None:
                self.errors['count'] += 1
                self.errors['circumstances_of_death'] = messages.ErrorSelectionRequiredMessage('circumstance of death')

            if self.possible_cod_1a.strip() == '':
                self.errors['count'] += 1
                self.errors['possible_cod'] = messages.ErrorFieldRequiredMessage('1a')

            if self.overall_outcome == '' or self.overall_outcome is None:
                self.errors['count'] += 1
                self.errors['overall_outcome'] = messages.ErrorSelectionRequiredMessage('overall outcome')

            if self.overall_outcome == enums.outcomes.CORONER and \
                    (self.coroner_outcome == '' or self.coroner_outcome is None):
                self.errors['count'] += 1
                self.errors['coroner_outcome'] = messages.ErrorSelectionRequiredMessage('coroner outcome')

            if self.governance_review == '' or self.governance_review is None:
                self.errors['count'] += 1
                self.errors['governance_review'] = messages.ErrorSelectionRequiredMessage('clinical governance review')
            elif self.governance_review == 'Yes' and self.governance_review_text.strip() == '':
                self.errors['count'] += 1
                self.errors['governance_review'] = messages.ErrorFieldRequiredMessage('governance review notes')

        return self.errors['count'] == 0

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
            "outcomeOfPreScrutiny": self.calc_outcome_of_pre_scrutiny(),
            "clinicalGovernanceReview": self.governance_review,
            "clinicalGovernanceReviewText": self.governance_review_text
        }

    def calc_outcome_of_pre_scrutiny(self):
        if self.overall_outcome == enums.outcomes.CORONER:
            return self.coroner_outcome
        else:
            return self.overall_outcome

    def calc_overall_outcome(self, outcome_of_pre_scrutiny):
        if outcome_of_pre_scrutiny in [enums.outcomes.CORONER_100A, enums.outcomes.CORONER_INVESTIGATION]:
            return enums.outcomes.CORONER
        else:
            return outcome_of_pre_scrutiny

    def calc_coroner_outcome(self, outcome_of_pre_scrutiny):
        if outcome_of_pre_scrutiny in [enums.outcomes.CORONER_100A, enums.outcomes.CORONER_INVESTIGATION]:
            return outcome_of_pre_scrutiny
        else:
            return ''

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.me_thoughts = draft.body
        self.circumstances_of_death = draft.circumstances_of_death
        self.possible_cod_1a = draft.cause_of_death_1a
        self.possible_cod_1b = draft.cause_of_death_1b
        self.possible_cod_1c = draft.cause_of_death_1c
        self.possible_cod_2 = draft.cause_of_death_2
        self.overall_outcome = self.calc_overall_outcome(draft.outcome_of_pre_scrutiny)
        self.coroner_outcome = self.calc_coroner_outcome(draft.outcome_of_pre_scrutiny)
        self.governance_review = draft.clinical_governance_review
        self.governance_review_text = draft.clinical_governance_review_text
        return self


class MeoSummaryEventForm:
    active = False

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('meo_summary_id'), '')
        self.meo_summary_notes = fallback_to(form_data.get('meo_summary_notes'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False
        self.errors = {'count': 0}

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        self.errors = {'count': 0}
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
    errors = {"count": 0}

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('other_notes_id'), '')
        self.more_detail = fallback_to(form_data.get('more_detail'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        self.errors = {'count': 0}
        if self.is_final and self.more_detail.strip() == '':
            self.errors['count'] += 1
            self.errors['more_detail'] = messages.ErrorFieldRequiredMessage('more detail')
            return False
        else:
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
    errors = {'count': 0}

    def __init__(self, form_data={}):
        self.event_id = fallback_to(form_data.get('medical_history_id'), '')
        self.medical_history_details = fallback_to(form_data.get('medical-history-details'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        self.errors = {'count': 0}
        if self.is_final and self.medical_history_details.strip() == '':
            self.errors['count'] += 1
            self.errors['medical_history_details'] = messages.ErrorFieldRequiredMessage('medical history details')
            return False
        else:
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
    QAP_PARTICIPANT = 'qap'
    OTHER_PARTICIPANT = 'other'

    active = False
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def make_active(self):
        self.active = True
        return self

    def __init__(self, form_data={}):
        self.errors = {'count': 0}
        self.event_id = fallback_to(form_data.get('qap_discussion_id'), '')

        self.discussion_participant_type = fallback_to(form_data.get('qap-discussion-doctor'), '')
        self.discussion_could_not_happen = fallback_to(form_data.get('qap_discussion_could_not_happen'),
                                                       enums.yes_no.NO)

        self.qap_default_qap_name = fallback_to(form_data.get('qap-default__full-name'), '')
        self.qap_default_qap_role = fallback_to(form_data.get('qap-default__role'), '')
        self.qap_default_qap_organisation = fallback_to(form_data.get('qap-default__organisation'), '')
        self.qap_default_qap_phone_number = fallback_to(form_data.get('qap-default__phone-number'), '')

        self.qap_discussion_name = fallback_to(form_data.get('qap-other__full-name'), '')
        self.qap_discussion_role = fallback_to(form_data.get('qap-other__role'), '')
        self.qap_discussion_organisation = fallback_to(form_data.get('qap-other__organisation'), '')
        self.qap_discussion_phone_number = fallback_to(form_data.get('qap-other__phone-number'), '')

        self.cause_of_death = CauseOfDeath()
        self.cause_of_death.section_1a = fallback_to(form_data.get('qap_discussion_revised_1a'), '')
        self.cause_of_death.section_1b = fallback_to(form_data.get('qap_discussion_revised_1b'), '')
        self.cause_of_death.section_1c = fallback_to(form_data.get('qap_discussion_revised_1c'), '')
        self.cause_of_death.section_2 = fallback_to(form_data.get('qap_discussion_revised_2'), '')

        self.discussion_details = fallback_to(form_data.get('qap_discussion_details'), '')

        self.outcome = fallback_to(form_data.get('qap-discussion-outcome'), '')
        self.outcome_decision = fallback_to(form_data.get('qap-discussion-outcome-decision'), '')
        self.coroner_decision = fallback_to(form_data.get('qap-coroner-outcome-decision'), '')

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

        self.discussion_details = fallback_to(draft.discussion_details, '')

        self.discussion_could_not_happen = enums.yes_no.YES if draft.discussion_unable_happen else enums.yes_no.NO

        self.__calculate_discussion_outcome_radio_button_combination(draft)

        # fill alternate cause of death boxes
        self.__fill_cause_of_death_from_draft(draft)

        return self

    def __fill_cause_of_death_from_draft(self, draft):
        self.cause_of_death = CauseOfDeath()
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
            self.qap_discussion_name = fallback_to(draft.participant_name, '')
            self.qap_discussion_role = fallback_to(draft.participant_role, '')
            self.qap_discussion_organisation = fallback_to(draft.participant_organisation, '')
            self.qap_discussion_phone_number = fallback_to(draft.participant_phone_number, '')

    def __fill_default_qap_from_draft(self, default_qap):
        if default_qap:
            self.qap_default_qap_name = default_qap.name
            self.qap_default_qap_role = default_qap.role
            self.qap_default_qap_organisation = default_qap.organisation
            self.qap_default_qap_phone_number = default_qap.phone_number

    def __calculate_discussion_outcome_radio_button_combination(self, draft):
        api_outcome = draft.qap_discussion_outcome
        if api_outcome is not None:
            if api_outcome in [enums.outcomes.CORONER_INVESTIGATION, enums.outcomes.CORONER_100A]:
                self.outcome = enums.outcomes.CORONER
                self.coroner_decision = api_outcome
                self.outcome_decision = ""
            else:
                self.outcome = enums.outcomes.MCCD
                self.outcome_decision = api_outcome
                self.coroner_decision = ""

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
        self.errors = {'count': 0}

        # if discussion could not happen then always valid
        if self.discussion_could_not_happen == enums.yes_no.YES:
            return True

        # validate date
        validate_date_time_field('time_of_conversation', self.errors,
                                 self.year_of_conversation, self.month_of_conversation, self.day_of_conversation,
                                 self.time_of_conversation,
                                 messages.ErrorFieldRequiredMessage("date and time of conversation"),
                                 require_not_blank=self.is_final)

        # final submission only
        if self.is_final:
            if self.discussion_participant_type == enums.people.OTHER:
                # validate name
                if self.qap_discussion_name == '':
                    self.errors['count'] += 1
                    self.errors['participant'] = messages.ErrorFieldRequiredMessage('QAP name')

            # validate details
            if self.discussion_details == '':
                self.errors['count'] += 1
                self.errors['details'] = messages.ErrorFieldRequiredMessage('discussion details')

            # validate outcomes
            self.__validate_outcomes()

        return self.errors['count'] == 0

    def __validate_outcomes(self):
        if self.outcome == '':
            self.errors['count'] += 1
            self.errors['outcome'] = messages.ErrorSelectionRequiredMessage('discussion outcome')
        elif self.outcome == enums.outcomes.MCCD:
            if self.outcome_decision == '':
                self.errors['count'] += 1
                self.errors['outcome_decision'] = messages.ErrorSelectionRequiredMessage('mccd outcome')
            elif self.outcome_decision in [enums.outcomes.MCCD_FROM_QAP_AND_ME,
                                           enums.outcomes.MCCD_FROM_QAP] and self.cause_of_death.section_1a == '':
                self.errors['count'] += 1
                self.errors['1a'] = messages.ErrorFieldRequiredMessage('revised cause of death')
        elif self.outcome == enums.outcomes.CORONER:
            if self.coroner_decision == '':
                self.errors['count'] += 1
                self.errors['coroner_decision'] = messages.ErrorSelectionRequiredMessage('coroner outcome')

    def for_request(self):

        if self.discussion_could_not_happen == enums.yes_no.YES:
            return self.__discussion_did_not_happen_request()
        else:
            return self.__full_discussion_request()

    def __discussion_did_not_happen_request(self):
        return {
            "eventId": self.event_id,
            "isFinal": self.is_final,
            "discussionUnableHappen": True if self.discussion_could_not_happen == enums.yes_no.YES else False,
        }

    def __full_discussion_request(self):
        name, role, organisation, phone_number = self.__participant_for_request()

        date_of_conversation = self.__calculate_full_date_of_conversation()

        outcome = self.__calculate_discussion_outcome()

        result = {
            "eventId": self.event_id,
            "eventType": "QapDiscussion",
            "isFinal": self.is_final,
            "participantRole": role,
            "participantOrganisation": organisation,
            "participantPhoneNumber": phone_number,
            "discussionUnableHappen": self.discussion_could_not_happen == enums.yes_no.YES,
            "discussionDetails": self.discussion_details,
            "qapDiscussionOutcome": outcome,
            "participantName": name,
            "causeOfDeath1a": self.cause_of_death.section_1a,
            "causeOfDeath1b": self.cause_of_death.section_1b,
            "causeOfDeath1c": self.cause_of_death.section_1c,
            "causeOfDeath2": self.cause_of_death.section_2,
            "dateOfConversation": date_of_conversation.strftime(API_DATE_FORMAT) if date_of_conversation else None
        }
        pop_if_falsey("dateOfConversation", result)
        return result

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
        if self.outcome == enums.outcomes.MCCD:
            return self.outcome_decision
        elif self.outcome == enums.outcomes.CORONER:
            return self.coroner_decision

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
        self.admission_date_unknown = True if \
            form_data.get('date_of_last_admission_not_known') == enums.true_false.TRUE else False
        self.admission_time = fallback_to(form_data.get('time_of_last_admission'), '')
        self.admission_time_unknown = True if \
            form_data.get('time_of_last_admission_not_known') == enums.true_false.TRUE else False
        self.admission_notes = fallback_to(form_data.get('latest_admission_notes'), '')
        self.coroner_referral = fallback_to(form_data.get('latest_admission_immediate_referral'), '')
        self.route_of_admission = fallback_to(form_data.get('latest_admission_route'), '')
        self.is_final = True if form_data.get('add-event-to-timeline') else False
        self.errors = {'count': 0}

    def make_active(self):
        self.active = True
        return self

    def is_valid(self):
        self.errors = {'count': 0}
        if self.is_final:
            self.check_valid_final()
        else:
            self.check_valid_draft()
        return self.errors['count'] == 0

    def check_valid_final(self):
        if validate_date(self.admission_year, self.admission_month,
                         self.admission_day) is False and self.admission_date_unknown is False:
            self.errors['count'] += 1
            self.errors['date_of_last_admission'] = messages.INVALID_DATE

        if self.admission_time == '' and self.admission_time_unknown is False:
            self.errors['count'] += 1
            self.errors['time_of_last_admission'] = messages.ErrorFieldRequiredMessage('time of last admission')

        if self.coroner_referral == '':
            self.errors['count'] += 1
            self.errors['latest_admission_immediate_referral'] = messages.ErrorSelectionRequiredMessage(
                'immediate referral')

        if self.route_of_admission == '':
            self.errors['count'] += 1
            self.errors['route_of_admission'] = messages.ErrorFieldRequiredMessage('admission route')

    def check_valid_draft(self):
        if date_is_valid_or_empty(self.admission_year, self.admission_month, self.admission_day) is False:
            self.errors['count'] += 1
            self.errors['date_of_last_admission'] = messages.INVALID_DATE

    def admission_date(self):
        if self.admission_date_unknown:
            return None
        else:
            return build_date(self.admission_year, self.admission_month, self.admission_day).strftime(self.date_format)

    def get_immediate_coroner_referral(self):
        if self.coroner_referral == 'yes':
            return True
        elif self.coroner_referral == 'no':
            return False
        else:
            return None

    def set_immediate_coroner_referral(self, draft_value):
        if draft_value is True:
            return 'yes'
        elif draft_value is None:
            return ''
        else:
            return 'no'

    def for_request(self):
        try:
            admission_date_for_request = self.admission_date()
        except ValueError:
            admission_date_for_request = None

        return {
            "eventId": self.event_id,
            "notes": self.admission_notes,
            "isFinal": self.is_final,
            "admittedDate": admission_date_for_request,
            "admittedDateUnknown": True if self.admission_date_unknown else None,
            "admittedTime": self.admission_time if self.admission_time else None,
            "admittedTimeUnknown": True if self.admission_time_unknown else None,
            "routeOfAdmission": self.route_of_admission,
            "immediateCoronerReferral": self.get_immediate_coroner_referral(),
        }

    def fill_from_draft(self, draft):
        self.event_id = draft.event_id
        self.admission_day = draft.admitted_date.day if draft.admitted_date else ''
        self.admission_month = draft.admitted_date.month if draft.admitted_date else ''
        self.admission_year = draft.admitted_date.year if draft.admitted_date else ''
        self.admission_date_unknown = draft.admitted_date_unknown
        self.admission_time = draft.admitted_time
        self.admission_time_unknown = draft.admitted_time_unknown
        self.admission_notes = draft.body
        self.route_of_admission = draft.route_of_admission
        self.coroner_referral = self.set_immediate_coroner_referral(draft.immediate_coroner_referral)
        return self


class BereavedDiscussionEventForm:
    # constants

    BEREAVED_OUTCOME_NO_CONCERNS = 'no concerns'
    BEREAVED_OUTCOME_CONCERNS = 'concerns'

    BEREAVED_CONCERNED_OUTCOME_CORONER = 'coroner'
    BEREAVED_CONCERNED_OUTCOME_100A = '100a'
    BEREAVED_CONCERNED_OUTCOME_ADDRESSED = 'addressed'

    REQUEST_OUTCOME_NO_CONCERNS = "CauseOfDeathAccepted"
    REQUEST_OUTCOME_CORONER = "ConcernsCoronerInvestigation"
    REQUEST_OUTCOME_100A = "ConcernsRequires100a"
    REQUEST_OUTCOME_ADDRESSED = "ConcernsAddressedWithoutCoroner"
    REQUEST_OUTCOME_COULD_NOT_HAPPEN = "DiscussionUnableToHappen"

    # properties
    active = False
    event_id = ''

    use_existing_bereaved = False
    use_custom_bereaved = True
    use_no_bereaved = False

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

    errors = {'count': 0}

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

        self.is_final = True if form_data.get('add-event-to-timeline') else False

    def __init_representatives(self, representatives):
        self.existing_representative = representatives[0]
        self.discussion_representative_type = enums.people.BEREAVED_REP
        self.use_existing_bereaved = True
        self.use_custom_bereaved = False

    def __init_representatives_from_draft(self, form_data):
        self.__init_existing_representative(form_data)
        self.__init_alternate_representative(form_data)
        self.__init_type_of_representative(form_data)

    def __init_type_of_representative(self, form_data):
        self.discussion_representative_type = fallback_to(form_data.get('bereaved_rep_type'), '')
        self.__set_use_existing_bereaved()

    def __set_use_existing_bereaved(self):
        if self.discussion_representative_type == enums.people.BEREAVED_REP:
            self.use_existing_bereaved = True
            self.use_custom_bereaved = False
            self.use_no_bereaved = False
        elif self.discussion_representative_type == enums.people.OTHER:
            self.use_existing_bereaved = False
            self.use_custom_bereaved = True
            self.use_no_bereaved = False
        elif self.discussion_representative_type == enums.people.NOBODY:
            self.use_existing_bereaved = False
            self.use_custom_bereaved = False
            self.use_no_bereaved = True
        elif self.existing_representative:
            self.use_existing_bereaved = True
            self.use_custom_bereaved = False
            self.use_no_bereaved = False
        else:
            self.use_existing_bereaved = False
            self.use_custom_bereaved = True
            self.use_no_bereaved = False

    def __init_alternate_representative(self, form_data):
        alternate_bereaved_data = {
            'fullName': fallback_to(form_data.get('bereaved_alternate_rep_name'), ''),
            'relationship': fallback_to(form_data.get('bereaved_alternate_rep_relationship'), ''),
            'phoneNumber': fallback_to(form_data.get('bereaved_alternate_rep_phone_number'), '')
        }
        self.alternate_representative = BereavedRepresentative(obj_dict=alternate_bereaved_data)

    def __init_existing_representative(self, form_data):
        self.existing_representative = None
        bereaved_existing_name = fallback_to(form_data.get('bereaved_existing_rep_name'), '')
        if len(bereaved_existing_name) > 0:
            existing_bereaved_data = {
                'fullName': bereaved_existing_name,
                'relationship': fallback_to(form_data.get('bereaved_existing_rep_relationship'), ''),
                'phoneNumber': fallback_to(form_data.get('bereaved_existing_rep_phone_number'), '')
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
            'bereaved_discussion_could_not_happen') == enums.true_false.TRUE else False

    def is_valid(self):
        self.errors = {'count': 0}

        if self.discussion_could_not_happen:
            return True

        # check date/time (this has to be valid whether it is a draft or not)
        validate_date_time_field('bereaved_time_of_conversation', self.errors,
                                 self.year_of_conversation, self.month_of_conversation,
                                 self.day_of_conversation, self.time_of_conversation, require_not_blank=self.is_final,
                                 error_message=messages.ErrorFieldRequiredMessage("date and time of discussion"))

        # other validation is only relevant for complete posts
        if self.is_final is False:
            return True

        # check bereaved name
        if not self.use_existing_bereaved:
            validate_is_not_blank('bereaved_participant_name', self.errors, self.alternate_representative.full_name,
                                  error_message=messages.ErrorFieldRequiredMessage('participant name'))

        # check outcome details
        validate_is_not_blank('bereaved_discussion_details', self.errors, self.discussion_details,
                              error_message=messages.ErrorFieldRequiredMessage('discussion details'))

        # check outcome decision
        validate_is_not_blank('bereaved_discussion_outcome', self.errors, self.discussion_outcome,
                              error_message=messages.ErrorSelectionRequiredMessage('discussion outcome'))

        if self.discussion_outcome == self.BEREAVED_OUTCOME_CONCERNS:
            validate_is_not_blank('bereaved_outcome_concerned_outcome', self.errors, self.discussion_concerned_outcome,
                                  error_message=messages.ErrorSelectionRequiredMessage('final outcome'))

        return self.errors['count'] == 0

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
            })
        if draft_participant is None:
            if self.existing_representative is not None:
                self.discussion_representative_type = enums.people.BEREAVED_REP
            else:
                self.discussion_representative_type = enums.people.NOBODY
        else:
            if draft_participant.equals(self.existing_representative):
                self.discussion_representative_type = enums.people.BEREAVED_REP
            else:
                self.discussion_representative_type = enums.people.OTHER
                self.alternate_representative = draft_participant

        self.__set_use_existing_bereaved()

    def for_request(self):

        if self.discussion_could_not_happen:
            return self.__discussion_did_not_happen_request()
        else:
            return self.__full_discussion_request()

    def __discussion_did_not_happen_request(self):
        return {
            "eventId": self.event_id,
            "isFinal": self.is_final,
            "eventType": "BereavedDiscussion",
            "discussionUnableHappen": self.discussion_could_not_happen,
        }

    def __full_discussion_request(self):
        date_of_conversation = self.__calculate_full_date_of_conversation()
        participant = self.__participant_for_request()
        request = {
            "eventId": self.event_id,
            "isFinal": self.is_final,
            "eventType": "BereavedDiscussion",
            "participantFullName": participant.full_name if participant else "",
            "participantRelationship": participant.relationship if participant else "",
            "participantPhoneNumber": participant.phone_number if participant else "",
            "dateOfConversation": date_of_conversation.strftime(API_DATE_FORMAT) if date_of_conversation else '',
            "discussionUnableHappen": self.discussion_could_not_happen,
            "discussionDetails": self.discussion_details,
            "bereavedDiscussionOutcome": self.__calculate_combined_outcome()
        }
        pop_if_falsey("bereavedDiscussionOutcome", request)
        return request

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

        return None

    def __participant_for_request(self):
        if self.discussion_representative_type == enums.people.BEREAVED_REP:
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

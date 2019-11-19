from errors.utils import handle_error, log_unexpected_api_response
from examinations import request_handler
from examinations.models.timeline_events import CaseEvent, CaseInitialEvent, CaseClosedEvent, VoidEvent
from medexCms.api import enums
from medexCms.utils import fallback_to, reformat_datetime


class CaseBreakdown:

    def __init__(self, obj_dict, medical_team):
        from examinations.presenters.core import PatientHeader

        self.case_header = PatientHeader(obj_dict.get("header"))

        self.prepopulated_items = PrePopulatedItemList(obj_dict.get('caseBreakdown'))

        # parse data
        self.event_list = ExaminationEventList(obj_dict.get('caseBreakdown'), self.case_header.date_of_death,
                                               self.case_header.full_name)
        self.event_list.sort_events_oldest_to_newest()
        self.event_list.add_event_numbers()
        self.medical_team = medical_team

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_case_breakdown_by_id(examination_id, auth_token)
        case_breakdown = None
        error = None
        case_status = None

        if response.ok:
            from examinations.models.medical_team import MedicalTeam
            medical_team, case_status, medical_team_error = MedicalTeam.load_by_id(examination_id, auth_token)
            if medical_team_error:
                error = medical_team_error
            else:
                case_breakdown = CaseBreakdown(response.json(), medical_team)
        else:
            error = handle_error(response, {'type': 'case breakdown', 'action': 'loading'})
        return case_breakdown, case_status, error


class CaseStatus:
    basic_details_entered = False
    name_entered = False
    dob_entered = False
    dod_entered = False
    nhs_number_entered = False
    additional_details_entered = False
    latest_admission_details_entered = False
    doctor_in_charge_entered = False
    qap_entered = False
    qap_cod_entered = False
    bereaved_info_entered = False
    me_assigned = False
    is_scrutiny_completed = False
    pre_scrutiny_event_entered = False
    qap_discussion_event_entered = False
    bereaved_discussion_event_entered = False
    is_case_items_completed = False
    mccd_issued = False
    cremation_form_info_entered = False
    gp_notified = False
    sent_to_coroner = False
    case_closed = False
    case_outcome = False
    have_been_scrutinised_by_ME = False
    me_scrutiny_confirmed = False

    def __init__(self, obj_dict):
        header = obj_dict.get("header")
        if header:
            self.basic_details_entered = header.get("basicDetailsEntered")
            self.name_entered = header.get("nameEntered")
            self.dob_entered = header.get("dobEntered")
            self.dod_entered = header.get("dodEntered")
            self.nhs_number_entered = header.get("nhsNumberEntered")
            self.additional_details_entered = header.get("additionalDetailsEntered")
            self.latest_admission_details_entered = header.get("latestAdmissionDetailsEntered")
            self.doctor_in_charge_entered = header.get("doctorInChargeEntered")
            self.qap_entered = header.get("qapEntered")
            self.qap_cod_entered = header.get("qapOriginalCodEntered")
            self.bereaved_info_entered = header.get("bereavedInfoEntered")
            self.me_assigned = header.get("meAssigned")
            self.is_scrutiny_completed = header.get("isScrutinyCompleted")
            self.pre_scrutiny_event_entered = header.get("preScrutinyEventEntered")
            self.qap_discussion_event_entered = header.get("qapDiscussionEventEntered")
            self.bereaved_discussion_event_entered = header.get("bereavedDiscussionEventEntered")
            self.is_case_items_completed = header.get("isCaseItemsCompleted")
            self.mccd_issued = header.get("mccdIssued")
            self.cremation_form_info_entered = header.get("cremationFormInfoEntered")
            self.gp_notified = header.get("gpNotified")
            self.sent_to_coroner = header.get("sentToCoroner")
            self.case_closed = header.get("caseClosed")
            self.case_outcome = header.get("caseOutcome")
            self.have_been_scrutinised_by_ME = header.get("haveBeenScrutinisedByME")
            self.me_scrutiny_confirmed = header.get("meScrutinyConfirmed")


class PrePopulatedItemList:
    date_format = '%d.%m.%Y'
    time_format = "%H:%M"

    def __init__(self, timeline_items):
        self.qap = self.__get_prepopulated_values_for_qap_discussion(
            timeline_items.get("qapDiscussion").get("prepopulated"))
        self.bereaved = self.__get_prepopulated_values_for_bereaved_discussion(
            timeline_items.get("bereavedDiscussion").get("prepopulated"))

    def __get_prepopulated_values_for_qap_discussion(self, obj_dict):
        return {"section_1a": fallback_to(obj_dict.get("causeOfDeath1a"), ""),
                "section_1b": fallback_to(obj_dict.get("causeOfDeath1b"), ""),
                "section_1c": fallback_to(obj_dict.get("causeOfDeath1c"), ""),
                "section_2": fallback_to(obj_dict.get("causeOfDeath2"), ""),
                "pre_scrutiny_status": fallback_to(obj_dict.get("preScrutinyStatus"),
                                                   enums.prescrutiny_status.NOT_HAPPENED),
                "medical_examiner": fallback_to(obj_dict.get("medicalExaminer"), ""),
                "date_of_latest_pre_scrutiny": fallback_to(obj_dict.get("dateOfLatestPreScrutiny"), ""),
                "user_for_latest_pre_scrutiny": fallback_to(obj_dict.get("userForLatestPrescrutiny"), ""),
                "display_date_of_latest_pre_scrutiny": reformat_datetime(obj_dict.get("dateOfLatestPreScrutiny"),
                                                                         self.date_format),
                "display_time_of_latest_pre_scrutiny": reformat_datetime(obj_dict.get("dateOfLatestPreScrutiny"),
                                                                         self.time_format)}

    def __get_prepopulated_values_for_bereaved_discussion(self, obj_dict):
        return {"section_1a": fallback_to(obj_dict.get("causeOfDeath1a"), ""),
                "section_1b": fallback_to(obj_dict.get("causeOfDeath1b"), ""),
                "section_1c": fallback_to(obj_dict.get("causeOfDeath1c"), ""),
                "section_2": fallback_to(obj_dict.get("causeOfDeath2"), ""),
                "pre_scrutiny_status": fallback_to(obj_dict.get("preScrutinyStatus"),
                                                   enums.prescrutiny_status.NOT_HAPPENED),
                "medical_examiner": fallback_to(obj_dict.get("medicalExaminer"), ""),
                "date_of_latest_pre_scrutiny": fallback_to(obj_dict.get("dateOfLatestPreScrutiny"), ""),
                "user_for_latest_pre_scrutiny": fallback_to(obj_dict.get("userForLatestPrescrutiny"), ""),
                "qap_discussion_status": fallback_to(obj_dict.get("qapDiscussionStatus"),
                                                     enums.qap_discussion_status.NO_RECORD),
                "qap_name_for_latest_qap_discussion": fallback_to(obj_dict.get("qapNameForLatestQAPDiscussion"), ""),
                "date_of_latest_qap_discussion": fallback_to(obj_dict.get("dateOfLatestQAPDiscussion"), ""),
                "user_for_latest_qap_discussion": fallback_to(obj_dict.get("userForLatestQAPDiscussion"), ""),
                "display_date_of_latest_pre_scrutiny": reformat_datetime(obj_dict.get("dateOfLatestPreScrutiny"),
                                                                         self.date_format),
                "display_time_of_latest_pre_scrutiny": reformat_datetime(obj_dict.get("dateOfLatestPreScrutiny"),
                                                                         self.time_format),
                "display_date_of_latest_qap_discussion": reformat_datetime(obj_dict.get("dateOfLatestQAPDiscussion"),
                                                                           self.date_format),
                "display_time_of_latest_qap_discussion": reformat_datetime(obj_dict.get("dateOfLatestQAPDiscussion"),
                                                                           self.time_format)}


class ExaminationEventList:

    def __init__(self, timeline_items, dod, patient_name):
        self.events = []
        self.drafts = {}
        self.latests = {}
        self.qap_discussion_draft = None
        self.other_notes_draft = None
        self.latest_admission_draft = None
        self.meo_summary_draft = None
        self.medical_history_draft = None
        self.bereaved_discussion_draft = None
        self.me_scrutiny_draft = None
        self.dod = dod
        self.parse_events(timeline_items, patient_name)

    def parse_events(self, timeline_items, patient_name):
        for key, event_type in timeline_items.items():
            if key == enums.timeline_event_keys.INITIAL_EVENT_KEY and event_type:
                self.events.append(CaseInitialEvent(event_type, patient_name))

            elif key == enums.timeline_event_keys.CASE_CLOSED_EVENT_KEY and event_type:
                self.events.append(CaseClosedEvent(event_type, patient_name))

            elif key == enums.timeline_event_keys.VOID_EVENT_KEY and event_type:
                self.events.append(VoidEvent(event_type, patient_name))

            elif key in enums.timeline_event_keys.all() and event_type:
                for event in event_type['history']:
                    if event['isFinal']:
                        self.events.append(CaseEvent.parse_event(event, event_type['latest']['eventId'], self.dod))
                if event_type['usersDraft']:
                    latest_id = event_type['latest']['eventId'] if event_type['latest'] else ''
                    self.drafts[key] = CaseEvent.parse_event(event_type['usersDraft'], latest_id, None)
                if event_type['latest']:
                    latest_id = event_type['latest']['eventId']
                    self.latests[CaseEvent.EVENT_TYPES[key]] = CaseEvent.parse_event(event_type['latest'], latest_id,
                                                                                     None)
            elif event_type:
                log_unexpected_api_response("case_breakdown.parse_events", "event_type", key)

    def sort_events_oldest_to_newest(self):
        self.events.sort(key=lambda event: event.created_date, reverse=False)

    def add_event_numbers(self):
        count = 1
        for event in self.events:
            event.number = count
            count += 1

    def get_qap_discussion_draft(self):
        return self.drafts.get(enums.timeline_event_keys.QAP_DISCUSSION_EVENT_KEY)

    def get_other_notes_draft(self):
        return self.drafts.get(enums.timeline_event_keys.OTHER_EVENT_KEY)

    def get_latest_admission_draft(self):
        return self.drafts.get(enums.timeline_event_keys.ADMISSION_NOTES_EVENT_KEY)

    def get_meo_summary_draft(self):
        return self.drafts.get(enums.timeline_event_keys.MEO_SUMMARY_EVENT_KEY)

    def get_medical_history_draft(self):
        return self.drafts.get(enums.timeline_event_keys.MEDICAL_HISTORY_EVENT_KEY)

    def get_bereaved_discussion_draft(self):
        return self.drafts.get(enums.timeline_event_keys.BEREAVED_DISCUSSION_EVENT_KEY)

    def get_me_scrutiny_draft(self):
        return self.drafts.get(enums.timeline_event_keys.PRE_SCRUTINY_EVENT_KEY)

    def get_latest_of_type(self, event_type):
        return self.latests.get(event_type)

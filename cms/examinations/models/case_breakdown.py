from rest_framework import status

from errors.utils import handle_error, logger, log_unexpected_api_response
from examinations import request_handler
from examinations.models.medical_team import MedicalTeam
from examinations.models.timeline_events import CaseEvent, CaseInitialEvent, CaseClosedEvent
from medexCms.api import enums


class CaseBreakdown:

    def __init__(self, obj_dict, medical_team):
        from examinations.models.core import PatientHeader

        self.case_header = PatientHeader(obj_dict.get("header"))

        # parse data
        self.event_list = ExaminationEventList(obj_dict.get('caseBreakdown'), self.case_header.date_of_death,
                                               self.case_header.full_name, "MEO")
        self.event_list.sort_events_oldest_to_newest()
        self.event_list.add_event_numbers()
        self.medical_team = medical_team

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_case_breakdown_by_id(examination_id, auth_token)

        medical_team = MedicalTeam.load_by_id(examination_id, auth_token)

        if response.status_code == status.HTTP_200_OK:
            return CaseBreakdown(response.json(), medical_team), None
        else:
            return None, handle_error(response, {'type': 'case', 'action': 'loading'})


class ExaminationEventList:

    def __init__(self, timeline_items, dod, patient_name, user_role):
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
        self.parse_events(timeline_items, patient_name, user_role)

    def parse_events(self, timeline_items, patient_name, user_role):
        for key, event_type in timeline_items.items():
            if key == enums.timeline_event_keys.INITIAL_EVENT_KEY and event_type:
                self.events.append(CaseInitialEvent(event_type, patient_name, user_role))

            elif key == enums.timeline_event_keys.CASE_CLOSED_EVENT_KEY and event_type:
                self.events.append(CaseClosedEvent(event_type, patient_name, user_role))

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

form_event_names = {
    'PreScrutinyEventForm': 'me review of records',
    'MeoSummaryEventForm': 'meo summary',
    'AdmissionNotesEventForm': 'latest admission details',
    'QapDiscussionEventForm': 'qap discussion',
    'BereavedDiscussionEventForm': 'bereaved discussion',
    'MedicalHistoryEventForm': 'medical and social history notes',
    'OtherEventForm': 'other',
}


class MedexLoggerEvents:
    CREATED_CASE = 'Created a case'
    CREATED_CASE_UNSUCCESSFUL = 'Created a case failed'
    CREATED_TIMELINE_EVENT = 'Posted a timeline event'
    CREATED_TIMELINE_EVENT_UNSUCCESSFUL = 'Posted a timeline event failed'
    SAVED_TIMELINE_EVENT = 'Saved a timeline event to draft'
    SAVED_TIMELINE_EVENT_UNSUCCESSFUL = 'Saved a timeline event to draft failed'
    COMPLETED_SCRUTINY = 'Completed scrutiny'
    COMPLETED_SCRUTINY_UNSUCCESSFUL = 'Completed scrutiny failed'


class MedexLogStream:
    def log(self, event_type, data):
        pass


class ConsoleLogStream(MedexLogStream):
    def log(self, event_type, data):
        print(event_type, data)


class TestLogStream(MedexLogStream):

    def __init__(self):
        self.event_history = []

    def log(self, event_type, data):
        self.event_history.append({"event_type": event_type, "data": data})

    def event_count(self):
        return len(self.event_history)

    def event(self, index):
        return self.event_history[index]

    def last(self, index):
        return self.event_history[self.event_count() - 1]

    def clear(self):
        self.event_history = []


class InsightsLogStream(MedexLogStream):
    def log(self, event_type, data):
        print('INSIGHTS', event_type, data)


class MedexMonitor:
    log_stream = None

    def __init__(self, log_stream: MedexLogStream):
        self.log_stream = log_stream

    def change_log_stream(self, log_stream: MedexLogStream):
        self.log_stream = log_stream

    def log_custom_event(self, event_type, data):
        self.log_stream.log(event_type, data)

    def log_case_create_event(self, user, examination_id, location_id):
        self.log_stream.log(MedexLoggerEvents.CREATED_CASE, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id
        })

    def log_case_create_event_unsuccessful(self, user, location_id, error_code):
        self.log_stream.log(MedexLoggerEvents.CREATED_CASE_UNSUCCESSFUL, {
            'user_id': user.user_id,
            'location_id': location_id,
            'error': error_code
        })

    def log_create_timeline_event_successful(self, user, examination_id, location_id, timeline_event_type, event_id):
        self.log_stream.log(MedexLoggerEvents.CREATED_TIMELINE_EVENT, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
            'timeline_event_type': form_event_names.get(str(timeline_event_type)),
            'event_id': event_id
        })

    def log_create_timeline_event_unsuccessful(self, user, examination_id, location_id, timeline_event_type,
                                               error_code):
        self.log_stream.log(MedexLoggerEvents.CREATED_TIMELINE_EVENT_UNSUCCESSFUL, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
            'timeline_event_type': form_event_names.get(str(timeline_event_type)),
            'error': error_code
        })

    def log_save_draft_timeline_event_successful(self, user, examination_id, location_id, timeline_event_type,
                                                 event_id):
        self.log_stream.log(MedexLoggerEvents.SAVED_TIMELINE_EVENT, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
            'timeline_event_type': form_event_names.get(str(timeline_event_type)),
            'event_id': event_id
        })

    def log_save_draft_timeline_event_unsuccessful(self, user, examination_id, location_id, timeline_event_type,
                                                   error_code):
        self.log_stream.log(MedexLoggerEvents.SAVED_TIMELINE_EVENT_UNSUCCESSFUL, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
            'timeline_event_type': form_event_names.get(str(timeline_event_type)),
            'error': error_code
        })

    def log_confirm_scrutiny(self, user, examination_id, location_id, outcome):
        self.log_stream.log(MedexLoggerEvents.COMPLETED_SCRUTINY, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
            'outcome_summary': outcome.case_outcome_summary,
            'outcome_review_of_records': outcome.case_pre_scrutiny_outcome,
            'outcome_qap': outcome.case_qap_outcome,
            'outcome_representative': outcome.case_representative_outcome,
        })

    def log_confirm_scrutiny_unsuccessful(self, user, examination_id, location_id):
        self.log_stream.log(MedexLoggerEvents.COMPLETED_SCRUTINY_UNSUCCESSFUL, {
            'user_id': user.user_id,
            'examination_id': examination_id,
            'location_id': location_id,
        })


monitor = MedexMonitor(log_stream=ConsoleLogStream())

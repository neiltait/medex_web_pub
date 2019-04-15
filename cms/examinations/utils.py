from . import request_handler
from examinations.forms import PreScrutinyEventForm, OtherEventForm, AdmissionNotesEventForm, MeoSummaryEventForm

PRE_SCRUTINY_FORM = 'pre-scrutiny'
MEO_SUMMARY_FORM = 'meo-summary'
OTHER_FORM = 'other'
ADMISSION_NOTES_FORM = 'admission-notes'

QAP_DISCUSSION_FORM = 'qap-discussion'


def event_form_parser(form_data):
    event_type = form_data.get('add-event-to-timeline') if form_data.get('add-event-to-timeline') else \
        form_data.get('save-as-draft')
    if event_type == PRE_SCRUTINY_FORM:
        return PreScrutinyEventForm(form_data)
    elif event_type == QAP_DISCUSSION_FORM:
        return QapDiscussionEventForm(form_data)
    elif event_type == MEO_SUMMARY_FORM:
        return MeoSummaryEventForm(form_data)
    elif event_type == OTHER_FORM:
        return OtherEventForm(form_data)
    elif event_type == ADMISSION_NOTES_FORM:
        return AdmissionNotesEventForm(form_data)


def event_form_submitter(auth_token, examination_id, form):
    form_type = type(form)
    if form_type == PreScrutinyEventForm:
        return request_handler.create_pre_scrutiny_event(auth_token, examination_id, form.for_request())
    elif form_type == MeoSummaryEventForm:
        return request_handler.create_meo_summary_event(auth_token, examination_id, form.for_request())
    elif form_type == OtherEventForm:
        return request_handler.create_other_event(auth_token, examination_id, form.for_request())
    elif form_type == AdmissionNotesEventForm:
        return request_handler.create_admission_notes_event(auth_token, examination_id, form.for_request())

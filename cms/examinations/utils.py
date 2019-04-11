from . import request_handler
from examinations.forms import PreScrutinyEventForm, OtherEventForm, AdmissionNotesEventForm

PRE_SCRUTINY_FORM = 'pre-scrutiny'
OTHER_FORM = 'other'
ADMISSION_NOTES_FORM= 'admission-notes'


def event_form_parser(form_data):
    event_type = form_data.get('add-event-to-timeline') if form_data.get('add-event-to-timeline') else \
        form_data.get('save-as-draft')
    if event_type == PRE_SCRUTINY_FORM:
        return PreScrutinyEventForm(form_data)
    elif event_type == OTHER_FORM:
        return OtherEventForm(form_data)
    elif event_type == ADMISSION_NOTES_FORM:
        return AdmissionNotesEventForm(form_data)


def event_form_submitter(auth_token, examination_id, form):
    form_type = type(form)
    if form_type == PreScrutinyEventForm:
        return request_handler.create_pre_scrutiny_event(auth_token, examination_id, form.for_request())
    elif form_type == OtherEventForm:
        return request_handler.create_other_event(auth_token, examination_id, form.for_request())
    elif form_type == AdmissionNotesEventForm:
        return request_handler.create_admission_notes_event(auth_token, examination_id, form.for_request())

from examinations.forms import PreScrutinyEventForm, MeoSummaryEventForm
from . import request_handler

PRE_SCRUTINY_FORM = 'pre-scrutiny'
MEO_SUMMARY_FORM = 'meo-summary'


def event_form_parser(form_data):
    event_type = form_data.get('add-event-to-timeline') if form_data.get('add-event-to-timeline') else \
        form_data.get('save-as-draft')
    print(event_type)
    if event_type == PRE_SCRUTINY_FORM:
        return PreScrutinyEventForm(form_data)
    elif event_type == MEO_SUMMARY_FORM:
        return MeoSummaryEventForm(form_data)


def event_form_submitter(auth_token, examination_id, form):
    form_type = type(form)
    if form_type == PreScrutinyEventForm:
        return request_handler.create_pre_scrutiny_event(auth_token, examination_id, form.for_request())
    elif form_type == MeoSummaryEventForm:
        return request_handler.create_meo_summary_event(auth_token, examination_id, form.for_request())

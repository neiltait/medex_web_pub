from . import request_handler
from examinations.forms.timeline_events import PreScrutinyEventForm, OtherEventForm, AdmissionNotesEventForm,\
    MeoSummaryEventForm, QapDiscussionEventForm, BereavedDiscussionEventForm, MedicalHistoryEventForm
from monitor.loggers import monitor

PRE_SCRUTINY_FORM = 'pre-scrutiny'
MEO_SUMMARY_FORM = 'meo-summary'
OTHER_FORM = 'other'
ADMISSION_NOTES_FORM = 'admission-notes'
QAP_DISCUSSION_FORM = 'qap-discussion'
BEREAVED_DISCUSSION_FORM = 'bereaved-discussion'
MEDICAL_HISTORY_FORM = 'medical-history'


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
    elif event_type == BEREAVED_DISCUSSION_FORM:
        return BereavedDiscussionEventForm(form_data=form_data)
    elif event_type == MEDICAL_HISTORY_FORM:
        return MedicalHistoryEventForm(form_data)


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
    elif form_type == QapDiscussionEventForm:
        return request_handler.create_qap_discussion_event(auth_token, examination_id, form.for_request())
    elif form_type == BereavedDiscussionEventForm:
        return request_handler.create_bereaved_discussion_event(auth_token, examination_id, form.for_request())
    elif form_type == MedicalHistoryEventForm:
        return request_handler.create_medical_history_event(auth_token, examination_id, form.for_request())


def log_successful_timeline_post(form, examination_id, user, location_id, response):
    if form.is_final:
        monitor.log_create_timeline_event_successful(user, examination_id, location_id,
                                                     form.__class__.__name__,
                                                     response.json()['eventId'])
    else:
        monitor.log_save_draft_timeline_event_successful(user, examination_id, location_id,
                                                         form.__class__.__name__,
                                                         response.json()['eventId'])


def log_unsuccessful_timeline_post(form, examination_id, user, location_id, response):
    if form.is_final:
        monitor.log_create_timeline_event_unsuccessful(user, examination_id, location_id,
                                                       form.__class__.__name__,
                                                       {"api error": response.status_code})
    else:
        monitor.log_save_draft_timeline_event_unsuccessful(user, examination_id, location_id,
                                                           form.__class__.__name__,
                                                           {"api error": response.status_code})


def get_tab_change_modal_config():
    return {
        'id': 'tab-change-modal',
        'content': 'You have unsaved changes, do you want to save them before continuing?',
        'confirm_btn_id': 'save-continue',
        'confirm_btn_text': 'Save and continue',
        'extra_buttons': [
            {
                'id': 'discard',
                'text': 'Discard and continue',
            }
        ],
    }


def text_field_is_not_null(field):
    return True if field and len(field.strip()) > 0 else False


class ReportGenerator:
    """ Class ReportGenerator """

    @staticmethod
    def create_report(template, report, filename="report.odt"):
        from secretary import Renderer

        engine = Renderer()
        result = engine.render(template, report=report)

        import tempfile
        with tempfile.NamedTemporaryFile() as output:
            output.write(result)
            output.flush()
            from django.http import FileResponse
            response = FileResponse(open(output.name, 'rb'), as_attachment=True, filename=filename)

        return response

    @staticmethod
    def create_csv_report(report, filename="report.csv"):
        import csv
        from django.http import HttpResponse

        result = report.data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        if len(result) > 0:
            keys = result[0].keys()
            writer = csv.writer(response)
            writer = csv.DictWriter(response, keys)
            writer.writeheader()
            writer.writerows(result)
        else:
            writer = csv.writer(response)

        return response

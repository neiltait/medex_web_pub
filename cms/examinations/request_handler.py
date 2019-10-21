import json

from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test.mocks import ExaminationMocks, DatatypeMocks, ReportMocks


def post_new_examination(examination_object, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_case_creation_response()
    else:
        return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, json.dumps(examination_object))


def load_examinations_index(params, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_case_index_response()
    else:
        return MedexRequest.get(auth_token, '%s/examinations' % settings.API_URL, params)


def load_patient_details_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_patient_details_load_response()
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/patient_details' % (settings.API_URL, examination_id))


def update_patient_details(examination_id, submission, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_patient_details_update_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/patient_details' % (settings.API_URL, examination_id),
                                submission)


def load_medical_team_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_medical_team_load_response(examination_id)
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/medical_team' % (settings.API_URL, examination_id))


def update_medical_team(examination_id, submission, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_medical_team_update_response()
    else:
        response = MedexRequest.put(auth_token, '%s/examinations/%s/medical_team' % (settings.API_URL, examination_id),
                                    submission)
        return response


def load_modes_of_disposal(auth_token):
    if settings.LOCAL:
        return DatatypeMocks.get_successful_modes_of_disposal_list_response()
    else:
        return MedexRequest.get(auth_token, '%s/data_types/mode_of_disposal' % settings.API_URL)


def load_case_breakdown_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_case_breakdown_load_response()
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/casebreakdown' % (settings.API_URL, examination_id))


def create_pre_scrutiny_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/prescrutiny' % (settings.API_URL, examination_id),
                                submission)


def create_other_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/other' % (settings.API_URL, examination_id),
                                submission)


def create_qap_discussion_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/qap_discussion' % (settings.API_URL, examination_id),
                                submission)


def create_meo_summary_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/meo_summary' % (settings.API_URL, examination_id),
                                submission)


def create_admission_notes_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/admission' % (settings.API_URL, examination_id),
                                submission)


def create_bereaved_discussion_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token,
                                '%s/examinations/%s/bereaved_discussion' % (settings.API_URL, examination_id),
                                submission)


def create_medical_history_event(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_timeline_event_create_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/medical_history' % (settings.API_URL, examination_id),
                                submission)


def load_case_outcome(auth_token, examination_id):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_case_outcome_response()
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s' % (settings.API_URL, examination_id))


def complete_case_scrutiny(auth_token, examination_id):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_scrutiny_complete_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/confirmation_of_scrutiny' % (settings.API_URL,
                                                                                             examination_id))


def confirm_coroner_referral(auth_token, examination_id):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_coroner_referral_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/coroner_referral' % (settings.API_URL, examination_id))


def update_outcomes_outstanding_items(auth_token, examination_id, submission):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_outstanding_items_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/outstanding_case_items' % (settings.API_URL,
                                                                                           examination_id), submission)


def close_case(auth_token, examination_id):
    if settings.LOCAL:
        return ExaminationMocks.get_successful_case_close_response()
    else:
        return MedexRequest.put(auth_token, '%s/examinations/%s/close_case' % (settings.API_URL, examination_id))


def load_coroner_report(auth_token, examination_id):
    if settings.LOCAL:
        return ReportMocks.get_successful_coroner_report_response()
    else:
        return MedexRequest.get(auth_token,
                                '%s/report/%s/coronal_referral_download' % (settings.API_URL, examination_id))

def load_financial_report(params, auth_token):
    if settings.LOCAL:
        return ReportMocks.get_successful_financial_report_response()
    else:
        return MedexRequest.get(auth_token, '%s/report/finance_download' % settings.API_URL, params)

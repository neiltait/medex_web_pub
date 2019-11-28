from rest_framework import status

from errors.utils import log_api_error, handle_error
from examinations import request_handler
from examinations.models.case_breakdown import CaseStatus
from examinations.presenters.core import PatientHeader
from medexCms.api import enums
from medexCms.utils import parse_datetime, fallback_to


class CaseOutcome:
    SCRUTINY_CONFIRMATION_FORM_TYPE = 'pre-scrutiny-confirmed'
    CORONER_REFERRAL_FORM_TYPE = 'coroner-referral'
    OUTSTANDING_ITEMS_FORM_TYPE = 'outstanding-items'
    CLOSE_CASE_FORM_TYPE = 'close-case'

    date_format = '%d.%m.%Y %H:%M'
    CORONER_INVESTIGATION_KEY = 'ReferToCoroner'
    MCCD_100A_KEY = 'IssueMCCDWith100a'
    MCCD_KEY = 'IssueMCCD'
    PENDING = 'PENDING'
    REFER_TO_CORONER_KEYS = [CORONER_INVESTIGATION_KEY, MCCD_100A_KEY]

    QAP_OUTCOMES = {
        enums.outcomes.MCCD_FROM_QAP: 'Medical Certificate of Cause of Death to be issued, COD provided by QAP',
        enums.outcomes.MCCD_FROM_ME: 'Medical Certificate of Cause of Death to be issued, COD provided by ME',
        enums.outcomes.MCCD_FROM_QAP_AND_ME: 'Medical Certificate of Cause of Death to be issued, new COD reached',
        enums.outcomes.CORONER_INVESTIGATION: 'Refer to coroner for investigation',
        enums.outcomes.CORONER_100A: ('Refer to coroner for permission to issue Medical Certificate of Cause of Death'
                                      ' with 100a'),
        enums.outcomes.DISCUSSION_UNABLE_TO_HAPPEN: 'Discussion was unable to happen'
    }

    REPRESENTATIVE_OUTCOMES = {
        enums.discussion.COD_ACCEPTED: 'Medical Certificate of Cause of Death to be issued, no concerns',
        enums.discussion.CONCERNS_CORONER: 'Refer to coroner for investigation, concerns raised',
        enums.discussion.CONCERNS_100A: 'Refer to coroner for 100a, concerns raised',
        enums.discussion.CONCERNS_ADDRESSED: ('Medical Certificate of Cause of Death to be issued, concerns addressed'
                                              ' without coroner'),
        enums.discussion.DISCUSSION_UNABLE_TO_HAPPEN: 'Discussion was unable to happen',
    }

    PRE_SCRUTINY_OUTCOMES = {
        enums.outcomes.MCCD: 'Medical Certificate of Cause of Death to be issued',
        enums.outcomes.CORONER_INVESTIGATION: 'Refer to coroner for investigation',
        enums.outcomes.CORONER_100A: ('Refer to coroner for permission to issue Medical Certificate of Cause of Death'
                                      ' with 100a')
    }

    OUTCOME_SUMMARIES = {
        CORONER_INVESTIGATION_KEY: {'heading': 'Refer to coroner', 'details': 'For investigation'},
        MCCD_100A_KEY: {'heading': 'Refer to coroner',
                        'details': 'For permission to issue Medical Certificate of Cause of Death with 100A'},
        MCCD_KEY: {'heading': 'Medical Certificate of Cause of Death to be issued'},
        PENDING: {'heading': 'OUTCOME PENDING'}
    }

    CORONER_DISCLAIMERS = {
        CORONER_INVESTIGATION_KEY: 'This case has been submitted to the coroner for an investigation.',
        MCCD_100A_KEY: ('This case has been submitted to the coroner for permission to issue an Medical Certificate'
                        ' of Cause of Death with 100a.'),
    }

    def __init__(self, obj_dict, examination_id):
        self.examination_id = examination_id
        self.case_header = PatientHeader(obj_dict.get("header"))
        self.case_outcome_summary = obj_dict.get("caseOutcomeSummary")
        self.case_representative_outcome = obj_dict.get("outcomeOfRepresentativeDiscussion")
        self.case_pre_scrutiny_outcome = obj_dict.get("outcomeOfPrescrutiny")
        self.case_qap_outcome = obj_dict.get("outcomeQapDiscussion")
        self.case_open = True if not obj_dict.get("caseCompleted") else False
        self.scrutiny_confirmed = parse_datetime(obj_dict.get("scrutinyConfirmedOn"))
        self.coroner_referral = obj_dict.get("coronerReferralSent")
        self.me_full_name = obj_dict.get("caseMedicalExaminerFullName")
        self.me_id = obj_dict.get('caseMedicalExaminerId')
        self.me_gmc_number = fallback_to(obj_dict.get('caseMedicalExaminerGmcNumber'), '')
        self.mccd_issued = obj_dict.get("mccdIssued")
        self.cremation_form_status = obj_dict.get("cremationFormStatus")
        self.gp_notified_status = obj_dict.get("gpNotifiedStatus")
        self.waive_fee = obj_dict.get('waiveFee')

    def me_full_name_with_gmc_number(self):
        if self.me_gmc_number:
            return '%s: %s' % (self.me_full_name, self.me_gmc_number)
        else:
            return self.me_full_name

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_case_outcome(auth_token, examination_id)

        if response.status_code == status.HTTP_200_OK:
            return CaseOutcome(response.json(), examination_id), CaseStatus(response.json()), None
        else:
            log_api_error('case outcome load', response.text if response.content != 'null' else '')
            return None, None, handle_error(response, {'type': 'case outcome', 'action': 'loading'})

    @classmethod
    def complete_scrutiny(cls, auth_token, examination_id):
        response = request_handler.complete_case_scrutiny(auth_token, examination_id)

        if response.status_code == status.HTTP_200_OK:
            return response.status_code
        else:
            return handle_error(response, {'type': 'case', 'action': 'completing'})

    @classmethod
    def confirm_coroner_referral(cls, auth_token, examination_id):
        response = request_handler.confirm_coroner_referral(auth_token, examination_id)

        if response.status_code == status.HTTP_200_OK:
            return response.status_code
        else:
            return handle_error(response, {'type': 'case', 'action': 'confirming coroner referral'})

    @classmethod
    def update_outstanding_items(cls, auth_token, examination_id, submission):
        response = request_handler.update_outcomes_outstanding_items(auth_token, examination_id, submission)

        if response.status_code == status.HTTP_200_OK:
            return response.status_code
        else:
            return handle_error(response, {'type': 'case', 'action': 'updating'})

    @classmethod
    def close_case(cls, auth_token, examination_id):
        response = request_handler.close_case(auth_token, examination_id)
        if response.status_code == status.HTTP_200_OK:
            return response.status_code
        else:
            return handle_error(response, {'type': 'case', 'action': 'closing'})

    def scrutiny_actions_complete(self):
        return not self.case_header.pending_scrutiny_notes and not self.case_header.pending_discussion_with_qap and \
            not self.case_header.pending_discussion_with_representative and self.case_header.admission_notes_added

    def is_coroner_investigation(self):
        return True if self.case_outcome_summary == self.CORONER_INVESTIGATION_KEY else False

    def is_coroner_referral(self):
        return True if self.case_outcome_summary in self.REFER_TO_CORONER_KEYS else False

    def show_coroner_referral(self):
        return self.is_coroner_referral()

    def show_outstanding_items(self):
        return not self.is_coroner_investigation()

    def coroner_referral_enabled(self):
        return True if self.scrutiny_confirmed and not self.coroner_referral else False

    def outstanding_items_enabled(self):
        return True if self.scrutiny_confirmed and self.coroner_referral_complete() and self.case_open else False

    def coroner_referral_complete(self):
        return self.coroner_referral or not self.is_coroner_referral()

    def outstanding_items_complete(self):
        if self.show_outstanding_items():
            return self.mccd_issued and self.cremation_form_status and self.gp_notified_status
        else:
            return True

    def can_close(self):
        return True if self.case_open and self.coroner_referral_complete() and self.outstanding_items_complete() \
            else False

    def coroner_referral_disclaimer(self):
        return self.CORONER_DISCLAIMERS.get(self.case_outcome_summary)

    def display_outcome_summary(self):
        if self.case_outcome_summary:
            return self.OUTCOME_SUMMARIES.get(self.case_outcome_summary)
        else:
            return self.OUTCOME_SUMMARIES.get(self.PENDING)

    def display_pre_scrutiny_outcome(self):
        return self.PRE_SCRUTINY_OUTCOMES.get(self.case_pre_scrutiny_outcome)

    def display_qap_outcome(self):
        return self.QAP_OUTCOMES.get(self.case_qap_outcome)

    def display_representative_outcome(self):
        return self.REPRESENTATIVE_OUTCOMES.get(self.case_representative_outcome)

    def display_scrutiny_date(self):
        return self.scrutiny_confirmed.strftime(self.date_format)

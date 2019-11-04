from rest_framework import status

from unittest.mock import patch
from unittest import skip, TestCase

from alerts.messages import ApiErrorMessages
from examinations.forms.case_outcomes import OutstandingItemsForm
from examinations.forms.timeline_events import PreScrutinyEventForm, AdmissionNotesEventForm, MeoSummaryEventForm, \
    OtherEventForm, MedicalHistoryEventForm, QapDiscussionEventForm, BereavedDiscussionEventForm
from examinations.models.case_breakdown import CaseBreakdown

from examinations.models.case_outcomes import CaseOutcome
from examinations.utils import event_form_parser
from medexCms.api import enums
from medexCms.test.mocks import SessionMocks, ExaminationMocks
from medexCms.test.utils import MedExTestCase


class ExaminationsViewsTests(MedExTestCase):

    # Create case tests

    def test_landing_on_create_case_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/create')
        self.assertTemplateUsed(response, 'examinations/create.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self, mock_user_validation):
        response = self.client.get('/cases/create')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_successful_case_creation_response_with_id_1())
    def test_create_case_endpoint_redirects_to_examination_page_if_creation_succeeds(self, post_response):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data["create-and-continue"] = "Create case and continue"
        response = self.client.post('/cases/create', form_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/cases/1/patient-details')

    def test_case_create_add_another_case_redirects_to_case_create(self):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/create.html')
        form = self.get_context_value(response.context, "form")
        self.assertEqual(form.first_name, "")

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response())
    def test_create_case_endpoint_returns_response_status_from_api_if_creation_fails(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_case_with_missing_required_fields_returns_bad_request(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.pop('first_name', None)
        response = self.client.post('/cases/create', form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'examinations/create.html')

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response_nhs_duplicate())
    def test_create_case_endpoint_raises_nhs_duplicate_error_if_raised_by_api(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        form = self.get_context_value(response.context, "form")

        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.DUPLICATE)

    @skip
    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response_nhs_whitespace())
    def test_create_case_endpoint_raises_nhs_whitespace_error_if_raised_by_api(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        form = self.get_context_value(response.context, "form")

        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.CONTAINS_WHITESPACE)

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response_nhs_invalid_characters())
    def test_create_case_endpoint_raises_nhs_invalid_characters_error_if_raised_by_api(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        form = self.get_context_value(response.context, "form")

        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.CONTAINS_INVALID_CHARACTERS)

    @skip
    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response_nhs_invalid())
    def test_create_case_endpoint_raises_nhs_invalid_error_if_raised_by_api(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        form = self.get_context_value(response.context, "form")

        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.INVALID)

    @skip
    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response_nhs_any_other_error())
    def test_create_case_endpoint_raises_nhs_unknown_error_if_raised_by_api(self, mock_case_create):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', ExaminationMocks.get_minimal_create_case_form_data())
        form = self.get_context_value(response.context, "form")

        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.UNKNOWN)

    # Edit case tests

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_edit_page_when_not_logged_in_redirects_to_login(self, mock_user_validation):
        response = self.client.get('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_landing_on_edit_page_redirects_to_edit_patient_details(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID)

    # Patient details tests

    @patch('examinations.request_handler.load_patient_details_by_id',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_load_response())
    def test_landing_on_edit_patient_details_page_when_the_case_cant_be_found_loads_the_error_template_with_correct_code(
            self, mock_case_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_edit_patient_details_page_redirects_to_landing_when_logged_out(self, mock_user_validation):
        response = self.client.get('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_landing_on_edit_patient_details_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')

    def test_submitting_a_form_with_missing_required_fields_returns_bad_request(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        form_data.pop('first_name', None)
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')

    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_update_response())
    def test_submitting_a_valid_form_that_fails_on_the_api_returns_the_code_from_the_api(self, mock_update):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code,
                         ExaminationMocks.get_unsuccessful_patient_details_update_response().status_code)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')

    @skip
    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_nhs_number_unknown_error())
    def test_patient_details_form_raises_nhs_unknown_error_if_unfamiliar_error_raised_by_api(self, mock_update):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)

        form = self.get_context_value(response.context, "form")
        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.UNKNOWN)

    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_nhs_number_duplicate_error())
    def test_patient_details_form_raises_nhs_duplicate_error_if_raised_by_api(self, mock_update):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)

        form = self.get_context_value(response.context, "form")
        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.DUPLICATE)

    @skip
    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_nhs_number_invalid_error())
    def test_patient_details_form_raises_nhs_invalid_error_if_raised_by_api(self, mock_update):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)

        form = self.get_context_value(response.context, "form")
        self.assertEqual(form.errors["count"], 1)
        self.assertEqual(form.errors["nhs_number"], ApiErrorMessages().nhs_numbers.INVALID)

    def test_submitting_a_valid_form_that_passes_on_the_api_returns_reloads_the_form(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')

    def test_submitting_a_valid_form_that_passes_on_the_api_redirects_to_the_next_tab(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details?nextTab=medical-team' % ExaminationMocks.EXAMINATION_ID,
                                    form_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/cases/%s/medical-team' % ExaminationMocks.EXAMINATION_ID)

    # Case breakdown tests

    def test_loading_the_case_breakdown_screen_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/edit_case_breakdown.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_loading_the_case_breakdown_screen_when_not_logged_in_redirects_to_login(self, mock_validate):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    @patch('examinations.request_handler.load_case_breakdown_by_id',
           return_value=ExaminationMocks.get_unsuccessful_case_load_response())
    def test_loading_the_case_breakdown_screen_returns_error_page_with_invalid_case_id(self, mock_breakdown_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    @patch('examinations.request_handler.create_pre_scrutiny_event',
           return_value=ExaminationMocks.get_unsuccessful_timeline_event_create_response())
    def test_posting_an_valid_form_that_fails_on_the_api_returns_the_api_response_code(self, mock_pre_scrutiny_create):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_pre_scrutiny_create_event_data()
        response = self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code,
                         ExaminationMocks.get_unsuccessful_timeline_event_create_response().status_code)
        self.assertTemplateUsed(response, 'examinations/edit_case_breakdown.html')

    def test_posting_a_valid_form_that_succeeds_on_the_api_returns_the_api_response_code(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_pre_scrutiny_create_event_data()
        response = self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, ExaminationMocks.get_successful_timeline_event_create_response().status_code)
        self.assertTemplateUsed(response, 'examinations/edit_case_breakdown.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_case_outcome_page_when_not_logged_in_redirects_to_login_page(self, mock_auth_check):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_landing_on_the_case_outcome_page_when_logged_in_displays_the_outcome_page(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/case_outcome.html')

    @patch('examinations.request_handler.load_case_outcome',
           return_value=ExaminationMocks.get_unsuccessful_case_outcome_response())
    def test_landing_on_the_case_outcome_page_with_invalid_case_id_returns_error_page(self, mock_outcome_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID)
        self.assertEqual(response.status_code, ExaminationMocks.get_unsuccessful_case_outcome_response().status_code)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    def test_posting_completion_of_scrutiny_sends_update_to_api(self):
        self.set_auth_cookies()
        form_data = {CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE: True}
        response = self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/case_outcome.html')

    @patch('examinations.request_handler.complete_case_scrutiny',
           return_value=ExaminationMocks.get_unsuccessful_scrutiny_complete_response())
    def test_posting_completion_of_scrutiny_returns_error_page_if_api_update_fails(self, mock_completion_response):
        self.set_auth_cookies()
        form_data = {CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE: True}
        response = self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code,
                         ExaminationMocks.get_unsuccessful_scrutiny_complete_response().status_code)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    def test_posting_to_the_case_outcome_view_with_unknown_form_returns_error_page(self):
        self.set_auth_cookies()
        form_data = {'unknown-form-type': True}
        response = self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    def test_posting_coroner_referral_sends_update_to_api(self):
        self.set_auth_cookies()
        form_data = {CaseOutcome.CORONER_REFERRAL_FORM_TYPE: True}
        response = self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/case_outcome.html')

    @patch('examinations.request_handler.confirm_coroner_referral',
           return_value=ExaminationMocks.get_unsuccessful_coroner_referral_response())
    def test_posting_coroner_referral_returns_error_page_if_api_update_fails(self, mock_completion_response):
        self.set_auth_cookies()
        form_data = {CaseOutcome.CORONER_REFERRAL_FORM_TYPE: True}
        response = self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code,
                         ExaminationMocks.get_unsuccessful_coroner_referral_response().status_code)
        self.assertTemplateUsed(response, 'errors/base_error.html')


class ExaminationsUtilsTests(MedExTestCase):

    # event_form_parser tests

    def test_event_form_parser_returns_a_pre_scrutiny_form_when_given_pre_scrutiny_form_data(self):
        form_data = {
            'add-event-to-timeline': 'pre-scrutiny'
        }

        result = event_form_parser(form_data)
        self.assertEqual(type(result), PreScrutinyEventForm)

    def test_event_form_parser_returns_a_admission_notes_form_when_given_admission_notes_form_data(self):
        form_data = {
            'date_of_last_admission_not_known': True,
            'time_of_last_admission_not_known': True,
            'add-event-to-timeline': 'admission-notes'
        }

        result = event_form_parser(form_data)
        self.assertEqual(type(result), AdmissionNotesEventForm)

    def test_event_form_parser_returns_a_meo_summary_form_when_given_meo_summary_form_data(self):
        form_data = {
            'meo_summary_notes': True,
            'add-event-to-timeline': 'meo-summary'
        }

        result = event_form_parser(form_data)
        self.assertEqual(type(result), MeoSummaryEventForm)

    def test_event_form_parser_returns_an_other_form_when_given_admission_notes_form_data(self):
        form_data = {
            'other_notes_id': True,
            'add-event-to-timeline': 'other'
        }

        result = event_form_parser(form_data)
        self.assertEqual(type(result), OtherEventForm)


class ExaminationsBreakdownValidationTests(MedExTestCase):

    # Medical and social history only requires notes to be non-blank for addition

    def test_medical_history_form_valid_for_timeline_if_notes_are_not_blank(self):
        form_data = {
            'medical_history_id': 'any id',
            'medical-history-details': 'any content',
            'add-event-to-timeline': True
        }

        form = MedicalHistoryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_medical_history_form_not_valid_for_timeline_if_notes_are_blank(self):
        form_data = {
            'medical_history_id': 'any id',
            'medical-history-details': '',
            'add-event-to-timeline': True
        }

        form = MedicalHistoryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_medical_history_form_valid_for_draft_even_if_notes_are_blank(self):
        form_data = {
            'medical_history_id': 'any id',
            'medical-history-details': '',
            'add-event-to-timeline': False
        }

        form = MedicalHistoryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    # Other notes only requires notes to be non-blank for addition

    def test_other_notes_form_valid_for_timeline_if_notes_are_not_blank(self):
        form_data = {
            'other_notes_id': 'any id',
            'more_detail': 'any content',
            'add-event-to-timeline': True
        }

        form = OtherEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_other_notes_form_not_valid_for_timeline_if_notes_are_blank(self):
        form_data = {
            'other_notes_id': 'any id',
            'more_detail': '',
            'add-event-to-timeline': True
        }

        form = OtherEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_other_notes_form_valid_for_draft_even_if_notes_are_blank(self):
        form_data = {
            'other_notes_id': 'any id',
            'more_detail': '',
            'add-event-to-timeline': False
        }

        form = OtherEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    # MEO Summary only requires notes to be non-blank for addition

    def test_meo_summary_form_valid_for_timeline_if_notes_are_not_blank(self):
        form_data = {
            'meo_summary_id': 'any id',
            'meo_summary_notes': 'any content',
            'add-event-to-timeline': True
        }

        form = MeoSummaryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_meo_summary_form_not_valid_for_timeline_if_notes_are_blank(self):
        form_data = {
            'meo_summary_id': 'any id',
            'meo_summary_notes': '',
            'add-event-to-timeline': True
        }

        form = MeoSummaryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_meo_summary_form_valid_for_draft_even_if_notes_are_blank(self):
        form_data = {
            'meo_summary_id': 'any id',
            'meo_summary_notes': '',
            'add-event-to-timeline': False
        }

        form = MeoSummaryEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    """
    LATEST ADMISSION FORM

    Draft - Date to be a valid date or blank

    Final - Date to be a valid date or unknown, Time or unknown, one of coroner referral radio buttons selected

    """

    def test_latest_admission_form_valid_for_draft_when_date_blank(self):
        blank_form_data = {
            'admission_notes_id': 'any id',
            'day_of_last_admission': '',
            'month_of_last_admission': '',
            'year_of_last_admission': '',
            'date_of_last_admission_not_known': '',
            'time_of_last_admission': '',
            'time_of_last_admission_not_known': '',
            'latest_admission_notes': '',
            'latest_admission_immediate_referral': '',
            'latest_admission_route': '',
            'add-event-to-timeline': False
        }

        form = AdmissionNotesEventForm(form_data=blank_form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_valid_for_draft_when_date_is_real_date(self):
        form_data_with_valid_date = {
            'admission_notes_id': 'any id',
            'day_of_last_admission': '9',
            'month_of_last_admission': '5',
            'year_of_last_admission': '2019',
            'date_of_last_admission_not_known': '',
            'time_of_last_admission': '',
            'time_of_last_admission_not_known': '',
            'latest_admission_notes': '',
            'latest_admission_immediate_referral': '',
            'latest_admission_route': 'ae',
            'add-event-to-timeline': False
        }

        form = AdmissionNotesEventForm(form_data=form_data_with_valid_date)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_not_valid_for_draft_when_date_is_not_real_date(self):
        form_data_where_month_is_13 = {
            'admission_notes_id': 'any id',
            'day_of_last_admission': '1',
            'month_of_last_admission': '13',
            'year_of_last_admission': '2019',
            'date_of_last_admission_not_known': '',
            'time_of_last_admission': '',
            'time_of_last_admission_not_known': '',
            'latest_admission_notes': '',
            'latest_admission_immediate_referral': '',
            'latest_admission_route': 'ae',
            'add-event-to-timeline': False
        }

        form = AdmissionNotesEventForm(form_data=form_data_where_month_is_13)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def valid_last_admission_final_data(self):
        return {
            'admission_notes_id': 'any id',
            'day_of_last_admission': '26',
            'month_of_last_admission': '8',
            'year_of_last_admission': '2019',
            'date_of_last_admission_not_known': '',
            'time_of_last_admission': '00:01',
            'time_of_last_admission_not_known': '',
            'latest_admission_notes': '',
            'latest_admission_immediate_referral': 'no',
            'latest_admission_route': 'ae',
            'add-event-to-timeline': True
        }

    def test_latest_admission_form_valid_for_mock_valid_final_data(self):
        form_data = self.valid_last_admission_final_data()

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_not_valid_for_final_when_date_fields_blank(self):
        form_data = self.valid_last_admission_final_data()
        form_data['day_of_last_admission'] = ''
        form_data['month_of_last_admission'] = ''
        form_data['year_of_last_admission'] = ''
        form_data['date_of_last_admission_not_known'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_latest_admission_form_valid_for_final_when_date_not_known_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['day_of_last_admission'] = ''
        form_data['month_of_last_admission'] = ''
        form_data['year_of_last_admission'] = ''
        form_data['date_of_last_admission_not_known'] = 'true'

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_valid_for_final_when_date_is_real(self):
        form_data = self.valid_last_admission_final_data()
        form_data['day_of_last_admission'] = '26'
        form_data['month_of_last_admission'] = '5'
        form_data['year_of_last_admission'] = '2019'
        form_data['date_of_last_admission_not_known'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_not_valid_for_final_when_date_is_not_real(self):
        form_data = self.valid_last_admission_final_data()
        form_data['day_of_last_admission'] = '26'
        form_data['month_of_last_admission'] = '13'
        form_data['year_of_last_admission'] = '2019'
        form_data['date_of_last_admission_not_known'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_latest_admission_form_not_valid_when_no_time_fields_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['time_of_last_admission'] = ''
        form_data['time_of_last_admission_not_known'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_latest_admission_form_valid_when_time_field_filled(self):
        form_data = self.valid_last_admission_final_data()
        form_data['time_of_last_admission'] = '00:55'
        form_data['time_of_last_admission_not_known'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_valid_when_time_not_known_checked(self):
        form_data = self.valid_last_admission_final_data()
        form_data['time_of_last_admission'] = ''
        form_data['time_of_last_admission_not_known'] = 'true'

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_not_valid_when_no_coroner_choice_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['latest_admission_immediate_referral'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_latest_admission_form_valid_when_coroner_choice_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['latest_admission_immediate_referral'] = 'yes'

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_latest_admission_form_valid_when_admission_route_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['latest_admission_route'] = 'ae'

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEqual(form.errors['count'], 0)

    def test_latest_admission_form_not_valid_when_admission_route_not_selected(self):
        form_data = self.valid_last_admission_final_data()
        form_data['latest_admission_route'] = ''

        form = AdmissionNotesEventForm(form_data=form_data)
        form.is_valid()

        self.assertEqual(form.errors['count'], 1)

    """
    PRE-SCRUTINY

    draft - no validation at all

    final - text in thoughts, text in 1a,
        radio-buttons: circumstances of death, outcome, and clinical governance selected
        clinical governance textbox filled in if clinical governance filled in
    """

    def valid_pre_scrutiny_final_data(self):
        return {
            'pre_scrutiny_id': 'any id',
            'me-thoughts': 'any thoughts',
            'cod': 'Unexpected',
            'possible-cod-1a': 'any 1a comment',
            'possible-cod-1b': '',
            'possible-cod-1c': '',
            'possible-cod-2': '',
            'ops': 'ReferToCoroner',
            'coroner-outcome': 'ReferToCoronerFor100a',
            'gr': 'No',
            'grt': '',
            'add-event-to-timeline': True
        }

    def test_pre_scrutiny_form_valid_for_mock_valid_final_data(self):
        form_data = self.valid_pre_scrutiny_final_data()

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_pre_scrutiny_form_not_valid_when_me_thoughts_not_filled_in(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['me-thoughts'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_not_valid_when_1a_not_filled_in(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['possible-cod-1a'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_not_valid_when_cod_radio_button_not_selected(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['cod'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_not_valid_when_outcome_radio_button_not_selected(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['ops'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_not_valid_when_governance_radio_button_not_selected(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['cod'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_not_valid_when_governance_radio_button_is_yes_with_no_text(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['gr'] = 'Yes'
        form_data['grt'] = ''

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_pre_scrutiny_form_valid_when_governance_radio_button_is_yes_with_text_comments(self):
        form_data = self.valid_pre_scrutiny_final_data()
        form_data['gr'] = 'Yes'
        form_data['grt'] = 'any comments'

        form = PreScrutinyEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    """

    BEREAVED DISCUSSION

    draft - date/time must be valid or empty

    final - tick for cannot happen is valid
          - otherwise:
            name
            date + time
            details
            radio buttons
    """

    def valid_bereaved_final_data(self):
        return {
            'bereaved_event_id': 'any id',
            'bereaved_rep_type': enums.people.OTHER,
            'bereaved_alternate_rep_name': 'Mrs Doe',
            'bereaved_alternate_rep_relationship': '',
            'bereaved_alternate_rep_phone_number': '',
            'bereaved_alternate_rep_present_at_death': '',
            'bereaved_alternate_rep_informed': '',
            'bereaved_existing_rep_name': '',
            'bereaved_existing_rep_relationship': '',
            'bereaved_existing_rep_phone_number': '',
            'bereaved_existing_rep_present_at_death': '',
            'bereaved_existing_rep_informed': '',
            'bereaved_discussion_could_not_happen': enums.yes_no.NO,
            'bereaved_day_of_conversation': '2',
            'bereaved_month_of_conversation': '2',
            'bereaved_year_of_conversation': '2002',
            'bereaved_time_of_conversation': '12:00',
            'bereaved_discussion_details': 'some discussion',
            'bereaved_discussion_outcome': BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS,
            'bereaved_outcome_concerned_outcome': BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_ADDRESSED,
            'add-event-to-timeline': True
        }

    def test_bereaved_form_valid_for_mock_valid_final_data(self):
        form_data = self.valid_bereaved_final_data()

        form = BereavedDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_bereaved_form_not_valid_when_conversation_details_not_filled_in(self):
        form_data = self.valid_bereaved_final_data()
        form_data['bereaved_discussion_details'] = ''

        form = BereavedDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_bereaved_form_not_valid_for_draft_when_invalid_date_filled_in(self):
        form_data = self.valid_bereaved_final_data()
        form_data['add-event-to-timeline'] = False
        form_data['bereaved_day_of_conversation'] = '2'
        form_data['bereaved_month_of_conversation'] = '223'
        form_data['bereaved_year_of_conversation'] = '2002'
        form_data['bereaved_time_of_conversation'] = '12:00'

        form = BereavedDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_bereaved_form_not_valid_when_outcome_is_not_selected(self):
        form_data = self.valid_bereaved_final_data()
        form_data['bereaved_discussion_outcome'] = ''

        form = BereavedDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_bereaved_form_not_valid_when_concerns_exist_but_final_outcome_is_not_selected(self):
        form_data = self.valid_bereaved_final_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data['bereaved_outcome_concerned_outcome'] = ''

        form = BereavedDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    """

    QAP DISCUSSION

    draft - date/time must be valid or empty

    final - tick for cannot happen is valid
          - otherwise:
            name
            date + time
            details
            radio buttons
          - if new cause of death required
            1a
    """

    def valid_qap_final_data(self):
        return {
            'qap_discussion_id': 'any id',
            'qap-discussion-doctor': QapDiscussionEventForm.OTHER_PARTICIPANT,
            'qap_discussion_could_not_happen': enums.yes_no.NO,
            'qap-default__full-name': '',
            'qap-default__role': '',
            'qap-default__organisation': '',
            'qap-default__phone-number': '',
            'qap-other__full-name': 'Robert Wilson',
            'qap-other__role': '',
            'qap-other__organisation': '',
            'qap-other__phone-number': '',
            'qap_discussion_revised_1a': 'Revised 1a',
            'qap_discussion_revised_1b': '',
            'qap_discussion_revised_1c': '',
            'qap_discussion_revised_1d': '',
            'qap_discussion_details': 'Some details',
            'qap-discussion-outcome': enums.outcomes.MCCD,
            'qap-discussion-outcome-decision': enums.outcomes.MCCD_FROM_QAP_AND_ME,
            'qap_day_of_conversation': '3',
            'qap_month_of_conversation': '6',
            'qap_year_of_conversation': '2017',
            'qap_time_of_conversation': '12:15',
            'add-event-to-timeline': True
        }

    def test_qap_form_valid_for_mock_valid_final_data(self):
        form_data = self.valid_qap_final_data()

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_qap_form_not_valid_for_draft_if_date_invalid(self):
        form_data = self.valid_qap_final_data()
        form_data['add-event-to-timeline'] = False
        form_data['qap_day_of_conversation'] = '26'
        form_data['qap_month_of_conversation'] = '262'
        form_data['qap_year_of_conversation'] = '2019'
        form_data['qap_time_of_conversation'] = '20:15'

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_valid_for_draft_if_nothing_entered(self):
        form_data = self.valid_qap_final_data()
        form_data['add-event-to-timeline'] = False
        form_data['qap_day_of_conversation'] = ''
        form_data['qap_month_of_conversation'] = ''
        form_data['qap_year_of_conversation'] = ''
        form_data['qap_time_of_conversation'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_qap_form_not_valid_for_final_if_nothing_entered(self):
        form_data = self.valid_qap_final_data()
        form_data['add-event-to-timeline'] = True
        form_data['qap_day_of_conversation'] = ''
        form_data['qap_month_of_conversation'] = ''
        form_data['qap_year_of_conversation'] = ''
        form_data['qap_time_of_conversation'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_not_valid_for_draft_if_date_partial(self):
        form_data = self.valid_qap_final_data()
        form_data['add-event-to-timeline'] = False
        form_data['qap_day_of_conversation'] = '26'
        form_data['qap_month_of_conversation'] = ''
        form_data['qap_year_of_conversation'] = '2019'
        form_data['qap_time_of_conversation'] = '20:15'

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_not_valid_for_other_participant_if_name_blank(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-doctor'] = QapDiscussionEventForm.OTHER_PARTICIPANT
        form_data['qap-other__full-name'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_not_valid_if_conversation_details_blank(self):
        form_data = self.valid_qap_final_data()
        form_data['qap_discussion_details'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_not_valid_if_outcome_not_selected(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_valid_if_coroner_as_outcome_with_coroner_action_decision(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = enums.outcomes.CORONER_INVESTIGATION

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_qap_form_not_valid_if_coroner_as_outcome_but_no_coroner_decision(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_not_valid_if_mccd_as_outcome_but_no_outcome_decision(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_valid_if_original_mccd_as_outcome_decision_and_no_revision(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_ME
        form_data['qap_discussion_revised_1a'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)

    def test_qap_form_not_valid_if_revised_mccd_as_outcome_decision_but_no_revision(self):
        form_data = self.valid_qap_final_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_QAP_AND_ME
        form_data['qap_discussion_revised_1a'] = ''

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 1)

    def test_qap_form_valid_if_discussion_could_not_happen(self):
        form_data = {
            'qap_discussion_id': 'any id',
            'qap-discussion-doctor': '',
            'qap_discussion_could_not_happen': enums.yes_no.YES,
            'qap-default__full-name': '',
            'qap-default__role': '',
            'qap-default__organisation': '',
            'qap-default__phone-number': '',
            'qap-other__full-name': '',
            'qap-other__role': '',
            'qap-other__organisation': '',
            'qap-other__phone-number': '',
            'qap_discussion_revised_1a': '',
            'qap_discussion_revised_1b': '',
            'qap_discussion_revised_1c': '',
            'qap_discussion_revised_1d': '',
            'qap_discussion_details': '',
            'qap-discussion-outcome': '',
            'qap-discussion-outcome-decision': '',
            'qap_day_of_conversation': '',
            'qap_month_of_conversation': '',
            'qap_year_of_conversation': '',
            'qap_time_of_conversation': '',
            'add-event-to-timeline': True
        }

        form = QapDiscussionEventForm(form_data=form_data)
        form.is_valid()

        self.assertEquals(form.errors['count'], 0)


class CaseBreakdownTests(MedExTestCase):

    def test_case_breakdown_object_does_generate_from_mock_data(self):
        mock_data = ExaminationMocks.get_case_breakdown_response_content()

        case_breakdown = CaseBreakdown(obj_dict=mock_data, medical_team=None)

        self.assertIsNotNone(case_breakdown)

    def test_case_breakdown_object_does_get_cause_of_death_from_prescrutiny_stage(self):
        mock_data = ExaminationMocks.get_case_breakdown_response_content()

        case_breakdown = CaseBreakdown(obj_dict=mock_data, medical_team=None)

        self.assertIsNotNone(case_breakdown.prepopulated_items)
        self.assertIsNotNone(case_breakdown.prepopulated_items.qap)

    def test_case_breakdown_object_does_add_essential_fields_to_cause_of_death_from_prescrutiny_stage(self):
        mock_data = ExaminationMocks.get_case_breakdown_response_content()

        case_breakdown = CaseBreakdown(obj_dict=mock_data, medical_team=None)

        essential_fields = ["section_1a", "section_1b", "section_1c", "section_2", "pre_scrutiny_status",
                            "medical_examiner", "date_of_latest_pre_scrutiny", "user_for_latest_pre_scrutiny"]
        for field in essential_fields:
            self.assertTrue(case_breakdown.prepopulated_items.qap.keys().__contains__(field))

    def test_case_breakdown_object_does_get_cause_of_death_from_qap_stage(self):
        mock_data = ExaminationMocks.get_case_breakdown_response_content()

        case_breakdown = CaseBreakdown(obj_dict=mock_data, medical_team=None)

        self.assertIsNotNone(case_breakdown.prepopulated_items)
        self.assertIsNotNone(case_breakdown.prepopulated_items.bereaved)

    def test_case_breakdown_object_does_add_essential_fields_to_cause_of_death_from_qap_stage(self):
        mock_data = ExaminationMocks.get_case_breakdown_response_content()

        case_breakdown = CaseBreakdown(obj_dict=mock_data, medical_team=None)

        essential_fields = ["section_1a", "section_1b", "section_1c", "section_2", "pre_scrutiny_status",
                            "medical_examiner", "date_of_latest_pre_scrutiny", "user_for_latest_pre_scrutiny",
                            "qap_discussion_status", "qap_name_for_latest_qap_discussion",
                            "date_of_latest_qap_discussion", "user_for_latest_qap_discussion"]
        for field in essential_fields:
            self.assertTrue(case_breakdown.prepopulated_items.bereaved.keys().__contains__(field))


class TestOutstandingItemsFormTests(TestCase):

    def _form(self, crem_form: str, crem_fee: bool or None) -> dict:
        return {
            'mccd_issued': False,
            'cremation_form': crem_form,
            'gp_notified': None,
            'waive_fee': crem_fee
        }

    def test_outstanding_items_for_request_sets_waive_fee_None(self):
        """
        Assert waive_fee is None when cremation form is no or unknown.
        """
        form_data = self._form(crem_form='Unknown', crem_fee=None)
        form = OutstandingItemsForm(form_data)
        form_request_data = form.for_request()
        self.assertEqual(form_request_data['waiveFee'], None)

    def test_outstanding_items_for_request_sets_waive_fee_True(self):
        """
        Assert waive_fee is True when cremation form is yes AND waive_fee is checked.
        """
        form_data = self._form(crem_form='Yes', crem_fee=True)
        form = OutstandingItemsForm(form_data)
        form_request_data = form.for_request()
        self.assertEqual(form_request_data['waiveFee'], True)

    def test_outstanding_items_for_request_sets_waive_fee_False(self):
        """
        Assert waive_fee is False when cremation form is yes AND waive_fee is not checked.
        """
        form_data = self._form(crem_form='Yes', crem_fee=None)
        form = OutstandingItemsForm(form_data)
        form_request_data = form.for_request()
        self.assertEqual(form_request_data['waiveFee'], False)

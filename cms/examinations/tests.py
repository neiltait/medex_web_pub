from datetime import datetime, timedelta

from rest_framework import status

from unittest.mock import patch

from alerts import messages
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, OtherEventForm, MedicalHistoryEventForm, QapDiscussionEventForm, \
    BereavedDiscussionEventForm
from examinations.models import Examination, PatientDetails, ExaminationOverview, MedicalTeam, CaseOutcome, CaseEvent, \
    CaseQapDiscussionEvent, MedicalTeamMember, CaseBereavedDiscussionEvent, CaseInitialEvent
from examinations.templatetags.examination_filters import case_card_presenter
from examinations.utils import event_form_parser
from medexCms.api import enums
from medexCms.test.mocks import SessionMocks, ExaminationMocks, PeopleMocks, DatatypeMocks
from medexCms.test.utils import MedExTestCase
from medexCms.utils import NONE_DATE, parse_datetime, NONE_TIME
from people.models import BereavedRepresentative


class ExaminationsViewsTests(MedExTestCase):

    #### Create case tests

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

    #### Edit case tests

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

    #### Patient details tests

    @patch('examinations.request_handler.load_patient_details_by_id',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_load_response())
    def test_landing_on_edit_patient_details_page_when_the_case_cant_be_found_loads_the_error_template_with_correct_code \
                    (self, mock_case_load):
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

    def test_submitting_a_valid_form_that_passes_on_the_api_returns_reloads_the_form(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')

    def test_submitting_a_valid_form_that_passes_on_the_api_returns_reloads_the_form(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data.update(ExaminationMocks.get_patient_details_bereaved_form_data())
        response = self.client.post('/cases/%s/patient-details?nextTab=medical-team' % ExaminationMocks.EXAMINATION_ID,
                                    form_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/cases/%s/medical-team' % ExaminationMocks.EXAMINATION_ID)

    #### Case breakdown tests

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

    def test_posting_an_valid_form_that_succeeds_on_the_api_returns_the_api_response_code(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_pre_scrutiny_create_event_data()
        response = self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code,
                         ExaminationMocks.get_successful_timeline_event_create_response().status_code)
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


class ExaminationsFormsTests(MedExTestCase):

    #### Primary Information Form
    def test_given_create_examination_without_first_name_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'data': 'test'})
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.errors["first_name"], messages.ErrorFieldRequiredMessage('first name'))

    def test_given_create_examination_with_first_name_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt'})
        form.is_valid()
        self.assertIsFalse("first_name" in form.errors)

    def test_given_create_examination_without_last_name_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'test': 'data'})
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.errors["last_name"], messages.ErrorFieldRequiredMessage('last name'))

    def test_given_create_examination_with_name_greater_than_250_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt' * 40,
                                                          'last_name': 'matt' * 40})
        form.is_valid()
        self.assertIsTrue("first_name" in form.errors)
        self.assertIsTrue("last_name" in form.errors)

    def test_given_create_examination_with_first_name_greater_than_150_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt' * 40})
        form.is_valid()
        self.assertIsTrue("first_name" in form.errors)

    def test_given_create_examination_with_last_name_greater_than_150_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'last_name': 'nicks' * 40})
        form.is_valid()
        self.assertIsTrue("last_name" in form.errors)

    def test_given_create_examination_with_last_name_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'last_name': 'nicks'})
        form.is_valid()
        self.assertIsFalse("last_name" in form.errors)

    def test_given_create_examination_without_gender_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'test': 'data'})
        result = form.is_valid()
        self.assertEqual(form.errors["gender"], messages.ErrorFieldRequiredMessage('gender'))

    def test_given_create_examination_with_gender_other_but_no_detail_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'gender': 'Other'})
        form.is_valid()
        self.assertIsTrue("gender" in form.errors)

    def test_given_create_examination_with_gender_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'gender': 'male'})
        form.is_valid()
        self.assertIsFalse("gender" in form.errors)

    def test_text_and_checkbox_group_validates_if_checkbox_is_ticked(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['']
        checkbox = True

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertTrue(group_valid)

    def test_text_and_checkbox_group_validates_if_textboxes_are_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['Filled']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertTrue(group_valid)

    def test_text_and_checkbox_group_does_not_validate_if_any_textbox_is_not_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['Filled', '']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertFalse(group_valid)

    def test_text_and_checkbox_group_does_not_validate_if_all_values_not_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertFalse(group_valid)

    def test_nhs_number_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '', 'nhs_number_not_known': True})
        form.is_valid()
        self.assertIsFalse("nhs_number" in form.errors)

    def test_nhs_number_group_does_validate_if_text_is_entered(self):
        form = PrimaryExaminationInformationForm({'nhs_number': 'ABC123', 'nhs_number_not_known': False})
        form.is_valid()
        self.assertIsFalse("nhs_number" in form.errors)

    def test_nhs_number_does_not_validate_if_nhs_number_too_long(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '12345678901234567890123456789012345678901234567890'})
        form.is_valid()
        self.assertIsTrue("nhs_number" in form.errors)

    def test_nhs_number_does_not_validate_if_nhs_number_too_short(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '1234'})
        form.is_valid()
        self.assertIsTrue("nhs_number" in form.errors)

    def test_nhs_number_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'nhs_number': ''})
        form.is_valid()
        self.assertEqual(form.errors["nhs_number"], messages.ErrorFieldRequiredMessage('NHS number'))

    def test_time_of_death_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm({'time_of_death': '', 'time_of_death_not_known': True})
        form.is_valid()
        self.assertIsFalse("time_of_death" in form.errors)

    def test_time_of_death_group_does_validate_if_text_is_entered(self):
        form = PrimaryExaminationInformationForm({'time_of_death': 'ABC123', 'time_of_death_not_known': False})
        form.is_valid()
        self.assertIsFalse("time_of_death" in form.errors)

    def test_time_of_death_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'time_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["time_of_death"], messages.ErrorFieldRequiredMessage('time of death'))

    def test_date_of_birth_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '', 'month_of_birth': '', 'year_of_birth': '', 'date_of_birth_not_known': True})
        form.is_valid()
        self.assertIsFalse("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_validate_if_all_date_boxes_are_filled(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '26', 'month_of_birth': '08', 'year_of_birth': '1978', 'date_of_birth_not_known': False})
        form.is_valid()
        self.assertIsFalse("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_not_validate_if_date_boxes_are_filled_with_bad_date(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '32', 'month_of_birth': '08', 'year_of_birth': '1978', 'date_of_birth_not_known': False})
        form.is_valid()
        self.assertIsTrue("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_birth': '', 'month_of_birth': '', 'year_of_birth': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_birth"], messages.ErrorFieldRequiredMessage('date of birth'))

    def test_date_of_birth_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_birth': '26', 'month_of_birth': '', 'year_of_birth': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_birth"], messages.ErrorFieldRequiredMessage('date of birth'))

    def test_date_of_death_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '', 'month_of_death': '', 'year_of_death': '', 'date_of_death_not_known': True})
        form.is_valid()
        self.assertIsFalse("date_of_death" in form.errors)

    def test_date_of_death_group_does_validate_if_all_date_boxes_are_filled(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '26', 'month_of_death': '08', 'year_of_death': '1978'})
        form.is_valid()
        self.assertIsFalse("date_of_death" in form.errors)

    def test_date_of_death_group_does_not_validate_if_date_boxes_are_filled_with_bad_date(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '32', 'month_of_death': '08', 'year_of_death': '2019'})
        form.is_valid()
        self.assertIsTrue("date_of_death" in form.errors)

    def test_date_of_death_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '', 'month_of_death': '', 'year_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], messages.ErrorFieldRequiredMessage('date of death'))

    def test_date_of_death_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '26', 'month_of_death': '', 'year_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], messages.ErrorFieldRequiredMessage('date of death'))

    def test_place_of_death_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["place_of_death"], messages.ErrorFieldRequiredMessage('place of death'))

    def test_place_of_death_does_validate_if_present(self):
        form = PrimaryExaminationInformationForm({'place_of_death': "London"})
        form.is_valid()
        self.assertIsFalse("place_of_death" in form.errors)

    def test_me_office_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["me_office"], messages.ErrorFieldRequiredMessage('ME office'))

    def test_me_office_does_validate_if_present(self):
        form = PrimaryExaminationInformationForm({'me_office': 1})
        form.is_valid()
        self.assertIsFalse("me_office" in form.errors)

    def test_form_validates_with_required_data(self):
        # Given a complete form
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form = PrimaryExaminationInformationForm(form_data)

        # When it is validated
        form_is_valid = form.is_valid()

        # The whole form is valid
        self.assertIsTrue(form_is_valid)

    def test_form_validates_with_optional_data(self):
        # Given a complete form including optional data
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['gender_details'] = 'example gender details'
        form_data['hospital_number_1'] = 'example hospital number 1'
        form_data['hospital_number_2'] = 'example hospital number 2'
        form_data['hospital_number_3'] = 'example hospital number 3'
        form_data['out_of_hours'] = True
        form = PrimaryExaminationInformationForm(form_data)

        # When it is validated
        form_is_valid = form.is_valid()

        # The whole form is valid
        self.assertIsTrue(form_is_valid)

    def test_form_stores_optional_data(self):
        # Given a complete form including optional data
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['gender_details'] = 'example gender details'
        form_data['hospital_number_1'] = 'example hospital number 1'
        form_data['hospital_number_2'] = 'example hospital number 2'
        form_data['hospital_number_3'] = 'example hospital number 3'
        form_data['out_of_hours'] = True
        form = PrimaryExaminationInformationForm(form_data)

        # The optional data is parsed
        self.assertIs(form.gender_details, 'example gender details')
        self.assertIs(form.hospital_number_1, 'example hospital number 1')
        self.assertIs(form.hospital_number_2, 'example hospital number 2')
        self.assertIs(form.hospital_number_3, 'example hospital number 3')

    def test_form_correctly_passes_dob_and_dod_for_request_if_known(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '2'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '20'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form_data.pop('date_of_birth_not_known', None)
        form_data.pop('date_of_death_not_known', None)
        form = PrimaryExaminationInformationForm(form_data)

        result = form.to_object()
        self.assertNotEqual(result['dateOfBirth'], NONE_DATE)
        self.assertNotEqual(result['dateOfDeath'], NONE_DATE)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_true_if_no_dates_given(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsTrue(result)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_false_if_dod_is_before_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '20'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '2'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsFalse(result)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_true_if_dod_is_after_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '2'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '20'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsTrue(result)

    def test_form_returns_is_invalid_if_dod_is_before_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '20'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '2'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.is_valid()
        self.assertIsFalse(result)

    def test_api_response_transformed_to_not_known_if_TOD_at_midnight(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['timeOfDeath'] = '00:00:00'

        patient_details = PatientDetails(loaded_data)
        form = PrimaryExaminationInformationForm()
        form.set_values_from_instance(patient_details)

        self.assertIsTrue(form.time_of_death_not_known)

    #### Secondary Info Form tests

    def test_secondary_form_initialised_empty_returns_as_valid(self):
        form = SecondaryExaminationInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_secondary_form_initialised_with_content_returns_as_valid(self):
        form = SecondaryExaminationInformationForm(ExaminationMocks.get_patient_details_secondary_info_form_data())
        self.assertIsTrue(form.is_valid())

    #### Bereaved Info Form tests

    def test_bereaved_form_initialised_empty_returns_as_valid(self):
        form = BereavedInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_content_returns_as_valid(self):
        form = BereavedInformationForm(ExaminationMocks.get_patient_details_bereaved_form_data())
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date1_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['year_of_appointment_1'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date1_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['day_of_appointment_1'] = '31'
        form_data['month_of_appointment_1'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date2_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['year_of_appointment_2'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date2_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['day_of_appointment_2'] = '31'
        form_data['month_of_appointment_2'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_form_initialised_from_db_correctly_sets_representatives(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['representatives'].append(PeopleMocks.get_bereaved_representative_response_dict())
        patient_details = PatientDetails(loaded_data)
        form = BereavedInformationForm()
        form.set_values_from_instance(patient_details)
        self.assertEqual(form.bereaved_name_1, loaded_data['representatives'][0]['fullName'])
        self.assertEqual(form.bereaved_name_2, '')

    #### Urgency Info Form tests

    def test_urgency_form_initialised_empty_returns_as_valid(self):
        form = UrgencyInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_urgency_form_initialised_with_content_returns_as_valid(self):
        form = UrgencyInformationForm(ExaminationMocks.get_patient_details_urgency_form_data())
        self.assertIsTrue(form.is_valid())

    #### Medical Team Form tests
    def test_medical_team_member_initialised_with_valid_medical_team_contains_lookups(self):
        medical_team = MedicalTeam(ExaminationMocks.get_medical_team_content(), ExaminationMocks.EXAMINATION_ID)

        self.assertGreater(len(medical_team.medical_examiner_lookup), 0)
        self.assertGreater(len(medical_team.medical_examiner_officer_lookup), 0)

    def test_medical_team_member_form_initialised_empty_returns_as_not_valid(self):
        form = MedicalTeamMembersForm()
        self.assertIsFalse(form.is_valid())
        self.assertEqual(form.errors['count'], 1)

    def test_medical_team_member_form_initialised_with_content_returns_as_valid(self):
        form = MedicalTeamMembersForm(ExaminationMocks.get_medical_team_tab_form_data())
        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_initialised_with_valid_medical_team_returns_as_valid(self):
        medical_team = MedicalTeam(ExaminationMocks.get_medical_team_content(), ExaminationMocks.EXAMINATION_ID)
        form = MedicalTeamMembersForm(medical_team=medical_team)

        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_without_consultant_1_is_not_valid(self):
        mock_data = ExaminationMocks.get_medical_team_tab_form_data()
        mock_data['consultant_name_1'] = ""
        mock_data['consultant_role_1'] = ""
        mock_data['consultant_organisation_1'] = ""
        mock_data['consultant_phone_number_1'] = ""
        form = MedicalTeamMembersForm(mock_data)

        self.assertIsFalse(form.is_valid())

    # PreScrutinyEventForm

    def test_is_valid_returns_true_if_the_pre_scrutiny_form_is_valid(self):
        form = PreScrutinyEventForm({})
        self.assertIsTrue(form.is_valid())

    def test_for_request_correctly_maps_the_pre_scrutiny_form_for_the_api(self):
        me_thoughts = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        cod = 'Expected'
        possible_cod_1a = 'Cause of death'
        possible_cod_1b = ''
        possible_cod_1c = ''
        possible_cod_2 = ''
        ops = 'IssueAnMccd'
        gr = 'Yes'
        grt = 'Palliative care were called too late.'
        add_event_to_timeline = 'pre-scrutiny'

        form_data = {
            'me-thoughts': me_thoughts,
            'cod': cod,
            'possible-cod-1a': possible_cod_1a,
            'possible-cod-1b': possible_cod_1b,
            'possible-cod-1c': possible_cod_1c,
            'possible-cod-2': possible_cod_2,
            'ops': ops,
            'gr': gr,
            'grt': grt,
            'add-event-to-timeline': add_event_to_timeline
        }
        form = PreScrutinyEventForm(form_data)
        result = form.for_request()
        self.assertEqual(result.get('medicalExaminerThoughts'), me_thoughts)
        self.assertEqual(result.get('circumstancesOfDeath'), cod)
        self.assertEqual(result.get('causeOfDeath1a'), possible_cod_1a)
        self.assertEqual(result.get('causeOfDeath1b'), possible_cod_1b)
        self.assertEqual(result.get('causeOfDeath1c'), possible_cod_1c)
        self.assertEqual(result.get('causeOfDeath2'), possible_cod_2)
        self.assertEqual(result.get('outcomeOfPreScrutiny'), ops)
        self.assertEqual(result.get('clinicalGovernanceReview'), gr)
        self.assertEqual(result.get('clinicalGovernanceReviewText'), grt)
        self.assertEqual(result.get('isFinal'), True)

    # AdmissionNotesEventForm

    def test_is_valid_returns_true_if_the_admission_notes_form_is_valid(self):
        form = AdmissionNotesEventForm({})
        self.assertIsTrue(form.is_valid())

    def test_for_request_correctly_maps_the_admission_notes_form_for_the_api(self):
        admission_day = 2
        admission_month = 2
        admission_year = 2019
        admission_date_unknown = False
        admission_time = '10:00'
        admission_time_unknown = False
        admission_notes = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        coroner_referral = 'no'
        add_event_to_timeline = 'admission-notes'

        form_data = {
            'day_of_last_admission': admission_day,
            'month_of_last_admission': admission_month,
            'year_of_last_admission': admission_year,
            'date_of_last_admission_not_known': admission_date_unknown,
            'time_of_last_admission': admission_time,
            'time_of_last_admission_not_known': admission_time_unknown,
            'latest_admission_notes': admission_notes,
            'latest_admission_immediate_referral': coroner_referral,
            'add-event-to-timeline': add_event_to_timeline
        }

        form = AdmissionNotesEventForm(form_data)
        result = form.for_request()

        self.assertEqual(result.get("notes"), admission_notes)
        self.assertEqual(result.get("admittedDate"), form.admission_date())
        self.assertEqual(result.get("admittedTime"), admission_time)
        self.assertEqual(result.get("immediateCoronerReferral"), False)
        self.assertEqual(result.get("isFinal"), True)

    def test_admission_date_returns_none_if_admission_date_unknown(self):
        admission_day = ''
        admission_month = ''
        admission_year = ''
        admission_date_unknown = enums.true_false.TRUE
        admission_time = '10:00'
        admission_time_unknown = enums.true_false.FALSE
        admission_notes = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        coroner_referral = 'no'
        add_event_to_timeline = 'admission-notes'

        form_data = {
            'day_of_last_admission': admission_day,
            'month_of_last_admission': admission_month,
            'year_of_last_admission': admission_year,
            'date_of_last_admission_not_known': admission_date_unknown,
            'time_of_last_admission': admission_time,
            'time_of_last_admission_not_known': admission_time_unknown,
            'latest_admission_notes': admission_notes,
            'latest-admission-suspect-referral': coroner_referral,
            'add-event-to-timeline': add_event_to_timeline
        }

        form = AdmissionNotesEventForm(form_data)
        result = form.admission_date()

        self.assertIsNone(result)

    # QapDiscussionEventForm

    def test_qap_discussion__request__maps_to_qap_discussion_api_put_request(self):
        # Given form data
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call data for an api request
        request = form.for_request()

        # then the data is not empty
        self.assertGreater(len(request), 0)

    def test_qap_discussion__request__maps_conversation_day_month_year_time_to_single_api_date(self):
        # Given form data with specific dates
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap_day_of_conversation'] = '20'
        form_data['qap_month_of_conversation'] = '5'
        form_data['qap_year_of_conversation'] = '2019'
        form_data['qap_time_of_conversation'] = '12:30'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the returned date starts with the expected reverse date
        expected_date_start = '2019-05-20T12:30'
        self.assertTrue(request['dateOfConversation'].startswith(expected_date_start))

    def test_qap_discussion__request__maps_mccd_and_qap_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_QAP
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 1 - qap updates the decision
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_QAP)

    def test_qap_discussion__request__maps_mccd_and_me_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_ME
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 2 - me's first decision
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_ME)

    def test_qap_discussion__request__maps_mccd_and_agreement_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_QAP_AND_ME
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 3 - agreement
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_QAP_AND_ME)

    def test_qap_discussion__request__maps_refer_to_coroner_and_100a_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = enums.outcomes.CORONER_100A
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to coroner referral
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.CORONER_100A)

    def test_qap_discussion__request__maps_refer_to_coroner_and_investigation_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = enums.outcomes.CORONER_INVESTIGATION
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to coroner referral
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.CORONER_INVESTIGATION)

    def test_qap_discussion__request__maps_default_qap_to_participant_if_discussion_type_qap_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-doctor'] = 'qap'
        form_data['qap-default__full-name'] = 'Default Qap'
        form_data['qap-other__full-name'] = 'Custom Qap'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantName'], 'Default Qap')

    def test_qap_discussion__request__maps_custom_qap_to_participant_if_discussion_type_qap_selected(self):
        # Given form data with the Other Qap radio button selected
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-doctor'] = 'other'
        form_data['qap-default__full-name'] = 'Default Qap'
        form_data['qap-other__full-name'] = 'Custom Qap'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the custom qap is assigned as participant
        self.assertEquals(request['participantName'], 'Custom Qap')

    def test_qap_discussion__fill_from_draft__recalls_fields_from_api_event_draft(self):
        # Given draft data from the api
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is created
        self.assertEquals(draft_data["discussionDetails"], form.discussion_details)

    def test_qap_discussion__fill_from_draft__maps_single_conversation_date_to_day_month_year_time_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        draft_data['dateOfConversation'] = "2019-04-08T08:30:00.000Z"
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, 8)
        self.assertEquals(form.month_of_conversation, 4)
        self.assertEquals(form.year_of_conversation, 2019)
        self.assertEquals(form.time_of_conversation, "08:30")

    def test_qap_discussion__fill_from_draft__maps_null_conversation_date_to_empty_string_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        draft_data['dateOfConversation'] = ""
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, '')
        self.assertEquals(form.month_of_conversation, '')
        self.assertEquals(form.year_of_conversation, '')
        self.assertEquals(form.time_of_conversation, '')

    def test_qap_discussion__fill_from_draft__sets_type_as_qap_if_default_qap_matches_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        qap_in_data = self.get_participant_from_draft(draft_data)
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, default_qap=qap_in_data)

        # Then the form is filled with individual date fields
        self.assertEquals(form.discussion_participant_type, 'qap')

    def test_qap_discussion__fill_from_draft__sets_type_as_other_if_default_qap_doesnt_match_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        any_medic = MedicalTeamMember(name='Any other qap')
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, default_qap=any_medic)

        # Then the form is filled with individual date fields
        self.assertEquals(form.discussion_participant_type, 'other')

    @staticmethod
    def get_participant_from_draft(draft_data):
        return MedicalTeamMember(name=draft_data["participantName"],
                                 role=draft_data["participantRole"],
                                 organisation=draft_data["participantOrganisation"],
                                 phone_number=draft_data["participantPhoneNumber"])

    # BereavedDiscussionEvent

    def test_bereaved_discussion__request__maps_to_bereaved_discussion_api_put_request(self):
        # Given form data
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call data for an api request
        request = form.for_request()

        # then the data is not empty
        self.assertGreater(len(request), 0)

    def test_bereaved_discussion__request__maps_conversation_day_month_year_time_to_single_api_date(self):
        # Given form data with specific dates
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_day_of_conversation'] = '20'
        form_data['bereaved_month_of_conversation'] = '5'
        form_data['bereaved_year_of_conversation'] = '2019'
        form_data['bereaved_time_of_conversation'] = '12:30'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the returned date starts with the expected reverse date
        expected_date_start = '2019-05-20T12:30'
        self.assertTrue(request['dateOfConversation'].startswith(expected_date_start))

    def test_bereaved_discussion__request__maps_no_concerns_to_a_single_field(self):
        # Given form data with outcome that there are no concerns
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_NO_CONCERNS
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 1 - Request_100a
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_NO_CONCERNS)

    def test_bereaved_discussion__request__maps_concerns_leading_to_coroner_investigation_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data[
            'bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_CORONER
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 2 - Coroner enquiry required
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_CORONER)

    def test_bereaved_discussion__request__maps_concerns_leading_to_100a_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data['bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_100A
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 3 - 100a required
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_100A)

    def test_bereaved_discussion__request__maps_concerns_leading_to_agreement_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data[
            'bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_ADDRESSED
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 4 - disagreements have been addressed
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_ADDRESSED)

    def test_bereaved_discussion__request__maps_existing_rep_to_participant_if_existing_rep_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_rep_type'] = enums.people.BEREAVED_REP
        form_data['bereaved_existing_rep_name'] = 'Existing rep'
        form_data['bereaved_alternate_rep_name'] = 'Alternate rep'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantFullName'], 'Existing rep')

    def test_bereaved_discussion__request__maps_alternate_rep_to_participant_if_alternate_rep_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_rep_type'] = enums.people.OTHER
        form_data['bereaved_existing_rep_name'] = 'Existing rep'
        form_data['bereaved_alternate_rep_name'] = 'Alternate rep'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantFullName'], 'Alternate rep')

    def test_bereaved_discussion__fill_from_draft__recalls_fields_from_api_event_draft(self):
        # Given draft data from the api
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is created
        self.assertEquals(draft_data["discussionDetails"], form.discussion_details)

    def test_bereaved_discussion__fill_from_draft__maps_single_conversation_date_to_day_month_year_time_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        draft_data['dateOfConversation'] = "2019-04-08T08:30:00.000Z"
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, 8)
        self.assertEquals(form.month_of_conversation, 4)
        self.assertEquals(form.year_of_conversation, 2019)
        self.assertEquals(form.time_of_conversation, "08:30")

    def test_bereaved_discussion__fill_from_draft__maps_null_conversation_date_to_empty_string_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        draft_data['dateOfConversation'] = ""
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, '')
        self.assertEquals(form.month_of_conversation, '')
        self.assertEquals(form.year_of_conversation, '')
        self.assertEquals(form.time_of_conversation, '')

    def test_bereaved_discussion__fill_from_draft__sets_type_as_existing_if_existing_rep_matches_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        representative_in_data = self.get_existing_bereaved_representative_from_draft(draft_data)
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft,
                                                             default_representatives=[representative_in_data])

        # Then the form is filled with individual date fields
        self.assertIsTrue(form.use_existing_bereaved)

    def test_bereaved_discussion__fill_from_draft__sets_type_as_other_if_existing_rep_doesnt_match_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        mock_existing_rep = BereavedRepresentative(
            {
                "fullName": "mock",
                "relationship": "mock",
                "phoneNumber": "1234"
            }
        )
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft,
                                                             default_representatives=[mock_existing_rep])

        # Then the form is filled with individual date fields
        self.assertIsFalse(form.use_existing_bereaved)

    @staticmethod
    def get_existing_bereaved_representative_from_draft(draft_data):
        return BereavedRepresentative({
            'fullName': draft_data.get("participantFullName"),
            'relationship': draft_data.get("participantRelationship"),
            'phoneNumber': draft_data.get("participantPhoneNumber")
        })


class ExaminationsModelsTests(MedExTestCase):

    #### PatientDetails tests

    def test_initialising_with_the_none_date_results_in_no_dob(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['dateOfBirth'] = NONE_DATE
        patient_details = PatientDetails(loaded_data)
        self.assertIsNone(patient_details.date_of_birth)
        self.assertIsNone(patient_details.day_of_birth)
        self.assertIsNone(patient_details.month_of_birth)
        self.assertIsNone(patient_details.year_of_birth)

    def test_initialising_with_the_none_date_results_in_no_dod(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['dateOfDeath'] = NONE_DATE
        patient_details = PatientDetails(loaded_data)
        self.assertIsNone(patient_details.date_of_death)
        self.assertIsNone(patient_details.day_of_death)
        self.assertIsNone(patient_details.month_of_death)
        self.assertIsNone(patient_details.year_of_death)

    def test_initialising_with_a_mode_of_disposal_and_the_enums_sets_the_mode_of_disposal(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        mode_of_disposal = list(DatatypeMocks.get_modes_of_disposal_list().keys())[0]
        loaded_data['modeOfDisposal'] = mode_of_disposal
        patient_details = PatientDetails(loaded_data, DatatypeMocks.get_modes_of_disposal_list())
        self.assertEqual(patient_details.mode_of_disposal, mode_of_disposal)

    def test_initialising_with_a_bereaved_sets_the_representatives(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        bereaved = PeopleMocks.get_bereaved_representative_response_dict()
        loaded_data['representatives'].append(bereaved)
        patient_details = PatientDetails(loaded_data, DatatypeMocks.get_modes_of_disposal_list())
        self.assertEqual(len(patient_details.representatives), 1)
        self.assertEqual(patient_details.representatives[0].full_name, bereaved['fullName'])

    #### ExaminationOverview tests

    def test_card_presenter_returns_a_correctly_formatted_dod_if_date_present(self):

        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])

        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_death = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['banner_dod']
        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_card_presenter_returns_a_correctly_formatted_dob_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['banner_dob']

        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_card_presenter_returns_a_correctly_formatted_appointment_date_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.appointment_date = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['appointment_date']

        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_calc_age_correctly_calculates_the_age_if_dates_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        birth_date = '2018-02-02T02:02:02.000Z'
        death_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(birth_date)
        examination_overview.date_of_death = parse_datetime(death_date)
        result = examination_overview.calc_age()
        expected_age = 1
        self.assertEqual(result, expected_age)

    def test_calc_age_returns_none_if_date_of_birth_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        death_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = parse_datetime(death_date)
        result = examination_overview.calc_age()

        self.assertIsNone(result)

    def test_calc_age_returns_none_if_date_of_death_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        birth_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(birth_date)
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()
        self.assertIsNone(result)

    def test_calc_age_returns_none_if__both_dates_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()

        self.assertIsNone(result)

    def test_calc_last_admission_days_ago_returns_correct_number_of_days_if_date_of_admission_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        admission_date = datetime.today() - timedelta(days=1)
        examination_overview.last_admission = admission_date
        result = examination_overview.calc_last_admission_days_ago()
        expected_days = 1
        self.assertEqual(result, expected_days)

    def test_calc_last_admission_days_ago_returns_0_if_date_of_admission_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        admission_date = None
        examination_overview.last_admission = parse_datetime(admission_date)
        result = examination_overview.calc_last_admission_days_ago()
        expected_days = 0
        self.assertEqual(result, expected_days)

    def test_calc_created_days_ago_returns_correct_number_of_days_if_case_created_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        case_created_date = datetime.today() - timedelta(days=1)
        examination_overview.case_created_date = case_created_date
        result = examination_overview.calc_created_days_ago()
        expected_days = 1
        self.assertEqual(result, expected_days)

    def test_calc_created_days_ago_returns_0_if_case_created_date_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        case_created_date = None
        examination_overview.case_created_date = parse_datetime(case_created_date)
        result = examination_overview.calc_created_days_ago()
        expected_days = 0
        self.assertEqual(result, expected_days)


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

    def test_other_notes_form_valid_for_draft_even_if_notes_are_blank(self):
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


class ExaminationsBreakdownTests(MedExTestCase):

    def test_initial_event_does_display_date_in_correct_format(self):
        data = {'dateOfDeath': '2019-05-12T00:00:00'}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_date(), '12.05.2019')

    def test_initial_event_does_display_time_in_correct_format(self):
        data = {'timeOfDeath': '00:55:00'}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_time(), '00:55:00')

    def test_initial_event_does_display_unknown_for_default_none_date(self):
        data = {'dateOfDeath': NONE_DATE}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_date(), CaseInitialEvent.UNKNOWN)


    def test_initial_event_does_display_unknown_for_default_none_time(self):
        data = {'timeOfDeath': NONE_TIME}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_time(), CaseInitialEvent.UNKNOWN)

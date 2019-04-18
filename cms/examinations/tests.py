from datetime import datetime, timedelta

from rest_framework import status

from unittest.mock import patch

from alerts import messages
from alerts.messages import ErrorFieldRequiredMessage
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, OtherEventForm, QapDiscussionEventForm
from examinations.models import Examination, PatientDetails, ExaminationOverview, MedicalTeam, CaseOutcome, CaseEvent, \
    CaseQapDiscussionEvent, MedicalTeamMember
from examinations.utils import event_form_parser
from medexCms.test.mocks import SessionMocks, ExaminationMocks, PeopleMocks, DatatypeMocks
from medexCms.test.utils import MedExTestCase
from medexCms.utils import NONE_DATE, parse_datetime


class ExaminationsViewsTests(MedExTestCase):

    #### Create case tests

    def test_landing_on_create_case_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/cases/create')
        self.assertTemplateUsed(response, 'examinations/create.html')
        alerts_list = self.get_context_value(response.context, 'alerts')
        self.assertEqual(len(alerts_list), 0)

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
        alerts_list = self.get_context_value(response.context, 'alerts')
        self.assertEqual(len(alerts_list), 1)
        self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

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
        self.assertEqual(form.errors["first_name"], ErrorFieldRequiredMessage('first name'))

    def test_given_create_examination_with_first_name_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt'})
        form.is_valid()
        self.assertIsFalse("first_name" in form.errors)

    def test_given_create_examination_without_last_name_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'test': 'data'})
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.errors["last_name"], ErrorFieldRequiredMessage('last name'))

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

    def test_given_create_examination_with_first_name_greater_than_150_characters_does_not_validate(self):
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
        self.assertEqual(form.errors["gender"], ErrorFieldRequiredMessage('gender'))

    def test_given_create_examination_with_gender_other_but_no_detail_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'gender': 'other'})
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

    def test_nhs_number_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'nhs_number': ''})
        form.is_valid()
        self.assertEqual(form.errors["nhs_number"], ErrorFieldRequiredMessage('NHS number'))

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
        self.assertEqual(form.errors["time_of_death"], ErrorFieldRequiredMessage('time of death'))

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
        self.assertEqual(form.errors["date_of_birth"], ErrorFieldRequiredMessage('date of birth'))

    def test_date_of_birth_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_birth': '26', 'month_of_birth': '', 'year_of_birth': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_birth"], ErrorFieldRequiredMessage('date of birth'))

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
        self.assertEqual(form.errors["date_of_death"], ErrorFieldRequiredMessage('date of death'))

    def test_date_of_death_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '26', 'month_of_death': '', 'year_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], ErrorFieldRequiredMessage('date of death'))

    def test_place_of_death_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["place_of_death"], ErrorFieldRequiredMessage('place of death'))

    def test_place_of_death_does_validate_if_present(self):
        form = PrimaryExaminationInformationForm({'place_of_death': 1})
        form.is_valid()
        self.assertIsFalse("place_of_death" in form.errors)

    def test_me_office_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["me_office"], ErrorFieldRequiredMessage('ME office'))

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
        self.assertIs(form.out_of_hours, True)

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

    def test_medical_team_member_form_initialised_empty_returns_as_not_valid(self):
        form = MedicalTeamMembersForm()
        self.assertIsFalse(form.is_valid())
        self.assertEqual(form.errors['count'], 1)

    def test_medical_team_member_form_initialised_with_content_returns_as_valid(self):
        form = MedicalTeamMembersForm(ExaminationMocks.get_medical_team_tab_form_data())
        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_initialised_with_valid_medical_team_returns_as_valid(self):
        medical_team = MedicalTeam(obj_dict=ExaminationMocks.get_medical_team_content())
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
            'latest-admission-suspect-referral': coroner_referral,
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
        admission_date_unknown = True
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
        form_data['qap-discussion-outcome'] = 'mccd'
        form_data['qap-discussion-outcome-decision'] = 'outcome-decision-1'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 1 - qap updates the decision
        self.assertEquals(request['qapDiscussionOutcome'], QapDiscussionEventForm.DISCUSSION_OUTCOME_MCCD_FROM_QAP)

    def test_qap_discussion__request__maps_mccd_and_me_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = 'mccd'
        form_data['qap-discussion-outcome-decision'] = 'outcome-decision-2'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 2 - me's first decision
        self.assertEquals(request['qapDiscussionOutcome'], QapDiscussionEventForm.DISCUSSION_OUTCOME_MCCD_FROM_ME)

    def test_qap_discussion__request__maps_mccd_and_agreement_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = 'mccd'
        form_data['qap-discussion-outcome-decision'] = 'outcome-decision-3'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 3 - agreement
        self.assertEquals(request['qapDiscussionOutcome'], QapDiscussionEventForm.DISCUSSION_OUTCOME_MCCD_AGREED_UPDATE)

    def test_qap_discussion__request__maps_refer_to_coroner_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = 'coroner'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to coroner referral
        self.assertEquals(request['qapDiscussionOutcome'], QapDiscussionEventForm.DISCUSSION_OUTCOME_CORONER)

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
                                 role=draft_data["participantRoll"],
                                 organisation=draft_data["participantOrganisation"],
                                 phone_number=draft_data["participantPhoneNumber"])


class ExaminationsModelsTests(MedExTestCase):

    #### Examination tests

    def test_load_by_id_returns_an_examination_instance_if_found(self):
        examination = Examination.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertEqual(type(examination), Examination)

    @patch('examinations.request_handler.load_by_id',
           return_value=ExaminationMocks.get_unsuccessful_case_load_response())
    def test_load_by_id_returns_none_if_not_found(self, mock_case_load):
        examination = Examination.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(examination)

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
        loaded_data['modeOfDisposal'] = DatatypeMocks.get_modes_of_disposal_list()[mode_of_disposal]
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

    def test_display_dod_returns_a_correctly_formatted_string_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_death = parse_datetime(given_date)
        result = examination_overview.display_dod()
        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_display_dob_returns_a_correctly_formatted_string_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(given_date)
        result = examination_overview.display_dob()
        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_display_appointment_date_returns_a_correctly_formatted_string_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.appointment_date = parse_datetime(given_date)
        result = examination_overview.display_appointment_date()
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

    def test_calc_age_returns_0_if_date_of_birth_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        death_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = parse_datetime(death_date)
        result = examination_overview.calc_age()
        expected_age = 0
        self.assertEqual(result, expected_age)

    def test_calc_age_returns_0_if_date_of_death_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        birth_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(birth_date)
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()
        expected_age = 0
        self.assertEqual(result, expected_age)

    def test_calc_age_returns_0_if__both_dates_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()
        expected_age = 0
        self.assertEqual(result, expected_age)

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

    def test_event_form_parser_returns_a_meo_summary_form_when_given_admission_notes_form_data(self):
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

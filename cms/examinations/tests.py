from unittest.mock import patch

from rest_framework import status

from alerts import messages
from alerts.messages import ErrorFieldRequiredMessage
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, MedicalTeamAssignedTeamForm
from medexCms.test import mocks
from medexCms.test.utils import MedExTestCase


@patch('examinations.request_handler.load_modes_of_disposal', return_value=mocks.LOAD_MODES_OF_DISPOSAL)
class ExaminationsViewsTests(MedExTestCase):

    #### Create case tests

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_create_case_page_loads_the_correct_template(self, mock_modes_of_disposal, mock_user_validation, mock_locations_list,
            mock_me_offices_list, mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/create')
        self.assertTemplateUsed(response, 'examinations/create.html')
        alerts_list = self.get_context_value(response.context, 'alerts')
        self.assertEqual(len(alerts_list), 0)

    @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self, mock_modes_of_disposal, mock_user_validation,
            mock_locations_list, mock_me_offices_list, mocks_permission_load):
        response = self.client.get('/cases/create')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.post_new_examination', return_value=mocks.SUCCESSFUL_CASE_CREATE)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_create_case_endpoint_redirects_to_home_if_creation_succeeds(self, mock_modes_of_disposal, mock_auth_validation, mock_case_create,
                                                                         mock_permission_load):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', mocks.get_minimal_create_form_data())
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.post_new_examination', return_value=mocks.UNSUCCESSFUL_CASE_CREATE)
    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_create_case_endpoint_returns_response_status_from_api_if_creation_fails(self, mock_modes_of_disposal, mock_auth_validation,
            mock_case_create, mock_locations_list, mock_me_offices_list, mock_permission_load):
        self.set_auth_cookies()
        response = self.client.post('/cases/create', mocks.get_minimal_create_form_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_creating_a_case_with_missing_required_fields_returns_bad_request(self, mock_modes_of_disposal, mock_user_validation,
            mock_locations_list, mock_me_offices_list, mock_permission_load):
        self.set_auth_cookies()
        form_data = mocks.get_minimal_create_form_data()
        form_data.pop('first_name', None)
        response = self.client.post('/cases/create', form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'examinations/create.html')
        alerts_list = self.get_context_value(response.context, 'alerts')
        self.assertEqual(len(alerts_list), 1)
        self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

    #### Edit case tests

    @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
    def test_landing_on_edit_page_when_not_logged_in_redirects_to_login(self, mock_modes_of_disposal, mock_user_validation):
        response = self.client.get('/cases/%s/patient-details' % mocks.CREATED_EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('people.request_handler.get_medical_examiners_list', return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS)
    @patch('people.request_handler.get_medical_examiners_officers_list',
           return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS)
    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_CASE_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_edit_page_redirects_to_edit_patient_details(self, mock_modes_of_disposal, mock_locations_list,
                                    mock_me_offices_list, mock_mes, mock_meos, mock_user_validation, mock_case_load,
                                    mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s' % mocks.CREATED_EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/cases/%s/patient-details' % mocks.CREATED_EXAMINATION_ID)

    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('people.request_handler.get_medical_examiners_list', return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS)
    @patch('people.request_handler.get_medical_examiners_officers_list',
           return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS)
    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.load_patient_details_by_id', return_value=mocks.UNSUCCESSFUL_PATIENT_DETAILS_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_edit_page_when_the_case_cant_be_found_loads_the_error_template_with_correct_code(self, mock_modes_of_disposal,
                 mock_locations_list, mock_me_offices_list, mock_mes, mock_meos, mock_user_validation, mock_case_load,
                 mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/cases/%s/patient-details' % mocks.CREATED_EXAMINATION_ID)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    @patch('locations.request_handler.get_locations_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
    @patch('locations.request_handler.get_me_offices_list', return_value=mocks.SUCCESSFUL_ME_OFFICES_LOAD)
    @patch('people.request_handler.get_medical_examiners_list', return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS)
    @patch('people.request_handler.get_medical_examiners_officers_list',
           return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS)
    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.load_patient_details_by_id', return_value=mocks.SUCCESSFUL_PATIENT_DETAILS_LOAD)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_submitting_a_form_with_missing_required_fields_returns_bad_request(self, mock_modes_of_disposal, mock_locations_list,
                                    mock_me_offices_list, mock_mes, mock_meos, mock_user_validation, mock_case_load,
                                    mock_permission_load):
        self.set_auth_cookies()
        form_data = mocks.get_minimal_create_form_data()
        form_data.update(mocks.get_bereaved_examination_data())
        form_data.pop('first_name', None)
        response = self.client.post('/cases/%s/patient-details' % mocks.CREATED_EXAMINATION_ID, form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'examinations/edit_patient_details.html')


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
        form_data = mocks.get_minimal_create_form_data()
        form = PrimaryExaminationInformationForm(form_data)

        # When it is validated
        form_is_valid = form.is_valid()

        # The whole form is valid
        self.assertIsTrue(form_is_valid)

    def test_form_validates_with_optional_data(self):
        # Given a complete form including optional data
        form_data = mocks.get_minimal_create_form_data()
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
        form_data = mocks.get_minimal_create_form_data()
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

    #### Secondary Info Form tests

    def test_secondary_form_initialised_empty_returns_as_valid(self):
        form = SecondaryExaminationInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_secondary_form_initialised_with_content_returns_as_valid(self):
        form = SecondaryExaminationInformationForm(mocks.SECONDARY_EXAMINATION_DATA)
        self.assertIsTrue(form.is_valid())

    #### Bereaved Info Form tests

    def test_bereaved_form_initialised_empty_returns_as_valid(self):
        form = BereavedInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_content_returns_as_valid(self):
        form = BereavedInformationForm(mocks.get_bereaved_examination_data())
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date1_returns_as_invalid(self):
        form_data = mocks.get_bereaved_examination_data()
        form_data['year_of_appointment_1'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date1_returns_as_invalid(self):
        form_data = mocks.get_bereaved_examination_data()
        form_data['day_of_appointment_1'] = '31'
        form_data['month_of_appointment_1'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date2_returns_as_invalid(self):
        form_data = mocks.get_bereaved_examination_data()
        form_data['year_of_appointment_2'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date2_returns_as_invalid(self):
        form_data = mocks.get_bereaved_examination_data()
        form_data['day_of_appointment_2'] = '31'
        form_data['month_of_appointment_2'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    #### Urgency Info Form tests

    def test_urgency_form_initialised_empty_returns_as_valid(self):
        form = UrgencyInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_urgency_form_initialised_with_content_returns_as_valid(self):
        form = UrgencyInformationForm(mocks.URGENCY_EXAMINATION_DATA)
        self.assertIsTrue(form.is_valid())

    #### Medical Team Form tests

    def test_medical_team_member_form_initialised_empty_returns_as_valid(self):
        form = MedicalTeamMembersForm()
        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_initialised_with_content_returns_as_valid(self):
        form = MedicalTeamMembersForm(mocks.get_medical_team_form_data())
        self.assertIsTrue(form.is_valid())

    #### Assigned Team Form tests

    def test_medical_team_assigned_team_form_initialised_empty_returns_as_valid(self):
        form = MedicalTeamAssignedTeamForm()
        self.assertIsTrue(form.is_valid())

    def test_medical_team_assigned_team_form_initialised_with_content_returns_as_valid(self):
        form = MedicalTeamAssignedTeamForm(mocks.get_assigned_medical_team_form_data())
        self.assertIsTrue(form.is_valid())

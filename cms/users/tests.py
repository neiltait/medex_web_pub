from examinations.models.case_breakdown import CaseBreakdown
from medexCms.test.utils import MedExTestCase
from medexCms.test.mocks import SessionMocks, UserMocks, PermissionMocks, ExaminationMocks

from rest_framework import status

from unittest.mock import patch

from alerts import messages
from permissions.models import Permission, PermittedActions

from .models import User
from .forms import CreateUserForm, EditUserProfileForm, ManageUserForm


class UsersViewsTest(MedExTestCase):

    # User create tests

    def test_landing_on_the_user_creation_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/users/new')
        self.assertTemplateUsed(response, 'users/new.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_user_creation_page_redirects_to_login_if_not_logged_in(self, mock_auth_validation):
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_user_creation_endpoint_returns_a_bad_request_response_if_form_invalid(self):
        self.set_auth_cookies()
        response = self.client.post('/users/new', {'email_address': 'test.user@email.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('users.request_handler.create_user', return_value=UserMocks.get_unsuccessful_user_creation_response())
    def test_user_creation_endpoint_returns_response_status_from_api_if_creation_fails(self, mock_user_creation):
        self.set_auth_cookies()
        response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_endpoint_returns_redirect_if_creation_succeeds(self):
        self.set_auth_cookies()
        response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/users/%s/add_permission' % UserMocks.USER_ID)


class PermissionViewsTests(MedExTestCase):
    # Add permission tests

    """ GENERAL """

    def test_landing_on_the_add_permission_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertTemplateUsed(response, 'users/permission_builder.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_add_permission_page_redirects_to_login_if_not_logged_in(self, mock_auth_validation):
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    """ GET """

    @patch('users.request_handler.load_by_id', return_value=UserMocks.get_unsuccessful_single_user_load_response())
    def test_landing_on_the_add_permission_page_loads_the_correct_template_if_the_user_cant_be_found(self,
                                                                                                     mock_user_load):
        self.set_auth_cookies()
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    """ POST """

    def test_submitting_a_valid_form_that_succeeds_on_api_returns_the_a_redirect_to_the_manage_user_page(self):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/users/%s/manage' % UserMocks.USER_ID)

    def test_a_valid_form_that_succeeds_on_api_returns_a_blank_permissions_page_if_add_another_selected(self):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': '', 'add_another': 'true'}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        context_form = self.get_context_value(response.context, 'form')
        self.assertIsNone(context_form.permission_level)
        self.assertIsNone(context_form.role)

    def test_submitting_an_invalid_form_returns_a_bad_request_response_and_an_error_message(self):
        self.set_auth_cookies()
        submission = {'role': '', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertTemplateUsed(response, 'users/permission_builder.html')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('permissions.request_handler.create_permission',
           return_value=PermissionMocks.get_unsuccessful_permission_creation_response())
    def test_submitting_a_valid_form_that_errors_on_api_returns_the_status_from_server_and_an_error_message(self,
                                                                                                            mock_permission_creation):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertTemplateUsed(response, 'users/permission_builder.html')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ UPDATE """

    def test_submitting_an_update_form_that_succeeds_on_api_redirects_to_the_manage_user_page(self):
        # Given - some valid permission update data'
        self.set_auth_cookies()
        data = PermissionMocks.get_permission_builder_form_mock_data()

        # When - we submit to the update endpoint (mocked to always return success)'
        response = self.client.post('/users/%s/edit_permission/%s' % (UserMocks.USER_ID, PermissionMocks.PERMISSION_ID),
                                    data)

        # Then - we should be get successful and redirect to the manage users page'
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/users/%s/manage' % UserMocks.USER_ID)

    def test_submitting_an_update_form_that_errors_on_cms_returns_error(self):
        # Given - some invalid permission update data'
        self.set_auth_cookies()
        data = PermissionMocks.get_permission_builder_invalid_form_mock_data()

        # When - we submit to the update endpoint (mocked to always return success if it gets to the api)'
        response = self.client.post('/users/%s/edit_permission/%s' % (UserMocks.USER_ID, PermissionMocks.PERMISSION_ID),
                                    data)

        # Then - we should be get failure and stay on the editor page'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'users/permission_editor.html')

    @patch('permissions.request_handler.update_permission',
           return_value=PermissionMocks.get_unsuccessful_permission_update_response())
    def test_submitting_a_valid_update_form_that_errors_on_api_returns_error(self, mock_permission_update):
        # Given - some valid permission update data'
        self.set_auth_cookies()
        data = PermissionMocks.get_permission_builder_form_mock_data()

        # When - we submit to the update endpoint (mocked to always return failure if it gets to the api)'
        response = self.client.post('/users/%s/edit_permission/%s' % (UserMocks.USER_ID, PermissionMocks.PERMISSION_ID),
                                    data)

        # Then - we should be get server failure and stay on the editor page'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'users/permission_editor.html')

    """ DELETE """

    def test_submitting_a_valid_delete_that_succeeds_on_api_redirects_to_the_manage_user_page(self):
        # Given - some valid delete data'
        self.set_auth_cookies()

        # When - we submit to the delete endpoint
        response = self.client.get('/users/%s/delete_permission/%s' % (UserMocks.USER_ID, PermissionMocks.PERMISSION_ID))

        # Then - we should get redirected to the manage user page
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/users/%s/manage' % UserMocks.USER_ID)


class UsersFormsTests(MedExTestCase):

    # CreateUserForm tests

    def test_CreateUserForm_initialises_blank_attributes_if_no_request_provided(self):
        create_form = CreateUserForm()
        self.assertEqual(create_form.email_address, '')

    def test_CreateUserForm_initialises_with_filled_attributes_if_request_provided(self):
        email_address = 'test.user@nhs.co.uk'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertEqual(create_form.email_address, email_address)

    def test_CreateUserForm_validates_as_false_if_email_is_empty_string_with_the_correct_error_message(self):
        email_address = ''
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsFalse(create_form.validate())
        self.assertEqual(create_form.email_error, messages.MISSING_EMAIL)

    def test_CreateUserForm_validates_as_false_if_email_is_missing_with_the_correct_error_message(self):
        email_address = None
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsFalse(create_form.validate())
        self.assertEqual(create_form.email_error, messages.MISSING_EMAIL)

    def test_CreateUserForm_validates_as_false_if_email_is_not_nhs_domain_with_the_correct_error_message(self):
        email_address = 'test.user@email.com'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsFalse(create_form.validate())
        self.assertEqual(create_form.email_error, messages.INVALID_EMAIL_DOMAIN)

    def test_CreateUserForm_validates_as_true_if_email_is_present_and_nhs_domain_with_no_error_message(self):
        email_address = 'test.user@nhs.uk'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsTrue(create_form.validate())
        self.assertEqual(create_form.email_error, None)

    def test_CreateUserForm_check_is_nhs_email_returns_true_if_email_is_nhs_domain(self):
        email_address = 'test.user@nhs.uk'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsTrue(create_form.check_is_nhs_email())

    def test_CreateUserForm_check_is_nhs_email_returns_false_if_email_is_not_nhs_domain(self):
        email_address = 'test.user@email.com'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsFalse(create_form.check_is_nhs_email())

    def test_CreateUserForm_register_response_errors_registers_email_error(self):
        email_address = 'test.user@email.com'
        create_form = CreateUserForm({'email_address': email_address})
        error_string = 'some_error'

        class mock_non_ok_response:
            ok = False

            @staticmethod
            def json():
                return {'Email': [error_string]}

        create_form.register_response_errors(mock_non_ok_response)
        self.assertEqual(error_string, create_form.email_error)

    class mockNonOkResponse:
        ok = False

        def __init__(self, json_response):
            self.json_response = json_response

        def json(self):
            return self.json_response

    def test_ManageUsersForm_register_reponse_errors_w_gmc_number(self):
        form = ManageUserForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'GmcNumber': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(1, form.errors['count'])
        self.assertEqual(error_string, form.errors['gmc_number'])

    def test_ManageUsersForm_register_reponse_errors_wo_gmc_number_w_additional(self):
        form = ManageUserForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'other_error': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(1, form.errors['count'])
        self.assertEqual(messages.GENERAL_ERROR % ("updating", "user"), form.form_error)

    def test_ManageUsersForm_register_reponse_errors_w_gmc_number_and_additional(self):
        form = ManageUserForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'GmcNumber': [error_string], 'other_error': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(2, form.errors['count'])
        self.assertEqual(error_string, form.errors['gmc_number'])
        self.assertEqual(messages.GENERAL_ERROR % ("updating", "user"), form.form_error)

    def test_EditUserProfileForm_register_reponse_errors_w_gmc_number(self):
        form = EditUserProfileForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'GmcNumber': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(1, form.errors['count'])
        self.assertEqual(error_string, form.errors['gmc_number'])

    def test_EditUserProfileForm_register_reponse_errors_wo_gmc_number_w_additional(self):
        form = EditUserProfileForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'other_error': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(1, form.errors['count'])
        self.assertEqual(messages.GENERAL_ERROR % ("updating", "user profile"), form.errors['form'])

    def test_EditUserProfileForm_register_reponse_errors_w_gmc_number_and_additional(self):
        form = EditUserProfileForm()
        error_string = 'some_error'
        response = self.mockNonOkResponse({'GmcNumber': [error_string], 'other_error': [error_string]})
        form.register_response_errors(response)
        self.assertEqual(2, form.errors['count'])
        self.assertEqual(error_string, form.errors['gmc_number'])
        self.assertEqual(messages.GENERAL_ERROR % ("updating", "user profile"), form.errors['form'])


class UsersModelsTests(MedExTestCase):

    # User tests

    def test_User_initialisation_correctly_sets_the_fields_from_dict(self):
        user_dict = UserMocks.get_filled_user_dict()
        user_obj = User(user_dict)

        self.assertEqual(user_obj.user_id, user_dict['userId'])
        self.assertEqual(user_obj.first_name, user_dict['firstName'])
        self.assertEqual(user_obj.last_name, user_dict['lastName'])
        self.assertEqual(user_obj.email_address, user_dict['email'])

    def test_User_full_name_method_returns_first_and_last_name_combined(self):
        user_dict = UserMocks.get_filled_user_dict()
        user_obj = User(user_dict)

        expected_result = user_dict['firstName'] + ' ' + user_dict['lastName']
        self.assertEqual(user_obj.full_name(), expected_result)

    def test_User_str_method_returns_first_and_last_name_combined(self):
        user_dict = UserMocks.get_filled_user_dict()
        user_obj = User(user_dict)

        expected_result = user_dict['firstName'] + ' ' + user_dict['lastName']
        self.assertEqual(user_obj.__str__(), expected_result)

    def test_User_load_by_id_returns_a_user_object_if_the_id_has_an_account(self):
        response = User.load_by_id(1, SessionMocks.ACCESS_TOKEN)
        self.assertEqual(type(response), User)

    @patch('users.request_handler.load_by_id', return_value=UserMocks.get_unsuccessful_single_user_load_response())
    def test_User_load_by_id_returns_a_None_object_if_the_id_doesnt_have_an_account(self, mock_user_load):
        response = User.load_by_id(0, SessionMocks.ACCESS_TOKEN)
        self.assertEqual(response, None)

    def test_load_examinations_adds_a_list_of_cases_to_the_user(self):
        user = User(UserMocks.get_filled_user_dict())
        user.auth_token = SessionMocks.ACCESS_TOKEN
        user.permissions.append(Permission(PermissionMocks.get_me_permission_dict()))
        user.load_examinations(20, 1, None, None, None)
        self.assertEquals(type(user.examinations), list)

    def test_get_forms_for_role_returns_the_correct_list_of_forms_for_an_me(self):
        user = User()
        user.auth_token = SessionMocks.ACCESS_TOKEN
        user.id_token = SessionMocks.ID_TOKEN_NAME
        user.permitted_actions = PermittedActions({"BereavedDiscussionEvent": True,
                                                   "QapDiscussionEvent": True,
                                                   "OtherEvent": True,
                                                   "PreScrutinyEvent": True
                                                   })

        available_forms = user.get_forms_for_role(
            CaseBreakdown(obj_dict=ExaminationMocks.get_case_breakdown_response_content(), medical_team=None))

        self.assertEquals(type(available_forms), list)
        self.assertEquals(available_forms[0]['id'], 'pre-scrutiny')
        self.assertEquals(available_forms[1]['id'], 'qap-discussion')
        self.assertEquals(available_forms[2]['id'], 'bereaved-discussion')
        self.assertEquals(available_forms[3]['id'], 'other')

    def test_get_forms_for_role_returns_the_correct_list_of_forms_for_an_meo(self):
        user = User()
        user.auth_token = SessionMocks.ACCESS_TOKEN
        user.id_token = SessionMocks.ID_TOKEN_NAME
        user.check_logged_in()

        available_forms = user.get_forms_for_role(
            CaseBreakdown(obj_dict=ExaminationMocks.get_case_breakdown_response_content(), medical_team=None))

        self.assertEquals(type(available_forms), list)
        self.assertEquals(available_forms[0]['id'], 'admin-notes')
        self.assertEquals(available_forms[1]['id'], 'medical-history')
        self.assertEquals(available_forms[2]['id'], 'meo-summary')
        self.assertEquals(available_forms[3]['id'], 'other')

    def test_get_forms_for_role_where_nothing_published_returns_form_with_enabled_true(self):
        user = User()
        user.auth_token = SessionMocks.ACCESS_TOKEN
        user.id_token = SessionMocks.ID_TOKEN_NAME
        user.check_logged_in()

        data = ExaminationMocks.get_empty_case_breakdown_response_content()
        available_forms = user.get_forms_for_role(
            CaseBreakdown(obj_dict=data, medical_team=None))

        self.assertEquals(available_forms[0]['id'], 'admin-notes')
        self.assertEquals(available_forms[0]['enabled'], 'true')

    def test_get_forms_for_role_with_items_published_returns_form_with_enabled_false(self):
        user = User()
        user.auth_token = SessionMocks.ACCESS_TOKEN
        user.id_token = SessionMocks.ID_TOKEN_NAME
        user.check_logged_in()

        data = ExaminationMocks.get_case_breakdown_response_content()
        data['caseBreakdown']['admissionNotes']['usersDraft'] = None
        available_forms = user.get_forms_for_role(
            CaseBreakdown(obj_dict=data, medical_team=None))

        self.assertEquals(available_forms[0]['id'], 'admin-notes')
        self.assertEquals(available_forms[0]['enabled'], 'false')

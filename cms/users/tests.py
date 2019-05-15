from medexCms.test.utils import MedExTestCase
from medexCms.test.mocks import SessionMocks, UserMocks, PermissionMocks

from rest_framework import status

from unittest.mock import patch

from alerts import messages
from permissions.models import Permission

from .models import User
from .forms import CreateUserForm


class UsersViewsTest(MedExTestCase):

    #### User create tests

    def test_landing_on_the_user_creation_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/users/new')
        self.assertTemplateUsed(response, 'users/new.html')

    @patch('users.request_handler.validate_session', return_value=SessionMocks.get_unsuccessful_validate_session_response())
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

    #### Add permission tests

    def test_landing_on_the_add_permission_page_loads_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertTemplateUsed(response, 'users/permission_builder.html')

    @patch('users.request_handler.validate_session', return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_add_permission_page_redirects_to_login_if_not_logged_in(self, mock_auth_validation):
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    @patch('users.request_handler.load_by_id', return_value=UserMocks.get_unsuccessful_single_user_load_response())
    def test_landing_on_the_add_permission_page_loads_the_correct_template_if_the_user_cant_be_found(self,
                                                                                                     mock_user_load):
        self.set_auth_cookies()
        response = self.client.get('/users/%s/add_permission' % UserMocks.USER_ID)
        self.assertTemplateUsed(response, 'errors/base_error.html')

    def test_submitting_an_invalid_form_returns_a_bad_request_response_and_an_error_message(self):
        self.set_auth_cookies()
        submission = {'role': '', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertTemplateUsed(response, 'users/permission_builder.html')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('permissions.request_handler.create_permission', return_value=PermissionMocks.get_unsuccessful_permission_creation_response())
    def test_submitting_a_valid_form_that_errors_on_api_returns_the_status_from_server_and_an_error_message(self,
                                                                                            mock_permission_creation):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertTemplateUsed(response, 'users/permission_builder.html')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submitting_a_valid_form_that_succeeds_on_api_returns_the_a_redirect_to_the_settings_page(self):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/settings')

    def test_a_valid_form_that_succeeds_on_api_returns_the_a_redirect_to_the_permissions_page_if_add_another_selected(
            self):
        self.set_auth_cookies()
        submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': '', 'add_another': 'true'}
        response = self.client.post('/users/%s/add_permission' % UserMocks.USER_ID, submission)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/users/%s/add_permission' % UserMocks.USER_ID)


class UsersFormsTests(MedExTestCase):

    #### CreateUserForm tests

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

    def test_check_is_nhs_email_returns_true_if_email_is_nhs_domain(self):
        email_address = 'test.user@nhs.uk'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsTrue(create_form.check_is_nhs_email())

    def test_check_is_nhs_email_returns_false_if_email_is_not_nhs_domain(self):
        email_address = 'test.user@email.com'
        create_form = CreateUserForm({'email_address': email_address})
        self.assertIsFalse(create_form.check_is_nhs_email())


class UsersModelsTests(MedExTestCase):


    #### User tests

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
        user.load_examinations()
        self.assertEquals(type(user.examinations), list)

    def test_get_forms_for_role_returns_the_correct_list_of_forms_for_an_me(self):
        user_data = UserMocks.get_filled_user_dict()
        user_data['role'] = User.ME_ROLE_TYPE
        user = User(user_data)
        available_forms = user.get_forms_for_role()
        self.assertEquals(type(available_forms), list)
        self.assertEquals(available_forms[0]['id'], 'pre-scrutiny')
        self.assertEquals(available_forms[1]['id'], 'qap-discussion')
        self.assertEquals(available_forms[2]['id'], 'bereaved-discussion')
        self.assertEquals(available_forms[3]['id'], 'other')

    def test_get_forms_for_role_returns_the_correct_list_of_forms_for_an_meo(self):
        user_data = UserMocks.get_filled_user_dict()
        user_data['role'] = User.MEO_ROLE_TYPE
        user = User(user_data)
        available_forms = user.get_forms_for_role()
        self.assertEquals(type(available_forms), list)
        self.assertEquals(available_forms[0]['id'], 'admin-notes')
        self.assertEquals(available_forms[1]['id'], 'medical-history')
        self.assertEquals(available_forms[2]['id'], 'meo-summary')
        self.assertEquals(available_forms[3]['id'], 'other')

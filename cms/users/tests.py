from django.conf import settings

from http.cookies import SimpleCookie

from medexCms.test.utils import MedExTestCase
from medexCms.test import mocks

from rest_framework import status

from unittest.mock import patch

import uuid

from alerts import utils, messages

from .models import User
from .forms import CreateUserForm, PermissionBuilderForm


class UsersViewsTest(MedExTestCase):


#### User create tests

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_the_user_creation_page_loads_the_correct_template(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/users/new')
    self.assertTemplateUsed(response, 'users/new.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)

  @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_the_user_creation_page_redirects_to_login_if_not_logged_in(self, mock_auth_validation):
    response = self.client.get('/users/new')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_user_creation_endpoint_returns_a_bad_request_response_and_the_correct_alert_if_form_invalid(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/new', {'email_address': 'test.user@email.com'})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('users.request_handler.create_user', return_value=mocks.UNSUCCESSFUL_USER_CREATION)
  @patch('users.request_handler.check_email_in_okta', return_value=mocks.SUCCESSFUL_USER_LOOKUP)
  def test_user_creation_endpoint_returns_response_status_from_api_and_the_correct_alert_if_creation_fails(self, mock_auth_validation, mock_user_creation, mock_okta_check):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('users.request_handler.create_user', return_value=mocks.SUCCESSFUL_USER_CREATION)
  @patch('users.request_handler.check_email_in_okta', return_value=mocks.SUCCESSFUL_USER_LOOKUP)
  def test_user_creation_endpoint_returns_redirect_if_creation_succeeds(self, mock_auth_validation, mock_user_creation, mock_okta_check):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/%s/add_permission' % mocks.CREATED_USER_ID)


#### Add permission tests

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  def test_landing_on_the_add_permission_page_loads_the_correct_template(self, mock_auth_validation, mock_location_list, mock_region_list, mock_load_user):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/users/%s/add_permission' % mocks.CREATED_USER_ID)
    self.assertTemplateUsed(response, 'users/permission_builder.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)

  @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_the_add_permission_page_redirects_to_login_if_not_logged_in(self, mock_auth_validation):
    response = self.client.get('/users/%s/add_permission' % mocks.CREATED_USER_ID)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.UNSUCCESSFUL_LOAD_USER)
  def test_landing_on_the_add_permission_page_loads_the_correct_template_with_alert_if_the_user_cant_be_found(self, mock_auth_validation, mock_location_list, mock_region_list, mock_user_load):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/users/%s/add_permission' % mocks.CREATED_USER_ID)
    self.assertTemplateUsed(response, 'users/permission_builder.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.OBJECT_NOT_FOUND % 'user')

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  def test_submitting_an_invalid_form_returns_a_bad_request_response_and_an_error_message(self, mock_auth_validation, mock_location_list, mock_region_list, mock_user_load):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    submission = {'role': '', 'permission_level': 'national', 'region': '', 'trust': ''}
    response = self.client.post('/users/%s/add_permission' % mocks.CREATED_USER_ID, submission)
    self.assertTemplateUsed(response, 'users/permission_builder.html')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  @patch('users.request_handler.create_permission', return_value=mocks.UNSUCCESSFUL_PERMISSION_CREATION)
  def test_submitting_a_valid_form_that_errors_on_api_returns_the_status_from_server_and_an_error_message(self, mock_auth_validation, mock_location_list, mock_region_list, mock_user_load, mock_permission_creation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
    response = self.client.post('/users/%s/add_permission' % mocks.CREATED_USER_ID, submission)
    self.assertTemplateUsed(response, 'users/permission_builder.html')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  @patch('users.request_handler.create_permission', return_value=mocks.SUCCESSFUL_PERMISSION_CREATION)
  def test_submitting_a_valid_form_that_succeeds_on_api_returns_the_a_redirect_to_the_settings_page(self, mock_auth_validation, mock_location_list, mock_region_list, mock_user_load, mock_permission_creation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': ''}
    response = self.client.post('/users/%s/add_permission' % mocks.CREATED_USER_ID, submission)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/settings')

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_TRUST_LOAD)
  @patch('locations.request_handler.load_region_list', return_value=mocks.SUCCESSFUL_REGION_LOAD)
  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  @patch('users.request_handler.create_permission', return_value=mocks.SUCCESSFUL_PERMISSION_CREATION)
  def test_submitting_a_valid_form_that_succeeds_on_api_returns_the_a_redirect_to_the_permissions_page_if_add_another_selected(self, mock_auth_validation, mock_location_list, mock_region_list, mock_user_load, mock_permission_creation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    submission = {'role': 'me', 'permission_level': 'national', 'region': '', 'trust': '', 'add_another': 'true'}
    response = self.client.post('/users/%s/add_permission' % mocks.CREATED_USER_ID, submission)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/%s/add_permission' % mocks.CREATED_USER_ID)


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

  @patch('users.request_handler.check_email_in_okta', return_value=mocks.UNSUCCESSFUL_USER_LOOKUP)
  def test_check_is_in_okta_returns_false_if_email_is_not_in_okta_and_sets_error_meesage(self, mock_okta_check):
    email_address = 'test.user@nhs.uk'
    create_form = CreateUserForm({'email_address': email_address})
    self.assertIsFalse(create_form.check_is_in_okta())
    self.assertEqual(create_form.email_error, messages.NOT_IN_OKTA)

  @patch('users.request_handler.check_email_in_okta', return_value=mocks.SUCCESSFUL_USER_LOOKUP)
  def test_check_is_in_okta_returns_false_if_email_is_not_in_okta(self, mock_okta_check):
    email_address = 'test.user@nhs.uk'
    create_form = CreateUserForm({'email_address': email_address})
    self.assertIsTrue(create_form.check_is_in_okta())

#### PermissionBuilderForm tests

  def test_is_valid_returns_false_when_no_role_given(self):
    form_content = {
      'role': None,
      'permission_level': 'national',
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsFalse(result)
    self.assertEqual(form.role_error, messages.FIELD_MISSING % "a role")

  def test_is_valid_returns_false_when_no_level_given(self):
    form_content = {
      'role': 'me',
      'permission_level': None,
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsFalse(result)
    self.assertEqual(form.permission_level_error, messages.FIELD_MISSING % "a level")

  def test_is_valid_returns_false_when_no_trust_given_for_a_trust_level_permission(self):
    form_content = {
      'role': 'me',
      'permission_level': 'trust',
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsFalse(result)
    self.assertEqual(form.trust_error, messages.FIELD_MISSING % "a trust")

  def test_is_valid_returns_false_when_no_region_given_for_a_region_level_permission(self):
    form_content = {
      'role': 'me',
      'permission_level': 'regional',
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsFalse(result)
    self.assertEqual(form.region_error, messages.FIELD_MISSING % "a region")

  def test_is_valid_returns_false_when_no_role_or_level_given(self):
    form_content = {
      'role': None,
      'permission_level': None,
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsFalse(result)
    self.assertEqual(form.role_error, messages.FIELD_MISSING % "a role")
    self.assertEqual(form.permission_level_error, messages.FIELD_MISSING % "a level")

  def test_is_valid_returns_true_when_role_at_national_level_given_with_no_locations(self):
    form_content = {
      'role': 'me',
      'permission_level': 'national',
      'region': None,
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsTrue(result)
    self.assertEqual(form.role_error, None)
    self.assertEqual(form.permission_level_error, None)
    self.assertEqual(form.region_error, None)
    self.assertEqual(form.trust_error, None)

  def test_is_valid_returns_true_when_role_at_regional_level_given_with_region_given(self):
    form_content = {
      'role': 'meo',
      'permission_level': 'regional',
      'region': '1',
      'trust': None
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsTrue(result)
    self.assertEqual(form.role_error, None)
    self.assertEqual(form.permission_level_error, None)
    self.assertEqual(form.region_error, None)
    self.assertEqual(form.trust_error, None)

  def test_is_valid_returns_true_when_role_at_trust_level_given_with_trust_given(self):
    form_content = {
      'role': 'sa',
      'permission_level': 'trust',
      'region': None,
      'trust': '1'
    }
    form = PermissionBuilderForm(form_content)
    result = form.is_valid()
    self.assertIsTrue(result)
    self.assertEqual(form.role_error, None)
    self.assertEqual(form.permission_level_error, None)
    self.assertEqual(form.region_error, None)
    self.assertEqual(form.trust_error, None)

  def test_to_dict_returns_form_fields_as_a_dict(self):
    role = 'sa'
    level = 'trust'
    trust = '1'
    form_content = {
      'role': role,
      'permission_level': level,
      'region': None,
      'trust': trust
    }
    form = PermissionBuilderForm(form_content)
    result = form.to_dict()
    self.assertEqual(result['role'], role)
    self.assertEqual(result['permission_level'], level)
    self.assertEqual(result['region'], None)
    self.assertEqual(result['trust'], trust)


class UsersModelsTests(MedExTestCase):


#### User tests

  def test_User_initialisation_correctly_sets_the_fields_from_dict(self):
    user_obj = User(mocks.user_dict)
    self.assertEqual(user_obj.user_id, mocks.user_dict['user_id'])
    self.assertEqual(user_obj.first_name, mocks.user_dict['first_name'])
    self.assertEqual(user_obj.last_name, mocks.user_dict['last_name'])
    self.assertEqual(user_obj.email_address, mocks.user_dict['email_address'])

  def test_User_full_name_method_returns_first_and_last_name_combined(self):
    user_obj = User(mocks.user_dict)
    expected_result = mocks.user_dict['first_name'] + ' ' + mocks.user_dict['last_name']
    self.assertEqual(user_obj.full_name(), expected_result)

  def test_User_str_method_returns_first_and_last_name_combined(self):
    user_obj = User(mocks.user_dict)
    expected_result = mocks.user_dict['first_name'] + ' ' + mocks.user_dict['last_name']
    self.assertEqual(user_obj.__str__(), expected_result)

  def test_User_load_by_email_returns_a_user_object_if_the_email_has_an_account(self):
    response = User.load_by_email('test.user@email.com')
    self.assertEqual(type(response), User)

  def test_User_load_by_email_returns_a_None_object_if_the_email_doesnt_have_an_account(self):
    response = User.load_by_email('a.user@email.com')
    self.assertEqual(response, None)

  @patch('users.request_handler.load_by_id', return_value=mocks.SUCCESSFUL_LOAD_USER)
  def test_User_load_by_id_returns_a_user_object_if_the_id_has_an_account(self, mock_user_load):
    response = User.load_by_id(1)
    self.assertEqual(type(response), User)

  @patch('users.request_handler.load_by_id', return_value=mocks.UNSUCCESSFUL_LOAD_USER)
  def test_User_load_by_id_returns_a_None_object_if_the_id_doesnt_have_an_account(self, mock_user_load):
    response = User.load_by_id(0)
    self.assertEqual(response, None)

from django.conf import settings

from http.cookies import SimpleCookie

from medexCms.test.utils import MedExTestCase
from medexCms.test import mocks

from rest_framework import status

from unittest.mock import patch

import json, uuid

from alerts import utils, messages

from .models import User
from .forms import CreateUserForm

from locations import request_handler


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
  def test_user_creation_endpoint_returns_response_status_from_api_and_the_correct_alert_if_creation_fails(self, mock_auth_validation, mock_user_creation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['message'], messages.ERROR_IN_FORM)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('users.request_handler.create_user', return_value=mocks.SUCCESSFUL_USER_CREATION)
  def test_user_creation_endpoint_returns_redirect_if_creation_succeeds(self, mock_auth_validation, mock_user_creation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/new', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/%s/add_permission' % mocks.CREATED_USER_ID)


#### User lookup tests

  def test_user_lookup_returns_unauthorised_when_called_whilst_not_logged_in(self):
    response = self.client.post('/users/lookup', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_user_lookup_returns_not_found_when_email_not_in_okta(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/lookup', {'email_address': 'test.user@email.com'})
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_user_lookup_returns_success_when_email_is_in_okta(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.post('/users/lookup', {'email_address': 'test.user@nhs.uk'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)


#### Add permission tests

  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  @patch('locations.request_handler.load_trusts_list', return_value=mocks.SUCCESSFUL_LOCATION_LOAD)
  def test_landing_on_the_add_permission_page_loads_the_correct_template(self, mock_auth_validation, mock_location_list):
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

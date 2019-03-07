from django.conf import settings

from http.cookies import SimpleCookie

from requests.models import Response

from rest_framework import status

from unittest.mock import patch

import json, uuid

from medexCms.test.utils import MedExTestCase

from alerts import messages, utils

from .forms import ForgottenPasswordForm
from .utils import redirect_to_landing, redirect_to_login


user_obj = {
  'user_id': '1',
  'first_name': 'Test',
  'last_name': 'User',
  'email_address': 'test.user@nhs.uk',
  'permissions': []
}
SUCCESSFUL_VALIDATE_SESSION = Response()
SUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
SUCCESSFUL_VALIDATE_SESSION._content = json.dumps(user_obj).encode('utf-8')

UNSUCCESSFUL_VALIDATE_SESSION = Response()
UNSUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_401_UNAUTHORIZED
UNSUCCESSFUL_VALIDATE_SESSION._content = json.dumps(None).encode('utf-8')

auth_token = 'f0c2474a-ae57-4e00-b467-cd6caaa4c466'

SUCCESSFUL_SESSION_CREATION = Response()
SUCCESSFUL_SESSION_CREATION.status_code = status.HTTP_200_OK
SUCCESSFUL_SESSION_CREATION._content = json.dumps({'auth_token': auth_token}).encode('utf-8')

UNSUCCESSFUL_SESSION_CREATION = Response()
UNSUCCESSFUL_SESSION_CREATION.status_code = status.HTTP_401_UNAUTHORIZED
UNSUCCESSFUL_SESSION_CREATION._content = json.dumps({'auth_token': None}).encode('utf-8')

class HomeViewsTests(MedExTestCase):

#### Login tests

  def test_landing_on_login_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/login')
    self.assertTemplateUsed(response, 'home/login.html')
    try: 
      self.assertEqual(self.get_context_value(response.context, 'email_address'), None)
      self.assertFalse('Test failed to produce expected key error')
    except KeyError:
      self.assertTrue('Test produced expected key error')


  @patch('users.request_handler.validate_session', return_value=SUCCESSFUL_VALIDATE_SESSION)
  def test_login_returns_redirect_to_landing_page_if_user_logged_in(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/login')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/')


#### Logout tests
  
  def test_logout_returns_redirect_to_login_page_on_submission(self):
    response = self.client.get('/logout')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


#### Index tests
  @patch('users.request_handler.validate_session', return_value=SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_the_landing_page_returns_the_correct_template(self, mock_auth_validation):
    #TODO expand the test once the page is filled out
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'home/index.html')

  def test_landing_on_the_landing_page_redirects_to_login_if_the_user_not_logged_in(self):
    #TODO expand the test once the page is filled out
    response = self.client.get('/')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


#### Settings index tests

  @patch('users.request_handler.validate_session', return_value=SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_logged_in(self, mock_auth_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/settings')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'home/settings_index.html')


  @patch('users.request_handler.validate_session', return_value=UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_not_logged_in(self, mock_auth_validation):
    response = self.client.get('/settings')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


class HomeFormsTests(MedExTestCase):


#### ForgottenPasswordForm tests

  def test_the_form_attributes_are_set_on_init(self):
    email_address = 'test.user@email.com'
    form = ForgottenPasswordForm({'email_address': email_address})
    self.assertEqual(form.email_address, email_address)

  def test_ForgottenPasswordForm_is_valid_returns_true_if_email_address_present(self):
    email_address = 'test.user@email.com'
    form = ForgottenPasswordForm({'email_address': email_address})
    self.assertIsTrue(form.is_valid())

  def test_ForgottenPasswordForm_is_valid_returns_false_if_email_address_not_present(self):
    email_address = ''
    form = ForgottenPasswordForm({'email_address': email_address})
    self.assertIsFalse(form.is_valid())


class HomeUtilsTests(MedExTestCase):

#### Redirect to landing tests

  def test_redirect_to_landing_returns_the_correct_status_code_and_path(self):
    result = redirect_to_landing()
    self.assertEqual(result.status_code, status.HTTP_302_FOUND)
    self.assertEqual(result.url, '/')


#### Redirect to login tests

  def test_redirect_to_login_returns_the_correct_status_code_and_path(self):
    result = redirect_to_login()
    self.assertEqual(result.status_code, status.HTTP_302_FOUND)
    self.assertEqual(result.url, '/login')

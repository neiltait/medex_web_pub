from django.conf import settings
from django.http import HttpRequest

from rest_framework import status

import uuid

from medexCms.test.utils import MedExTestCase

from alerts import messages, utils

from .forms import LoginForm, ForgottenPasswordForm, ForgottenUserIdForm
from .utils import redirect_to_landing, redirect_to_login, check_logged_in

class HomeViewsTests(MedExTestCase):

  #### Login tests

  def test_landing_on_login_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/login')
    self.assertTemplateUsed(response, 'home/login.html')
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 0)
    try: 
      self.assertEqual(self.get_context_value(response.context, 'email_address'), None)
      self.assertFalse('Test failed to produce expected key error')
    except KeyError:
      self.assertTrue('Test produced expected key error')

  def test_login_returns_redirect_to_landing_page_on_sucess(self):
    email_address = 'Matt'
    user_login_credentials = {
      'email_address': email_address,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/')

  def test_login_returns_unauthourised_and_error_message_when_no_password_given(self):
    email_address = 'Matt'
    user_login_credentials = {
      'email_address': email_address,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address.lower())
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_user_id_given(self):
    email_address = ''
    user_login_credentials = {
      'email_address': email_address,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_password_or_user_id_given(self):
    email_address = ''
    user_login_credentials = {
      'email_address': email_address,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_password_given(self):
    email_address = 'Matt'
    user_login_credentials = {
      'email_address': email_address,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address.lower())
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_given(self):
    email_address = 'david'
    user_login_credentials = {
      'email_address': email_address,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_and_password_given(self):
    email_address = 'matt'
    user_login_credentials = {
      'email_address': email_address,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 1)
    self.assertEqual(alert_list[0]['type'], utils.ERROR)
    self.assertEqual(alert_list[0]['message'], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'email_address'), email_address)
    self.assertTemplateUsed(response, 'home/login.html')


  #### Forgotten Password tests

  def test_landing_on_forgotten_password_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/forgotten-password')
    self.assertTemplateUsed(response, 'home/forgotten-password.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)


  def test_forgotten_password_returns_success_and_notification_on_success(self):
    reset_form = {
      'user_id': 'TestUser'
    }
    response = self.client.post('/forgotten-password', reset_form)
    self.assertTemplateUsed(response, 'home/forgotten-password.html')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.INFO)
    self.assertEqual(alerts_list[0]['message'], messages.FORGOTTEN_PASSWORD_SENT)


  def test_forgotten_password_returns_bad_request_and_and_correct_error_on_missing_userid(self):
    reset_form = {
      'user_id': ''
    }
    response = self.client.post('/forgotten-password', reset_form)
    self.assertTemplateUsed(response, 'home/forgotten-password.html')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.ERROR)
    self.assertEqual(alerts_list[0]['message'], messages.MISSING_USER_ID)


  #### Forgotten User ID tests

  def test_landing_on_forgotten_user_id_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/forgotten-userid')
    self.assertTemplateUsed(response, 'home/forgotten-userid.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)

  def test_forgotten_userid_returns_success_and_notification_on_success(self):
    reset_form = {
      'email_address': 'Test.User@email.com'
    }
    response = self.client.post('/forgotten-userid', reset_form)
    self.assertTemplateUsed(response, 'home/forgotten-userid.html')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.INFO)
    self.assertEqual(alerts_list[0]['message'], messages.FORGOTTEN_ID_SENT)

  def test_forgotten_userid_returns_bad_request_and_and_correct_error_on_missing_email(self):
    reset_form = {
      'email_address': ''
    }
    response = self.client.post('/forgotten-userid', reset_form)
    self.assertTemplateUsed(response, 'home/forgotten-userid.html')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.ERROR)
    self.assertEqual(alerts_list[0]['message'], messages.MISSING_EMAIL)


  #### Logout tests
  
  def test_logout_returns_redirect_to_login_page_on_submission(self):
    response = self.client.get('/logout')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


  #### Index tests

  def test_landing_on_the_landing_page_returns_the_correct_template(self):
    #TODO expand the test once the page is filled out
    response = self.client.get('/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'home/index.html')


class HomeFormsTests(MedExTestCase):


  #### LoginForm tests

  def test_passing_in_submissions_sets_the_attributes(self):
    email_address = 'Test User'
    password = 'TestPassword'
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertEqual(form.email_address, email_address.lower())
    self.assertEqual(form.password, password)
    self.assertIsFalse(form.persist_user)

  def test_LoginForm_is_valid_returns_true_if_user_id_and_password_both_present(self):
    email_address = 'Test User'
    password = 'TestPassword'
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsTrue(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_password_is_not_present(self):
    email_address = 'Test User'
    password = ''
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_user_id_is_not_present(self):
    email_address = ''
    password = 'TestPassword'
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_user_id_and_password_both_not_present(self):
    email_address = ''
    password = ''
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())

  #TODO needs to be switched from inital dummy creds to Test creds after OCTA integration
  def test_LoginForm_is_authorised_returns_true_if_user_id_and_password_both_correct(self):
    email_address = 'Matt'
    password = 'Password'
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsTrue(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_password_is_not_correct(self):
    email_address = 'Matt'
    password = ''
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_user_id_is_not_correct(self):
    email_address = ''
    password = 'Password'
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_user_id_and_password_both_not_correct(self):
    email_address = ''
    password = ''
    persist = False
    form = LoginForm({'email_address': email_address, 'password': password, 'persist': persist})
    self.assertIsFalse(form.is_valid())


  #### ForgottenPasswordForm tests

  def test_the_form_attributes_are_set_on_init(self):
    user_id = 'Test User'
    form = ForgottenPasswordForm({'user_id': user_id})
    self.assertEqual(form.user_id, user_id)

  def test_ForgottenPasswordForm_is_valid_returns_true_if_user_id_present(self):
    user_id = 'Test User'
    form = ForgottenPasswordForm({'user_id': user_id})
    self.assertIsTrue(form.is_valid())

  def test_ForgottenPasswordForm_is_valid_returns_false_if_user_id_not_present(self):
    user_id = ''
    form = ForgottenPasswordForm({'user_id': user_id})
    self.assertIsFalse(form.is_valid())


  #### ForgottenUserIdForm tests

  def test_the_form_attributes_are_set_on_init(self):
    email_address = 'Test.User@email.com'
    form = ForgottenUserIdForm({'email_address': email_address})
    self.assertEqual(form.email_address, email_address.lower())

  def test_ForgottenUserIdForm_is_valid_returns_true_if_email_address_present(self):
    email_address = 'Test.User@email.com'
    form = ForgottenUserIdForm({'email_address': email_address})
    self.assertIsTrue(form.is_valid())

  def test_ForgottenUserIdForm_is_valid_returns_false_if_email_address_not_present(self):
    email_address = ''
    form = ForgottenUserIdForm({'email_address': email_address})
    self.assertIsFalse(form.is_valid())

class HomeUtilsTests(MedExTestCase):

  #### Checked logged in tests

  def test_check_logged_in_returns_True_if_the_auth_token_is_valid(self):
    request = HttpRequest()
    request.COOKIES[settings.AUTH_TOKEN_NAME] = uuid.uuid4()
    result = check_logged_in(request)
    self.assertIsTrue(result)


  #### TODO test needs updating and implementing when connected to OKTA
  # def test_check_logged_in_returns_False_if_the_auth_token_is_valid(self):
  #   request = HttpRequest()
  #   request.COOKIES[settings.AUTH_TOKEN_NAME] = uuid.uuid4()
  #   result = check_logged_in(request)
  #   self.assertIsFalse(result)


  def test_check_logged_in_returns_False_if_there_is_no_auth_token(self):
    request = HttpRequest()
    result = check_logged_in(request)
    self.assertIsFalse(result)

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

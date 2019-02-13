from medexCms.test.utils import MedExTestCase

from rest_framework import status

from alerts import messages, utils

from .forms import LoginForm, ForgottenPasswordForm, ForgottenUserIdForm

class HomeViewsTests(MedExTestCase):

  #### Login tests

  def test_landing_on_login_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/login')
    self.assertTemplateUsed(response, 'home/login.html')
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 0)
    try: 
      self.assertEqual(self.get_context_value(response.context, 'user_id'), None)
      self.assertFalse('Test failed to produce expected key error')
    except KeyError:
      self.assertTrue('Test produced expected key error')

  def test_login_returns_redirect_to_landing_page_on_sucess(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/')

  def test_login_returns_unauthourised_and_error_message_when_no_password_given(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_password_or_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.MISSING_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_password_given(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_and_password_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.INVALID_CREDENTIALS)
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
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
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 0)

  def test_forgotten_userid_returns_success_and_notification_on_success(self):
    response = self.client.get('/forgotten-userid')
    self.assertTemplateUsed(response, 'home/forgotten-userid.html')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.INFO)
    self.assertEqual(alerts_list[0]['message'], messages.FORGOTTEN_PASSWORD_SENT)

  def test_forgotten_userid_returns_bad_request_and_and_correct_error_on_missing_email(self):
    response = self.client.get('/forgotten-password')
    self.assertTemplateUsed(response, 'home/forgotten-password.html')
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

  def test_the_form_attributes_are_set_on_init(self):
    user_id = 'Test User'
    password = 'TestPassword'
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertEqual(form.user_id, user_id)
    self.assertEqual(form.password, password)

  def test_LoginForm_is_valid_returns_true_if_user_id_and_password_both_present(self):
    user_id = 'Test User'
    password = 'TestPassword'
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsTrue(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_password_is_not_present(self):
    user_id = 'Test User'
    password = ''
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_user_id_is_not_present(self):
    user_id = ''
    password = 'TestPassword'
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_valid_returns_false_if_user_id_and_password_both_not_present(self):
    user_id = ''
    password = ''
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsFalse(form.is_valid())

  #TODO needs to be switched from inital dummy creds to Test creds after OCTA integration
  def test_LoginForm_is_authorised_returns_true_if_user_id_and_password_both_correct(self):
    user_id = 'Matt'
    password = 'Password'
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsTrue(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_password_is_not_correct(self):
    user_id = 'Matt'
    password = ''
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_user_id_is_not_correct(self):
    user_id = ''
    password = 'Password'
    form = LoginForm({'user_id': user_id, 'password': password})
    self.assertIsFalse(form.is_valid())

  def test_LoginForm_is_authorised_returns_false_if_user_id_and_password_both_not_correct(self):
    user_id = ''
    password = ''
    form = LoginForm({'user_id': user_id, 'password': password})
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
    self.assertEqual(form.email_address, email_address)

  def test_ForgottenUserIdForm_is_valid_returns_true_if_email_address_present(self):
    email_address = 'Test.User@email.com'
    form = ForgottenUserIdForm({'email_address': email_address})
    self.assertIsTrue(form.is_valid())

  def test_ForgottenUserIdForm_is_valid_returns_false_if_email_address_not_present(self):
    email_address = ''
    form = ForgottenUserIdForm({'email_address': email_address})
    self.assertIsFalse(form.is_valid())

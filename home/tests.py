from medexCms.test.utils import MedExTestCase

from .views import login

from errors import messages, status

class HomeViewsTests(MedExTestCase):

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
    self.assertEqual(response.status_code, status.redirect())
    self.assertEqual(response.url, '/')

  def test_login_returns_unauthourised_and_error_message_when_no_password_given(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_password_or_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_password_given(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_and_password_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = self.get_context_value(response.context, 'errors')
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(self.get_context_value(response.context, 'user_id'), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

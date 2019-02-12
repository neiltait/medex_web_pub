from medexCms.test.utils import MedExTestCase

from .views import login

from errors import messages, status

def get_error_list(response):
  return response.context['errors']

def get_user_id(response):
  return response.context['user_id']

class HomeViewsTests(MedExTestCase):

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
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_no_password_or_user_id_given(self):
    user_id = ''
    user_login_credentials = {
      'user_id': user_id,
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.missing_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_password_given(self):
    user_id = 'Matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_and_password_given(self):
    user_id = 'matt'
    user_login_credentials = {
      'user_id': user_id,
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, status.unauthorised())
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
    self.assertEqual(error_list[0], messages.invalid_credentials())
    self.assertEqual(get_user_id(response), user_id)
    self.assertTemplateUsed(response, 'home/login.html')

from medexCms.test.utils import MedExTestCase

from rest_framework import status

class UsersViewsTest(MedExTestCase):


  #### Lookup tests

  def test_landing_on_the_user_lookup_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/users/lookup')
    self.assertTemplateUsed(response, 'users/lookup.html')
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 0)

  def test_user_lookup_returns_redirect_to_manage_user_page_if_user_found(self):
    user_email = {
      'email_address': 'user.test@email.com',
    }
    response = self.client.post('/users/lookup', user_email)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/TestUser') # TODO need to swap 'TestUser' for the user id for the found user

  def test_user_lookup_returns_bad_request_and_correct_error_on_missing_email(self):
    user_email = {
      'email_address': ''
    }
    response = self.client.post('/users/lookup', user_email)
    self.assertTemplateUsed(response, 'users/lookup.html')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.ERROR)
    self.assertEqual(alerts_list[0]['message'], messages.MISSING_EMAIL)

class UsersFormsTests(MedExTestCase):


  #### LookupForm tests

  def test_the_form_attributes_are_set_on_init(self):
    email = 'Test.User@email.com'
    form = LoginForm({ 'email_address': email })
    self.assertEqual(form.email_address, email)

  def test_LookupForm_is_valid_returns_true_if_email_is_present(self):
    email = 'Test.User@email.com'
    form = LoginForm({ 'email_address': email })
    self.assertIsTrue(form.is_valid())

  def test_LookupForm_is_valid_returns_false_if_email_is_not_present(self):
    email = ''
    form = LoginForm({ 'email_address': email })
    self.assertIsFalse(form.is_valid())

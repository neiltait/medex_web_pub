from medexCms.test.utils import MedExTestCase

from rest_framework import status

from alerts import utils, messages

from .forms import UserLookupForm
from .models import User

user_dict = {
  'user_id': 'TestUser',
  'first_name': 'Test',
  'last_name': 'User',
  'email_address': 'test.user@email.com',
  'role': 'MEO',
  'permissions': [],
}

class UsersViewsTest(MedExTestCase):


  #### Lookup tests

  def test_landing_on_the_user_lookup_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/users/lookup')
    self.assertTemplateUsed(response, 'users/lookup.html')
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 0)

  def test_user_lookup_returns_redirect_to_manage_user_page_if_user_exists(self):
    user_email = {
      'email_address': user_dict['email_address'],
    }
    response = self.client.post('/users/lookup', user_email)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/manage/' + user_dict['user_id'])

  def test_user_lookup_returns_redirect_to_new_user_page_if_user_doesnt_exist(self):
    user_email = {
      'email_address': 'another.user@email.com',
    }
    response = self.client.post('/users/lookup', user_email)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/users/new')

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


  #### User manage tests

  def test_landing_on_the_user_manage_page_loads_the_correct_template_with_the_users_details_present_if_they_exist(self):
    user_id = 'TestUser'
    response = self.client.get('/users/manage/' + user_id)
    self.assertTemplateUsed(response, 'users/manage.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)
    managed_user = self.get_context_value(response.context, 'managed_user')
    self.assertEqual(managed_user.user_id, user_id)

  def test_landing_on_the_user_manage_page_loads_the_correct_template_with_no_users_details_present_if_they_dont_exist(self):
    user_id = 'AUser'
    response = self.client.get('/users/manage/' + user_id)
    self.assertTemplateUsed(response, 'users/manage.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 1)
    self.assertEqual(alerts_list[0]['type'], utils.ERROR)
    self.assertEqual(alerts_list[0]['message'], messages.OBJECT_NOT_FOUND % 'user')
    managed_user = self.get_context_value(response.context, 'managed_user')
    self.assertEqual(managed_user, None)


  #### User create tests

  def test_landing_on_the_user_creation_page_loads_the_correct_template(self):
    response = self.client.get('/users/new')
    self.assertTemplateUsed(response, 'users/new.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)


class UsersFormsTests(MedExTestCase):


  #### UserLookupForm tests

  def test_the_form_attributes_are_set_on_init(self):
    email = 'Test.User@email.com'
    form = UserLookupForm({ 'email_address': email })
    self.assertEqual(form.email_address, email.lower())

  def test_UserLookupForm_is_valid_returns_true_if_email_is_present(self):
    email = 'Test.User@email.com'
    form = UserLookupForm({ 'email_address': email })
    self.assertIsTrue(form.is_valid())

  def test_UserLookupForm_is_valid_returns_false_if_email_is_not_present(self):
    email = ''
    form = UserLookupForm({ 'email_address': email })
    self.assertIsFalse(form.is_valid())


class UsersModelsTests(MedExTestCase):


  #### User tests

  def test_User_initialisation_correctly_sets_the_fields_from_dict(self):
    user_obj = User(user_dict)
    self.assertEqual(user_obj.user_id, user_dict['user_id'])
    self.assertEqual(user_obj.first_name, user_dict['first_name'])
    self.assertEqual(user_obj.last_name, user_dict['last_name'])
    self.assertEqual(user_obj.email_address, user_dict['email_address'])
    self.assertEqual(user_obj.permissions, user_dict['permissions'])

  def test_User_full_name_method_returns_first_and_last_name_combined(self):
    user_obj = User(user_dict)
    expected_result = user_dict['first_name'] + ' ' + user_dict['last_name']
    self.assertEqual(user_obj.full_name(), expected_result)

  def test_User_str_method_returns_first_and_last_name_combined(self):
    user_obj = User(user_dict)
    expected_result = user_dict['first_name'] + ' ' + user_dict['last_name']
    self.assertEqual(user_obj.__str__(), expected_result)

  def test_User_load_by_email_returns_a_user_object_if_the_email_has_an_account(self):
    response = User.load_by_email('test.user@email.com')
    self.assertEqual(type(response), User)

  def test_User_load_by_email_returns_a_None_object_if_the_email_doesnt_have_an_account(self):
    response = User.load_by_email('a.user@email.com')
    self.assertEqual(response, None)

  def test_User_load_by_user_id_returns_a_user_object_if_the_id_has_an_account(self):
    response = User.load_by_user_id('TestUser')
    self.assertEqual(type(response), User)

  def test_User_load_by_user_id_returns_a_None_object_if_the_id_doesnt_have_an_account(self):
    response = User.load_by_user_id('AUser')
    self.assertEqual(response, None)

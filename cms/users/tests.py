from medexCms.test.utils import MedExTestCase

from rest_framework import status

from alerts import utils, messages

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


  #### User create tests

  def test_landing_on_the_user_creation_page_loads_the_correct_template(self):
    response = self.client.get('/users/new')
    self.assertTemplateUsed(response, 'users/new.html')
    alerts_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alerts_list), 0)


# class UsersFormsTests(MedExTestCase):



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

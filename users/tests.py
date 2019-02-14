from medexCms.test.utils import MedExTestCase

class UsersViewsTest(MedExTestCase):

  def test_landing_on_the_user_lookup_page_loads_the_correct_template_with_empty_context(self):
    response = self.client.get('/users/lookup')
    self.assertTemplateUsed(response, 'users/lookup.html')
    alert_list = self.get_context_value(response.context, 'alerts')
    self.assertEqual(len(alert_list), 0)

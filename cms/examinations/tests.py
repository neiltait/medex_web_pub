from django.conf import settings

from http.cookies import SimpleCookie

from rest_framework import status

import uuid

from medexCms.test.utils import MedExTestCase

class ExaminationsViewsTests(MedExTestCase):

  #### Create case tests

  def test_landing_on_create_case_page_loads_the_correct_template(self):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'examinations/create.html')


  def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self):
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')

from django.conf import settings

from http.cookies import SimpleCookie

from rest_framework import status

from unittest.mock import patch

import json

from medexCms.test import mocks
from medexCms.test.utils import MedExTestCase


class ExaminationsViewsTests(MedExTestCase):

#### Create case tests
  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_create_case_page_loads_the_correct_template(self, mock_user_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: json.dumps(mocks.AUTH_TOKEN)})
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'examinations/create.html')


  @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self, mock_user_validation):
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


#### Edit case tests

  @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_edit_page_when_not_logged_in_redirects_to_login(self, mock_user_validation):
    response = self.client.get('/cases/%s' % mocks.CREATED_EXAMINATION_ID)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')


  @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_edit_page_when_logged_in_loads_the_correct_template(self, mock_user_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: json.dumps(mocks.AUTH_TOKEN)})
    response = self.client.get('/cases/%s' % mocks.CREATED_EXAMINATION_ID)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'examinations/edit.html')

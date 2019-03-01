from django.conf import settings

from http.cookies import SimpleCookie

from requests.models import Response

from rest_framework import status

from unittest.mock import patch

import json, uuid

from medexCms.test.utils import MedExTestCase

user_obj = {
  'user_id': '1',
  'first_name': 'Test',
  'last_name': 'User',
  'email_address': 'test.user@nhs.uk',
  'permissions': []
}
SUCCESSFUL_VALIDATE_SESSION = Response()
SUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
SUCCESSFUL_VALIDATE_SESSION._content = json.dumps(user_obj).encode('utf-8')

UNSUCCESSFUL_VALIDATE_SESSION = Response()
UNSUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_401_UNAUTHORIZED
UNSUCCESSFUL_VALIDATE_SESSION._content = json.dumps(None).encode('utf-8')


class ExaminationsViewsTests(MedExTestCase):

  #### Create case tests
  @patch('users.request_handler.validate_session', return_value=SUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_create_case_page_loads_the_correct_template(self, mock_user_validation):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'examinations/create.html')


  @patch('users.request_handler.validate_session', return_value=UNSUCCESSFUL_VALIDATE_SESSION)
  def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self, mock_user_validation):
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')

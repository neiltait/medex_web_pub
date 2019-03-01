import json
from unittest.mock import patch

from django.conf import settings

from http.cookies import SimpleCookie

from requests import Response
from rest_framework import status

import uuid

from medexCms.test.utils import MedExTestCase

locations = [{
    'id': '1',
    'name': 'Barnet Hospital',
  }, {
    'id': '2',
    'name': 'Sheffield Hospital',
  }, {
    'id': '3',
    'name': 'Gloucester Hospital',
  }]
GET_LOCATIONS_RESPONSE = Response()
GET_LOCATIONS_RESPONSE.status_code = status.HTTP_200_OK
GET_LOCATIONS_RESPONSE._content = json.dumps(locations).encode('utf-8')

offices = [{
        'id': '1',
        'name': 'Barnet Hospital ME Office',
    }, {
        'id': '2',
        'name': 'Sheffield Hospital ME Office',
    }, {
        'id': '3',
        'name': 'Gloucester Hospital ME Office',
    }]
GET_ME_OFFICES_RESPONSE = Response()
GET_ME_OFFICES_RESPONSE.status_code = status.HTTP_200_OK
GET_ME_OFFICES_RESPONSE._content = json.dumps(offices).encode('utf-8')

class ExaminationsViewsTests(MedExTestCase):

  #### Create case tests

  @patch('examinations.request_handler.get_locations_list', return_value=locations)
  @patch('examinations.request_handler.get_me_offices_list', return_value=offices)
  def test_landing_on_create_case_page_loads_the_correct_template(self, mock_locations, mock_me_offices):
    self.client.cookies = SimpleCookie({settings.AUTH_TOKEN_NAME: uuid.uuid4()})
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'examinations/create.html')


  def test_landing_on_create_page_when_not_logged_in_redirects_to_login(self):
    response = self.client.get('/cases/create')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertEqual(response.url, '/login')

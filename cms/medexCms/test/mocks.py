from requests.models import Response

from rest_framework import status

import json

empty_user = {
  'user_id': None,
  'first_name': None,
  'last_name': None,
  'email_address': None,
}

user_dict = {
  'user_id': '1',
  'first_name': 'Test',
  'last_name': 'User',
  'email_address': 'test.user@email.com',
}

SUCCESSFUL_VALIDATE_SESSION = Response()
SUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
SUCCESSFUL_VALIDATE_SESSION._content = json.dumps(user_dict).encode('utf-8')

UNSUCCESSFUL_VALIDATE_SESSION = Response()
UNSUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
UNSUCCESSFUL_VALIDATE_SESSION._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_LOCATION_LOAD = [
    {
      'id': 1,
      'name': 'Gloucester NHS Trust',
    },
    {
      'id': 2,
      'name': 'Sheffield NHS Trust',
    },
    {
      'id': 3,
      'name': 'Barts NHS Trust',
    }
  ]

CREATED_USER_ID = 1
SUCCESSFUL_USER_CREATION = Response()
SUCCESSFUL_USER_CREATION.status_code = status.HTTP_200_OK
SUCCESSFUL_USER_CREATION._content = json.dumps({'id': CREATED_USER_ID}).encode('utf-8')

UNSUCCESSFUL_USER_CREATION = Response()
UNSUCCESSFUL_USER_CREATION.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_USER_CREATION._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_LOAD_USER = Response()
SUCCESSFUL_LOAD_USER.status_code = status.HTTP_200_OK
SUCCESSFUL_LOAD_USER._content = json.dumps(user_dict).encode('utf-8')

UNSUCCESSFUL_LOAD_USER = Response()
UNSUCCESSFUL_LOAD_USER.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_LOAD_USER._content = json.dumps(empty_user).encode('utf-8')

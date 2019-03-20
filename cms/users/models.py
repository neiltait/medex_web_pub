import logging

from django.conf import settings

from rest_framework import status

from examinations.models import ExaminationOverview
from examinations import request_handler as examination_request_handler

from home import request_handler as home_request_handler

from permissions import request_handler as permissions_request_handler
from permissions.models import Permission

from . import request_handler


logger = logging.getLogger(__name__)


class User:

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.user_id = obj_dict['userId']
            self.first_name = obj_dict['firstName']
            self.last_name = obj_dict['lastName']
            self.email_address = obj_dict['email']
        self.examinations = []
        self.permissions = []

    @classmethod
    def initialise_with_token(cls, request):
        user = User()

        try:
            user.auth_token = request.COOKIES[settings.AUTH_TOKEN_NAME]
            user.id_token = request.COOKIES[settings.ID_TOKEN_NAME]
        except KeyError:
            user.auth_token = None
            user.id_token = None

        return user

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def check_logged_in(self):
        if self.auth_token:
            response = request_handler.validate_session(self.auth_token)

            authenticated = response.status_code == status.HTTP_200_OK

            if authenticated:
                response_data = response.json()
                self.user_id = response_data['user_id']
                self.first_name = response_data['first_name']
                self.last_name = response_data['last_name']
                self.email_address = response_data['email_address']
                self.load_permissions()

            return authenticated
        else:
            return False

    def examinations_count(self):
        return len(self.examinations)

    def logout(self):
        if self.auth_token and self.id_token:
            home_request_handler.end_session(self.id_token)

    @classmethod
    def load_by_email(cls, email_address):
        # r = requests.post(settings.API_URL + '/users/find_by_email', data = {'email_address': email_address})
        # TODO need to tie into the api when possible
        if email_address == 'test.user@email.com':
            return User({
                'user_id': 'TestUser',
                'first_name': 'Test',
                'last_name': 'User',
                'email_address': 'test.user@email.com',
                'permissions': [],
            })
        else:
            return None

    @classmethod
    def load_by_id(cls, user_id, auth_token):
        response = request_handler.load_by_id(user_id, auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            return User(response.json())
        else:
            return None

    def load_permissions(self):
        response = permissions_request_handler.load_permissions_for_user(self.user_id, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            for permission in response.json()['permissions']:
                self.permissions.append(Permission(permission))
        else:
            logger.error(response.status_code)

    def load_examinations(self):
        query_params = {
            "locationId": None,
            "userId": self.user_id,
            "caseStatus": None,
            "orderBy": "Urgency",
            "pageSize": 20,
            "pageNumber": 1
        }

        response = examination_request_handler.load_examinations_index(query_params, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            for examination in response.json()['examinations']:
                self.examinations.append(ExaminationOverview(examination))
        else:
            logger.error(response.status_code)

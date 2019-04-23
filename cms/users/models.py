import json
import logging

from django.conf import settings

from rest_framework import status

from examinations.models import ExaminationOverview
from examinations import request_handler as examination_request_handler

from home import request_handler as home_request_handler
from home.models import IndexOverview

from locations import request_handler as location_request_handler
from locations.models import Location

from permissions import request_handler as permissions_request_handler
from permissions.models import Permission

from . import request_handler

logger = logging.getLogger(__name__)


class User:
    ME_ROLE_TYPE = 'MedicalExaminer'
    MEO_ROLE_TYPE = 'MedicalExaminerOfficer'

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.user_id = obj_dict['userId']
            self.first_name = obj_dict['firstName']
            self.last_name = obj_dict['lastName']
            self.email_address = obj_dict['email']
        self.auth_token = None
        self.id_token = None
        self.index_overview = None
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

    @property
    def role_type(self):
        # TODO This is changed to force the system into accepting us as an ME.
        #  Remove after development of ME only features
        #return self.ME_ROLE_TYPE
        return self.permissions[0].role_type

    def check_logged_in(self):
        if self.auth_token:
            response = request_handler.validate_session(self.auth_token)

            authenticated = response.status_code == status.HTTP_200_OK

            if authenticated:
                response_data = response.json()
                self.user_id = response_data['userId']
                self.first_name = response_data['firstName']
                self.last_name = response_data['lastName']
                self.email_address = response_data['emailAddress']
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

    def load_examinations(self, location='', person=''):
        if person:
            user = person
        else:
            user = self.user_id if self.role_type == self.ME_ROLE_TYPE else ''
        query_params = {
            "LocationId": location,
            "UserId": user,
            "CaseStatus": '',
            "OrderBy": "CaseCreated",
            "OpenCases": True,
            "PageSize": 20,
            "PageNumber": 1
        }

        response = examination_request_handler.load_examinations_index(query_params, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            self.index_overview = IndexOverview(location, response.json())
            for examination in response.json()['examinations']:
                self.examinations.append(ExaminationOverview(examination))
        else:
            logger.error(response.status_code)

    def load_closed_examinations(self, location='', person=''):
        if person:
            user = person
        else:
            user = ''

        query_params = {
            "LocationId": location,
            "UserId": user,
            "CaseStatus": '',
            "OrderBy": "CaseCreated",
            "OpenCases": False,
            "PageSize": 20,
            "PageNumber": 1
        }

        response = examination_request_handler.load_examinations_index(query_params, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            self.index_overview = IndexOverview(location, response.json())
            for examination in response.json()['examinations']:
                self.examinations.append(ExaminationOverview(examination))
        else:
            logger.error(response.status_code)

    def get_permitted_locations(self):
        permitted_locations = []
        location_data = location_request_handler.get_permitted_locations_list(self.auth_token)
        for location in location_data:
            permitted_locations.append(Location().set_values(location))
        return permitted_locations

    def get_forms_for_role(self):
        if self.role_type == self.MEO_ROLE_TYPE:
            return [
                {
                    'id': 'admin-notes',
                    'name': 'Latest hospital admission details'
                },
                {
                    'id': 'history-notes',
                    'name': 'Medical and social history notes'
                },
                {
                    'id': 'meo-summary',
                    'name': 'MEO summary'
                },
                {
                    'id': 'other',
                    'name': 'Other case info'
                }
            ]
        elif self.role_type == self.ME_ROLE_TYPE:
            return [
                {
                    'id': 'pre-scrutiny',
                    'name': 'ME pre-scrutiny'
                },
                {
                    'id': 'qap-discussion',
                    'name': 'QAP discussion'
                },
                {
                    'id': 'bereaved-discussion',
                    'name': 'Bereaved/representative discussion'
                },
                {
                    'id': 'other',
                    'name': 'Other case info'
                }
            ]
        else:
            logger.error('Unknown role type')

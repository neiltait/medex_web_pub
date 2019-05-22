import json

from django.conf import settings

from rest_framework import status

from errors.utils import log_api_error, log_internal_error
from examinations.models import ExaminationOverview, ExaminationEventList, CaseEvent
from examinations import request_handler as examination_request_handler

from home import request_handler as home_request_handler
from home.models import IndexOverview

from locations.models import Location

from permissions import request_handler as permissions_request_handler
from permissions.models import Permission, PermittedActions

from . import request_handler


class User:
    ME_ROLE_TYPE = 'MedicalExaminer'
    MEO_ROLE_TYPE = 'MedicalExaminerOfficer'

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.user_id = obj_dict.get('userId')
            self.first_name = obj_dict.get('firstName')
            self.last_name = obj_dict.get('lastName')
            self.email_address = obj_dict.get('email')
            self.role = obj_dict.get('role')
            self.permitted_actions = PermittedActions(obj_dict.get('permissions'))
        self.auth_token = None
        self.id_token = None
        self.index_overview = None
        self.examinations = []
        self.permissions = []

    def __str__(self):
        return self.full_name()

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

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def check_logged_in(self):
        if self.auth_token:
            response = request_handler.validate_session(self.auth_token)

            authenticated = response.status_code == status.HTTP_200_OK

            if authenticated:
                response_data = response.json()
                self.user_id = response_data.get('userId')
                self.first_name = response_data.get('firstName')
                self.last_name = response_data.get('lastName')
                self.email_address = response_data.get('emailAddress')
                self.role = response_data.get('role')
                self.permitted_actions = PermittedActions(response_data.get('permissions'))

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

    @classmethod
    def create(cls, submission, auth_token):
        return request_handler.create_user(json.dumps(submission), auth_token)

    def add_permission(self, form, auth_token):
        return Permission.create(form.to_dict(self.user_id), self.user_id, auth_token)

    def load_permissions(self):
        response = permissions_request_handler.load_permissions_for_user(self.user_id, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            for permission in response.json()['permissions']:
                self.permissions.append(Permission(permission))
        else:
            log_api_error('permissions load', response.text)

    def load_examinations(self, page_size, page_number, location, person):
        query_params = {
            "LocationId": location,
            "UserId": person,
            "CaseStatus": '',
            "OrderBy": "CaseCreated",
            "OpenCases": True,
            "PageSize": page_size,
            "PageNumber": page_number
        }

        response = examination_request_handler.load_examinations_index(query_params, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            self.index_overview = IndexOverview(location, response.json(), page_size, page_number)
            for examination in response.json().get('examinations'):
                examination['open'] = True
                self.examinations.append(ExaminationOverview(examination))
        else:
            log_api_error('permissions load', response.text)

    def load_closed_examinations(self, page_size, page_number, location, person):
        query_params = {
            "LocationId": location,
            "UserId": person,
            "CaseStatus": '',
            "OrderBy": "CaseCreated",
            "OpenCases": False,
            "PageSize": page_size,
            "PageNumber": page_number
        }

        response = examination_request_handler.load_examinations_index(query_params, self.auth_token)

        success = response.status_code == status.HTTP_200_OK

        if success:
            self.index_overview = IndexOverview(location, response.json(), page_size, page_number)
            for examination in response.json()['examinations']:
                examination['open'] = False
                self.examinations.append(ExaminationOverview(examination))
        else:
            log_api_error('case load', response.text)

    def get_permitted_locations(self):
        return Location.get_permitted_locations_for_user(self.auth_token)

    def get_permitted_trusts(self):
        return Location.load_trusts_list_for_user(self.auth_token)

    def get_permitted_regions(self):
        return Location.load_region_list_for_user(self.auth_token)

    def get_permitted_me_offices(self):
        return Location.load_me_offices(self.auth_token)

    def default_filter_user(self):
        return self.user_id if self.is_me() else None

    def default_filter_options(self):
        return {
            'location': None,
            'person': self.default_filter_user()
        }

    def is_me(self):
        return self.role == self.ME_ROLE_TYPE

    def is_meo(self):
        return self.role == self.MEO_ROLE_TYPE

    def get_forms_for_role(self, case_breakdown):

        existing_events = [event.event_type for event in case_breakdown.event_list.events if event.published]
        if self.is_meo():
            return [
                {
                    'id': 'admin-notes',
                    'name': 'Latest hospital admission details',
                    'enabled': 'false' if CaseEvent.ADMISSION_NOTES_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'medical-history',
                    'name': 'Medical and social history notes',
                    'enabled': 'false' if CaseEvent.MEDICAL_HISTORY_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'meo-summary',
                    'name': 'MEO summary',
                    'enabled': 'false' if CaseEvent.MEO_SUMMARY_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'other',
                    'name': 'Other case info',
                    'enabled': 'true'
                }
            ]
        elif self.is_me():
            return [
                {
                    'id': 'pre-scrutiny',
                    'name': 'ME pre-scrutiny',
                    'enabled': 'false' if CaseEvent.PRE_SCRUTINY_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'qap-discussion',
                    'name': 'QAP discussion',
                    'enabled': 'false' if CaseEvent.QAP_DISCUSSION_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'bereaved-discussion',
                    'name': 'Bereaved/representative discussion',
                    'enabled': 'false' if CaseEvent.BEREAVED_DISCUSSION_EVENT_TYPE in existing_events else 'true'
                },
                {
                    'id': 'other',
                    'name': 'Other case info',
                    'enabled': 'true'
                }
            ]
        else:
            log_internal_error('(User) get_form_for_role', 'Unknown role type')

    def editable_event_types(self):
        if self.is_meo():
            return [
                'admission-notes',
                'medical-history',
                'meo-summary',
                'other',
            ]
        elif self.is_me():
            return [
                'pre-scrutiny',
                'qap-discussion',
                'bereaved-discussion',
                'other',
            ]
        else:
            log_internal_error('(User) get_form_for_role', 'Unknown role type')
            return []

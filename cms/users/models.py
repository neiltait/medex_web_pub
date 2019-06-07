import json

from django.conf import settings

from rest_framework import status

from errors.utils import log_api_error, log_internal_error
from examinations.models import ExaminationOverview, CaseEvent
from examinations import request_handler as examination_request_handler

from home import request_handler as home_request_handler
from home.models import IndexOverview

from locations.models import Location

from medexCms.api import enums

from permissions import request_handler as permissions_request_handler
from permissions.models import Permission, PermittedActions

from . import request_handler


class User:
    ME_ROLE_TYPE = 'MedicalExaminer'
    MEO_ROLE_TYPE = 'MedicalExaminerOfficer'
    SERVICE_ADMIN_ROLE_TYPE = 'ServiceAdministrator'
    SERVICE_OWNER_ROLE_TYPE = 'ServiceOwner'

    def __init__(self, obj_dict=None):
        self.auth_token = None
        self.id_token = None
        self.index_overview = None
        self.examinations = []
        self.permissions = []
        if obj_dict:
            self.user_id = obj_dict.get('userId')
            self.first_name = obj_dict.get('firstName')
            self.last_name = obj_dict.get('lastName')
            self.email_address = obj_dict.get('email')
            self.roles = obj_dict.get('role')
            if type(obj_dict.get('permissions')) == list:
                self.permissions = obj_dict.get('permissions')
            else:
                self.permitted_actions = PermittedActions(obj_dict.get('permissions'))

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
                self.roles = response_data.get('role')
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
        return self.user_id if self.is_me() and not self.is_meo() else None

    def default_filter_options(self):
        return {
            'location': None,
            'person': self.default_filter_user()
        }

    def is_me(self):
        return self.ME_ROLE_TYPE in self.roles

    def is_meo(self):
        return self.MEO_ROLE_TYPE in self.roles

    def is_service_admin(self):
        return self.SERVICE_ADMIN_ROLE_TYPE in self.roles

    def is_service_owner(self):
        return self.SERVICE_OWNER_ROLE_TYPE in self.roles

    def display_role(self):
        if self.is_me():
            return enums.role_types.ME
        elif self.is_meo():
            return enums.role_types.MEO
        elif self.is_service_admin():
            return enums.role_types.SERVICE_ADMIN
        elif self.is_service_owner():
            return enums.role_types.SERVICE_OWNER
        else:
            log_internal_error('user display role', 'Unknown role type or no role type present for user')
            return ''

    def get_forms_for_role(self, case_breakdown):
        existing_events = [event.event_type for event in case_breakdown.event_list.events if event.published]
        forms_list = []
        if self.permitted_actions.permitted_forms.admissionEvent:
            forms_list.append({
                    'id': 'admin-notes',
                    'name': 'Latest hospital admission details',
                    'enabled': self.check_form_type_accessible(CaseEvent.ADMISSION_NOTES_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_latest_admission_draft())
                })
        if self.permitted_actions.permitted_forms.medicalHistoryEvent:
            forms_list.append({
                'id': 'medical-history',
                'name': 'Medical and social history notes',
                'enabled': self.check_form_type_accessible(CaseEvent.MEDICAL_HISTORY_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_medical_history_draft())
            })
        if self.permitted_actions.permitted_forms.meoSummaryEvent:
            forms_list.append({
                'id': 'meo-summary',
                'name': 'MEO summary',
                'enabled': self.check_form_type_accessible(CaseEvent.MEO_SUMMARY_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_meo_summary_draft())
            })
        if self.permitted_actions.permitted_forms.preScrutinyEvent:
            forms_list.append({
                'id': 'pre-scrutiny',
                'name': 'ME pre-scrutiny',
                'enabled': self.check_form_type_accessible(CaseEvent.PRE_SCRUTINY_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_me_scrutiny_draft())
            })
        if self.permitted_actions.permitted_forms.qapDiscussionEvent:
            forms_list.append({
                'id': 'qap-discussion',
                'name': 'QAP discussion',
                'enabled': self.check_form_type_accessible(CaseEvent.QAP_DISCUSSION_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_qap_discussion_draft())
            })
        if self.permitted_actions.permitted_forms.bereavedDiscussionEvent:
            forms_list.append({
                'id': 'bereaved-discussion',
                'name': 'Bereaved/representative discussion',
                'enabled': self.check_form_type_accessible(CaseEvent.BEREAVED_DISCUSSION_EVENT_TYPE, existing_events,
                                                           case_breakdown.event_list.get_bereaved_discussion_draft())
            })
        if self.permitted_actions.permitted_forms.otherEvent:
            forms_list.append({
                'id': 'other',
                'name': 'Other case info',
                'enabled': 'true'
            })
        return forms_list

    def check_form_type_accessible(self, event_type, events, draft):
        return 'false' if event_type in events and draft is None else 'true'

    def editable_event_types(self):
        forms_list = []
        if self.permitted_actions.permitted_forms.admissionEvent:
            forms_list.append('admission-notes')
        if self.permitted_actions.permitted_forms.medicalHistoryEvent:
            forms_list.append('medical-history')
        if self.permitted_actions.permitted_forms.meoSummaryEvent:
            forms_list.append('meo-summary')
        if self.permitted_actions.permitted_forms.preScrutinyEvent:
            forms_list.append('pre-scrutiny')
        if self.permitted_actions.permitted_forms.qapDiscussionEvent:
            forms_list.append('qap-discussion')
        if self.permitted_actions.permitted_forms.bereavedDiscussionEvent:
            forms_list.append('bereaved-discussion')
        if self.permitted_actions.permitted_forms.otherEvent:
            forms_list.append('other')
        return forms_list

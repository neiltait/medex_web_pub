import json

from examinations.constants import get_display_short_user_role, get_display_user_role
from medexCms.utils import fallback_to
from permissions import request_handler


class Permission:
    ROLES = {
        '0': 'MedicalExaminerOfficer',
        '1': 'MedicalExaminer',
        '2': 'ServiceAdministrator',
        '3': 'ServiceOwner',
    }

    def __init__(self, obj_dict):
        self.permission_id = obj_dict.get("permissionId")
        self.user_id = obj_dict.get("userId")
        self.location_id = obj_dict.get("locationId")
        self.location_name = fallback_to(obj_dict.get("locationName"), self.location_id)

        # TODO: Revert to commented code when API team have updated Permissions endpoint
        # self.user_role = obj_dict.get("userRole")
        role = obj_dict.get("userRole")
        self.user_role = self.ROLES.get(str(role)) if isinstance(role, int) else role

    @property
    def role_type(self):
        return self.user_role

    @classmethod
    def create(cls, submission, user_id, auth_token):
        return request_handler.create_permission(json.dumps(submission), user_id, auth_token)

    @classmethod
    def delete(cls, user_id, permission_id, auth_token):
        return request_handler.delete_permission(permission_id, user_id, auth_token)

    def user_display_role(self):
        return get_display_user_role(self.user_role)

    @classmethod
    def update(cls, location_id, user_role, user_id, auth_token):
        return request_handler.update_permission(json.dumps({"locationId": location_id, "userRole": user_role}),
                                                 user_id, auth_token)

    @classmethod
    def load_by_id(cls, user_id, permission_id, auth_token):
        response = request_handler.load_single_permission_for_user(user_id, permission_id, auth_token)
        return Permission(obj_dict=response.json())


class PermittedActions:

    def __init__(self, obj_dict):
        self.can_get_users = obj_dict.get("GetUsers") if obj_dict else False
        self.can_get_user = obj_dict.get("GetUser") if obj_dict else False
        self.can_invite_user = obj_dict.get("InviteUser") if obj_dict else False
        self.can_suspend_user = obj_dict.get("SuspendUser") if obj_dict else False
        self.can_enable_user = obj_dict.get("EnableUser") if obj_dict else False
        self.can_delete_user = obj_dict.get("DeleteUser") if obj_dict else False
        self.can_update_user = obj_dict.get("UpdateUser") if obj_dict else False
        self.can_get_user_permissions = obj_dict.get("GetUserPermissions") if obj_dict else False
        self.can_get_user_permission = obj_dict.get("GetUserPermission") if obj_dict else False
        self.can_create_user_permission = obj_dict.get("CreateUserPermission") if obj_dict else False
        self.can_update_user_permission = obj_dict.get("UpdateUserPermission") if obj_dict else False
        self.can_delete_user_permission = obj_dict.get("DeleteUserPermission") if obj_dict else False
        self.can_get_locations = obj_dict.get("GetLocations") if obj_dict else False
        self.can_get_location = obj_dict.get("GetLocation") if obj_dict else False
        self.can_get_examinations = obj_dict.get("GetExaminations") if obj_dict else False
        self.can_get_examination = obj_dict.get("GetExamination") if obj_dict else False
        self.can_create_examination = obj_dict.get("CreateExamination") if obj_dict else False
        self.can_assign_examination_to_medical_examiner = obj_dict.get("AssignExaminationToMedicalExaminer") \
            if obj_dict else False
        self.can_update_examination = obj_dict.get("UpdateExamination") if obj_dict else False
        self.can_update_examination_state = obj_dict.get("UpdateExaminationState") if obj_dict else False
        self.can_add_event_to_examination = obj_dict.get("AddEventToExamination") if obj_dict else False
        self.can_get_examination_events = obj_dict.get("GetExaminationEvents") if obj_dict else False
        self.can_get_examination_event = obj_dict.get("GetExaminationEvent") if obj_dict else False
        self.can_get_profile = obj_dict.get("GetProfile") if obj_dict else False
        self.can_update_profile = obj_dict.get("UpdateProfile") if obj_dict else False
        self.can_get_profile_permissions = obj_dict.get("GetProfilePermissions") if obj_dict else False
        self.permitted_forms = PermittedForms(obj_dict)

    def can_access_settings_index(self):
        return self.can_get_users


class PermittedForms:

    def __init__(self, obj_dict):
        self.bereavedDiscussionEvent = obj_dict.get("BereavedDiscussionEvent") if obj_dict else False
        self.meoSummaryEvent = obj_dict.get("MeoSummaryEvent") if obj_dict else False
        self.qapDiscussionEvent = obj_dict.get("QapDiscussionEvent") if obj_dict else False
        self.otherEvent = obj_dict.get("OtherEvent") if obj_dict else False
        self.admissionEvent = obj_dict.get("AdmissionEvent") if obj_dict else False
        self.medicalHistoryEvent = obj_dict.get("MedicalHistoryEvent") if obj_dict else False
        self.preScrutinyEvent = obj_dict.get("PreScrutinyEvent") if obj_dict else False

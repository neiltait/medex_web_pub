import json

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
        self.user_role = obj_dict.get("userRole")

    @property
    def role_type(self):
        return self.ROLES[str(self.user_role)]

    @classmethod
    def create(cls, submission, user_id, auth_token):
        return request_handler.create_permission(json.dumps(submission), user_id, auth_token)

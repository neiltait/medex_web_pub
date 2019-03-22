from alerts import messages

from . import request_handler


class CreateUserForm:
    submit_btn_text = 'Save and add role/permission'

    def __init__(self, request=None):
        self.email_error = None
        if request:
            self.email_address = request.get('email_address')
        else:
            self.email_address = ''

    def validate(self):
        self.email_error = None

        if self.email_address == '' or self.email_address is None:
            self.email_error = messages.MISSING_EMAIL
        elif not self.check_is_nhs_email():
            self.email_error = messages.INVALID_EMAIL_DOMAIN

        return False if self.email_error else True

    def check_is_nhs_email(self):
        return True
        # return '@nhs.uk' in self.email_address

    def response_to_dict(self):
        return {
            "email": self.email_address,
        }


class PermissionBuilderForm:
    submit_btn_text = 'Save'

    def __init__(self, request=None):
        self.role_error = None
        self.permission_level_error = None
        self.trust_error = None
        self.region_error = None

        if request:
            self.role = request.get('role')
            self.permission_level = request.get('permission_level')
            self.region = request.get('region')
            self.trust = request.get('trust')
        else:
            self.role = None
            self.permission_level = None
            self.region = None
            self.trust = None

    def is_valid(self):

        if self.role is None or self.role is '':
            self.role_error = messages.FIELD_MISSING % "a role"

        if self.permission_level is None or self.permission_level is '':
            self.permission_level_error = messages.FIELD_MISSING % "a level"

        if self.permission_level == 'trust' and not self.trust_present():
            self.trust_error = messages.FIELD_MISSING % "a trust"

        if self.permission_level == 'regional' and not self.region_present():
            self.region_error = messages.FIELD_MISSING % "a region"

        return False if self.role_error or self.permission_level_error \
                        or self.trust_error or self.region_error else True

    def trust_present(self):
        return self.trust is not None and self.trust is not '' and self.trust != 'None'

    def region_present(self):
        return self.region is not None and self.region is not '' and self.region != 'None'

    def location_id(self):
        if self.region_present():
            print('region')
            return self.region
        elif self.trust_present():
            print('trust')
            return self.trust
        else:
            print('national')
            return None

    def to_dict(self, user_id):
        return {
            'userId': user_id,
            'userRole': 0,
            'locationId': self.location_id()
        }

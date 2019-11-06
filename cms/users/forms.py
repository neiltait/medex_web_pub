from alerts import messages
from medexCms.settings import EMAIL_WHITELIST
from medexCms.utils import fallback_to


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
        for email_option in EMAIL_WHITELIST:
            if email_option in self.email_address:
                return True
        return False

    def response_to_dict(self):
        return {
            "email": self.email_address,
        }

    def register_response_errors(self, response):
        if response.ok is False:
            errors = response.json()
            if errors and 'Email' in errors.keys():
                self.email_error = errors['Email'][0]


class ManageUserForm:
    submit_btn_text = 'Update user'

    def __init__(self, request=None):
        self.gmc_error = None
        if request:
            self.gmc_number = request.get('gmc_number')
        else:
            self.gmc_number = ''

    def validate(self):
        self.gmc_error = None
        return True

    def register_response_errors(self, response):
        if response.ok is False:
            errors = response.json()
            if errors and 'Gmc' in errors.keys():
                self.gmc_error = errors['Gmc'][0]
                errors['Gmc'] = None

            if len(errors) > 0:
                self.form_error = messages.GENERAL_ERROR % ("updating", "user")

    def response_to_dict(self):
        return {
            "gmc_number": self.gmc_number
        }


class EditUserProfileForm:
    submit_btn_text = 'Update user'


    def __init__(self, request=None):
        self.gmc_error = None
        self.errors = {'count': 0}
        if request:
            self.gmc_number = fallback_to(request.get('gmc_number'), '')
        else:
            self.gmc_number = ''

    @classmethod
    def from_user(cls, user):
        form = EditUserProfileForm()
        form.gmc_number = fallback_to(user.gmc_number, '')
        return form

    def validate(self):
        self.gmc_error = None
        return True

    def register_response_errors(self, response):
        if response.ok is False:
            errors = response.json()
            if errors and 'GmcNumber' in errors.keys():
                self.errors['gmc_number'] = errors['GmcNumber'][0]
                self.errors['count'] += 1
                errors['GmcNumber'] = None

            if len(errors) > 0:
                self.errors['form'] = messages.GENERAL_ERROR % ("updating", "user profile")
                self.errors['count'] += 1

    def response_to_dict(self):
        return {
            "gmcNumber": self.gmc_number
        }

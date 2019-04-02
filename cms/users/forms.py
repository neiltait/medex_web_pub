from alerts import messages


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
        return '@nhs.uk' in self.email_address or '@nhs.net' in self.email_address\
               or '@methods.co.uk' in self.email_address

    def response_to_dict(self):
        return {
            "email": self.email_address,
        }

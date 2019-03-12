INVALID_CREDENTIALS = "Your email and password combination doesn't seem to work. Please try again"

MISSING_CREDENTIALS = 'Please enter a User ID and Password'

MISSING_USER_ID = 'Please enter a User ID'

MISSING_EMAIL = 'Please enter an email address'

INVALID_EMAIL_DOMAIN = 'You must use an nhs.uk email address'

FORGOTTEN_PASSWORD_SENT = 'If the email address provided is valid password reset instructions have been sent.'

OBJECT_NOT_FOUND = 'The %s requested could not be found'

FIELD_MISSING = 'Please enter %s'

ERROR_IN_FORM = 'There are errors in the form see below for details'

NOT_IN_OKTA = 'Users must be added to OKTA to show in the system'

INVALID_DATE = 'Please enter a valid date'

def ErrorFieldRequiredMessage(field_name):
    return ("Please enter %s") % field_name

def ErrorFieldTooLong(character_max):
    return ("Please enter fewer than %d characters") % character_max

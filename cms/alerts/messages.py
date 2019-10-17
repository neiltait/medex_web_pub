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

NAME_TOTAL_TOO_LONG = 'Please enter fewer than 250 characters in total'

DEATH_IS_NOT_AFTER_BIRTH = 'Birth date must be before death date'

GENERAL_ERROR = 'There was an error whilst %s the %s'

NOT_ALLOWED = 'The action you tried is not supported by the service'

NOT_PERMITTED_HEADER = 'Not Permitted'

NOT_PERMITTED = 'Your permissions do not allow you to access this page'

NO_ROLES_HEADER = 'No Roles Assigned'

NO_ROLES = 'You do not currently have roles assigned to your account, please contact your service lead to request' \
           ' assignment'

NHS_NUMBER_ERROR = 'Please enter a valid 10 digit NHS number'

DEATH_DATE_MISSING_WHEN_TIME_GIVEN = 'Date of death is required if time is given'

NO_GENDER = "Please choose a gender"

DOB_IN_FUTURE = "Date of birth must be in the past"

DOD_IN_FUTURE = "Date of death must be in the past"

ME_OFFICE = "Please choose an ME office"


def ErrorFieldRequiredMessage(field_name):
    return ("Please enter %s") % field_name


def ErrorSelectionRequiredMessage(field_name):
    return ("Please select a value for %s") % field_name


def ErrorFieldTooLong(character_max):
    return ("Please enter fewer than %d characters") % character_max


class NhsNumberErrors:
    CONTAINS_INVALID_CHARACTERS = "This NHS number includes invalid characters"
    DUPLICATE = "This NHS number already exists on another case"
    NO_NUMBER_AND_NO_UNKNOWN = "an NHS number"


class DateOfBirthErrors:
    DATE_OF_BIRTH_AFTER_DATE_OF_DEATH = "Date of birth is after date of death"
    DOB_IN_FUTURE = "Date of birth must be in the past"


class ApiErrorMessages:
    nhs_numbers = NhsNumberErrors()
    date_of_birth = DateOfBirthErrors()


api_error_messages = ApiErrorMessages()

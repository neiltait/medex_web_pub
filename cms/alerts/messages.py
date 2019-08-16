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

DEATH_IS_NOT_AFTER_BIRTH = 'Birth death must be before death date'

GENERAL_ERROR = 'There was an error whilst %s the %s'

NOT_ALLOWED = 'The action you tried is not supported by the service'

NOT_PERMITTED_HEADER = 'Not Permitted'

NOT_PERMITTED = 'Your permissions do not allow you to access this page'

NO_ROLES_HEADER = 'No Roles Assigned'

NO_ROLES = 'You do not currently have roles assigned to your account, please contact your service lead to request' \
           ' assignment'

NHS_NUMBER_ERROR = 'Please enter a valid NHS number in format "123 456 7890"'

DEATH_DATE_MISSING_WHEN_TIME_GIVEN = 'Date of death is required if time is given'


def ErrorFieldRequiredMessage(field_name):
    return ("Please enter %s") % field_name


def ErrorSelectionRequiredMessage(field_name):
    return ("Please select a value for %s") % field_name


def ErrorFieldTooLong(character_max):
    return ("Please enter fewer than %d characters") % character_max


class NhsNumberErrors:
    CONTAINS_INVALID_CHARACTERS = "This NHS number includes invalid characters"
    CONTAINS_WHITESPACE = "This NHS number includes spaces"
    DUPLICATE = "This NHS number already exists on another case"
    INVALID = "This NHS number is invalid"
    UNKNOWN = "There is a problem with this NHS number"
    NO_NUMBER_AND_NO_UNKNOWN = "an NHS number"


class CustomErrorMessages:
    NO_GIVEN_NAME = "a given name"
    NO_SURNAME = "a surname"
    NO_GENDER = "a gender"
    NO_TEXT_OTHER_GENDER = "other gender details"
    NO_DOD_DAY = "a day"
    NO_DOD_MONTH = "a month"
    NO_DOD_YEAR = "a year"
    DOD_IN_FUTURE = "Date of death must be in the past"
    NO_PLACE_OF_DEATH = "a place of death"
    NO_ME_OFFICE = "an ME OFFICE"


class DateOfBirthErrors:
    DATE_OF_BIRTH_AFTER_DATE_OF_DEATH = "Date of birth is after date of death"
    DOB_IN_FUTURE = "Date of birth must be in the past"
    NO_DOB_DAY = "a day"
    NO_DOB_YEAR = "a year"


class ApiErrorMessages:
    nhs_numbers = NhsNumberErrors()
    date_of_birth = DateOfBirthErrors()
    custom_error_messages = CustomErrorMessages()


api_error_messages = ApiErrorMessages()

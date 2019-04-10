import datetime

API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

NONE_DATE = "0001-01-01T00:00:00"
NONE_DATE_WITH_TIME_ZONE = "0001-01-01T00:00:00+00:00"


def build_date(year, month, day, hour='00', min='00'):
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(min))


def validate_date(year, month, day, hour='00', min='00'):
    try:
        build_date(year, month, day, hour, min)
        return True
    except (ValueError, TypeError, AttributeError) as ex:
        return False


def parse_datetime(datetime_string):
    if datetime_string and not is_empty_date(datetime_string):
        return datetime.datetime.fromisoformat(datetime_string)
    else:
        return None


def is_empty_date(datetime_string):
    return NONE_DATE == datetime_string or NONE_DATE_WITH_TIME_ZONE == datetime_string


def bool_to_string(bool_value):
    return 'true' if bool_value else 'false'

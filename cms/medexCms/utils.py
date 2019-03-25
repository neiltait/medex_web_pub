import datetime

API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

NONE_DATE = "0001-01-01T00:00:00"


def validate_date(year, month, day, hour='00', min='00'):
    try:
        datetime.datetime(int(year), int(month), int(day), int(hour), int(min))
        return True
    except (ValueError, TypeError, AttributeError) as ex:
        return False


def parse_datetime(datetime_string):
    if datetime_string:
        return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT)
    else:
        return datetime_string


def is_empty_date(datetime_string):
    return NONE_DATE == datetime_string

import datetime
import re

API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
API_DATE_FORMAT_2 = '%Y-%m-%dT%H:%M:%S.%fZ'
API_DATE_FORMAT_3 = '%Y-%m-%dT%H:%M:%SZ'
API_DATE_FORMAT_4 = '%Y-%m-%dT%H:%M:%S'
API_DATE_FORMAT_5 = '%Y-%m-%dT%H:%M:%S.%f'

NONE_TIME = "00:00:00"

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
        try:
            date_and_time, microseconds_and_zone = datetime_string.split('.')
            arr = list(filter(None, re.split('(\d+)', microseconds_and_zone)))
            microseconds = arr.pop(0)[:6]
            datetime_string = '%s.%s%s' % (date_and_time, microseconds, ''.join(arr))
            return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT)
        except (ValueError, TypeError):
            try:
                return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT_2)
            except ValueError:
                try:
                    return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT_3)
                except ValueError:
                    try:
                        return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT_4)
                    except ValueError:
                        try:
                            return datetime.datetime.strptime(datetime_string, API_DATE_FORMAT_5)
                        except ValueError:
                            print('Unknown date format received: %s' % datetime_string)
                            return None
    else:
        return None


def fallback_to(value, default_value):
    return value if value is not None else default_value


def is_empty_date(datetime_string):
    return NONE_DATE == datetime_string or NONE_DATE_WITH_TIME_ZONE == datetime_string


def is_empty_time(time_string):
    return NONE_TIME == time_string


def bool_to_string(bool_value):
    return 'true' if bool_value else 'false'

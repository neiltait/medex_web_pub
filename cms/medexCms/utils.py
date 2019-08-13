from django.conf import settings

import datetime
import re
from alerts import messages
from errors.utils import log_internal_error

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
        log_internal_error('validate_date', ex)
        return False


def pop_if_falsey(key, from_dict):
    if key in from_dict and not from_dict[key]:
        from_dict.pop(key)


def all_not_blank(*args):
    return all(v != '' for v in args)


def any_not_blank(*args):
    return any(v != '' for v in args)


def validate_date_time_field(field_name, errors, year, month, day, time, error_message=messages.INVALID_DATE,
                             require_not_blank=False):
    valid = not require_not_blank

    if all_not_blank(year, month, day, time):
        hours = time.split(':')[0]
        mins = time.split(':')[1]
        valid = validate_date(year, month, day, hours, mins)

    elif any_not_blank(year, month, day, time):
        valid = False

    if not valid:
        errors['count'] += 1
        errors[field_name] = error_message

    return valid


def validate_is_not_blank(field_name, errors, value, error_message=messages.FIELD_MISSING):
    if value is None or value == '':
        errors['count'] += 1
        errors[field_name] = error_message
        return False
    else:
        return True


def date_is_valid_or_empty(year, month, day, hour='00', min='00'):
    if year == '' and month == '' and day == '':
        return True
    else:
        return validate_date(year, month, day, hour, min)


def parse_datetime(datetime_string):
    if datetime_string and not is_empty_date(datetime_string):
        try:
            date_and_time, microseconds_and_zone = datetime_string.split('.')
            arr = list(filter(None, re.split("(\d+)", microseconds_and_zone)))
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


def reformat_datetime(datetime_string, new_format, default_value=''):
    if datetime_string:
        full_date_time = parse_datetime(datetime_string)
        return full_date_time.strftime(new_format) if full_date_time else default_value
    else:
        return default_value


def fallback_to(value, default_value):
    return value if value is not None else default_value


def is_empty_date(datetime_string):
    return NONE_DATE == datetime_string or NONE_DATE_WITH_TIME_ZONE == datetime_string


def is_empty_time(time_string):
    return NONE_TIME == time_string


def bool_to_string(bool_value):
    return 'true' if bool_value else 'false'


def key_not_empty(key, obj_dict):
    return key in obj_dict and obj_dict[key]


def get_code_version():
    return settings.VERSION


def no_cache(response):
    response['Cache-Control'] = 'no-cache'
    return response

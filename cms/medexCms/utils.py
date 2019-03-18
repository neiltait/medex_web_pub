import datetime


def validate_date(year, month, day, hour='00', min='00'):
    try:
        datetime.datetime(int(year), int(month), int(day), int(hour), int(min))
        return True
    except (ValueError, TypeError, AttributeError) as ex:
        return False

def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%fZ')

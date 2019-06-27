ERROR = 'error'

SUCCESS = 'success'

INFO = 'info'


def generate_error_alert(message):
    return {
        'type': ERROR,
        'message': message
    }


def generate_success_alert(message):
    return {
        'type': SUCCESS,
        'message': message
    }


def generate_info_alert(message):
    return {
        'type': INFO,
        'message': message
    }

from errors.models import MethodNotAllowedError


def __handle_method_not_allowed_error(user):
    template = 'errors/base_error.html'
    result = MethodNotAllowedError()

    context = {
        'session_user': user,
        'error': result,
    }

    return template, context, result.status_code

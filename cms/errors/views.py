from errors.models import MethodNotAllowedError, NotPermittedError
from medexCms.utils import get_code_versions


def __handle_method_not_allowed_error(user):
    template = 'errors/base_error.html'
    result = MethodNotAllowedError()

    context = {
        'session_user': user,
        'error': result,
        'version': get_code_versions(),
    }

    return template, context, result.status_code


def __handle_not_permitted_error(user):
    template = 'errors/base_error.html'
    result = NotPermittedError()

    context = {
        'session_user': user,
        'error': result,
        'version': get_code_versions(),
    }

    return template, context, result.http_code

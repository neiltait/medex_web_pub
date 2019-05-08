from django.shortcuts import render

from errors.models import MethodNotAllowedError, NotPermittedError


def handle_method_not_allowed_error(request, user):
    template = 'errors/base_error.html'
    result = MethodNotAllowedError()

    context = {
        'session_user': user,
        'error': result,
    }

    return render(request, template, context, status=result.status_code)



def __handle_method_not_allowed_error(user):
    template = 'errors/base_error.html'
    result = MethodNotAllowedError()

    context = {
        'session_user': user,
        'error': result,
    }

    return template, context, result.status_code


def handle_not_permitted_error(request, user):
    template = 'errors/base_error.html'
    result = NotPermittedError()

    context = {
        'session_user': user,
        'error': result
    }

    return render(request, template, context, status=result.status_code)


def __handle_not_permitted_error(user):
    template = 'errors/base_error.html'
    result = NotPermittedError()

    context = {
        'session_user': user,
        'error': result
    }

    return template, context, result.http_code

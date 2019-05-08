from django.shortcuts import render

from .models import MethodNotAllowedError


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


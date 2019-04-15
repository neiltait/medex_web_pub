from rest_framework import status
from errors.models import NotFoundError, GenericError


def handle_error(error_response, params):
    if error_response.status_code == status.HTTP_404_NOT_FOUND:
        return NotFoundError(params.get('type'))
    else:
        return GenericError(error_response, params)

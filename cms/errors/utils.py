import logging

from rest_framework import status
from errors.models import NotFoundError, GenericError

logger = logging.getLogger(__name__)


def handle_error(error_response, params):
    if error_response.status_code == status.HTTP_404_NOT_FOUND:
        return NotFoundError(params.get('type'))
    else:
        return GenericError(error_response, params)


def log_unexpected_method(method, view):
    logger.error('Unexpected HTTP method received (%s) on the %s endpoint')

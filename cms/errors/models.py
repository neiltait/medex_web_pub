from django.conf import settings
from requests.models import Response
from rest_framework import status

from alerts import messages


class NotFoundError:
    status_code = status.HTTP_404_NOT_FOUND
    error_message = messages.OBJECT_NOT_FOUND

    def __init__(self, obj_type):
        self.obj_type = obj_type

    def get_message(self):
        return self.error_message % self.obj_type


class MethodNotAllowedError:
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    error_message = messages.NOT_ALLOWED

    def get_message(self):
        return self.error_message


class NotPermittedError:
    http_code = status.HTTP_401_UNAUTHORIZED
    status_code = messages.NOT_PERMITTED_HEADER
    error_message = messages.NOT_PERMITTED

    def get_message(self):
        return self.error_message


class NoRoleError:
    http_code = status.HTTP_401_UNAUTHORIZED
    status_code = messages.NO_ROLES_HEADER
    error_message = messages.NO_ROLES

    def get_message(self):
        return self.error_message


class GenericError:
    error_message = messages.GENERAL_ERROR

    def __init__(self, response, params):
        self.response = response
        self.params = params

    def get_message(self):
        return self.error_message % (self.params.get('action'), self.params.get('type'))

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def stack_trace(self):
        return self.prepare_content() if settings.DEBUG else None

    def prepare_content(self):
        content = self.response.text
        content = content.replace('<pre', '<div')
        content = content.replace('/pre', '/div')
        content = content.replace('==', '')
        return content


class BadRequestResponse:

    @classmethod
    def new(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

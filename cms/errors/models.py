from django.conf import settings
from rest_framework import status

from alerts import messages


class NotFoundError:
    status_code = status.HTTP_404_NOT_FOUND
    error_message = messages.OBJECT_NOT_FOUND

    def __init__(self, obj_type):
        self.obj_type = obj_type

    def get_message(self):
        return self.error_message % self.obj_type


class GenericError:
    error_message = messages.GENERAL_ERROR

    def __init__(self, response, params):
        self.response = response
        self.params = params

    def get_message(self):
        return self.error_message % (self.params.get('action'),self.params.get('type'))

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

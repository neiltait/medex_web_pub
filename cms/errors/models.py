from rest_framework import status

from alerts import messages


class NotFoundError:
    status_code = status.HTTP_404_NOT_FOUND
    error_message = messages.OBJECT_NOT_FOUND

    def __init__(self, obj_type):
        self.obj_type = obj_type

    def get_message(self):
        return self.error_message % self.obj_type

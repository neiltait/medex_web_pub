from django.conf import settings
from django.test import SimpleTestCase

from http.cookies import SimpleCookie

from medexCms.test.mocks import SessionMocks


class MedExTestCase(SimpleTestCase):

    def setUp(self):
        settings.LOCAL = True

    def assertIsTrue(self, value):
        self.assertIs(value, True)

    def assertIsFalse(self, value):
        self.assertIs(value, False)

    def assertIsNone(self, value):
        self.assertIsTrue(value is None)

    def assertIsNotNone(self, value):
        self.assertIsTrue(value is not None)

    def set_auth_cookies(self):
        self.client.cookies = SimpleCookie(SessionMocks.get_auth_cookies())

    def clear_auth_cookies(self):
        self.client.cookies = SimpleCookie(SessionMocks.get_empty_cookies())

    def get_context_value(self, context, key):
        return context[key]

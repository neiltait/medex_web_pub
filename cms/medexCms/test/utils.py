from django.conf import settings
from django.test import TestCase

from http.cookies import SimpleCookie

from medexCms.test import mocks


class MedExTestCase(TestCase):

    def setUp(self):
        settings.LOCAL = True
  
    def assertIsTrue(self, value):
        self.assertIs(value, True)

    def assertIsFalse(self, value):
        self.assertIs(value, False)

    def assertIsNone(self, value):
        self.assertIsTrue(value is None)

    def set_auth_cookies(self):
        self.client.cookies = SimpleCookie(mocks.AUTH_COOKIES)

    def get_context_value(self, context, key):
      return context[key]

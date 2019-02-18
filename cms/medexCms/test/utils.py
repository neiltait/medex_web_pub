from django.test import TestCase

class MedExTestCase(TestCase):
  
    def assertIsTrue(self, value):
        self.assertIs(value, True)

    def assertIsFalse(self, value):
        self.assertIs(value, False)

    def get_context_value(self, context, key):
      return context[key]

from django.test import TestCase

class MedExTestCase(TestCase):
  
    def assertIsTrue(self, value):
        self.assertIs(value, True)

    def assertIsFalse(self, value):
        self.assertIs(value, False)

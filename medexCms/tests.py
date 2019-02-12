from .test.utils import MedExTestCase

class MedexTestUtilsTests(MedExTestCase):

  def test_MedExTestCase_assertIsTrue_returns_true_when_passed_True(self):
    result = self.assertIsTrue(True)

  def test_MedExTestCase_assertIsTrue_returns_false_when_passed_False(self):
    try:
      self.assertIsTrue(False)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

  def test_MedExTestCase_assertIsTrue_returns_false_when_passed_a_truthy_value(self):
    try:
      truthy_variable = 'A string'
      result = self.assertIsTrue(truthy_variable)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

  def test_MedExTestCase_assertIsTrue_returns_false_when_passed_a_falsey_value(self):
    try:
      falsey_variable = None
      result = self.assertIsTrue(falsey_variable)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

  def test_MedExTestCase_assertIsFalse_returns_true_when_passed_False(self):
    result = self.assertIsFalse(False)

  def test_MedExTestCase_assertIsFalse_returns_false_when_passed_True(self):
    try:
      self.assertIsFalse(True)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

  def test_MedExTestCase_assertIsFalse_returns_false_when_passed_a_truthy_value(self):
    try:
      truthy_variable = 'A string'
      result = self.assertIsFalse(truthy_variable)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

  def test_MedExTestCase_assertIsFalse_returns_false_when_passed_a_falsey_value(self):
    try:
      falsey_variable = None
      result = self.assertIsFalse(falsey_variable)
      self.assertFalse('Test failed to produce expected assertion error')
    except AssertionError:
      self.assertTrue('Test produced expected assertion error')

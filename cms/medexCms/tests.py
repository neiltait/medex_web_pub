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

  def test_get_context_value_loads_the_correct_value_for_a_valid_key(self):
    key = 'testKey'
    value = 'A short test string'
    context = {
      key: value,
    }
    result = self.get_context_value(context, key)
    self.assertEqual(result, value)

  def test_get_context_value_throws_a_key_error_when_passed_an_invalid_key(self):
    key = 'testKey'
    value = 'A short test string'
    invalidKey = 'wrongKey'
    context = {
      key: value,
    }
    try:
      result = self.get_context_value(context, invalidKey)
      self.assertFalse('Test failed to produce expected key error')
    except KeyError:
      self.assertTrue('Test produced expected key error')
    

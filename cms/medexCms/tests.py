from .test.utils import MedExTestCase

from .utils import validate_date


class MedexTestUtilsTests(MedExTestCase):

    def test_MedExTestCase_assertIsTrue_returns_true_when_passed_True(self):
        self.assertIsTrue(True)

    def test_MedExTestCase_assertIsTrue_returns_false_when_passed_False(self):
        try:
            self.assertIsTrue(False)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsTrue_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsTrue(truthy_variable)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsTrue_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsTrue(falsey_variable)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsFalse_returns_true_when_passed_False(self):
        self.assertIsFalse(False)

    def test_MedExTestCase_assertIsFalse_returns_false_when_passed_True(self):
        try:
            self.assertIsFalse(True)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsFalse_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsFalse(truthy_variable)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsFalse_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsFalse(falsey_variable)
            self.assertFalse('Test failed to produce expected assertion error')
        except AssertionError:
            self.assertTrue('Test produced expected assertion error')

    def test_MedExTestCase_assertIsNone_returns_true_when_passed_None(self):
        self.assertIsNone(None)

    def test_MedExTestCase_assertIsNone_returns_false_when_passed_something_other_than_None(self):
        try:
            self.assertIsNone("test")
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
            self.get_context_value(context, invalidKey)
            self.assertFalse('Test failed to produce expected key error')
        except KeyError:
            self.assertTrue('Test produced expected key error')


class MedexUtilsTests(MedExTestCase):

    def test_validate_date_returns_true_for_a_valid_date_with_no_time_provided(self):
        self.assertIsTrue(validate_date('2019', '12', '25'))

    def test_validate_date_returns_true_for_a_valid_date_with_valid_time_provided(self):
        self.assertIsTrue(validate_date('2019', '12', '25', '12', '00'))

    def test_validate_date_returns_false_for_a_valid_date_with_invalid_time_provided(self):
        self.assertIsFalse(validate_date('2019', '12', '25', '28', '70'))

    def test_validate_date_returns_false_for_a_invalid_date_with_no_time_provided(self):
        self.assertIsFalse(validate_date('2019', '2', '31'))

    def test_validate_date_returns_false_for_a_invalid_date_with_invalid_time_provided(self):
        self.assertIsFalse(validate_date('2019', '2', '31', '28', '70'))

    def test_validate_date_returns_false_for_a_invalid_date_with_valid_time_provided(self):
        self.assertIsFalse(validate_date('2019', '2', '31', '12', '00'))

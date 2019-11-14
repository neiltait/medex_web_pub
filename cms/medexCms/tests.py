from alerts import messages
from .test.utils import MedExTestCase

from .utils import validate_date, parse_datetime, all_not_blank, any_not_blank, validate_date_time_field


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

    def test_parse_datetime_returns_a_correct_date_object_when_passed_a_valid_date(self):
        parsed_date = parse_datetime('2019-03-26T13:29:50.473Z')
        self.assertEqual(parsed_date.day, 26)
        self.assertEqual(parsed_date.month, 3)
        self.assertEqual(parsed_date.year, 2019)
        self.assertEqual(parsed_date.hour, 13)
        self.assertEqual(parsed_date.minute, 29)

    def test_parse_datetime_returns_none_if_passed_a_falsey_argument(self):
        parsed_date = parse_datetime('')
        self.assertEqual(parsed_date, None)

    def test_all_not_blank_returns_false_if_all_args_are_blank(self):
        self.assertIsFalse(all_not_blank('', '', ''))

    def test_all_not_blank_returns_false_if_some_args_are_blank(self):
        self.assertIsFalse(all_not_blank('x', 'y', ''))

    def test_all_not_blank_returns_true_if_all_args_are_not_blank(self):
        self.assertIsTrue(all_not_blank('x', 'y', 'z'))

    def test_any_not_blank_returns_false_if_all_args_are_blank(self):
        self.assertIsFalse(any_not_blank('', '', ''))

    def test_any_not_blank_returns_true_if_some_args_are_not_blank(self):
        self.assertIsTrue(any_not_blank('x', 'y', ''))

    def test_any_not_blank_returns_true_if_all_args_are_not_blank(self):
        self.assertIsTrue(any_not_blank('x', 'y', 'z'))

    def test_validate_date_time_field_returns_true_by_default_for_empty_input(self):
        # Given empty fields
        year = ''
        month = ''
        day = ''
        time = ''
        errors = {'count': 0}

        # When validated
        date_time_valid = validate_date_time_field('any', errors, year, month, day, time)

        # Then should return valid
        self.assertIsTrue(date_time_valid)

    def test_validate_date_time_field_returns_false_when_date_required(self):
        # Given empty fields
        year = ''
        month = ''
        day = ''
        time = ''
        errors = {'count': 0}

        # When validated with require_not_blank set to true
        date_time_valid = validate_date_time_field('any', errors, year, month, day, time, require_not_blank=True)

        # Then should return valid
        self.assertFalse(date_time_valid)

    def test_validate_date_time_field_returns_true_for_a_valid_date_and_time(self):
        # Given valid fields
        year = '2019'
        month = '5'
        day = '8'
        time = '12:00'
        errors = {'count': 0}

        # When validated
        date_time_valid = validate_date_time_field('any', errors, year, month, day, time)

        # Then should return valid
        self.assertIsTrue(date_time_valid)

    def test_validate_date_time_field_returns_false_for_invalid_date_and_time(self):
        # Given invalid month
        year = '2019'
        month = '205'
        day = '8'
        time = '12:00'
        errors = {'count': 0}

        # When validated
        date_time_valid = validate_date_time_field('any', errors, year, month, day, time)

        # Then should return valid
        self.assertFalse(date_time_valid)

    def test_validate_date_time_field_returns_false_when_some_date_and_time_fields_are_empty(self):
        # Given invalid month
        year = '2019'
        month = ''
        day = '8'
        time = '12:00'
        errors = {'count': 0}

        # When validated
        date_time_valid = validate_date_time_field('any', errors, year, month, day, time)

        # Then should return valid
        self.assertFalse(date_time_valid)

    def test_validate_date_time_field_updates_errors_when_date_time_is_invalid(self):
        # Given invalid month
        year = '2019'
        month = ''
        day = '8'
        time = '12:00'
        errors = {'count': 0}

        # When validated
        validate_date_time_field('field_name', errors, year, month, day, time)

        # Then should return valid
        self.assertEquals(errors['field_name'], messages.INVALID_DATE)
        self.assertEquals(errors['count'], 1)

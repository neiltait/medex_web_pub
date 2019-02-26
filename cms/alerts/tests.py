from medexCms.test.utils import MedExTestCase

from . import messages, utils
from .utils import generate_error_alert, generate_success_alert, generate_info_alert

class AlertsUtilsTests(MedExTestCase):

  def test_generate_error_alert_returns_a_dict_with_error_type_an_the_provided_message(self):
    result = generate_error_alert(messages.INVALID_CREDENTIALS)
    self.assertEqual(result['type'], utils.ERROR)
    self.assertEqual(result['message'], messages.INVALID_CREDENTIALS)

  def test_generate_success_alert_returns_a_dict_with_success_type_an_the_provided_message(self):
    result = generate_success_alert(messages.MISSING_CREDENTIALS)
    self.assertEqual(result['type'], utils.SUCCESS)
    self.assertEqual(result['message'], messages.MISSING_CREDENTIALS)

  def test_generate_info_alert_returns_a_dict_with_info_type_an_the_provided_message(self):
    result = generate_info_alert(messages.MISSING_CREDENTIALS)
    self.assertEqual(result['type'], utils.INFO)
    self.assertEqual(result['message'], messages.MISSING_CREDENTIALS)  

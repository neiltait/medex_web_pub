from unittest.mock import patch

from medexCms.test.mocks import ExaminationMocks
from monitor.loggers import monitor, TestLogStream, MedexLoggerEvents
from medexCms.test.utils import MedExTestCase


class TestMonitorTests(MedExTestCase):

    def init_test_log_stream(self):
        new_log_stream = TestLogStream()
        monitor.change_log_stream(new_log_stream)
        return new_log_stream

    def test_monitor_on_add_custom_event_adds_a_log_item(self):
        log_stream = self.init_test_log_stream()

        monitor.log_custom_event("test", "test_data")

        self.assertEqual(log_stream.event_count(), 1)

    def test_monitor_on_add_custom_event_saves_data(self):
        log_stream = self.init_test_log_stream()

        monitor.log_custom_event("test", "test_data")

        event = log_stream.event(0)
        self.assertEqual(event['event_type'], 'test')
        self.assertEqual(event['data'], 'test_data')

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_successful_case_creation_response_with_id_1())
    def test_logger_does_record_case_create_event(self, mock):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()

        self.client.post('/cases/create', form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CREATED_CASE)

    @patch('examinations.request_handler.post_new_examination',
           return_value=ExaminationMocks.get_unsuccessful_case_creation_response())
    def test_logger_does_record_unsuccessful_case_create_event(self, mock):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_minimal_create_case_form_data()

        self.client.post('/cases/create', form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CREATED_CASE_UNSUCCESSFUL)

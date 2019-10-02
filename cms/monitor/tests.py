from unittest.mock import patch

from examinations.models.case_outcomes import CaseOutcome
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

    def test_logger_does_record_create_timeline_event(self):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_pre_scrutiny_create_event_data()

        self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CREATED_TIMELINE_EVENT)

    @patch('examinations.request_handler.create_pre_scrutiny_event',
           return_value=ExaminationMocks.get_unsuccessful_timeline_event_create_response())
    def test_logger_does_record_create_timeline_event_unsuccessful(self, mock_pre_scrutiny_create):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_pre_scrutiny_create_event_data()

        self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CREATED_TIMELINE_EVENT_UNSUCCESSFUL)

    def test_logger_does_record_create_draft_timeline_event(self):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_pre_scrutiny_draft_event_data()

        self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.SAVED_TIMELINE_EVENT)

    @patch('examinations.request_handler.create_pre_scrutiny_event',
           return_value=ExaminationMocks.get_unsuccessful_timeline_event_create_response())
    def test_logger_does_record_create_draft_timeline_event_unsuccessful(self, mock_pre_scrutiny_create):
        self.set_auth_cookies()
        log_stream = self.init_test_log_stream()
        form_data = ExaminationMocks.get_pre_scrutiny_draft_event_data()

        self.client.post('/cases/%s/case-breakdown' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.SAVED_TIMELINE_EVENT_UNSUCCESSFUL)

    def test_logger_does_record_complete_scrutiny_event(self):
        self.set_auth_cookies()
        form_data = {CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE: True}
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.COMPLETED_SCRUTINY)

    @patch('examinations.request_handler.complete_case_scrutiny',
           return_value=ExaminationMocks.get_unsuccessful_scrutiny_complete_response())
    def test_logger_does_record_complete_scrutiny_unsuccessful_event(self, mock):
        self.set_auth_cookies()
        form_data = {CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE: True}
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.COMPLETED_SCRUTINY_UNSUCCESSFUL)

    def test_logger_does_record_coroner_referral(self):
        self.set_auth_cookies()
        form_data = {CaseOutcome.CORONER_REFERRAL_FORM_TYPE: True}
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CONFIRMED_CORONER_REFERRAL)

    @patch('examinations.request_handler.confirm_coroner_referral',
           return_value=ExaminationMocks.get_unsuccessful_coroner_referral_response())
    def test_logger_does_record_coroner_referral_unsuccessful(self, mock_completion_response):
        self.set_auth_cookies()
        form_data = {CaseOutcome.CORONER_REFERRAL_FORM_TYPE: True}
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CONFIRMED_CORONER_REFERRAL_UNSUCCESSFUL)

    def test_logger_does_record_outstanding_items_submission(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_case_outcome_outstanding_items_form_data()
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.SAVED_OUTSTANDING_ITEM)

    @patch('examinations.request_handler.update_outcomes_outstanding_items',
           return_value=ExaminationMocks.get_unsuccessful_outstanding_items_response())
    def test_logger_does_record_outstanding_items_submission_unsuccessful(self, mock_completion_response):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_case_outcome_outstanding_items_form_data()
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.SAVED_OUTSTANDING_ITEM_UNSUCCESSFUL)

    def test_logger_does_record_close_case(self):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_case_outcome_close_case_form_data()
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CLOSED_CASE)

    @patch('examinations.request_handler.close_case',
           return_value=ExaminationMocks.get_unsuccessful_case_close_response())
    def test_logger_does_record_close_case_unsuccessful(self, mock_completion_response):
        self.set_auth_cookies()
        form_data = ExaminationMocks.get_case_outcome_close_case_form_data()
        log_stream = self.init_test_log_stream()

        self.client.post('/cases/%s/case-outcome' % ExaminationMocks.EXAMINATION_ID, form_data)

        self.assertEqual(log_stream.event_count(), 1)
        event = log_stream.event(0)
        self.assertEqual(event['event_type'], MedexLoggerEvents.CLOSED_CASE_UNSUCCESSFUL)

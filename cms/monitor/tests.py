from monitor.loggers import monitor, TestLogStream
from medexCms.test.utils import MedExTestCase


def init_test_log_stream():
    log_stream = TestLogStream()
    monitor.change_log_stream(log_stream)
    return log_stream


class TestMonitorTests(MedExTestCase):

    def test_monitor_on_add_custom_event_adds_a_log_item(self):
        log_stream = init_test_log_stream()

        monitor.log_custom_event("test", "test_data")

        self.assertEqual(log_stream.event_count(), 1)

    def test_monitor_on_add_custom_event_saves_data(self):
        log_stream = init_test_log_stream()

        monitor.log_custom_event("test", "test_data")

        event = log_stream.event(0)
        self.assertEqual(event['event_type'], 'test')
        self.assertEqual(event['data'], 'test_data')

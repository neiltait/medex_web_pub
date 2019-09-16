class MedexLoggerEvents:
    CREATE_USER = 'create user'


class MedexLogStream:
    def log(self, event_type, data):
        pass


class ConsoleLogStream(MedexLogStream):
    def log(self, event_type, data):
        print(event_type, data)


class TestLogStream(MedexLogStream):
    event_history = []

    def log(self, event_type, data):
        self.event_history.append({"event_type": event_type, "data": data})

    def event_count(self):
        return len(self.event_history)

    def event(self, index):
        return self.event_history[index]

    def last(self, index):
        return self.event_history[self.event_count() - 1]

    def clear(self):
        self.event_history = []


class InsightsLogStream(MedexLogStream):
    def log(self, event_type, data):
        print('INSIGHTS', event_type, data)


class MedexMonitor:

    def __init__(self, log_stream: MedexLogStream):
        self.log_stream = log_stream

    def change_log_stream(self, log_stream: MedexLogStream):
        self.log_stream = log_stream

    def log_custom_event(self, event_type, data):
        self.log_stream.log(event_type, data)


monitor = MedexMonitor(log_stream=ConsoleLogStream())

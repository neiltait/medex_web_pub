class MedexLoggerEvents:
    CREATE_USER = 'create user'


class MedexLogger:
    def log(self, event_type, data):
        pass


class ConsoleLogger(MedexLogger):
    def log(self, event_type, data):
        print(event_type, data)


class TestLogger(MedexLogger):
    event_history = []

    def log(self, event_type, data):
        self.event_history.append({"event_type": event_type, "data": data})

    def get_count(self):
        return len(self.event_history)

    def get_item(self, index):
        return self.event_history[index]

    def get_last(self, index):
        return self.event_history[self.get_count() - 1]

    def clear(self):
        self.event_history = []


class InsightsLogger(MedexLogger):
    def log(self, event_type, data):
        print('INSIGHTS', event_type, data)


class Monitor:

    def __init__(self, logger: MedexLogger):
        self.logger = logger

    def change_logger(self, logger: MedexLogger):
        self.logger = logger

    def log_custom_event(self, event_type, data):
        self.logger.log(event_type, data)


monitor = Monitor(logger=ConsoleLogger())

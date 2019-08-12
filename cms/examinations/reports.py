
class CoronerDownloadReport:

    def __init__(self):
        self.forename = None
        self.surname = None

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        report = CoronerDownloadReport()
        report.forename = 'Tarquin'
        report.surname = 'the Bear'
        report.examination_id = examination_id

        errors = {'count': 0}

        return report, errors

    def to_object(self):
        return {'forename': self.forename, 'surname': self.surname}



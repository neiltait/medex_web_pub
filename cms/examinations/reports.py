from examinations import request_handler
from medexCms.api import enums
from medexCms.utils import fallback_to, reformat_datetime


class CoronerDownloadReport:

    def __init__(self):
        self.given_names = None
        self.surname = None
        self.nhs_number = None
        self.gender = None
        self.able_to_issue_mccd = False
        self.cause_of_death_1a = None
        self.cause_of_death_1b = None
        self.cause_of_death_1c = None
        self.cause_of_death_2 = None

    @classmethod
    def load_by_id(cls, examination_id, auth_token):

        response = request_handler.load_coroner_report(auth_token, examination_id)
        report = None
        errors = {'count': 0}

        if response.ok:
            data = response.json()
            report = CoronerDownloadReport()
            report.given_names = fallback_to(data.get('givenNames'), '')
            report.surname = fallback_to(data.get('surname'), '')
            report.nhs_number = fallback_to(data.get('nhsNumber'), 'Unknown')
            report.able_to_issue_mccd = 'Y' if fallback_to(data.get('ableToIssueMCCD'), False) else 'N'
            report.cause_of_death_1a = fallback_to(data.get('causeOfDeath1a'), '')
            report.cause_of_death_1b = fallback_to(data.get('causeOfDeath1b'), '')
            report.cause_of_death_1c = fallback_to(data.get('causeOfDeath1c'), '')
            report.cause_of_death_2 = fallback_to(data.get('causeOfDeath2'), '')

            report.date_of_birth = fallback_to(data.get('dateOfBirth'), '')
            report.display_date_of_birth = reformat_datetime(report.date_of_birth, new_format="%d-%m-%Y")
            report.date_of_death = fallback_to(data.get('dateOfDeath'), '')
            report.display_date_of_death = reformat_datetime(report.date_of_death, new_format="%d-%m-%Y")
            report.time_of_death = fallback_to(data.get('timeOfDeath'), '')

            report.gender = fallback_to(data.get('gender'), '')
            report.street_address = fallback_to(data.get('houseNameNumber'), '') + ' ' + fallback_to(data.get('street'),
                                                                                                     '')
            report.town = fallback_to(data.get('town'), '')
            report.county = fallback_to(data.get('county'), '')
            report.postcode = fallback_to(data.get('postcode'), '')
            report.place_of_death = fallback_to(data.get('placeOfDeath'), '')
            report.address = [line for line in [report.street_address, report.town, report.county, report.postcode] if
                              len(line.strip()) > 0]
            report.any_implants = yes_no_unknown(data.get('anyImplants'))

            report.examination_id = examination_id

            bereaved_data = data.get('latestBereavedDiscussion')
            report.bereaved = {
                'name': fallback_to(bereaved_data.get('participantFullName'), '') if bereaved_data else '',
                'relationship': fallback_to(bereaved_data.get('participantRelationship'), '') if bereaved_data else '',
                'phone': fallback_to(bereaved_data.get('participantPhoneNumber'), '') if bereaved_data else '',
                "informed": fallback_to(bereaved_data.get('informedAtDeath'), '') if bereaved_data else '',
                "result": fallback_to(bereaved_data.get('bereavedDiscussionOutcome'), '') if bereaved_data else '',
            }
            if report.bereaved['result'] != enums.discussion.COD_ACCEPTED:
                report.bereaved['concerns'] = fallback_to(bereaved_data.get('discussionDetails'),
                                                          '') if bereaved_data else ''
            else:
                report.bereaved['concerns'] = ''

            qap_data = data.get('qap')
            report.qap = {
                'name': fallback_to(qap_data.get('name'), '') if qap_data else '',
                'role': fallback_to(qap_data.get('role'), '') if qap_data else '',
                'organisation': fallback_to(qap_data.get('organisation'), '') if qap_data else '',
                'phone': fallback_to(qap_data.get('phone'), '') if qap_data else '',
                'notes': fallback_to(qap_data.get('notes'), '') if qap_data else '',
                'gmc': fallback_to(qap_data.get('gmcNumber'), '') if qap_data else '',
            }

            consultant_data = data.get('consultant')
            report.consultant = {
                'name': fallback_to(consultant_data.get('name'), '') if consultant_data else '',
                'role': fallback_to(consultant_data.get('role'), '') if consultant_data else '',
                'organisation': fallback_to(consultant_data.get('organisation'), '') if consultant_data else '',
                'phone': fallback_to(consultant_data.get('phone'), '') if consultant_data else '',
                'notes': fallback_to(consultant_data.get('notes'), '') if consultant_data else '',
                'gmc': fallback_to(consultant_data.get('gmcNumber'), '') if consultant_data else '',
            }

            gp_data = data.get('gp')
            report.gp = {
                'name': fallback_to(gp_data.get('name'), '') if gp_data else '',
                'role': fallback_to(gp_data.get('role'), '') if gp_data else '',
                'organisation': fallback_to(gp_data.get('organisation'), '') if gp_data else '',
                'phone': fallback_to(gp_data.get('phone'), '') if gp_data else '',
                'notes': fallback_to(gp_data.get('notes'), '') if gp_data else '',
                'gmc': fallback_to(gp_data.get('gmcNumber'), '') if gp_data else '',
            }

            latest_admission_data = data.get('latestAdmissionDetails')
            if latest_admission_data:
                report.latest_admission = {
                    'date': 'Unknown' if fallback_to(latest_admission_data.get('admittedDateUnknown'),
                                                     False) else reformat_datetime(
                        latest_admission_data.get('admittedDate'), '%d-%m-%Y'),
                    'time': 'Unknown' if fallback_to(latest_admission_data.get('admittedTimeUnknown'),
                                                     False) else fallback_to(latest_admission_data.get('admittedTime'),
                                                                             ''),
                    'location': '',
                    'notes': fallback_to(latest_admission_data.get('notes'), '')
                }
            else:
                report.latest_admission = {
                    'date': '',
                    'time': '',
                    'loaction': '',
                    'notes': ''
                }

            report.medical_history = fallback_to(data.get('detailsAboutMedicalHistory'), '')

        else:
            errors['count'] += 1
            errors['report'] = "Could not download report"

        return report, errors

    def to_object(self):
        return self


def yes_no_unknown(value):
    if value is None:
        return "Unknown"
    else:
        return 'Y' if value else 'N'


class FinancialReport:

    def __init__(self):
        self.data = None

    @classmethod
    def get_locations(cls, auth_token):
        return request_handler.load_financial_report_locations(auth_token)

    @classmethod
    def load_by_query(cls, params, auth_token):

        query_params = {
            "LocationId": params["me_office"],
            "ExaminationsCreatedFrom": params["date_from"],
            "ExaminationsCreatedTo": params["date_to"],
        }

        response = request_handler.load_financial_report(query_params, auth_token)
        report = None
        errors = {'count': 0}

        if response.ok:
            data = response.json()
            report = FinancialReport()
            report.data = fallback_to(data.get("data"), [])

        else:
            errors['count'] += 1
            errors['form'] = "Could not download report"

        return report, errors

    def to_object(self):
        return self

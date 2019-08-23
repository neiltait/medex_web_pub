from examinations.request_handler import load_coroner_report
from medexCms.api import enums
from medexCms.utils import fallback_to, reformat_datetime


class CoronerDownloadReport:
    item = {
        "givenNames": "string",
        "surname": "string",
        "nhsNumber": "string",
        "ableToIssueMCCD": True,
        "causeOfDeath1a": "string",
        "causeOfDeath1b": "string",
        "causeOfDeath1c": "string",
        "causeOfDeath2": "string",
        "dateOfBirth": "2019-08-20T16:05:36.574Z",
        "gender": "Male",
        "houseNameNumber": "string",
        "street": "string",
        "town": "string",
        "county": "string",
        "postcode": "string",
        "placeOfDeath": "string",
        "dateOfDeath": "2019-08-20T16:05:36.574Z",
        "timeOfDeath": "string",
        "anyImplants": True,
        "implantDetails": "string",
        "latestBereavedDiscussion": {
            "userFullName": "string",
            "usersRole": "string",
            "created": "2019-08-20T16:05:36.574Z",
            "eventId": "string",
            "userId": "string",
            "isFinal": True,
            "eventType": "Other",
            "participantFullName": "string",
            "participantRelationship": "string",
            "participantPhoneNumber": "string",
            "presentAtDeath": "Yes",
            "informedAtDeath": "Yes",
            "dateOfConversation": "2019-08-20T16:05:36.574Z",
            "timeOfConversation": "string",
            "discussionUnableHappen": True,
            "discussionUnableHappenDetails": "string",
            "discussionDetails": "string",
            "bereavedDiscussionOutcome": "CauseOfDeathAccepted"
        },
        "qap": {
            "name": "string",
            "role": "string",
            "organisation": "string",
            "phone": "string",
            "notes": "string",
            "gmcNumber": "string"
        },
        "consultant": {
            "name": "string",
            "role": "string",
            "organisation": "string",
            "phone": "string",
            "notes": "string",
            "gmcNumber": "string"
        },
        "gp": {
            "name": "string",
            "role": "string",
            "organisation": "string",
            "phone": "string",
            "notes": "string",
            "gmcNumber": "string"
        },
        "latestAdmissionDetails": {
            "userFullName": "string",
            "usersRole": "string",
            "eventId": "string",
            "userId": "string",
            "notes": "string",
            "isFinal": True,
            "eventType": "Other",
            "admittedDate": "2019-08-20T16:05:36.574Z",
            "admittedDateUnknown": True,
            "admittedTime": "string",
            "admittedTimeUnknown": True,
            "immediateCoronerReferral": True,
            "created": "2019-08-20T16:05:36.574Z",
            "routeOfAdmission": "AccidentAndEmergency"
        },
        "detailsAboutMedicalHistory": "string"
    }

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

        response = load_coroner_report(auth_token, examination_id)
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
                "informed": fallback_to(bereaved_data.get('informedOfDeath'), '') if bereaved_data else '',
                "result": fallback_to(bereaved_data.get('bereavedDiscussionOutcome'), '') if bereaved_data else '',
            }
            if report.bereaved['result'] != enums.discussion.COD_ACCEPTED:
                report.bereaved['concerns'] = fallback_to(bereaved_data.get('discussionDetails'),
                                                          '') if bereaved_data else ''
            else:
                report.bereaved['concerns'] = ''

            bereaved_data = data.get('latestBereavedDiscussion')
            report.bereaved = {
                'name': fallback_to(bereaved_data.get('participantFullName'), ''),
                'relationship': fallback_to(bereaved_data.get('participantRelationship'), ''),
                'phone': fallback_to(bereaved_data.get('participantPhoneNumber'), ''),
                "informed": fallback_to(bereaved_data.get('informedOfDeath'), ''),
                "result": fallback_to(bereaved_data.get('bereavedDiscussionOutcome'), ''),
            }
            if report.bereaved['result'] != enums.discussion.COD_ACCEPTED:
                report.bereaved['concerns'] = fallback_to(bereaved_data.get('discussionDetails'), '')
            else:
                report.bereaved['concerns'] = ''
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

from medexCms.utils import fallback_to


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
        "anyImplants": true,
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

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        data = CoronerDownloadReport.item

        report = CoronerDownloadReport()
        report.given_names = fallback_to(data.get('givenNames'), '')
        report.surname = fallback_to(data.get('surname'), '')
        report.nhs_number = fallback_to(data.get('nhsNumber'), '')
        report.able_to_issue_mccd = fallback_to(data.get('ableToIssueMCCD'), '')
        report.cause_of_death_1a = fallback_to(data.get('causeOfDeath1a'), '')
        report.cause_of_death_1b = fallback_to(data.get('causeOfDeath1b'), '')
        report.cause_of_death_1c = fallback_to(data.get('causeOfDeath1c'), '')
        report.cause_of_death_2 = fallback_to(data.get('causeOfDeath2'), '')
        report.date_of_birth = fallback_to(data.get('dateOfBirth'), '')
        report.gender = fallback_to(data.get('gender'), '')
        report.house_name_number = fallback_to(data.get('houseNameNumber'), '')
        report.street = fallback_to(data.get('street'), '')
        report.town = fallback_to(data.get('town'), '')
        report.county = fallback_to(data.get('county'), '')
        report.postcode = fallback_to(data.get('postcode'), '')
        report.place_of_death = fallback_to(data.get('place_of_death'), '')

        report.examination_id = examination_id

        errors = {'count': 0}

        return report, errors

    def to_object(self):
        return {'forename': self.forename, 'surname': self.surname}

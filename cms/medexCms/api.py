class APIGenderStrings:
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class APITrueFalseStrings:
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class APIYesNoStrings:
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"


class APIFuneralArrangements:
    CREMATION = "Cremation"
    BURIAL = "Burial"
    BURIED_AT_SEA = "BuriedAtSea"
    REPATRIATION = "Repatriation"
    UNKNOWN = "Unknown"


class APICircumstancesOfDeath:
    EXPECTED = "Expected"
    SUDDEN_NOT_UNEXPECTED = "SuddenButNotUnexpected"
    UNEXPECTED = 'Unexpected'
    END_OF_LIFE_CARE_PLAN = 'PartOfAnIndividualisedEndOfLifeCarePlan'


class APIPrescrutinyStatus:
    HAPPENED = "PrescrutinyHappened"
    NOT_HAPPENED = "PrescrutinyNotHappened"


class APIQapDiscussionStatus:
    HAPPENED_NO_REVISION = 'HappenedNoRevision'
    HAPPENED_WITH_REVISIONs = 'HappenedWithRevisions'
    COULD_NOT_HAPPEN = 'CouldNotHappen'
    NO_RECORD = 'NoRecord'


class APIOutcomes:
    MCCD = 'IssueAnMccd'
    CORONER_100A = 'ReferToCoronerFor100a'
    CORONER_INVESTIGATION = 'ReferToCoronerInvestigation'
    CORONER = 'ReferToCoroner'
    MCCD_FROM_ME = 'MccdCauseOfDeathProvidedByME'
    MCCD_FROM_QAP = 'MccdCauseOfDeathProvidedByQAP'
    MCCD_FROM_QAP_AND_ME = 'MccdCauseOfDeathAgreedByQAPandME'


class APICauseOfDeathStatuses:
    NOT_DISCUSSED = 'NotDiscussed'
    DISCUSSION_NOT_POSSIBLE = 'NotPossible'
    MCCD = 'IssueAnMccd'
    CORONER = 'ReferToCoroner'
    MCCD_FROM_ME = 'MccdCauseOfDeathProvidedByME'
    MCCD_FROM_QAP = 'MccdCauseOfDeathProvidedByQAP'
    MCCD_FROM_QAP_AND_ME = 'MccdCauseOfDeathAgreedByQAPandME'


class APIDiscussionOutcomes:
    COD_ACCEPTED = 'CauseOfDeathAccepted'
    CONCERNS_CORONER = 'ConcernsCoronerInvestigation'
    CONCERNS_100A = 'ConcernsRequires100a'
    CONCERNS_ADDRESSED = 'ConcernsAddressedWithoutCoroner'


class APIPeopleStrings:
    QAP = 'qap'
    BEREAVED_REP = 'bereaved-representative'
    OTHER = 'other'


class APIRoles:
    ME = 'MedicalExaminer'
    MEO = 'MedicalExaminerOfficer'
    SERVICE_ADMIN = 'ServiceAdministrator'
    SERVICE_OWNER = 'ServiceOwner'


class UserRoleTypes:
    ME = 'Medical Examiner'
    MEO = 'Medical Examiner Officer'
    SERVICE_ADMIN = 'Service Administrator'
    SERVICE_OWNER = 'Service Owner'


class APIGPNotifiedStatus:
    NOTIFIED = 'GPNotified'
    NOT_NOTIFIED = 'GPUnabledToBeNotified'
    NA = 'NA'


class ExaminationSections:
    PATIENT_DETAILS = 'patient_details'
    MEDICAL_TEAM = 'medical_team'
    CASE_BREAKDOWN = 'case_breakdown'
    CASE_OUTCOMES = 'case_outcomes'


class TimelineEventKeys:
    QAP_DISCUSSION_EVENT_KEY = 'qapDiscussion'
    OTHER_EVENT_KEY = 'otherEvents'
    ADMISSION_NOTES_EVENT_KEY = 'admissionNotes'
    MEO_SUMMARY_EVENT_KEY = 'meoSummary'
    MEDICAL_HISTORY_EVENT_KEY = 'medicalHistory'
    BEREAVED_DISCUSSION_EVENT_KEY = 'bereavedDiscussion'
    PRE_SCRUTINY_EVENT_KEY = 'preScrutiny'
    INITIAL_EVENT_KEY = 'patientDeathEvent'
    CASE_CLOSED_EVENT_KEY = 'caseClosed'

    @classmethod
    def all(cls):
        return [
            cls.QAP_DISCUSSION_EVENT_KEY, cls.OTHER_EVENT_KEY, cls.ADMISSION_NOTES_EVENT_KEY, cls.MEO_SUMMARY_EVENT_KEY,
            cls.MEDICAL_HISTORY_EVENT_KEY, cls.BEREAVED_DISCUSSION_EVENT_KEY, cls.PRE_SCRUTINY_EVENT_KEY,
            cls.CASE_CLOSED_EVENT_KEY, cls.INITIAL_EVENT_KEY
        ]


class TimelineEventTypes:
    OTHER_EVENT_TYPE = 'Other'
    PRE_SCRUTINY_EVENT_TYPE = 'PreScrutiny'
    BEREAVED_DISCUSSION_EVENT_TYPE = 'BereavedDiscussion'
    MEO_SUMMARY_EVENT_TYPE = 'MeoSummary'
    QAP_DISCUSSION_EVENT_TYPE = 'QapDiscussion'
    MEDICAL_HISTORY_EVENT_TYPE = 'MedicalHistory'
    ADMISSION_NOTES_EVENT_TYPE = 'Admission'
    INITIAL_EVENT_TYPE = 'patientDeathEvent'
    CASE_CLOSED_TYPE = 'caseClosed'


class SystemValidationErrors:
    DUPLICATE = "Duplicate"
    CONTAINS_WHITESPACE = "ContainsWhitespace"
    CONTAINS_INVALID_CHARACTERS = "ContainsInvalidCharacters"
    INVALID = "Invalid"
    REQUIRED = "Required"
    MAXIMUM_LENGTH_150 = "MaximumLength150"
    MINIMUM_LENGTH_1 = "MinimumLengthOf1"
    INVALID_FORMAT = "InvalidFormat"
    END_DATE_NOT_FOUND = "EndDateNotFound"
    END_DATE_BEFORE_START_DATE = "EndDateBeforeStartDate"
    ID_NOT_FOUND = "IdNotFound"
    UNKNOWN = "Unknown"


class APIStrings:
    true_false = APITrueFalseStrings()
    yes_no = APIYesNoStrings()
    gender = APIGenderStrings()
    funeral_arrangements = APIFuneralArrangements()
    cod = APICircumstancesOfDeath()
    outcomes = APIOutcomes()
    discussion = APIDiscussionOutcomes()
    people = APIPeopleStrings()
    cod_status = APICauseOfDeathStatuses()
    roles = APIRoles()
    role_types = UserRoleTypes()
    gp_notified_status = APIGPNotifiedStatus()
    examination_sections = ExaminationSections()
    timeline_event_keys = TimelineEventKeys()
    timeline_event_types = TimelineEventTypes()
    errors = SystemValidationErrors()
    prescrutiny_status = APIPrescrutinyStatus()
    qap_discussion_status = APIQapDiscussionStatus()


enums = APIStrings()

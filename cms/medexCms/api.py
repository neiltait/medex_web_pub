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


class APIOutcomes:
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
    OTHER = 'other'


class APIStrings:
    true_false = APITrueFalseStrings()
    yes_no = APIYesNoStrings()
    gender = APIGenderStrings()
    funeral_arrangements = APIFuneralArrangements()
    cod = APICircumstancesOfDeath()
    outcomes = APIOutcomes()
    discussion = APIDiscussionOutcomes()
    people = APIPeopleStrings()


enums = APIStrings()

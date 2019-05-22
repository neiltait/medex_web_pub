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
    No = "No"
    UNKNOWN = "Unknown"


class APIFuneralArrangements:
    CREMATION = "Cremation"
    BURIAL = "Burial"
    BURIED_AT_SEA = "BuriedAtSea"
    REPATRIATION = "Repatriation"
    UNKNOWN = "Unknown"


class APICircumstancesOfDeath:
    expected = "Expected"
    sudden_but_not_unexpected = "SuddenButNotUnexpected"
    unexpected = 'Unexpected'
    part_of_life_care_plan = 'PartOfAnIndividualisedEndOfLifeCarePlan'


class APIOutcomes:
    issue_an_mccd = 'IssueAnMccd'
    refer_to_coroner = 'ReferToCoroner'


class APIStrings:
    true_false = APITrueFalseStrings()
    yes_no = APIYesNoStrings()
    gender = APIGenderStrings()
    funeral_arrangements = APIFuneralArrangements()
    cod = APICircumstancesOfDeath()
    outcomes = APIOutcomes()


enums = APIStrings()

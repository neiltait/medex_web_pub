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


class APIStrings:
    true_false = APITrueFalseStrings()
    yes_no = APIYesNoStrings()
    gender = APIGenderStrings()
    funeral_arrangements = APIFuneralArrangements()


enums = APIStrings()

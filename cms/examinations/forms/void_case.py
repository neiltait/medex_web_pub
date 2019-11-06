from alerts.messages import ErrorFieldRequiredMessage


class CaseSettingsForm:
    VOID_CASE_FORM_TYPE = 'void-case'
    """
    ToDos:
    - form types
    - map validators to forms types (maybe WITH the above)
    """

    def __init__(self, request=None):
        self.initialise_errors()
        if request:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.void_case = ""
        self.void_case_reason = ""

    def initialise_errors(self):
        self.errors = {"count": 0}

    @property
    def error_count(self):
        return self.errors['count']

    def is_valid(self):

        self.errors["count"] = 0




        return self.errors["count"] == 0



    def _is_valid_void_case(self):
        if self.void_case_reason is None or len(self.void_case_reason.strip()) == 0:
            self.errors["void_case_reason"] = ErrorFieldRequiredMessage("a reason why this case must be voided.")
            self.errors["count"] += 1


    def to_object(self):

        return {
            "isVoid": self.void_case,
            "voidReason": self.void_case_reason
        }

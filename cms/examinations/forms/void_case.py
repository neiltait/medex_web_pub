from alerts.messages import ErrorFieldRequiredMessage


class VoidCaseForm:

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

        if self.void_case is None or len(self.void_case.strip()) == 0:
            self.errors["void_case"] = ErrorFieldRequiredMessage("a reason")
            self.errors["count"] += 1

        if self.void_case_reason is None or len(self.void_case_reason.strip()) == 0:
            self.errors["void_case_reason"] = ErrorFieldRequiredMessage("a reason")
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def to_object(self):

        return {
            "isVoid": self.void_case,
            "voidReason": self.void_case_reason
        }

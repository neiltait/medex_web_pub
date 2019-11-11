from alerts.messages import ErrorFieldRequiredMessage


class VoidCaseForm:

    def __init__(self, obj_dict=None):
        self.initialise_errors()
        if obj_dict:
            self.initialise_form(obj_dict)
        else:
            self.initialise_blank_form()

    @property
    def error_count(self):
        return self.errors['count']

    def initialise_form(self, obj_dict):
        self.void_case = obj_dict.get('void_case')
        self.void_case_reason = obj_dict.get('void_case_reason')

    def initialise_blank_form(self):
        self.void_case = ""
        self.void_case_reason = ""

    def initialise_errors(self):
        self.errors = {"count": 0}

    def is_valid(self):
        self.initialise_errors()

        if self.void_case_reason is None or len(self.void_case_reason.strip()) == 0:
            self.errors["void_case_reason"] = ErrorFieldRequiredMessage("a reason why this case must be voided")
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def to_object(self):

        return {
            "voidReason": self.void_case_reason
        }
